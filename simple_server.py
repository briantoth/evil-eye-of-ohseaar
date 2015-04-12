import socket
import sys
import thread

HOST = ''
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'


def clientThread(conn, image_num):

    received = ""
    while True:
        data = conn.recv(1024)
        if not data:
            with open('test-image-upload-' + str(image_num) + '.jpg', 'w+') as f:
                f.write(received)

            break

        received += data
        print 'Received data!'

    conn.close()

i = 0
while True:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    thread.start_new_thread(clientThread, (conn, i))
    i += 1

s.close()
