import socket 
def start_client():
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((socket.gethostname(),1234))
        s.close()
if __name__=="__main__":
    start_client()
