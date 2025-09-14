import requests
import time
import random

SERVER = "http://127.0.0.1:5000/update_traffic"

DIRECTIONS = ["NORTH", "SOUTH", "EAST", "WEST"]

def simulate():
    while True:
        for direction in DIRECTIONS:
            count = random.randint(1, 15)  # random gaadiyon ka count
            try:
                res = requests.post(SERVER, json={
                    "direction": direction,
                    "count": count
                })
                print(f"[{direction}] Sent {count} vehicles → {res.text}")
            except Exception as e:
                print(f"Error sending to server: {e}")
        time.sleep(5)  # har 5 second me update

if __name__ == "__main__":
    simulate()
