import hashlib

#hashing 
def HashingAValue(Value):
    #Salting the string before hashing which makes it more secure
    SaltValue = "#######"
    PasswordWithSaltValue = Value + SaltValue
    #Needs to be in byte form first before it can be converted into a hash 256 value
    EncodedValue = bytes(Value, 'utf-8')
    HashingObject = hashlib.sha256()
    HashingObject.update(EncodedValue)
    value = HashingObject.hexdigest()
    return value



