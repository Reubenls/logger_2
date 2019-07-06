import asyncio

async def tcp_client(message, loop):
    reader, writer = await asyncio.open_connection('localhost', 9999,
                                                   loop=loop)
    print('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()


def send(message):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_client(message, loop))
    loop.close()
