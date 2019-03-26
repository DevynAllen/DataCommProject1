"""A set of libraries that are useful to both the proxy and regular servers."""

#Testing github connection

# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# The Python socket API is based closely on the Berkeley sockets API which
# was originally written for the C programming language.
#
# https://en.wikipedia.org/wiki/Berkeley_sockets
#
# The API is more flexible than you need, and it does some quirky things to
# provide that flexibility. I recommend tutorials instead of complete
# descriptions because those can skip the archaic bits. (The API was released
# more than 35 years ago!)
import socket

import time

# Read this many bytes at a time of a command. Each socket holds a buffer of
# data that comes in. If the buffer fills up before you can read it then TCP
# will slow down transmission so you can keep up. We expect that most commands
# will be shorter than this.
COMMAND_BUFFER_SIZE = 256

def CreateServerSocket(port):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('localhost', port)) #bind host address and port together
    serverSocket.listen(1) #how many clients server can listen to at once
    print("Waiting for client to connect...")
    return serverSocket

def ConnectClientToServer(server_sock, port):
    clientSocket, address = server_sock.accept() #accept new connection
    return clientSocket, (address, port)

def CreateClientSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ReadCommand(clientSocket):
    data = clientSocket.recv(1024)
    return data

def ParseCommand(command):
  args = command.strip().split(' ')
  command = None
  if args:
    command = args[0]
  arg1 = None
  if len(args) > 1:
    arg1 = args[1]
  remainder = None
  if len(args) > 2:
    remainder = ' '.join(args[2:])
  return command, arg1, remainder


class KeyValueStore(object):
  """A dictionary of strings keyed by strings.

  The values can time out once they get sufficiently old. Otherwise, this
  acts much like a dictionary.
  """

  def __init__(self):
    #TODO: Implement __init__ Function
    self._dictionary = {}

  def GetValue(self, key, max_age_in_sec=None):
    """Gets a cached value or `None`.

    Values older than `max_age_in_sec` seconds are not returned.

    Args:
      key: string. The name of the key to get.
      max_age_in_sec: float. Maximum time since the value was placed in the
        KeyValueStore. If not specified then values do not time out.
    Returns:
      None or the value.
    """
    if not self._dictionary[key]:
        return None
    elif self._dictionary[key] > max_age_in_sec:
        return None
    else:
        return self._dictionary[key]
    # Check if we've ever put something in the cache.

  def StoreValue(self, key, value):
    #Stores a value under a specific key.
    self._dictionary[key] = value
    print("stored %s with value of %s" % (key, value))

  def Keys(self):
      for value in self._dictionary:
          print(self._dictionary[key])
