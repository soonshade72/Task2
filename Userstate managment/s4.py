import socket 
import threading
import datetime
import sqlite3
import db
DB_name='music_server.db'
Max_conn=3
active_conn={}
conn_lock=threading.Lock()
class ClientState:
    def __init__(self,uid,username,ip_address):
        self.uid = uid
        self.username=username
        self.ip_address=ip_address
        self.last_seen=datetime.datetime.now().isoformat()
        self.is_active=1
def save_client_state(db_path,client:ClientState):
    conn = sqlite3.connect(db_path)
    cursor=conn.cursor()
    cursor.execute(""" 
INSERT OR REPLACE INTO UserState (uid,username,ip_address,last_seen,is_active)
                   VALUES(?,?,?,?,?)
""",(
    client.uid,
    client.username,
    client.ip_address,
    client.last_seen,
    client.is_active,
   ),
    )
    conn.commit()
    conn.close()
def handle_client(clientsocket,address):
    ip_address=address[0]
    with conn_lock:
        curr_conn=active_conn.get(ip_address,0)
        if curr_conn >= Max_conn:
         clientsocket.close()
         return
        active_conn[ip_address]=curr_conn +1 
    try:
        temp_uid = "guest_" + ip_address.replace('.', '_')
        state = ClientState(uid=temp_uid, username="Guest", ip_address=ip_address)  
        save_client_state(DB_name, state)  
        while True:
            data = clientsocket.recv(1024)
            if not data:
                break           
    finally:
        with conn_lock:
            active_conn[ip_address] -= 1
            if active_conn[ip_address] == 0:
                del active_conn[ip_address] 
        clientsocket.close()    
def start_server():
    db.init_db()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(5)
    
    print("Server started. Listening for connections...")
    while True:
        clientsocket, address = s.accept()
        thread = threading.Thread(target=handle_client, args=(clientsocket, address))
        thread.start()

if __name__=="__main__":
    start_server()