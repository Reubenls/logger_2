import asyncio
import json
import sys
import time
import datetime
import csv
from collections import defaultdict
job_fn = "profile.json"



instruments = {}
operations = []
groups = {}
data_fn = ""
start_time = time.time()
header = []

def setup():
    job_profile = {}
    global instruments
    with open(job_fn, "r") as job_profile_file:
        job_profile = json.load(job_profile_file)
    inst_spec = job_profile.get("instruments")
    instruments = {}
    

    for inst_id, instrument in inst_spec.items():
            if inst_id in instruments:
                break
            else:
                if isinstance(instrument, str):
                    try:
                        print(instrument)

                        instrument = json.load(open(instrument))
                    except (OSError, ValueError):
                        sys.stderr.write("Error Loading Insturment: {}".format(inst_id))
                        sys.exit(1)
                inst_id = instrument["instrument_id"]
                driver_name= instrument.get("driver")
                driver = getattr(__import__("drivers." + driver_name), driver_name)
                klass = getattr(driver, driver_name)
                inst_driver = klass(instrument)
                instruments[inst_id] = inst_driver

    global header
    header = ["datetime","runtime"]
    for operation in job_profile.get("operations"):
        operation = operation+".-1"
        inst_id,op_id, group = (operation.split('.')[:3])
        header.append(inst_id+"."+op_id)
        operations.append((inst_id,op_id,group))
    
    global data_fn
    data_fn = job_profile.get("datafile_raw")
    with open(data_fn, "w+") as outfile:
        for k, v in job_profile.items():
            if k not in ["instruments", "logged_operations"]:
                outfile.write(k + ": " + str(v) + "\n")
        writer = csv.writer(outfile, header, lineterminator='\n')
        writer.writerow(header)

    global groups
    groups = defaultdict(list)
    for item in operations:
        k = 0 if item[2]== "-1" else 1
        groups[item[k]].append(item)

    

async def main_loop():
    print(groups)
    group_req = [sync_group(g) for g in groups.values()]
    requests = asyncio.gather(*group_req)
    await requests
    print (requests)
    
    result = {}
    for d in requests.result():
        result.update(d)
    result.update(timestamp())
    print (result)
    to_file(result)
    
def timestamp():
    date_time = datetime.datetime.now()
    runtime = time.time() - start_time
    return {"datetime":date_time,"runtime":runtime}

    


async def sync_group(group):
    res = {}
    print(group)
    for item in group:
        i, o, g= item
        # r = await request(item[0],item[1])
        print(i,o)
        r = instruments[i].read(o)
        res[i+"."+o] = r
    return res

        


def to_file(results):
    with open(data_fn, "a") as output:
            writer = csv.DictWriter(output, fieldnames=header, lineterminator='\n', dialect="excel")
            writer.writerow(results)

async def request(inst_id, op_id):
    print("starting {}.{}",ins_id,op_id)
    result = await instruments[inst_id].read_instrument(op_id)
    print("finished {}.{}",inst_id,op_id)
    return result


setup()
asyncio.run(main_loop())