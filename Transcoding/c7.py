import socket 
import pyaudio
import threading
import curses 
from curses import wrapper 
import time
import subprocess
import re
def hb(stdscr,target_host):
    while True:
        try:
            output=subprocess.check_output(
                ['ping','-n','1',target_host],
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            rtt_match=re.search(r'time[=<]([\d]+)ms',output,re.IGNORECASE)
            if rtt_match:
                rtt=int(rtt_match.group(1))
                if rtt<10:
                    quality="Excellent"
                elif rtt<50:
                    quality="Good"
                else:
                    quality="Poor"
                stdscr.addstr(6,1,f"strength:{quality}(Ping:{rtt}ms)")
            else:
                stdscr.addstr(6,1,"Timeout")
            stdscr.refresh()
        except subprocess.CalledProcessError:
            stdscr.addstr(6,1,"Server Offline")
            stdscr.refresh()
        except Exception as e:
            pass
        time.sleep(1)        

def main(stdscr):
    stdscr.addstr(0,1,"Press P to Play")
    stdscr.addstr(1,1,"Press Q to Stop")
    stdscr.refresh()
    server_host=socket.gethostname()
    monitor_thread = threading.Thread(target=hb, args=(stdscr, server_host), daemon=True)
    monitor_thread.start()
    is_playing = False
    while True:
        try :
            key = stdscr.getkey()
        except:
            key= None    
        if key in['p','P'] and not is_playing:
            is_playing=True
            stdscr.addstr(3,1,"Connecting to server and playing..")
            stdscr.addstr(4,1,"press'q' to exit. ")
            stdscr.refresh()
            a=threading.Thread(target=start_client,daemon=True)
            a.start()
        elif key in ['q','Q']:
            break
def start_client():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((socket.gethostname(),1234))
    quality = s.recv(1)
    ch=1 if quality==b'0' else 2
    rt=11025 if quality==b'0' else 44100
    p = pyaudio.PyAudio()
    CHUNK = 1024
    stream=p.open(format=p.get_format_from_width(2),
                  channels = ch,
                  rate=rt,
                  output=True,
                  frames_per_buffer=CHUNK)
    while True:
        try:
            data=s.recv(4096)
            if not data: 
                break
            stream.write(data)
        except Exception as e:
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    s.close()
if __name__=="__main__":
    wrapper(main)
