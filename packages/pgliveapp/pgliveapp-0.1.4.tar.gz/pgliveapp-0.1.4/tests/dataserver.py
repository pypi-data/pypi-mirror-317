import math
import pickle
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCK_ADDRESS = ("localhost", 4000)

try:
    while True:
        time.sleep(0.02)

        t = time.time()
        sock.sendto(
            pickle.dumps(
                {
                    "x": t,
                    "y1": math.sin(2 * math.pi * t),
                    "y2": math.sin(2 * math.pi * t),
                    "y3": math.sin(2 * math.pi * t),
                    "y4": -math.sin(2 * math.pi * t),
                    "y5": -math.sin(2 * math.pi * t),
                    "y6": -math.sin(2 * math.pi * t),
                    "y7": math.sin(2 * math.pi * t * 2),
                    "y8": math.sin(2 * math.pi * t * 2),
                    "y9": math.sin(2 * math.pi * t * 2),
                    "y10": -math.sin(2 * math.pi * t * 2),
                    "y11": -math.sin(2 * math.pi * t * 2),
                    "y12": -math.sin(2 * math.pi * t * 2),
                    "y13": math.sin(2 * math.pi * t * 0.5),
                    "y14": math.sin(2 * math.pi * t * 0.5),
                    "y15": math.sin(2 * math.pi * t * 0.5),
                    "y16": -math.sin(2 * math.pi * t * 0.5),
                    "y17": -math.sin(2 * math.pi * t * 0.5),
                    "y18": math.sin(2 * math.pi * t * 0.5),
                }
            ),
            SOCK_ADDRESS,
        )

except KeyboardInterrupt:
    sock.close()
    print("Closed socket.")
