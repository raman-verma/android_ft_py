import subprocess
import os
import re

dirList = []
process = subprocess.Popen(["adb shell ls /sdcard"], shell=True, stdout=subprocess.PIPE)
stdout = process.communicate()[0]
dirList = [i.replace(" ", "\\ ") for i in format(stdout.decode("utf-8")).split("\n")]
print(dirList)

pattern = ['.txt', '.mp3', '.mp4', '.xls', '.ulog']
print(str.join("", dirList))

reg = r"\.\w+"

a = re.search(reg, str.join("", dirList), re.MULTILINE)
print("---->", a)

# a = (f for f in dirList if f.endswith())
# for _ in a:
#     print(_)


# list = ["guru99 get", "guru99 give", "guru Selenium"]
# for element in list:
#     z = re.match("(g\w+)\W(g\w+)", element)
#     print((z.groups()))
