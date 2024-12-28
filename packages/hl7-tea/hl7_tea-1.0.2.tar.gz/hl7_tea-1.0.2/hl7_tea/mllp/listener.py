import socket
import threading
import logging
import traceback
from hl7_tea import Message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

START_BLOCK = '\x0b'
END_BLOCK = '\x1c\x0d'


class MllpListener:
    def __init__(self):
        self.ack_type = 'AA'
    
    def handle_data(self, data: Message):
        pass

    def __create_acknowledgement(self, data: str):
        msg = Message(data)
        sending_app = msg.get_field('MSH-3').value
        sending_fac = msg.get_field('MSH-4').value
        receiving_app = msg.get_field('MSH-5').value
        receiving_fac = msg.get_field('MSH-6').value
        msg_time = msg.get_field('MSH-7').value
        control_id = msg.get_field('MSH-10').value
        processing_id = msg.get_field('MSH-11').value
        version_id = msg.get_field('MSH-12').value
        ack = f"{START_BLOCK}MSH|^~\\&|{sending_app}|{sending_fac}|{receiving_app}|{receiving_fac}|{msg_time}||ACK|{control_id}|{processing_id}|{version_id}\rMSA|{self.ack_type}|{control_id}\r{END_BLOCK}"
        return ack


    def send_ack(self, client_socket, data: str):
        ack_message = self.__create_acknowledgement(data)
        client_socket.sendall(ack_message.encode())


    def __handle_client(self, client_socket, ack: bool=True):
        """
        Handle incoming client connections.
        """
        try:
            data = client_socket.recv(1024)
            data = data.decode('utf-8').strip()
            logger.info(f"Received data: {data}")
            if isinstance(data, bytes):
                    data = data.decode('utf-8')
            if data:
                if data.startswith(START_BLOCK) and data.endswith(END_BLOCK):
                    data = data[len(START_BLOCK):-len(END_BLOCK)]
                
                logger.info(f"Received message: {data.split()[0]}")
                
                if ack:
                    logger.info(f"Sending ACK")
                    self.send_ack(client_socket, data)
                    logger.info(f"Sent ACK")

                self.handle_data(Message(data))
        
        except Exception as e:
            logger.error(f"Error handling client: {e}")
            traceback.print_exc()
        finally:
            client_socket.close()


    def start(self, port: int, ack: bool=True):
        """
        Start the TCP listener.
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', port))
        server.listen(5) #  the number of unaccepted connections that the system will allow before refusing new connections.
        logger.info(f"Listening on {port}")

        while True:
            client_socket, addr = server.accept()
            logger.info(f"Connection from {addr}")
            client_handler = threading.Thread(target=self.__handle_client, args=(client_socket, ack))
            client_handler.start()

