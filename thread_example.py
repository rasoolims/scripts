import threading
 
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)
 
# Example usage
def someOtherFunc(data, key):
    print "someOtherFunc was called : data=%s; key=%s" % (str(data), str(key))
 
t1 = FuncThread(someOtherFunc, [1,2], 6)
t2 = FuncThread(someOtherFunc, [3,4], 12)
t3 = FuncThread(someOtherFunc, [5,6], 24)
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()

