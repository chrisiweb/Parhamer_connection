import re
import os

x = "C:/Users/Christoph/Desktop/LaMA Test/.tex"

print(os.path.basename(x))

rsp = re.search("[_&]", os.path.basename(x))

print(rsp)