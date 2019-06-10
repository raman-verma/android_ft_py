import subprocess
import os
dirList = []
process = subprocess.Popen(["adb shell ls /sdcard/WhatsApp/Media"], shell=True, stdout=subprocess.PIPE)
stdout = process.communicate()[0]
dirList = [i.replace(" ","\\ ") for i in format(stdout.decode("utf-8")).split("\n")]
print(dirList)