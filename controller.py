#!/usr/bin/python3
import os
import signal
import sys

def sigusr1_handler(signum, frame):
    global produced_count
    output = "Produced: " + str(produced_count) + "\n"
    sys.stderr.write(output)

signal.signal(signal.SIGUSR1, sigusr1_handler)

pipe1to0 = os.pipe()
pipe0to2 = os.pipe()
pipe2to0 = os.pipe()

P1 = os.fork()

if P1 == 0:
    os.close(pipe0to2[0])
    os.close(pipe0to2[1])
    os.close(pipe2to0[0])
    os.close(pipe2to0[1])
    os.close(pipe1to0[0])
    os.dup2(pipe1to0[1], sys.stdout.fileno())
    os.execve('./producer.py', ['./producer.py'], os.environ)
    os._exit(0)

P2 = os.fork()

if P2 == 0:
    os.close(pipe1to0[0])
    os.close(pipe1to0[1])
    os.close(pipe0to2[1])
    os.close(pipe2to0[0])
    os.dup2(pipe0to2[0], sys.stdin.fileno())
    os.dup2(pipe2to0[1], sys.stdout.fileno())
    os.execve('/usr/bin/bc', ['/usr/bin/bc'], os.environ)
    os._exit(0)

os.close(pipe1to0[1])
os.close(pipe0to2[0])
os.close(pipe2to0[1])

produced_count = 0

while True:
    ariphmetic_expression = os.read(pipe1to0[0], 1024).decode("utf-8")
    if not ariphmetic_expression:
        os.kill(os.getpid(), signal.SIGUSR1)
        break
    os.write(pipe0to2[1], ariphmetic_expression.encode("utf-8"))
    bc_result = os.read(pipe2to0[0], 1024).decode("utf-8")
    print(f"{ariphmetic_expression.strip()} = {bc_result.strip()}")
    produced_count += 1

os.kill(P1, signal.SIGTERM)
os.kill(P2, signal.SIGTERM)

os._exit(0)