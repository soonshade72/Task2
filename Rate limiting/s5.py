import socket
import threading
import sqlite3
import datetime
import db
Max_Limit=3
Ban_duration=15
uns={}
lock=threading.Lock()
def is_banned(ip_address):
    conn=sqlite3.connect('music_server.db')
    c=conn.cursor()
    c.execute("SELECT expires_at FROM ActiveBans WHERE ip_address=?",(ip_address,))
    row=c.fetchone()
    conn.close()
    if row:
        expires_at=datetime.datetime.fromisoformat(row[0])
        if datetime.datetime.now() <expires_at:
            return True
        else:
            conn = sqlite3.connect('music_server.db')
            c=conn.cursor()
            c.execute("DELETE FROM ActiveBans WHERE ip_address=?",(ip_address,))
            conn.commit()
            conn.close()
            with lock:
                if ip_address in uns:
                    del uns[ip_address]
                return False
            return False
def ban_ip(ip_address):
    now=datetime.datetime.now()
    expires = now + datetime.timedelta(minutes=Ban_duration)
    conn=sqlite3.connect('music_server.db')
    c=conn.cursor()
    c.execute("""INSERT OR REPLACE INTO ActiveBans (ip_address, ban_timestamp, expires_at)
                 VALUES (?, ?, ?)""", (ip_address, now.isoformat(), expires.isoformat()))
    conn.commit()
    conn.close()        
def handle_client(clientsocket,address):
    ip_address=address[0]
    conn=None
    if is_banned(ip_address):
        clientsocket.send("Access Denied: You are temporarily banned.".encode('utf-8'))
        clientsocket.close()
        return
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
             auth(uid,nm,pwd,clientsocket,ip_address)
        else :
             c.execute("""INSERT INTO Users(uid,username,password)
                       VALUES(?,?,?)""",(uid,nm,pwd))
             conn.commit()
             clientsocket.send("New user registered".encode('utf-8'))
    finally:
         if conn:
             conn.close()
         clientsocket.close()           
def auth(uid,nm,pwd,clientsocket,ip_address):
    try:     
        conn=sqlite3.connect('music_server.db')
        c=conn.cursor()          
        c.execute("SELECT * FROM Users WHERE uid =? AND username=? AND password=?",(uid,nm,pwd))
        user = c.fetchone()
        if user:
            clientsocket.send("Authentication Succesful".encode('utf-8'))
            print(f"Auth success")
            with lock:
                if ip_address in uns:
                    del uns[ip_address]
        else:
            clientsocket.send("Authentication UnSuccesful".encode('utf-8'))
            print(f"Auth Unsuccess")
            with lock:
                count = uns.get(ip_address, 0) + 1
                uns[ip_address] = count
                
                if count >= Max_Limit:
                    ban_ip(ip_address)
                    clientsocket.send("Authentication Unsuccessful. You are now banned.".encode('utf-8'))
                else:
                    remaining =Max_Limit - count
                    clientsocket.send(f"Authentication Unsuccessful. {remaining} attempts left.".encode('utf-8'))
        conn.close()
    except Exception as e:
     print("Error")   
def start_server():
    db.init_db()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((socket.gethostname(),1234))
    s.listen(5)
    while True:
        clientsocket,address = s.accept()
        thread = threading.Thread(target=handle_client ,args=(clientsocket,address))
        thread.start()
if __name__=="__main__":
    start_server()