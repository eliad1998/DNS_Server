from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
from CacheHandler import CacheHandler
from timeit import default_timer
from Mapping import Mapping
import random
# In this demo of dns we just return random ip not the real (it is demo of dns)
# The mapping file is an argument to main
mapFile = argv[3]


def searchInServer(port, key, type, sock, cache, startMsg):
    dest_ip = '127.0.0.1'
    dest_port = int(port)
    # I split the message because we need to hold the key and type but doing an iterative function (asking for the
    #domain)
    message = startMsg + "|" + key +" " + type
    sock.sendto(message, (dest_ip, dest_port))
    # Receive the answer to the query
    data, sender_info = sock.recvfrom(2048)
    # We made the messages to end at @ and after it there will be string represent the map
    queries = data.split("\n")
    splitted = queries[0].split("@")
    print "Message: ", splitted[0], " from: ", sender_info
    foundMap = Mapping.fromString(splitted[1])
    # Adding the mapping file
    cache.addMapping(foundMap, default_timer())
    if (len(queries) > 1):
        splitted = queries[1].split("@")
        print "Message: ", splitted[0], " from: ", sender_info
        foundMap = Mapping.fromString(splitted[1])
        # Adding the mapping file
        cache.addMapping(foundMap, default_timer())
    return foundMap
  #  s.close()
def getIpPort(mapFile):
    lst = []
    file = open(mapFile, "r")
    for line in file:
        # Splitting the line by spaces
        splitted = line.split()
        # The last variable is TTL - always int so we will convert it.
        if len(splitted) == 2:
            lst.append(splitted[0])
            lst.append(splitted[1])
            file.close()
            return lst
    # Closing the file.
    file.close()
# Suppose that the mapping file contains in the last line the ip and port of this server
# For example 127.0.0.2 15222
source_ip = getIpPort(mapFile)[0]
source_port = int(getIpPort(mapFile)[1])
def main():
   # In the cache we will check if this quert has a result.
   # Cache our cache
   # Key the key we want to find it's dns query
   # Type - the type of DNS query (A or NS in our excercise)

    cacheHandler = CacheHandler(mapFile)
    # Argv command line arguments
    # The first parameter to the server is if the server is resolver
    resolver = argv[1]
    # The second parameter to the server is the root server ip and the port
   # For example 127.0.0.2:11111
    rootPort = argv[2]

    s = socket(AF_INET, SOCK_DGRAM)

   # The socket to our server
    s.bind((source_ip, source_port))
    while True:
        #  Updataing the cache ttl
        if (cacheHandler != None):
            cacheHandler.updateTTL(default_timer())
        #cacheHandler.printCache()
        data, sender_info = s.recvfrom(2048)
        # Printing the query to the client
        if resolver == "1":
            print "Message: ", data.split("@")[0], " from: ", sender_info
            splitted = data.split()
        else:
            print "Message: ", data.split("|")[0], " from: ", sender_info
            splitted = data.split("|")[1].split()

        # The last variable is TTL - always int so we will convert it.
        key = ""
        typeQ = ""
        msg = "Please send key and the type for example 'com A'"
        if len(splitted) == 2:
            # The ip or nsof the server we want to find answer to the query
            serverToSearch = '127.0.0.1'
            portToSearch = rootPort
            # The requested key and type.
            requestedKey = splitted[0]
            requestedType = splitted[1]
            # Key and type that changes each iterate by our sub query
            key = requestedKey
            typeQ = requestedType
            # First searching for ns
    #        typeA = typeQ == "A"
            # Search for map with this key or value
            mapSearch = cacheHandler.search(key, typeQ)
            # 1 if resolver
            if resolver == "1":
                # First check if the cache can handle this query
                if mapSearch != None:
                    msg = "The answer for " + mapSearch.getKey() +\
                          " is " + mapSearch.getValue() + "@" + Mapping.stringConvert(mapSearch)
                # Did not found answer in the cache
                else:
                    # Splitting the domain by points.
                    splitAddress = key.split('.')
                    # Starting the iterating (from the end of caurse)
                    for i in range(len(splitAddress) - 1,-1,-1):
                        if i == len(splitAddress) - 1:
                            key = splitAddress[i]
                        else:
                            # Updating the key from com to ac.come for example.
                            key = splitAddress[i] + "." + key
                        # Search for result to this query
                        mapSearch = cacheHandler.search(key, typeQ)
                        # Found
                        if mapSearch != None:
                            serverToSearch = '127.0.0.1'
                            msg = "The answer for " + key + " " \
                                  + typeQ + "  is " + mapSearch.getValue() + "@" + mapSearch.stringConvert()
                        else:
                            # Search in the root server and adding the asnwer to the cache
                            # The mapping we got from the server
                            if requestedType == "A" and i != 0:
                                mapServer = searchInServer(portToSearch, key,"NS", s, cacheHandler,data.split("@")[0])
                                portToSearch = mapServer.getPort()
                            if i == 0 and requestedType == "A":
                                mapServer = searchInServer(portToSearch, key, "A", s, cacheHandler, data.split("@")[0])
                                portToSearch = mapServer.getPort()
                                msg = "The answer for " + requestedKey + " is " + mapServer.getValue() + "@" \
                                      + mapServer.stringConvert()

                            if requestedType == "NS":
                                mapServer = searchInServer(portToSearch, key, "NS", s, cacheHandler, data.split("@")[0])
                                cacheHandler.addMapping(mapServer, default_timer())

            # Not resolver - check only by it's mapping and cache
            else:
                if (mapSearch != None):
                    msg = "The answer for " + requestedKey + " is " + mapSearch.getValue() + "@" \
                          + mapSearch.stringConvert()
                    if (requestedType == "NS"):
                        # Now we do A query on the name server.
                        key = mapSearch.getValue()
                        typeQ = "A"
                        mapSearch = cacheHandler.search(key, typeQ)
                        if mapSearch != None:
                            msg2 = "\n" + "The answer for " + key + " is " + mapSearch.getValue()
                            msg3 = "@" + mapSearch.stringConvert()
                            msg = "".join((msg, msg2))
                            msg = "".join((msg, msg3))
        else:
            # Did not found the answer in the cache or mapping file.
            #his server is not resolver so we can not return answer to this query.
            msg = "Did not found answer to this query"

        s.sendto(msg, sender_info)

# Running the main
if __name__ == "__main__":
    main()


