import socket
import threading
from tkinter import *
from time import sleep

HOST = '127.0.0.1'
PORT = 55555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nickname = input("Input your nickname\n")

def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode("ascii")
            if msg == "NICK":
                try:
                    client_socket.send(nickname.encode("ascii"))
                except Exception as e:
                    client_socket.send(f"Error on client recive function {e}".encode("ascii"))
            else:
                msg_list.insert(END, msg)
            
        except:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    ____ = f"{nickname}-->  " + msg
    client_socket.send(____.encode("ascii")) 

    if msg == "{quit}":
        client_socket.close()
        print("Closing connection")
        top.quit()

def on_closing(event=None):
    my_msg.set("{quit}")
    send()






top = Tk()
top.title("Client App")

messages_frame = Frame(top)
my_msg = StringVar()
scrollbar = Scrollbar(messages_frame)
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
def init():
    msg_list.insert(END, "Send {quit} to quit ")
    sleep(1)
    ###initialize socket connection
    msg_list.insert(END, f"Connecting to {HOST}, {PORT}")
    sleep(3)
    try:
        client_socket.connect((HOST, PORT))
        msg_list.insert(END, "Connected!")
    except:
        msg_list.insert(END, "Error with connecting to server")
        sleep(4)
        exit()
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    ###



if __name__ == "__main__":
    init_thread = threading.Thread(target=init)
    init_thread.start()

top.mainloop()