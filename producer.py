#!/usr/bin/python3
import random
import time
import sys
import os

N = random.randint(120, 180)

for _ in range(N):
    X = random.randint(1, 9)
    O = random.choice(['+', '-', '*', '/'])
    Y = random.randint(1, 9)

    print(f"{X} {O} {Y}")
    sys.stdout.flush()

    time.sleep(1)

os._exit(0)