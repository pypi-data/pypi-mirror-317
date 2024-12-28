from collections import OrderedDict
import re
import copy
from datetime import datetime


class Segment:
    def __init__(self, name: str, fields: list):
        self.name = name
        self.fields = fields # Example: ['^~\\&', 'ADM', 'RCH', '', '', '202403270202', '', 'SIU^A03', '6125797', 'P', '2.4', '', '', '', 'NE']

    def __repr__(self):
        return '%s|%s' % (self.name, '|'.join(self.fields))
    
    def get_field(self, field_subfield: str) -> str:
        sp = SegmentPath(f'{self.name}-{field_subfield}')
        
        res = self.fields[sp.field-1]
        if sp.subfield:
            subs = res.split('^')
            if sp.subfield <= len(subs):
                return subs[sp.subfield-1]
            else:
                return None
        return res

    def set_field(self, field_subfield: str, val: str):
        sp = SegmentPath(f'{self.name}-{field_subfield}')        
        if sp.subfield:
            for _ in range(0, sp.field-len(self.fields)):
                self.fields.append('')
            
            subfields = self.fields[sp.field-1].split('^')
            for _ in range(0, sp.subfield-len(subfields)):
                subfields.append('')
            subfields[sp.subfield-1] = val
            self.fields[sp.field-1] = '^'.join(subfields)
        else:
            for _ in range(0, sp.field-len(self.fields)):
                self.fields.append('')
            
            self.fields[sp.field-1] = val


class SegmentPath:
    def __init__(self, path: str):
        """
        path format is MSH-9.2 or MSH-9 
        """
        self.path = path
        regex = re.compile(r'^[A-Z]+.\-\d+(\.\d+)?$')
        if regex.match(path) is None:
            raise ValueError(f'Invalid HL7 path {path}. It must be like AAA-1.3')

        self.seg_name, field_subfield = path.split('-')
        field = field_subfield
        self.subfield = None
        if '.' in field_subfield:
            field, subfield = field_subfield.split('.')[:2]
            try:
                self.subfield = int(subfield)
                if self.subfield < 1:
                    raise ValueError(f'Invalid subfield_val value {self.subfield}. It should be >= 1.')
            except ValueError:
                raise Exception(f'Invalid non-integer subfield {subfield}')
             
        try:
            self.field = int(field)
        except ValueError:
            raise Exception(f'Invalid non-integer field {field}')
        
        if self.field < 1:
            raise ValueError(f'Invalid field value {self.field}. It should be >= 1.')
        
        if self.seg_name == 'MSH': # special case:
            self.field -= 1

    def is_field(self) -> bool:
        return self.field is not None and self.subfield is None

    def is_subfield(self) -> bool:
        return self.subfield is not None
    
    def __repr__(self):
        return self.path

class Field:
    def __init__(self, msg, name, value):
        self.msg = msg
        self.name = name
        self.value = value

    def get_sub(self, ind: int):
        if ind < 1:
            raise Exception('Please specify a valid index greater equal to 1.')
        
        parts = self.value.split('^')
        if ind < len(parts):
            return parts[ind-1]
        return ''
    
    def set_sub(self, ind: int, val: str):
        if ind < 1:
            raise Exception('Please specify a valid index greater equal to 1.')
        
        parts = self.value.split('^')
        while ind > len(parts):
            parts.append('')
        
        parts[ind-1] = val
        self.value = '^'.join(parts)
        # update message:
        self.msg.set_field(self.name, self.value)
    
    def delete(self):
        pass

    def __repr__(self):
        return f'<{self.name}:{self.value}>'


