import sys
from numpy import mat, mean, power

def read_input(lines):
    for line in lines:
        yield line.rstrip()

f = open("inputFile.txt", "r", encoding='utf-16')
lines = f.readlines()

input = read_input(lines)

input = [float(line) for line in input]

numInputs = len(input)
input = mat(input)
sqInput = power(input,2)
print("%d\t%f\t%f" % (numInputs, mean(input), mean(sqInput)))
# print("report: still alive")
