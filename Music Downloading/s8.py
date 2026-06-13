import socket
import threading
import yt_dlp
import os
MUSIC_PATH ="music"
def download_audio(url):
    if not os.path.exists(MUSIC_PATH):
        os.makedirs(MUSIC_PATH)
    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
        'outtmpl': os.path.join(MUSIC_PATH, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "Download complete!"
    except Exception as e:
        return"Download failed"
def handle_client(clientsocket,address):
    try:
        url = clientsocket.recv(1024).decode('utf-8')
        if url:
            print("Requst received to download")
            response = download_audio(url)
            clientsocket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Client error")
    finally:    
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