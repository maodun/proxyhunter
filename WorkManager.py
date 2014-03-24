#coding=utf-8

import Queue, sys
from threading import Thread
import urllib

##class ResultDict:
##    def __init__(self, resultDict):
##        self.resultDict = resultDict
##    def put(self, index, result):
##        self.resultDict[index] = result
##    def get(self, index):
##        return self.resultDict.pop(index, None)
##        

#work thread
class Worker(Thread):
    worker_count = 0
    def __init__(self, workQueue, resultQueue, timeout=0 ,**kwds):
        Thread.__init__(self, **kwds)
        self.id = Worker.worker_count
        Worker.worker_count += 1
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.timeout = timeout
        self.start()
    def run(self):
        while True:
            try:
                callable_func, args, kwds = self.workQueue.get(timeout=self.timeout)
                res = callable_func(*args, **kwds)
                #print "worker[%2d]: %s" %(self.id, str(res))
                self.resultQueue.put(res)
            except Queue.Empty:
                break
            except :
                print 'worker[%2d]' % self.id, sys.exc_info()[:2]
                
class WorkerManager:
    def __init__(self, num_of_workers = 10, timeout=1):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruitThreads(num_of_workers)
        
    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue, self.timeout)
            self.workers.append(worker)
            
    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)
        #return True
    #    print "Done."
    def add_job(self, callable_func, *args, **kwds):
        self.workQueue.put((callable_func, args, kwds))
    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)

