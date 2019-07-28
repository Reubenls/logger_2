import asyncio
import concurrent.futures
import xlwings as xw
from job import Job
from xl_job import Xl_Job




async def main():
    ctrl_queue = asyncio.Queue()
    
    server =  Ctrl_Server(ctrl_queue,'localhost',9999)
    await server.start_server()
    wb = xw.Book(r'C:\Users\j.lovellsmith\PycharmProjects\xl_log\xllogger.xlsm')
    job = Xl_Job(wb)
    job.ctrl_queue = ctrl_queue
       
    loop = asyncio.get_running_loop()
    try:
        await asyncio.gather(
            server.serve_forever(), job.main_loop())
    except asyncio.CancelledError:
        print ('canceled error')
    except RuntimeError:
        print ("rt errror")
         


def stop(ctrl_queue):
    ctrl_queue.put_nowait(('stop'))
    for tasks in asyncio.all_tasks():
        print (dir(tasks))
    ctrl_queue.put_nowait(('stop',))

def pause(ctrl_queue):
    ctrl_queue.put_nowait(('pause',))

def resume(ctrl_queue):
    ctrl_queue.put_nowait(('resume',))

def request(ctrl_queue,req):
    ctrl_queue.put_nowait(('request',req))



    
class Ctrl_Server:
    def __init__(self,queue,host,port):
        self.ctrl_queue = queue
        self.host = host
        self.port = port

    async def start_server(self):
        self.server = await asyncio.start_server(self.handle,self.host,self.port)

    async def serve_forever(self):
        await self.server.serve_forever()

    async def handle(self,reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))
        if message == 'stop':  
            stop(self.ctrl_queue)
        elif message == 'pause':
            pause(self.ctrl_queue)
            print("pause sent to queue")
        elif message == 'resume':
            resume(self.ctrl_queue)
        elif message.startswith('request'):
            cmd,req = message.split('.',1)
            request(self.ctrl_queue,req)

        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()
        print("Close the client socket")
        writer.close()

if __name__ == "__main__":
    asyncio.run(main())