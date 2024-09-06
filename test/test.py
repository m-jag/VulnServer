import requests
import requests_unixsocket
import json
import websockets
import asyncio
import struct
import socket
import select

# Docker Unix socket path
docker_socket = f"http+unix://{'/var/run/docker.sock'.replace('/', '%2f')}"
docker_websocket = f"ws+unix://{'/var/run/docker.sock'.replace('/', '%2f')}"
# docker_socket = "tcp://localhost:2375"
# docker_socket = "unix:///var/run/docker-cli.sock"

# Docker API endpoint for Windows
# docker_socket = "http://localhost:2375"

# URL to Docker API
url = f"{docker_socket}/version"

def poll_socket(sock):
    while True:
        # Use select to wait until the socket is ready for reading
        read_sockets, _, _ = select.select([sock], [], [], 1.0)
        
        # Check if the socket has data available
        if sock in read_sockets:
            data = sock.recv(4096)  # Read up to 4096 bytes from the socket
            if not data:
                print("Connection closed by the peer.")
                break
            print(data.decode('utf-8'), end="")
            # print("Received data:", data.decode('utf-8'))
        # else:
            # print("No data received, continuing to poll...")

# Send a GET request to list all containers
try:
    # Create a session using requests_unixsocket
    session = requests_unixsocket.Session()

    response = session.get(url, headers={"Content-Type": "application/json"}, timeout=5)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse JSON response
    version = response.json()
    # api_version = version["Components"][0]["Details"]["ApiVersion"]
    api_version = "1.46"
    
    url = f"{docker_socket}/v{api_version}/containers/json"
    response = session.get(url, headers={"Content-Type": "application/json"}, timeout=5)
    containers = response.json()

    # Print container details
    for container in containers:
        container_id = container['Id']
        print(f"Container ID: {container['Id']}")
        print(f"Image: {container['Image']}")
        print(f"Command: {container['Command']}")
        print(f"Status: {container['Status']}")
        print("-" * 40)

        # Example cURL
        # curl -v --no-buffer --unix-socket /var/run/docker.sock -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: localhost" -H "Origin:http://localhost" -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" -H "Sec-WebSocket-Version: 13" http://localhost/containers/d11edf1493a370cc6cd92c610385fa817218ce80e07b42e17c09c50c507922d1/attach/ws?stream=1&stdin=1&stdout=1&stderr=1
    
    # Attach a websocket to Docker
    # https://docs.docker.com/reference/api/engine/v1.46/#tag/Container/operation/ContainerAttachWebsocket
    # uri = f"ws://localhost/containers/{container_id}/attach/ws?stream=true&stdout=true&stderr=true"
    # async def attach_to_container():
    #     async with websockets.unix_connect("/var/run/docker.sock", uri) as websocket:
    #         print(f"Connected to container {container_id} via WebSocket.")

    #         # Listen for messages from the container
    #         try:
    #             s = websocket.transport.get_extra_info('socket')
    #             print(f"Peer Name: {s.getpeername()}")
    #             print(f"Sock Name: {s.getsockname()}")

    #             try:
    #                 # Start polling the socket
    #                 poll_socket(s)
    #             finally:
    #                 # Clean up and close the socket
    #                 print("Closing the socket.")
    #                 s.close()  
                
    #             # in_message = b"pwd\n"
    #             # print(f"Container input: {in_message.decode('utf-8')}")
    #             # header = struct.pack(">B3xI", 0, len(in_message))
    #             # # frame = header + in_message
    #             # frame = in_message
    #             # print("Frame in hex:", frame.hex())
    #             # test = await websocket.send(frame)
    #             # print(test)

    #             # # send_frame(frame)
                
    #             # # out_message = await websocket.recv()
    #             # # print(f"Container output: {out_message.decode('utf-8')}")

    #             # # while True:
    #             #     # if (len(websocket.messages) > 0):
    #             #     #     print(websocket.messages)
    #             #     # print("Waiting on recv")
    #             #     # message = await websocket.recv()
    #             #     # print(f"Container output: {message.decode('utf-8')}")
    #         except websockets.ConnectionClosed:
    #             print("Connection closed.")
    #         except Exception as e:
    #             print(f"Error: {e}") 

    # # Start the asyncio event loop
    # asyncio.run(attach_to_container())
    
    # Works
    url = f"{docker_socket}/v{api_version}/containers/{container_id}/attach?stream=true&stdout=true&stderr=true"
    headers={
        "Content-Type": "application/json",
        "Upgrade": "tcp",
        "Connection": "Upgrade"
    }
    response = session.post(url, headers=headers, stream=True)
    print(f"Headers: {response.headers}")
    # print(f"Content: {response.content}")

    s = socket.fromfd(response.raw.fileno(), socket.AF_UNIX, socket.SOCK_STREAM)
    print(f"Peer Name: {s.getpeername()}")
    print(f"Sock Name: {s.getsockname()}")

    try:
        # Start polling the socket
        poll_socket(s)
    finally:
        # Clean up and close the socket
        print("Closing the socket.")
        s.close()  

except requests.exceptions.RequestException as e:
    print(f"Error communicating with Docker API: {e}")

