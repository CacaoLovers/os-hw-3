#!/bin/python3
import os
import sys
import signal

def handler(signum, frame):
    if signum == signal.SIGUSR1:
        print(f"Produced: {produced}")
        sys.exit(0)

def main():
    global produced
    produced = 0

    signal.signal(signal.SIGUSR1, handler)

    pipe1_read, pipe1_write = os.pipe()
    pipe0_read, pipe0_write = os.pipe()
    pipe2_read, pipe2_write = os.pipe()

    pid1 = os.fork()

    if pid1 == 0:
        os.close(pipe1_read)
        os.dup2(pipe1_write, sys.stdout.fileno())
        os.execve("producer.py", ["pyp"], os.environ)

    pid2 = os.fork()

    if pid2 == 0:  # P2
        os.close(pipe0_read)
        os.dup2(pipe0_write, sys.stdin.fileno())
        os.close(pipe2_write)
        os.dup2(pipe2_read, sys.stdout.fileno())
        os.execve("/usr/bin/bc", ["bc"], os.environ)

    os.close(pipe1_write)

    while True:
        expression = os.read(pipe1_read, 100).decode("utf-8").strip()
        if not expression:
            break

        os.write(pipe0_write, (expression + "\n").encode("utf-8"))
        result = os.read(pipe2_read, 100).decode("utf-8").strip()
        print(f"{expression} = {result}")

        produced += 1


    os.kill(os.getpid(), signal.SIGUSR1)

if __name__ == "__main__":
    main()
