#!/bin/python3

import random
import time

def generate_expression():
    x = random.randint(1, 9)
    o = random.choice(['+', '-', '*', '/'])
    y = random.randint(1, 9)
    return f"{x} {o} {y}"

def main():
    N = random.randint(1, 18)

    for _ in range(N):
        expression = generate_expression()
        print(expression)
        time.sleep(1)

if __name__ == "__main__":
    main()
