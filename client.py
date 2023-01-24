import socket
import threading
from tkinter import *
from time import sleep

HOST = '127.0.0.1'
PORT = 55555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nickname = input("Input your nickname\n")




    


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(1024).decode("ascii")
            if msg == "NICK":
                try:
                    client_socket.send(nickname.encode("ascii"))
                except Exception as e:
                    msg_list.insert(END, f"Error {e}")
                    
            else:
                msg_list.insert(END, msg)
            
        except:
            break

def inputhandler(event=None):
    """Handles commands and message input"""
    input = my_msg.get()
    my_msg.set("")
    if input == "{quit}":
        client_socket.close()
        print("Quiting...")
        msg_list.insert(END, "Quiting...")
        top.quit()

    elif input == "{connect}":
        msg_list.insert(END, f"Connecting to {HOST}, {PORT}")
        sleep(1)
        try:
            client_socket.connect((HOST, PORT))
            msg_list.insert(END, "Connected!")
        except:
            msg_list.insert(END, "Error with connecting to server")
            sleep(2)
            pass
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
    elif input == "{disconnect}":
        try:
            msg_list.insert(END, "Disconnecting from server")
            sleep(1)
            client_socket.close()
            msg_list.insert(END, "Disconnected!")
        except:
            msg_list.insert(END, "You are already disconnected")
    elif input == "{help}":
        msg_list.insert(END, "Avaible commands: \n ")
        msg_list.insert(END, "\n {help} Prints this message")
        msg_list.insert(END, "\n {connect} Connects to server")
        msg_list.insert(END, "\n {disconnect} disconnects from server")
        msg_list.insert(END, "\n {quit} quits from this app")
        msg_list.insert(END, "\n {clear} clears message history")
    elif input == "{clear}":
        msg_list.delete(0, END)
    else:
        try:
            send(input)
        except:
            msg_list.insert(END, "First connect to server")




def send(msg):
    """Handles sending of messages."""
    ____ = f"{nickname}-->  " + msg
    client_socket.send(____.encode("ascii")) 


def on_closing(event=None):
    my_msg.set("{quit}")







top = Tk()
top.title("Chat App")

messages_frame = Frame(top)
my_msg = StringVar()
scrollbar = Scrollbar(messages_frame)
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", inputhandler)
entry_field.pack()
send_button = Button(top, text="Send", command=inputhandler)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
def init():
    ###initialize program
    msg_list.insert(END, f"Welcome {nickname} \n")
    msg_list.insert(END, "Enter {connect} to connect to server or enter {help} to see other commands")
    sleep(2)
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    ###



if __name__ == "__main__":
    init_thread = threading.Thread(target=init)
    init_thread.start()

top.mainloop()