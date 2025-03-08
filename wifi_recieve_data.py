import socket

import asyncio
import websockets


def please_work(keyCode):
    HOST = "172.20.10.10" # IP address of your Raspberry PI
    PORT = 65432          # The port used by the server


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(keyCode.encode())     
        data = s.recv(1024)
        message = str(data)
        print("from server: ", data)
        return message

async def process_key(connection):
    while True:
        try:
            keycode = await connection.recv()
            print(f"Received keycode: {keycode}")
            please_work(keycode)



            await connection.send(f"Key {keycode} processed")
        
        except websockets.exceptions.ConnectionClosed:
            break



async def send_repeated_key(connection):
        while True:
            try:
                await asyncio.sleep(0.2)  
                print("Sending keycode: 114")
                data = please_work('114')  
                print(data)
         
                await connection.send(data[2:-1])  
            except websockets.exceptions.ConnectionClosed:
                break



async def start_server():
    server = await websockets.serve(process_key, "0.0.0.0", 8765)
    print("Hello")

    print("HERE2")
    serverw = await websockets.serve(send_repeated_key, "0.0.0.0", 8766)


    await server.wait_closed()
    await serverw.wait_closed()


asyncio.run(start_server())