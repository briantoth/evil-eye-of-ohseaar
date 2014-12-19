import socket
import sys
import thread
import Image
import cStringIO as StringIO
import binascii

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


def clientThread(conn):

    received = ""
    while True:
        data = conn.recv(1024)
        if not data:
            with open('test-image-upload.jpg', 'w+') as f:
                f.write(received)

            image = Image.open('test-image-upload.jpg')
            image.show()
            break

        received += data
        print 'Received data!'

    conn.close()

while True:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    thread.start_new_thread(clientThread, (conn,))

s.close()
