import asyncio


async def tcp_client(message):
    ip = "127.0.0.1"
    port = 8000
    reader, writer = await asyncio.open_connection(ip, port)

    print(f"Send: {message!r}")
    writer.write(message.encode())

    data = await reader.read(100)
    print(f"Received: {data.decode()!r}")

    print("Close the connection")
    writer.close()


asyncio.run(tcp_client("Hello World!"))
