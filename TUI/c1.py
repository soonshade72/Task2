import socket 
import pyaudio
import threading
import curses 
from curses import wrapper 
import time
def main(stdscr):
    stdscr.addstr(0,1,"Press P to Play")
    stdscr.addstr(1,1,"Press Q to Stop")
    stdscr.refresh()
    while True:
        try :
            key = stdscr.getkey()
        except:
            key= None    
        if key in['p','P']:
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
    p = pyaudio.PyAudio()
    CHUNK = 1024
    stream=p.open(format=p.get_format_from_width(2),
                  channels = 2,
                  rate=44100,
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
