import random

def get_random_number(min, max, decimal=0):
    x = round(random.uniform(min,max),decimal)

    if decimal == 0:
        return int(x)
    else:
        return x

x = get_random_number(0,100,3)
y= get_random_number(0,100,2)

print(x)
print(y)
print('{0} + {1} = {2}'.format(x,y,x+y))