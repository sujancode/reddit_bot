import time
from bots.account_create import run as account_create

while True:
    print("Starting Creating Account Process")
    account_create()
    print("Process Ended")
    time.sleep(10*60)