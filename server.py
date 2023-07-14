import socket
from  threading import Thread
import time
IPAddress='127.0.0.1'
Port=8080
clients_list={}
BUFFER_SIZE=4096

def handle_showList(c):
    # print()

    count=0
    for cl in clients_list:
        count=count+1
        cl_addr=clients_list[cl]['address'][0]
        conn_with=clients_list[cl]['connected_with']
        msg=''
        if conn_with:
            msg=f'{count},{cl},{cl_addr}, connected with {conn_with} \n'
        else: 
            msg=f'{count},{cl},{cl_addr}, available \n'
        
        cl.send(msg.encode())
        time.sleep(1)
        
        

def handle_msg(c,msg,c_n):
    # print()
    if msg=="show_list":
        handle_showList(c)

def handle_client(c,c_n):
    global clients_list
    global BUFFER_SIZE
    global server

    msg1="Welcome! You are connected to server"
    c.send(msg1.encode())

    while True:
        try:
            BUFFER_SIZE=clients_list[c_n]['file_size']
            chunk=c.recv(BUFFER_SIZE)
            msg=chunk.decode().lower().strip()
            if msg:
                handle_msg(c,msg,c_n)
        except:
            pass

def setup():
    global server
    global IPAddress
    global Port

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((IPAddress,Port))
    server.listen(100)
    print("Server is waiting...")
    accept_conn()

def accept_conn():
    global server
    global client
    client,addr=server.accept()
    print("Connected established with: ",client,"\t",addr)

    client_name=client.recv(4096).decode().lower()

    clients_list[client_name]={'client':client,"address":addr,"connected_with":'',"file_name":'','file_size':4096}




setup_thread=Thread(target=setup).start()
