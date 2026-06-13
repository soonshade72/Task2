import socket
import threading, wave
def handle_client(clientsocket,address):
    CHUNK=1024
    wf=wave.open("c.wav",'rb')
    data = wf.readframes(CHUNK)
    while data:
        try:
            clientsocket.sendall(data)
            data=wf.readframes(CHUNK)
        except Exception as e:
            print(f"Error sending data to{address}:{e}")
            break
    clientsocket.close()
def start_server():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((socket.gethostname(),1234))
    s.listen(5)
    while True:
        clientsocket,address = s.accept()
        thread = threading.Thread(target=handle_client ,args=(clientsocket,address))
        thread.start()
if __name__=="__main__":
    start_server()