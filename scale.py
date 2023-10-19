import sys, serial, argparse
import numpy as np
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation


# plot class
class AnalogPlot:
    # constr
    def __init__(self, strPort, maxLen):
        # open serial port
        self.ser = serial.Serial(strPort, 57600)

        self.ax = deque([0.0] * maxLen)
        self.maxLen = maxLen

    # add to buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        self.addToBuf(self.ax, data)

    # update plot
    def update(self, frameNum, a0, maxval):
        try:
            line = self.ser.readline()
            data = float(line)
            # print data debug
            print(data)
            self.add(data)
            a0.set_data(range(self.maxLen), self.ax)
            maxval.set_text(f'max = {max(self.ax)}')
        except KeyboardInterrupt:
            print("exiting")

        return (a0,)

    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()



# main() function
def main():
    # create parser
    parser = argparse.ArgumentParser(description="Load cell serial")
    # add expected arguments
    parser.add_argument("--port", dest="port", required=True)

    # parse args
    args = parser.parse_args()

    # strPort = '/dev/cu.usbserial-A600ahtO'
    strPort = args.port

    print("reading from serial port %s..." % strPort)

    # plot parameters
    analogPlot = AnalogPlot(strPort, 100)

    print("plotting data...")

    # set up animation
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 100), ylim=(0, 200))
    a0, = ax.plot([], [])
    maxval = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    anim = animation.FuncAnimation(fig, analogPlot.update, frames=100, repeat=False, fargs=(a0,maxval), interval=100)

    # show plot
    plt.show()


    # clean up
    analogPlot.close()

    print("exiting.")


# call main
if __name__ == "__main__":
    main()
