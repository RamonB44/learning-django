
def rename(self,key,new_key):
    ind = self._keys.index(key)  #get the index of old key, O(N) operation
    self._keys[ind] = new_key    #replace old key with new key in self._keys
    self[new_key] = self[key]    #add the new key, this is added at the end of self._keys
    self._keys.pop(-1)           #pop the last item in self._keys