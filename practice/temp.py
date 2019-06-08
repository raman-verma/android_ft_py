import subprocess
import os
# dirList = []
# process = subprocess.Popen(["adb shell ls"], shell=True, stdout=subprocess.PIPE)
# stdout = process.communicate()[0]
# dirList = [i for i in format(stdout.decode("utf-8")).split("\n")]
# print(dirList)


def add(paths):
    entry = '/'
    return os.path.join(paths, entry)

while 1:
    a = input()
    print(add(a))
