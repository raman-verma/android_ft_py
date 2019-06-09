import subprocess
import os
dirList = []
process = subprocess.Popen(["adb shell ls /sdcard/mp3"], shell=True, stdout=subprocess.PIPE)
stdout = process.communicate()[0]
dirList = [i for i in format(stdout.decode("utf-8")).split("\n")]
print(dirList)