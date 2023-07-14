import socket
from  threading import Thread
from tkinter import *
from tkinter import ttk,filedialog

server=None
port=8080
IPAddress='127.0.0.1'
listbox=None
textarea=None
BUFFER_SIZE=4096
# name_input=None

def show_clientList():
    global server
    global listbox
    print()
    listbox.delete(0,"END")
    server.send("show_list".encode())

def conn_to_server():
    global server
    global name_input

    client_n=name_input.get()
    server.send(client_n.encode())

def open_chat_window():
    window=Tk()
    window.title("FTP")
    window.geometry("580x400")

    name_Label=Label(window,text="Name ",font=("Comic Sans MS",15))
    name_Label.place(x=10,y=10)

    global name_input
    name_input=Entry(window,width=30,font=("Comic Sans MS",10))
    name_input.place(x=150,y=10)
    name_input.focus()

    connect_to_server_button=Button(window,text="Connect to server",font=("Comic Sans MS",10),command=conn_to_server)
    connect_to_server_button.place(x=400,y=10)

    seperator=ttk.Separator(window,orient="horizontal")
    seperator.place(x=0,y=50,relwidth=1,relheight=0.01)

    active_users_label=Label(window,text='Active Users',font=("Comic Sans MS",15))
    active_users_label.place(x=10,y=70)

    list_box=Listbox(window,width=70,height=5,activestyle="dotbox",font=("Comic Sans MS",12))
    list_box.place(x=10,y=100)

    scroll_list=Scrollbar(list_box)
    scroll_list.place(relx=1,relheight=1)
    scroll_list.config(command=list_box.yview)

    connect_button=Button(window,text="Connect",font=("Comic Sans MS",10))
    connect_button.place(x=120,y=180)

    disconnect_button=Button(window,text="Disconnect",font=("Comic Sans MS",10))
    disconnect_button.place(x=200,y=180)

    refresh_button=Button(window,text="Refresh",font=("Comic Sans MS",10),command=show_clientList)
    refresh_button.place(x=300,y=180)

    seperator=ttk.Separator(window,orient="horizontal")
    seperator.place(x=0,y=210,relwidth=1,relheight=0.01)

    chat_window_label=Label(window,text="Chat Window", font=("Comic Sans MS",15))
    chat_window_label.place(x=0,y=220)

    text_area=Text(window,font=("Comic Sans MS",12),width=70,height=6).place(x=10,y=250)

    attach_send_button=Button(window,text="Attach and send",font=("Comic Sans MS",12)).place(x=20,y=350)
    enter_msg_button=Entry(window,font=("Comic Sans MS",10),width=50).place(x=160,y=350)
    send_button=Button(window,text="Send",font=("Comic Sans MS",10)).place(x=500,y=350)

    # scroll_text=Scrollbar(text_area)
    # scroll_text.place(relx=1,relheight=1)
    # scroll_text.config(command=text_area.yview)
    window.mainloop()
def recv_msg():
    global server
    global BUFFER_SIZE
    

    while True:
        chunk = server.recv(BUFFER_SIZE)
        try:
            if("tiul" in chunk.decode() and "1.0," not in chunk.decode()):
                letter_list = chunk.decode().split(",")
                listbox.insert(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
                print(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
            else:
                textarea.insert(END,"\n"+chunk.decode('ascii'))
                textarea.see("end")
                print(chunk.decode('ascii'))
        except:
            pass

def setup():
    global server
    global IPAddress
    global port

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((IPAddress,port))

    open_chat_window()

setup()