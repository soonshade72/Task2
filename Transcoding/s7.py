import socket
import threading, wave
import subprocess 
import time 
import re 
actct=[]
def hb():
    while True:
        for ip in actct:
            try:
                output=subprocess.check_output(
                    ['ping','-n','1',ip],
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                rtt_match=re.search(r'time[<=]([\d]+)ms',output,re.IGNORECASE)
            except Exception:
                print("Ping failed")
        time.sleep(3)              
def handle_client(clientsocket,address):
    ip,port=address
    actct.append(ip)
    CHUNK=1024
    rtt=0
    try:
        output=subprocess.check_output(['ping','-n','1',ip],text=True,creationflags=subprocess.CREATE_NO_WINDOW)
        match=re.search(r'time[<=]([\d]+)ms',output,re.IGNORECASE)
        if match: rtt = int(match.group(1))
    except Exception:
        pass
    if rtt>50:
        clientsocket.sendall(b'0')
        cmd=['ffmpeg','-i','c.wav','-f','s16le','-ac','1','-ar','11025','pipe:1']
    else:
        clientsocket.sendall(b'1')
        cmd=['ffmpeg','-i','c.wav','-f','s16le','-ac','2','-ar','44100','pipe:1']    
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    data=proc.stdout.read(CHUNK)
    while data:
        try:
            clientsocket.sendall(data)
            data=proc.stdout.read(CHUNK)
        except Exception as e:
            print(f"Error sending data to{address}:{e}")
            break
    proc.terminate()
    clientsocket.close()
    if ip in actct:
        actct.remove(ip)
def start_server():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((socket.gethostname(),1234))
    s.listen(5)
    monitor_thread=threading.Thread(target=hb,daemon=True)
    monitor_thread.start()
    
    while True:
        clientsocket,address = s.accept()
        thread = threading.Thread(target=handle_client ,args=(clientsocket,address))
        thread.start()
if __name__=="__main__":
    start_server()