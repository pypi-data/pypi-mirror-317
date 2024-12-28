import socket

START_BLOCK = '\x0b'
END_BLOCK = '\x1c\x0d'


def send_message(msg: str, host: str, port: int, ack: bool=False, timeout: int=5):
    """
    @timeout: is in seconds
    returns the acknowledgement response if ack is set to True
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.settimeout(timeout)
        framed_message = f"{START_BLOCK}{msg}{END_BLOCK}"
        
        s.sendall(framed_message.encode())
        print("Sent the message")
        if ack:
            ack = s.recv(4096).decode()
        return ack
    return None
