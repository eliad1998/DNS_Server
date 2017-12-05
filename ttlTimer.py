class ttlTimer(object) :
    def __init__(self, map, startTime):
        self._map = map
        self._startTime = startTime

    def getMap(self):
        return self._map

    def getStartTime(self):
        return self._startTime
