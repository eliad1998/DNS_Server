from socket import socket, AF_INET, SOCK_DGRAM
from Mapping import  Mapping
from timeit import default_timer
from CacheHandler import CacheHandler
s = socket(AF_INET, SOCK_DGRAM)
# My ip in this case.
dest_ip = '127.0.0.1'
dest_port = 12345
msg = raw_input("Message to send: ")
cache = CacheHandler("")
while not msg == 'quit':
    splitted = msg.split()
    # The requested key and type.
    if (len(splitted) == 2):
        #  Updataing the cache ttl
        if cache != None:
            cache.updateTTL(default_timer())
        requestedKey = splitted[0]
        requestedType = splitted[1]
        # First searching for ns
        #        typeA = typeQ == "A"
        # Search for map with this key or value
        mapSearch = cache.search(requestedKey, requestedType)
        if (mapSearch == None):
            s.sendto(msg, (dest_ip,dest_port))
            data, _ = s.recvfrom(2048)
            # We made the messages to end at @ and after it there will be string represent the map
            splitted = data.split("@")
            message = splitted[0]
          #  foundMap = Mapping.fromString(splitted[1])
            # Adding the mapping file
           # cache.addMapping(foundMap, default_timer())
            print "Server sent: ", message
        else:
            print "The answer for " + requestedKey + " " \
                  + requestedType + "  is " + mapSearch.getValue()

    # Wrong query
    else :
        print "Wrong query, try again"
    msg = raw_input("Message to send: ")
#s.close()
