"""
A proxy server that forwards requests from one port to another server.

To run this using Python 2.7:

% python proxy.py

It listens on a port (`LISTENING_PORT`, below) and forwards commands to the
server. The server is at `SERVER_ADDRESS`:`SERVER_PORT` below.
"""

# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to thxe language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import library
import socket
import sys

# Where to find the server. This assumes it's running on the same machine
# as the proxy, but on a different port.
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 7777

# The port that the proxy server is going to occupy. This could be the same
# as SERVER_PORT, but then you couldn't run the proxy and the server on the
# same machine.
LISTENING_PORT = 8888

# Cache values retrieved from the server for this long.
MAX_CACHE_AGE_SEC = 60.0  # 1 minute


def ForwardCommandToServer(command, server_addr, server_port):
  Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  Socket.connect((server_addr, server_port))
  Socket.send(command)
  response = library.ReadCommand(Socket)
  return response

def CheckCachedResponse(command_line, cache, server_addr, server_port):
  cmd, name, text = library.ParseCommand(command_line)
  if cmd == "GET":
      if cache.GetValue(name, MAX_CACHE_AGE_SEC): #if in cache
          return cache.GetValue(name, MAX_CACHE_AGE_SEC) #get the value at key
      else: #if not in cache
          get = ForwardCommandToServer(command_line, server_addr, server_port) #forward cmd to server, store in database
          cache.StoreValue(name, get) #store in cache
          return get #return GET

  elif cmd == "PUT":
      if cache.GetValue(name, MAX_CACHE_AGE_SEC):
          cache.StoreValue(name, text)
      return ForwardCommandToServer(command_line, server_addr, server_port)

  else:
      return ForwardCommandToServer(command_line, server_addr, server_port)

def ProxyClientCommand(sock, server_addr, server_port, cache):
  command_line = library.ReadCommand(sock)
  response = CheckCachedResponse(command_line, cache, server_addr, server_port)
  sock.send(response)


def main():
  # Listen on a specified port...
  server_sock = library.CreateServerSocket(LISTENING_PORT) #proxy
  cache = library.KeyValueStore()
  # Accept incoming commands indefinitely.
  while True:
    # Wait until a client connects and then get a socket that connects to the
    # client.
    try:
        client_sock, (address, port) = library.ConnectClientToServer(server_sock, SERVER_PORT)
        print('Received connection from %s:%d' % (address, port))
        ProxyClientCommand(client_sock, SERVER_ADDRESS, SERVER_PORT,
                           cache)
    except KeyboardInterrupt:
        print("\nUser closed proxy server")
        sys.exit(0)

    client_sock.close()


main()
