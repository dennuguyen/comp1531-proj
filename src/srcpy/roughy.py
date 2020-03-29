import threading
import time

package = []

def collect_and_send():
    global package
    message = f'{package[0]}' ' + ' f'{package[1]}' ' + ' f'{package[2]}'
    print(message)

def pack1():
    global package
    package.append('package1')
    return

def pack2():
    global package
    package.append('package1')
    return
 
def pack3():
    global package
    package.append('package3')
    return

t1 = threading.Timer(5.0, collect_and_send)
t2 = threading.Timer(1.0, pack1)
t3 = threading.Timer(2.0, pack2)
t4 = threading.Timer(3.0, pack3)
t1.start()
t2.start()
t3.start()
t4.start()