                                        #Identity Operators
#Identity operators are used to compare the memory locations of two objects to check if they refer to the same object.
a = [1,2,3]
b=a
c = [1,2,3]
#is : Returns True if both variables refer to the same object in memory
a is b  #output=True
#is not : Returns True if variables do not refer to the same object
a is not c  #output=True
