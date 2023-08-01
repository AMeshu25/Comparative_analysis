import sys, os, time
import threading
import Settings as s #Global settings variables



class Realsense (threading.Thread) :

    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        os.system(s.realsense_path)
    def stop(self):
        os.system("taskkill /f /im  nuitrack_console_sample.exe")
        print("stop realsense")
        # os.system("taskkill /f /im  cpp-realsense.exe")

if __name__ == '__main__':
    r = Realsense()
    s.realsense_path = R'C:\Users\TEMP.NAAMA\PycharmProjects\Nuitrack\nuitrack\Examples\nuitrack_console_sample\out\build\x64-Debug\nuitrack_console_sample.exe'
    r.run()
