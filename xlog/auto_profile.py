# import numpy as np
# import pandas as pd 
import csv
import time
import sys

class Auto_Profile_Manager(object):
    def __init__(self,ap_fn):
        self.profile = self.read_csv('xlog\\'+ap_fn)
        
        print(self.profile)
        self.row_num = 0
        self.current = self.profile[0]
        self.at_row_count = 0
        self.row_time = time.time()
        self.action_queue = 0

    def read_csv(self,fn):
        profile = []
        header = ['a']
        
        with open(fn,'r') as ap:
            # header = ap.readline()
            csv_reader = csv.DictReader(ap)
            actions = csv_reader.__next__() 
            checks = csv_reader.__next__()
            for row in csv_reader:
                profile.append(row)
            actions = {v:k for (k,v) in actions.items()}
            actions.pop('',0)
            self.actions = actions
            print(self.actions)
        return profile

    def to_excel(self):
        #todo
        pass

    def save_state(self):
        with open('savestate.csv','w+') as save_file:
            writer = csv.writer(save_file)
            writer.writerow(self.current)

    def load_state(self,fn):
        pass
        #todo load saved state

    def goto(self,row):
        self.row_num = row
        self.current = self.profile[row]
        self.at_row_count = 0
        self.row_time = time.time()
        self._inst_actions()
        self._log()
        #todo go to row

    def _log(self):
        with open('ap_log.csv','a+') as ap_log:
           writer = csv.writer(ap_log)
           writer.writerow(self.current.values())

    def _inst_actions(self):
        for action, v_key in self.actions.items():
            val = self.current.get(v_key)
            self.action_queue.put_nowait((action,val))

    def restart(self):
        self.goto(0)

    def _update(self,u_time):
        u_time = u_time - self.row_time
        self.at_row_count+=1
        self.current['time'] = u_time
        self.current['arc'] = self.at_row_count
        self._log()
        if u_time >= float(self.current['soak']):
            return self.next()
        else:
            return ('pass')

    def save_points(self,n):
        pass

    def close(self):
        pass
        

    def finished(self):
        print('finished')
        sys.exit(0)
        # todo check if repeat and notifie logger 

    def next(self):
        #todo check assured soak
        # check if finished
        self.row_num += 1
        if self.row_num >= len(self.profile):
            return('finished')
            self.finished()



        self.current = self.get_row(self.row_num)
        self.at_row_count = 0
        a = self._inst_actions()
        #todo update generator
        #todo check generator updated
        self._log()
        return(a)
        
    def get_row(self,row):
        return self.profile[row]

def main():
    apm = Auto_Profile_Manager('profile.csv')
    for _ in range(20):
        apm._update(time.time())
        time.sleep(10)


if __name__ == "__main__":
    main()