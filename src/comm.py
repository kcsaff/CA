# External communications through a socket.
#  Allows sending/receiving events from other applications.

import socket
import threading
import SocketServer
import events
from events import Event

def __server():
    class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    
        def handle(self):
            data = self.request.recv(1024)
            if data:
                #print 'S: ', data
                events.put(eval('Event(%s)' % data))
                self.request.send('1')
            else:
                self.request.send('0')
                
    class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        pass
    
    HOST, PORT = 'localhost', 0
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    
    while 1:
        #print ip, port
        yield ip, port
        
server = __server().next
    
def client(ip, port, event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    #print 'C: ', event.format_args()
    sock.send(event.format_args())
    result = sock.recv(1) == '1' # should be '1' if successful
    sock.close()
    return result