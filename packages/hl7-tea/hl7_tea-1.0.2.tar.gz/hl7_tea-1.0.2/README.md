hl7_tea
==========
![Alt text](img/hl7_tea.jpeg)

**hl7_tea** is a package for parsing and manipulating HL7 data.

# Installation
You can install it using pip:
`pip install hl7_tea`


## Parsing data
Example 1:
```python
from hl7_tea import Message
msg_str = """MSH|^~\\&|ADM|RCH|||202403270202||ADT^A03|4425797|P|2.4||||NE
EVN|A03|202403270202|||UNKNOWN^RUN^MIDNT^^^^^^^^^^U|20240326
PID|1||RC123^^^^MR^RCH~9872360649^^^^HCN^RCH~123^^^^PI^RCH~E456^^^^EMR^RCH~66292A7E8541^^^^PT^RCH||MICROTEST^CRIT^ONE^^^^L~OPENHOUSE^CRIT^ONE^^^^A||19690414|F|||123 MAIN ST^^Seattle^WA^12345^CAN||(896)321-4545^PRN^CELL||ENG|||RC1234/24|3452353232
PV1|1|O|RC.ERZ1|||ER-ERIN1^ERERINZ1-1^IRM|LABTESTG1^Labtest^Generic Doc1^Doc1^^^MD^^^^^^XX|||||||||||RCR||CL|||||||||||||||||||RCH||DIS|||202309081450|202403260001|
GT1|768||Doe^Jane
ZFH|CVC|V|F||test1@gmail.com
ZFH|CVC|C|F||test2@gmail.com,hi^there"""

msg = Message(msg_str)

print(msg.get_field('GT1-3.2'))
```

```shell
Jane
```

Example 2:
```python
print(msg.get_repeated_fields('PID-3'))
```

```shell
[<PID-3:RC123^^^^MR^RCH>, <PID-3:9872360649^^^^HCN^RCH>, <PID-3:123^^^^PI^RCH>, <PID-3:E456^^^^EMR^RCH>, <PID-3:66292A7E8541^^^^PT^RCH>]
```

Example 3:
```python
for pid3 in msg.get_repeated_fields('PID-3'):
    print('PID-3.5 = ', pid3.get_sub(5))
```

```shell
PID-3.5 =  MR
PID-3.5 =  HCN
PID-3.5 =  PI
PID-3.5 =  EMR
PID-3.5 =  PT
```

## Data mapping
You can map fields using the method `direct_map`.
You can specify either the segment name, or field or subfield.
Example 4:
```python
res = msg.direct_map('MSH', 'PID', 'PV1-1', 'PV1-2', 'PV1-3', 'PV1-6.1')
print(res)
```

```shell
MSH|^~\&|ADM|RCH|||202403270202||ADT^A03|4425797|P|2.4||||NE
PID|1||RC123^^^^MR^RCH~9872360649^^^^HCN^RCH~123^^^^PI^RCH~E456^^^^EMR^RCH~66292A7E8541^^^^PT^RCH||MICROTEST^CRIT^ONE^^^^L~OPENHOUSE^CRIT^ONE^^^^A||19690414|F|||123 MAIN ST^^Seattle^WA^12345^CAN||(896)321-4545^PRN^CELL||ENG|||RC1234/24|3452353232
(venv) kouroshparsa@Kouroshs-MacBook-Pro hl7_tea % python test.py
MSH|^~\&|ADM|RCH|||202403270202||ADT^A03|4425797|P|2.4||||NE
PID|1||RC123^^^^MR^RCH~9872360649^^^^HCN^RCH~123^^^^PI^RCH~E456^^^^EMR^RCH~66292A7E8541^^^^PT^RCH||MICROTEST^CRIT^ONE^^^^L~OPENHOUSE^CRIT^ONE^^^^A||19690414|F|||123 MAIN ST^^Seattle^WA^12345^CAN||(896)321-4545^PRN^CELL||ENG|||RC1234/24|3452353232
PV1|1|O|RC.ERZ1|||ER-ERIN1
```

