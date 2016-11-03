'''
Master control class
--------------------------------------------
'''

import logging
import threading
import time
import multiprocessing
import traceback
import sys


import config
from store import store
from remote import remote

log = logging.getLogger(__name__)

SEED_FILE_PATH = 'seed.txt'
THREAD_PAUSE_TIME = 1 # seconds

''' Top Level Method '''
def start():

    store.empty_db()
    f = open(SEED_FILE_PATH, 'r')
    urls = f.read().splitlines()

    # for url in urls:
    #     if remote.checkValidity(url):
    #         print("seeeeeeee:      "+url)
    #     else:
    #         print('oooooooops')
    # return

    for url in urls:
        # give those urls highest priority
        store.queue_push(url, 0)

    cpu_count = multiprocessing.cpu_count()
    # cpu_count = 1
    
    print('Mutithreading Number is %s' % str(cpu_count))

    for cpu_index in range(cpu_count):
        try:
            t = threading.Thread(target=_single_crawler, args=("Thread-"+str(cpu_index),))
            t.daemon=True
            t.start()
        except:
            log.debug("Error: unable to start thread %s" % cpu_index)

    # keep the main thread alive
    while True:
        time.sleep(1)

def _single_crawler(thread_name):
    '''
    one threading function that calls remote run constantly
    '''
    while True:
        try:
            remote.run(thread_name)
        except Exception as e:
            print('[%s] (BUG!!!)Unhandled exception occurs' % thread_name)
            print(e)
            print(traceback.format_exc())
        time.sleep(THREAD_PAUSE_TIME)
        # break;
