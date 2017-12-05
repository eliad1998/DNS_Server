# CacheHandler

# This class handles with the cache.
# First reading the mapping file and than updataing it.
from timeit import default_timer
from ttlTimer import ttlTimer
from Mapping import Mapping
import time
class CacheHandler(object):
    def __init__(self, mappingFile):
        # Save the mappings
        self._maps = []
        # List of start times of ttl
        self._ttlStart = []
        # Creates new list of mappings
        self._cache = []
        # In case we put mapping file
        if mappingFile != "":
            # We will read the mapping file and copy the content to the cache
            # We assume that the mapping file is ok (this is not the purpose of this excercise..)
            file = open(mappingFile, "r")
            for line in file:
                # Splitting the line by spaces
                splitted = line.split()
                # The last variable is TTL - always int so we will convert it.
                if len(splitted) == 4:
                    map = Mapping(splitted[0], splitted[1], splitted[2], int(splitted[3]))
                    self._maps.append(map)
                    self._cache.append(map)
                    self._ttlStart.append(ttlTimer(map, default_timer()))
            # Closing the file.
            file.close()

        self._time = time.clock()

    def addMapping(self, mapping, time):
        self._cache.append(mapping)
        self._ttlStart.append(ttlTimer(mapping, time))


    def getCache(self):
        return self._cache

    def getMap(self):
        return self._maps
    # Get list of current time and update the ttl if the time passed
    # Get default time to check how many time passed since we added each file
    def updateTTL(self, defaultTime):
        ttl = 0
        removed = 0
        # Moving on all the cache
        for i in range(0, len(self._cache)):
            map = self._cache[i - removed]
            # Removes the map when ttl passed
            current = map.getTTL()
            # Find the ttl related to this map
            for ttlTime in self._ttlStart:
                ttl = ttlTime.getStartTime()
                # Check if the time passed
                if defaultTime - ttl >= current:
                    # We need to remove this mapping because the ttl passed
                    self._cache.remove(map)
                    removed += 1
                    break

    # End
    # In the cache we will check if this query has a result.
    # Cache our cache
    # Key the key we want to find it's dns query
    # Type - the type of DNS query (A or NS in our excercise)
    def search(self, key, typeQ):
        # Search in the mapping
        for mapping in self.getMap():
            if mapping.getKey() == key and mapping.getType() == typeQ:
                return mapping
        # Search in the cache
        for mapping in self.getCache():
            if mapping.getKey() == key and mapping.getType() == typeQ:
                return mapping

        return None


    # Printing the cache content
    def printCache(self):
        for mapping in self._cache:
           print mapping

