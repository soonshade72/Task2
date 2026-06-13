import socket
import threading
import sqlite3
def handle_client(clientsocket,address):
    try:
        data=clientsocket.recv(1024).decode('utf-8')
        if not data:
            return
        uid,nm,pwd = data.split(',')
        conn=sqlite3.connect('music_server.db')
        c=conn.cursor()
        c.execute("SELECT uid FROM Users WHERE uid=?",(uid,))
        d=c.fetchone()
        if d:
             auth(uid,nm,pwd,clientsocket)
        else :
             c.execute("""INSERT INTO Users(uid,username,password)
                       VALUES(?,?,?)""",(uid,nm,pwd))
             conn.commit()
             clientsocket.send("New user registered".encode('utf-8'))
    finally:
         if conn:
             conn.close()
         clientsocket.close()           
def auth(uid,nm,pwd,clientsocket):
    try:     
        conn=sqlite3.connect('music_server.db')
        c=conn.cursor()          
        c.execute("SELECT * FROM Users WHERE uid =? AND username=? AND password=?",(uid,nm,pwd))
        user = c.fetchone()
        if user:
            clientsocket.send("Authentication Succesful".encode('utf-8'))
            print(f"Auth success")
        else:
            clientsocket.send("Authentication UnSuccesful".encode('utf-8'))
            print(f"Auth Unsuccess")
        conn.close()
    except Exception as e:
     print("Error")   
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