Example 5: This example demonstrates how to map repeated fields.
```python
msg = Message(msg_str)
res = msg.direct_map('MSH', 'PID', 'PV1', 'GT1')

# We only want to map patient identifiers whose
# Identifier Type Code is 'MR'
res.remove_field('PID-3')
pid3_to_map = []
for pid3 in msg.get_repeated_fields('PID-3'):
    if pid3.get_sub(5) == 'MR':
        pid3_to_map.append(pid3)

res.set_repeated_fields(pid3_to_map)
print(res)
```

```shell
MSH|^~\&|ADM|RCH|||202403270202||ADT^A03|4425797|P|2.4||||NE
PID|1||RC123^^^^MR^RCH||MICROTEST^CRIT^ONE^^^^L~OPENHOUSE^CRIT^ONE^^^^A||19690414|F|||123 MAIN ST^^Seattle^WA^12345^CAN||(896)321-4545^PRN^CELL||ENG|||RC1234/24|3452353232
PV1|1|O|RC.ERZ1|||ER-ERIN1^ERERINZ1-1^IRM|LABTESTG1^Labtest^Generic Doc1^Doc2^^^MD^^^^^^XX|||||||||||RCR||CL|||||||||||||||||||RCH||DIS|||202309081450|202403260001|
GT1|768||Doe^Jane
```

Example 6: The example below demonstrate how you can promote properties:
```python
msg.promote({'message_type': 'MSH-9.1',
             'trigger_event': 'MSH-9.2'})
print(msg.message_type)
```

```shell
ADT
```

Example 7: You can view the segments like so
```python
print(msg.segments)
```
```shell
OrderedDict({'MSH': [['^~\\&', 'ADM', 'RCH', '', '', '202403270202', '', 'ADT^A03', '4425797', 'P', '2.4', '', '', '', 'NE']], 'EVN': [['A03', '202403270202', '', '', 'UNKNOWN^RUN^MIDNT^^^^^^^^^^U', '20240326']], 'PID': [['1', '', 'RC123^^^^MR^RCH~9872360649^^^^HCN^RCH~123^^^^PI^RCH~E456^^^^EMR^RCH~66292A7E8541^^^^PT^RCH', '', 'MICROTEST^CRIT^ONE^^^^L~OPENHOUSE^CRIT^ONE^^^^A', '', '19690414', 'F', '', '', '123 MAIN ST^^Seattle^WA^12345^CAN', '', '(896)321-4545^PRN^CELL', '', 'ENG', '', '', 'RC1234/24', '3452353232']], 'PV1': [['1', 'O', 'RC.ERZ1', '', '', 'ER-ERIN1^ERERINZ1-1^IRM', 'LABTESTG1^Labtest^Generic Doc1^Doc2^^^MD^^^^^^XX', '', '', '', '', '', '', '', '', '', '', 'RCR', '', 'CL', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'RCH', '', 'DIS', '', '', '202309081450', '202403260001', '']], 'GT1': [['768', '', 'Doe^Jane']], 'ZFH': [['CVC', 'V', 'F', '', 'test1@gmail.com'], ['CVC', 'C', 'F', '', 'test2@gmail.com,hi^there']]})
```

As you can see, it an OrderedDict. The values are lists because some segments such as OBX can appear several times.

If you want to remove a field, use the `remove_field` method.
```python
msg.remove_field('ZFH-2')
print(msg)
```

Note that if you print the message, it displays the content with new line characters for the convenience but the correct HL7 format uses carriage return instead. If you want to get the string representation with carriage returns, you can call the `content` method like so:
```
res =  msg.content()
```

You can also update fields like so:
```python
msg.set_field('GT1-1', 'ABC')
print(msg)
```

