import socket 
def start_client():
    uid=input("Enter UserID:")
    nm=input("Enter Username: ")
    pwd=input("Enter Password: ")
    auth_data=f"{uid},{nm},{pwd}"
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((socket.gethostname(),1234))
        s.send(auth_data.encode('utf-8'))
        response=s.recv(1024).decode('utf-8')
        print(f"Server Response:{response}")
    except ConnectionRefusedError:
        print(f"Couldn't Connect")
    finally:
        s.close()
if __name__=="__main__":
    start_client()