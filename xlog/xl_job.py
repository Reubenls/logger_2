import xlwings as xw
import asyncio
import threading 
import os
import sys
import time

from job import Job



class Xl_Job(Job):
    def __init__(self, book):
        self.book = book
        main_sht = book.sheets[0]
        profile_fn = main_sht[0, 1].value
        main_sht[2, 2].value = os.getcwd()
        Job.__init__(self, profile_fn)

    def setup_output(self, job_profile):
        self.out_sht = self.book.sheets[1]
        self.out_range = self.out_sht[0,0]
        self.out_range.value= self.header
        self.out_range = self.out_range.offset(1)

    def to_file(self, results):
        row = [results.get(h) for h in self.header]
        self.out_range.value = row
        self.out_range = self.out_range.offset(1)

# def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
#     asyncio.set_event_loop(loop)
#     job = Xl_Job(xw.Book(r'C:\Users\Reube\Documents\xllogger\xllogger.xlsm'))
#     loop.run_forever(job.main_loop())

# def start_logger():
#     loop = asyncio.new_event_loop()
#     t = Thread(target=start_background_loop, args=(loop,), daemon=True)
#     t.start()
#     time.sleep(60)
    # wb = xw.Book.caller()
    # job = Xl_Job(wb)
    # task = asyncio.run_coroutine_threadsafe(job.main_loop(),loop)
    # time.sleep(60)

# async def start_server():
#     HOST, PORT = "localhost", 9999
#     server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler)
#     server.ctrl_queue = asyncio.Queue()
#     server.serve_forever()

# async def main():
#     wb = xw.Book(r'C:\Users\Reube\Documents\xllogger\xllogger.xlsm')
#     job = Xl_Job(wb)
#     m = asyncio.create_task(job.main_loop())
#     coro = asyncio.start_server(handle, '127.0.0.1', 8888, loop=loop)
    
#     server = loop.run_until_complete(coro)

# if __name__ == "__main__":
#     # book_path = sys.argv[1] 
#     asyncio.run(main())
    

    
    # HOST, PORT = "localhost", 9999
    # server = SocketServer.TCPServer((HOST, PORT), MyTCPSocketHandler)
    # server.serve_forever()

    # asyncio.run(job.main_loop())