class Message:
    def __init__(self, msg: str=None):
        self.segments = OrderedDict()
        if msg != None:
            msg = msg.replace('\n', '\r').replace('\r\r', '\r').strip()
            for line in msg.split('\r'):
                fields = line.split('|')
                seg = fields[0]
                if seg in self.segments.keys():
                    self.segments[seg].append(fields[1:])
                else:
                    self.segments[seg] = [fields[1:]]
            
            for segment_name, segs in self.segments.items():
                setattr(self, segment_name, [Segment(segment_name, seg) for seg in segs])

        self.promotions = {} # put this at the end because it is checked in __setattr__

            
    def __validate_path(self, path):
        regex = re.compile(r'^[A-Z]+.\-\d+(\.\d+)?$')
        if regex.match(path) is None:
            raise ValueError(f'Invalid HL7 path {path}. It must be like AAA-1.3')
    

    def get_fields(self, path: str) -> list:
        self.__validate_path(path)
        sp = SegmentPath(path)
        
        res = []
        if sp.subfield is None:
            for fields in self.segments[sp.seg_name]:
                if sp.field <= len(fields):
                    val = fields[sp.field-1]
                    res.append(Field(self, path, val))
        else:
            for fields in self.segments[sp.seg_name]:
                if sp.field <= len(fields):
                    subs = fields[sp.field-1].split('^')
                    if sp.subfield <= len(subs):
                        val = subs[sp.subfield-1]
                        res.append(Field(self, path, val))
        
        return res


    def get_repeated_fields(self, path: str) -> list:
        self.__validate_path(path)
        sp = SegmentPath(path)

        res = []
        if sp.subfield is None:
            for fields in self.segments[sp.seg_name]:
                if sp.field <= len(fields):
                    for val in fields[sp.field-1].split('~'):
                        res.append(Field(self, path, val))
        else:
            for fields in self.segments[sp.seg_name]:
                if sp.field <= len(fields):
                    subs = fields[sp.field-1].split('^')
                    if sp.subfield <= len(subs):
                        for val in subs[sp.subfield-1].split('~'):
                            res.append(Field(self, path, val))
        
        return res


    def set_repeated_fields(self, fields: list):
        for field in fields:
            sp = SegmentPath(field.name)        
            if sp.subfield is None:
                for fields in self.segments[sp.seg_name]:
                    while sp.field > len(fields):
                        fields.append('')
                    fields[sp.field-1] = field.value
            else:
                for fields in self.segments[sp.seg_name]:
                    while sp.field > len(fields):
                        fields.append('')
                    
                    new_rep_fields = []
                    for rep_fields in fields.split('~'):
                        subs = rep_fields[sp.field-1].split('^')
                        while sp.subfield > len(subs):
                            subs.append('')
                        subs[sp.subfield-1] = field.value
                        new_rep_fields.append('~'.join(subs))
                    self.segments[sp.seg_name] = new_rep_fields 
    

    def get_field(self, path: str) -> Field:
        res = self.get_fields(path)
        if len(res) < 1:
            return None
        
        return res[0]

    def remove_field(self, path: str):
        sp = SegmentPath(path)
        if sp.subfield is None:
            for fields in self.segments[sp.seg_name]:
                if sp.field <= len(fields):
                    fields[sp.field-1] = ''
        else:
            for fields in self.segments[sp.seg_name]:
                if sp.field <= len(fields):
                    subs = fields[sp.field-1].split('^')
                    if sp.subfield <= len(subs):
                        subs[sp.subfield-1] = ''
                        self.segments[sp.seg_name][sp.field-1] = '^'.join(subs)
    

    def set_field(self, path: str, new_value: str):
        self.__validate_path(path)
        sp = SegmentPath(path)
        self.__update_segments(sp, new_value)
        
        # update promotions:
        for key, val in self.promotions.items():
            if val == path:
                self.promotions[key] = new_value
                setattr(self, key, new_value)


    def direct_map(self, *paths):
        new_msg = Message()
        for path in paths:
            if '-' not in path: # the whole segment:
                if path in self.segments:
                    new_msg.segments[path] = copy.deepcopy(self.segments[path])
            else:
                new_msg.set_field(path, self.get_field(path).value)
        return new_msg


    def content(self):
        lines = []
        for seg_name, seg_list in self.segments.items():
            for seg in seg_list:
                lines.append(f'{seg_name}|{'|'.join(seg)}')
        return '\r'.join(lines)
    
    def __repr__(self):
        return self.content().replace('\r', '\r\n')

    def remove_segments(self, segment_name, indecies: list=None):
        if indecies is None:
            del self.segments[segment_name]
        else:
            indecies.sort(reverse=True)
            for ind in indecies:
                del self.segments[segment_name][ind]
        delattr(self, segment_name)
        if segment_name in self.segments:
            setattr(self, segment_name, [Segment(segment_name, seg) for seg in self.segments[segment_name]])

    def add_segments(self, val: str):
        parts = val.strip().split('|')
        segment_name = parts.pop(0)
        self.segments[segment_name].add(parts)
        # update the attribute:
        delattr(self, segment_name)
        setattr(self, segment_name, [Segment(segment_name, seg) for seg in self.segments[segment_name]])

    def promote(self, values: dict):
        for key, val in values.items():
            setattr(self, key, self.get_field(val).value)
        self.promotions.update(values)

    def __update_segments(self, sp: SegmentPath, val: str):
        if sp.seg_name not in self.segments:
            self.segments[sp.seg_name] = [[]]
        
        for seg in self.segments[sp.seg_name]:
            if sp.subfield:
                for _ in range(0, sp.field-len(seg)):
                    seg.append('')
                
                subfields = seg[sp.field-1].split('^')
                for _ in range(0, sp.subfield-len(subfields)):
                    subfields.append('')
                subfields[sp.subfield-1] = val
                seg[sp.field-1] = '^'.join(subfields)
            else:
                for _ in range(0, sp.field-len(seg)):
                    seg.append('')
                seg[sp.field-1] = val
    
    def __setattr__(self, name, value):
        if hasattr(self, 'promotions'):
            if name in self.promotions:
                path = self.promotions[name]
                sp = SegmentPath(path)
                # update segments:
                self.__update_segments(sp, value)
                # update attributes:
                getattr(self, sp.seg_name).set_field(path.split('-')[-1], value)
        # now update promotions:
        super().__setattr__(name, value)

    def get_patient_age(self):
        if 'PID' not in self.segments:
            return None
        
        pid7 = self.get_field('PID-7').value
        if not pid7.isnumeric():
            return None

        dob = datetime.strptime(pid7, '%Y%m%d')
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age