```shell
MSH|^~\&|ADM|RCH|||202403270202||ADT^A03|4425797|P|2.4||||NE
EVN|A03|202403270202|||UNKNOWN^RUN^MIDNT^^^^^^^^^^U|20240326
PID|1||RC123^^^^MR^RCH~9872360649^^^^HCN^RCH~123^^^^PI^RCH~E456^^^^EMR^RCH~66292A7E8541^^^^PT^RCH||MICROTEST^CRIT^ONE^^^^L~OPENHOUSE^CRIT^ONE^^^^A||19690414|F|||123 MAIN ST^^Seattle^WA^12345^CAN||(896)321-4545^PRN^CELL||ENG|||RC1234/24|3452353232
PV1|1|O|RC.ERZ1|||ER-ERIN1^ERERINZ1-1^IRM|LABTESTG1^Labtest^Generic Doc1^Doc2^^^MD^^^^^^XX|||||||||||RCR||CL|||||||||||||||||||RCH||DIS|||202309081450|202403260001|
GT1|ABC||Doe^Jane
ZFH|CVC||F||test1@gmail.com
ZFH|CVC||F||test2@gmail.com,hi^ther
```

Example: This example shows how to set subfields:
```python
msg = Message(msg_str)
pid_field = msg.get_field('PV1-6')
print(pid_field)
print('value is:', pid_field.value)
print('sub=', pid_field.get_sub(2))
pid_field.set_sub(2, 'X')
print(pid_field)
print(msg)
```

```shell
<PV1-6:ER-ERIN1^ERERINZ1-1^IRM>
value is: ER-ERIN1^ERERINZ1-1^IRM
sub= ERERINZ1-1
<PV1-6:ER-ERIN1^X^IRM>
MSH|^~\&|ADM|RCH|||202403270202||ADT^A03|4425797|P|2.4||||NE
EVN|A03|202403270202|||UNKNOWN^RUN^MIDNT^^^^^^^^^^U|20240326
PID|1||RC123^^^^MR^RCH~9872360649^^^^HCN^RCH~123^^^^PI^RCH~E456^^^^EMR^RCH~66292A7E8541^^^^PT^RCH||MICROTEST^CRIT^ONE^^^^L~OPENHOUSE^CRIT^ONE^^^^A||19690414|F|||123 MAIN ST^^Seattle^WA^12345^CAN||(896)321-4545^PRN^CELL||ENG|||RC1234/24|3452353232
PV1|1|O|RC.ERZ1|||ER-ERIN1^X^IRM|LABTESTG1^Labtest^Generic Doc1^Doc2^^^MD^^^^^^XX|||||||||||RCR||CL|||||||||||||||||||RCH||DIS|||202309081450|202403260001|
GT1|768||Doe^Jane
ZFH|CVC|V|F||test1@gmail.com
ZFH|CVC|C|F||test2@gmail.com,hi^there
```
## Helper functions

Example: To get patient's age:
```python
print(msg.get_patient_age())
```

## MLLP data transport
Below is an example for sending and receiving MLLP messages:

Example: Sending a message:
```python
from hl7_tea.mllp.sender import send_message

msg_str = """MSH|^~\\&|ADM|RCH|||202403270202||ADT^A03|4425797|P|2.4||||NE
EVN|A03|202403270202|||UNKNOWN^RUN^MIDNT^^^^^^^^^^U|20240326
PID|1||RC123^^^^MR^RCH~9872360649^^^^HCN^RCH~123^^^^PI^RCH~E456^^^^EMR^RCH~6629$
PV1|1|O|RC.ERZ1|||ER-ERIN1^ERERINZ1-1^IRM|LABTESTG1^Labtest^Generic Doc1^Doc2^^$
GT1|768||Doe^Jane
ZFH|CVC|V|F||test1@gmail.com
ZFH|CVC|C|F||test2@gmail.com,hi^there"""

send_message(msg_str, 'localhost', 6000)
```

Example: Receiving a message:
```python
from hl7_tea.mllp.listener import MllpListener
class Listener(MllpListener):
    def handle_data(self, msg):
        print('PID-7=', msg.get_field('PID-7').value)

listener = Listener()
listener.start(6000)
```
