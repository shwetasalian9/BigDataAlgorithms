##########################################################################
## streamingCSE545sp22_lastname_id.py  v1
## 
## Template code for assignment 1 part 1. 
## Do not edit anywhere except blocks where a #[TODO]# appears
##
## Student Name:
## 1) Shweta Salian
## 2) Saurabh Pandey
## 3) Sai Raghava Mallik Vaddipati



import sys
from pprint import pprint
from random import random
from collections import deque
from sys import getsizeof
import resource
import math
import random
import numpy as np

##########################################################################
##########################################################################
# Methods: implement the methods of the assignment below.  
#
# Each method gets 1 100 element array for holding ints of floats. 
# This array is called memory1a, memory1b, or memory1c
# You may not store anything else outside the scope of the method.
# "current memory size" printed by main should not exceed 8,000.

MEMORY_SIZE = 100 #do not edit

memory1a =  deque([None] * MEMORY_SIZE, maxlen=MEMORY_SIZE) #do not edit

"""
Method to implement formula to calculate hash value of the element 
with given estimated values of a and b
"""
def calculate_hash(estimate_a, estimate_b, element):
    return (estimate_a * element + estimate_b) % 2**16

"""
Method to implement flojet martin algorithm to get distinct values
in a given stream of data using the median of means approach
"""
def flojet_martin_algorithm(element):
    count = 0
    for estimate_a in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]:
        for estimate_b in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]:
            # running the loop for each hash function
            max_element = 0

            # Processing binary 0 count
            hash_value = calculate_hash(estimate_a, estimate_b, element)
            if hash_value != 0:
                for i in bin(hash_value)[:1:-1]:
                    if i == "0":
                        max_element += 1
                    else:
                        break

            if memory1a[count] == None:
                memory1a[count] = 2**max_element
            else:
                if memory1a[count] < 2**max_element:
                    memory1a[count] = 2**max_element

            count += 1


def task1ADistinctValues(element, returnResult=True):
    # [TODO]#
    # procss the element you may only use memory1a, storing at most 100

    flojet_martin_algorithm(element)

    if returnResult:  # when the stream is requesting the current result
        means = []
        temp_array = np.array(memory1a)
        for i in range(5):
            means.append(np.mean(temp_array[5 * i : 5 * i + 5]))
        return np.median(means)

    else:  # no need to return a result
        pass



memory1b =  deque([None] * MEMORY_SIZE, maxlen=MEMORY_SIZE) #do not edit

def task1BMedian(element, returnResult = True):
    #[TODO]#
    #procss the element

    """
    Method to implement formula to calculate median of given stream of elements
    """
    def med(stream):
        alpha = len(stream) / np.sum([np.log(x) for x in stream])
        return np.power(2, 1 / alpha)

    """
    Method to call function to calculate median
    """
    def calculate_median(stream):
        median = med(stream)
        return median

    if bool(memory1b) and memory1b[0] is None:
        memory1b.clear()
        memory1b.append(element)
    elif len(memory1b) < memory1b.maxlen:
        memory1b.append(element)
    else:
        k = len(memory1b)
        result = calculate_median(memory1b)
        memory1b.clear()
        return result    
    
    if returnResult:  # when the stream is requesting the current result
        result = 0
        # [TODO]#
        # any additional processing to return the result at this point
        if len(memory1b) > 1:
            result = calculate_median(memory1b)

        return result
    else:  # no need to return a result
        pass
    

memory1c =  deque([None] * MEMORY_SIZE, maxlen=MEMORY_SIZE) #do not edit

def task1CMostFreqValue(element, returnResult = True):
    #[TODO]#
    #procss the element
    
    """
    Method to call function to calculate mode
    """
    def calculate_mode(a, axis=0):
        unique_values = np.unique(np.ravel(a))
        shape = list(a.shape)
        shape[axis] = 1
        most_freq= np.zeros(shape)
        count = np.zeros(shape)

        for value in unique_values:
            is_equal = (a == value)
            value_counts = np.expand_dims(np.sum(is_equal, axis), axis)
            most_freq = np.where(value_counts > count, value, most_freq)
            count = np.maximum(value_counts, count)

        return most_freq, count

    """
    Method to call function to calculate most frequent value
    """
    def calc_most_freq_value(stream):
        mode_prev = stream.popleft()
        count_prev = stream.popleft()
        mode, count = calculate_mode(np.array(stream))
        stream.clear()
        if count > count_prev:
            stream.append(mode)
            stream.append(count)
        else:
            stream.append(mode_prev)
            stream.append(count_prev)

    if memory1c[0] == None:
        memory1c.clear()
        memory1c.append(element)
        memory1c.append(1)
    elif len(memory1c) == memory1c.maxlen:
        calc_most_freq_value(memory1c)
        memory1c.append(element)
    else:
        memory1c.append(element)

    if returnResult:  # when the stream is requesting the current result
        result = 0
        # [TODO]#
        # any additional processing to return the result at this point
        if len(memory1c) > 2:
            calc_most_freq_value(memory1c)
        result = memory1c[0]

        return result
    else:  # no need to return a result
        pass


##########################################################################
##########################################################################
# MAIN: the code below setups up the stream and calls your methods
# Printouts of the results returned will be done every so often
# DO NOT EDIT BELOW

def getMemorySize(l): #returns sum of all element sizes
    return sum([getsizeof(e) for e in l])+getsizeof(l)

if __name__ == "__main__": #[Uncomment peices to test]
    
    print("\n\nTESTING YOUR CODE\n")
    
    ###################
    ## The main stream loop: 
    print("\n\n*************************\n Beginning stream input \n*************************\n")
    filename = sys.argv[1]#the data file to read into a stream
    printLines = frozenset([10**i for i in range(1, 20)]) #stores lines to print
    peakMem = 0 #tracks peak memory usage
    
    with open(filename, 'r') as infile:
        i = 0#keeps track of lines read

        for line in infile:
            #remove \n and convert to int
            element = int(line.strip())
            i += 1
            #call tasks         
            if i in printLines: #print status at this point: 
                result1a = task1ADistinctValues(element, returnResult=True)
                result1b = task1BMedian(element, returnResult=True)
                result1c = task1CMostFreqValue(element, returnResult=True)
                
                print(" Result at stream element # %d:" % i)
                print("   1A:     Distinct values: %d" % int(result1a))
                print("   1B:              Median: %.2f" % float(result1b))
                print("   1C: Most frequent value: %d" % int(result1c))
                print(" [current memory sizes: A: %d, B: %d, C: %d]\n" % \
                    (getMemorySize(memory1a), getMemorySize(memory1b), getMemorySize(memory1c)))
                
            else: #just pass for stream processing
                result1a = task1ADistinctValues(element, False) 
                result1b = task1BMedian(element, False)
                result1c = task1CMostFreqValue(element, False)
                
            memUsage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if memUsage > peakMem: peakMem = memUsage
        
    print("\n*******************************\n       Stream Terminated \n*******************************")
    print("(peak memory usage was: ", peakMem, ")")