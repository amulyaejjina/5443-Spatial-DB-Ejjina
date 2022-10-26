import time
import requests
from globals import MISSILE_GEN_INTERVAL

while True:
    x = requests.get("http://localhost:8080/bg")
    time.sleep(MISSILE_GEN_INTERVAL)

