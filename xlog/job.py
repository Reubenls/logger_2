import asyncio
import concurrent.futures
import functools
import json
import sys
import time
import datetime
import csv
import importlib
from collections import defaultdict
from threading import Lock
from auto_profile import Auto_Profile_Manager as apm

job_fn = "profile.json"
ap_fn = "profile.csv"

pool = concurrent.futures.ThreadPoolExecutor()
write_queue = ""


class Job(object):
    def __init__(self,profile_fn):
        self.instruments = {}
        self.operations = []
        self.groups = {}
        self.header = []
        self.setup(profile_fn)
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.ctrl_queue = ''
        self.action_queue = asyncio.Queue


    def setup(self,job_fn):
        job_profile = {}
        with open(job_fn, "r") as job_profile_file:
            job_profile = json.load(job_profile_file)
        inst_spec = job_profile.get("instruments")
        ops_spec = job_profile.get("operations")
        self.load_instruments(inst_spec)
        self.setup_operations(ops_spec)
        self.setup_output(job_profile)
        self.min_interval = job_profile.get("min_interval")
        self.auto_profile = apm(ap_fn)
        
    
    def load_instruments(self,inst_spec):
        for inst_id, instrument in inst_spec.items():
                if inst_id in self.instruments:
                    break
                else:
                    if isinstance(instrument, str):
                        try:
                            if instrument.endswith(".json"):
                                instrument = json.load(open(instrument))
                                inst_id = instrument["instrument_id"]
                                driver_name= instrument.get("driver")
                                driver = getattr(importlib.import_module("."+driver_name,"xlog.drivers"),driver_name)#, package="logger_2.drivers"))
                            else:
                                driver = getattr(__import__("drivers." + instrument), instrument)

                            # klass = getattr(driver, driver_name)
                            klass = driver
                            inst_driver = klass(instrument)
                            self.instruments[inst_id] = inst_driver

                        except (OSError, ValueError):
                            sys.stderr.write("Error Loading Insturment: {}/n driver: {}".format(inst_id,driver))
                            sys.exit(1)

    def load_autoprofile(self,ap_fn):
        with open(ap_fn,'r') as ap:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['first_name'], row['last_name'])
            return 

    def setup_operations(self,ops_spec):  
        self.header = ["datetime","runtime"]
        for operation in ops_spec:
            operation = operation+".-1"
            inst_id,op_id, group = (operation.split('.')[:3])
            self.header.append(inst_id+"."+op_id)
            self.operations.append((inst_id,op_id))
        
        self.groups = defaultdict(list)
        # for item in self.operations:
        #     k = 0 if item[2]== "-1" else 2
        #     self.groups[item[k]].append(item)
        
       
    
    def setup_output(self,job_profile):
        self.out_fn = job_profile.get("datafile_raw")   
        with open(self.out_fn, "w+") as outfile:
            for k, v in job_profile.items():
                if k not in ["instruments", "operations"]:
                    outfile.write(k + ": " + str(v) + "\n")
            writer = csv.writer(outfile, self.header, lineterminator='\n')
            writer.writerow(self.header)

        
    async def main_loop(self):
        self.start_time = time.time() 
        self.action_queue = asyncio.Queue()
        self.auto_profile.action_queue = self.action_queue
        self.auto_profile.restart()
        self.running = True
        self.paused = False
        self.waiting = False
        await asyncio.gather(self.action_loop(),self.ctrl_loop(),self.log_loop())
        print("exit job loop")
        return True

    async def ctrl_loop(self):
        while self.running:
            ctrl_msg = await self.ctrl_queue.get()
            cmd = ctrl_msg[0]
            if cmd == 'stop':
                self.stop()
            elif cmd == 'pause':
                self.pause()
            elif cmd == 'resume':
                self.resume()
            elif cmd == 'request':
                req = ctrl_msg[1]
                self.action_queue.put_nowait(req)
                
            self.ctrl_queue.task_done()
            
    def stop(self):
        self.paused = True
        self.running = False

    def pause(self):
        self.paused = True

    def wait(self):
        self.waiting = True

    def unwait(self):
        self.waiting = False


    
    def resume(self):
        self.paused = False

    async def log_loop(self):
        await asyncio.sleep(1)
        while self.running:
            print("."," ")
            while not self.paused and not self.waiting:
                loop = asyncio.get_running_loop()
                latest_time = loop.time()
                result = await self.log_ops()
                self.to_file(result)
                self.auto_profile._update(time.time())
                next_time = latest_time + self.min_interval
                latest_time = loop.time()

                #print('Sleep',(next_time-loop.time()))
                if next_time > latest_time:
                    #print('Sleep %s',(next_time-loop.time()))
                    await asyncio.sleep(next_time-loop.time())

            await asyncio.sleep(1)

    async def log_ops(self):

        loop = asyncio.get_running_loop()
        latest_time = loop.time()
        req = [self.request(*op) for op in self.operations]
        requests = asyncio.gather(*req)
        await requests
        result = {}
       # print(requests)
        for res in requests.result():
            result.update(res)
        result.update(self.timestamp())
        return result

    async def action_loop(self):
        while self.running:
            try:
                req = await asyncio.wait_for(self.action_queue.get(), timeout=1.0)
                self.wait()
                inst_op, args = req
                inst_id, op_id = inst_op.split('.')
                res = await self.request(inst_id,op_id,args)
               # print(res)
                self.action_queue.task_done()
                if self.action_queue.empty():
                    self.unwait()
            except asyncio.TimeoutError:
                pass

    async def request(self,inst_id,op_id,args=None):
        
        a = []
        a.append(args)
        instrument  = self.instruments[inst_id]
        
        lock = self.lock_inst(instrument)
        async with lock:
            if hasattr(instrument,op_id) and callable(getattr(instrument,op_id)):
                f = getattr(instrument,op_id)
                if args is not None:
                    result = f(*a)
                else:
                    result = f()
            else:
                print ("error _ to fix lookup json ")
                return(-1)
        result = {inst_id+"."+op_id:result}
        return (result)

        
        
    def lock_inst(self,inst):
        if inst.lock is None:
            inst.lock = asyncio.Lock()
        return inst.lock    
        
    def timestamp(self):
        date_time = datetime.datetime.now()
        runtime = (time.time() - self.start_time)/60
        #print("runtime (min) ",runtime)
        return {"datetime":date_time,"runtime":runtime}

    def to_file(self, results):
        with open(self.out_fn, "a") as output:
                writer = csv.DictWriter(output, fieldnames=self.header, lineterminator='\n', dialect="excel")
                writer.writerow(results)




if __name__ == "__main__":
  job = Job()
  asyncio.run(job.main_loop())