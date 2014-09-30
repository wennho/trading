import sys, os
import time

if len(sys.argv) < 3:
    print "Usage: python main.py <classList> <quarterList>"
    sys.exit()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from course import courseScheduler


def readIntoList(input):
    inputList = []
    for rawLine in open(input):
        line = rawLine.strip()
        if line :
            inputList.append(line)
    return inputList


classList = readIntoList(sys.argv[1])
quarterList = readIntoList(sys.argv[2])


startTime = time.clock()

result = courseScheduler.findSchedule(classList, quarterList)

for _ in range(3):
    possSch = next(result, None)

    if possSch:
        print "Possible schedule:"
        possSch.printOut()
    else:
        print "No more schedules"

timeTaken = time.clock() - startTime
print "timeTaken=", timeTaken
print classList
