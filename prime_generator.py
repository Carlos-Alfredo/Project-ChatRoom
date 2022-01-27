from random import randint
from mod import isPrime,findPrimitive

x=randint(pow(10,15),pow(10,16))
while not isPrime(x):
	x=randint(pow(10,15),pow(10,16))
print(x)
y=findPrimitive(x)
print(y)