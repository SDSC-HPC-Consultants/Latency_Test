_author_='Syed Sadat Nazrul'

import subprocess
import numpy as np
import re
from itertools import combinations
import datetime

def latency_time(filename):
    '''
    Collects latency value from output file
    :param filename (string): name of output file
    :return: latency times for 1 Mb (CSV file)
    '''
    file=open(filename)
    str2search=''
    for message in file:
	    str2search += message
    word_search=re.search('(?!1\s+)([\d\.]+)',str2search)
    result=(word_search.group()).split()
    return result

def BatchScript(Rack, Node_List, begin_time='now', Email='sadatnazrul@gmail.com'):
    '''
    Generates and submits a batch script for running OMB Latency testing
    :param Rack (int): Rack number
    :param Node_List (int list): List of nodes in given rack
    :param begin_time (str): Time to begin running the job
    :param Email (string): Email address for receiving job updates
    :return: None
    '''
    #Get time
    now = datetime.datetime.now()
    time = int(now.strftime("%Y%m%d"))

    #Generate a batch script
    f=open("batch_script", "w")
    f.write("#!/bin/bash")
    description='''
#SBATCH --job-name=comet-%02d-[%02d-%02d]
#SBATCH -o osu_%d_comet-%02d-[%02d-%02d].out
#SBATCH -e osu_%d_comet-%02d-[%02d-%02d].err
#SBATCH --nodes %d
#SBATCH -w comet-%02d-[%02d-%02d]
#SBATCH --ntasks-per-node 1
#SBATCH -t 00:00:20
#SBATCH --mail-type END
#SBATCH --mail-user %s
#SBATCH -A use300
#SBATCH --begin=%s
export BINARY=/home/ssnazrul/mpi_test/osu-micro-benchmarks-4.4.1/mpi/pt2pt/osu_latency
        '''%(
            Rack, Node_List[0], Node_List[-1],          #Job Name
            time, Rack, Node_List[0], Node_List[-1],    #Output File
            time, Rack, Node_List[0], Node_List[-1],    #Error File
            len(Node_List),                             #Number of Nodes
            Rack, Node_List[0], Node_List[-1],          #Node list
            Email                                       #Email address for job updates
            begin_time					#Time to start job
    )
    f.write(description)
    Node_Combinations=combinations(Node_List, 2)
    for Node_Pair in Node_Combinations:
        [node1,node2]=Node_Pair
        node1=int(node1)
        node2=int(node2)
        f.write("\n")
        f.write("echo comet-%02d-%02d,comet-%02d-%02d\n"%(Rack,node1,Rack,node2))
        f.write("srun -t 00:00:03 -w comet-%02d-%02d,comet-%02d-%02d -N 2 -n 2  --mpi=pmi2 $BINARY\n"%(Rack,node1,Rack,node2))
    f.write("python analyze.py *out")
    f.close()
    subprocess.call(["sbatch","batch_script"])     #Submit Batch Script
    subprocess.call(["rm","batch_script"])         #Delete Batch Script after submission

#Running latency test
#racks=[int(i) for i in np.linspace(1,29,29)]
#racks.remove(9)
#racks.remove(24)
#for rack in racks:
#    BatchScript(rack,np.linspace(1,18,18))
#    BatchScript(rack,np.linspace(19,36,18))
#    BatchScript(rack,np.linspace(37,54,18))
#    BatchScript(rack,np.linspace(55,72,18))

BatchScript(21, np.linspace(1,18,18))
BatchScript(21, np.linspace(19,36,18))
BatchScript(21, np.linspace(37,54,18))
BatchScript(21, np.linspace(55,72,18))
