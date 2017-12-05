# Mapping

# This class stores data about a mapping

# Mapping contains 4 fields: Key, Type, Value and TTL.


class Mapping(object):
    # key - What the query search for
    # type - what is the type A or NS
    # value - what is the value (ip or ns)
    # ttl - time to leave
    def __init__(self, key, type ,value, ttl):
        self._key = key
        self._type = type
        self._value = value
        self._ttl = ttl

    # Get functions
    def getKey(self):
        return self._key

    def getType(self):
        return self._type

    def getValue(self):
        # In case of ip:port
        str = self._value.split(":")[0]
        return str

    def getTTL(self):
        return self._ttl

    def getPort(self):
        # In case of ip:port
        str = ""
        if len(self._value.split(":")) > 1:
            str = self._value.split(":")[1]
        return str


    def __str__(self):
        str = "[Key :{}] [Type:{}] [Value {}] [TTL: {}]".format(self._key, self._type, self._value,self._ttl)
        return str

    def stringConvert(self):
        if self.getPort() != "":
            str = "{},{},{}:{},{}".format(self._key, self._type,self._value,self.getPort(),self._ttl)
        else:
            str = "{},{},{},{}".format(self._key, self._type, self._value, self._ttl)
        return str

    @staticmethod
    def fromString(str):
        splitted= str.split(",")
        mapping = None
        if len(splitted) >= 4:
            mapping = Mapping(splitted[0], splitted[1], splitted[2], int(splitted[3]))
        return mapping



