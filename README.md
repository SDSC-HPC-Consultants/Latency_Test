Latency Test
============

This repo contains the codes to carry out Latency Tests on [Comet](http://www.sdsc.edu/support/user_guides/comet.html).

Background
----------

Latency is the time delay between simulation and response between 2 nodes. For this test, we send 1 Mb data from one node to another and calculate the time delay. This calculation is carried out using the [OMB Benchmark](https://www.nersc.gov/users/computational-systems/cori/nersc-8-procurement/trinity-nersc-8-rfp/nersc-8-trinity-benchmarks/omb-mpi-tests/) module under the [MVAPICH Package](http://mvapich.cse.ohio-state.edu/benchmarks/) to carry out our Latency tests.

The Comet CPU node architecture is illustrated below:
![Architecture](https://github.com/SDSC-HPC-Consultants/Latency_Test/blob/master/static/Nodes.png)

Let us first look at some of theese 18 CPU nodes. Below you can see the label of 3 nodes: comet-07-26, comet-07-27 and comet-07-28.

![Individual CPU Nodes](https://github.com/SDSC-HPC-Consultants/Latency_Test/blob/master/static/CPU%20nodes.jpg)

Each node contains 48 Intel processor cores. These are 48 cores are distributed among 4 sockets. 36 cores are used for compputations while 12 cores are used as parity under [RAID 5](http://en.wikipedia.org/wiki/Standard_RAID_levels#RAID_5) technology. A user is allowed to access 36 cores per node on Comet.

On the label, the first part, "comet" tells you that these are Comet nodes. The second part, "07", means the node is on Rack 07. The third part, "26", "27" and "28" represent the unique identifier of each node on Rack 07. 

All 18 of these switches, comet-07-[19-36], are connected to the L1 switch via InfiniBand Interconnects as seen below:

![L1 level](https://github.com/SDSC-HPC-Consultants/Latency_Test/blob/master/static/L1%20Switches.jpg)

The L1 switches from each set of 18 nodes are connected to all the other sets on the same rack via the L2 switch. Finally, all the racks on Comet are connected to eachother via the MID TIER switch.

For this test, we will check the latency of every node pair combination of the sets of 18 at the L1 level:

![Latency Test](https://github.com/SDSC-HPC-Consultants/Latency_Test/blob/master/static/LT.png)

Recommended Setup
-----------------

Install MVAPICH Benchmark on your local system by entering the following on your terminal:
```
  wget http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-4.4.1.tar.gz

  gunzip xvf osu-micro-benchmarks-4.4.1.tar.gz

  tar xvf osu-micro-benchmarks-4.4.1.tar

  cd osu-micro-benchmarks-4.4.1

  ./configure

  make
```

Running Tests
-------------

For running a sample OMB Benchmark Latency Test between nodes comet-10-01 and comet-10-02, 
use the sample [Slurm](http://slurm.schedmd.com/) batch script:

```

#!/bin/bash

#SBATCH -o results.out
#SBATCH -e results.err
#SBATCH --nodes 2
#SBATCH --ntasks-per-node 1
#SBATCH -w comet-10-01, comet-10-02 
#SBATCH -t 01:00:00
#SBATCH --mail-type ALL
#SBATCH --mail-user <User Email>
#SBATCH -A use300

#We dont have a root binary for latency and hence using our own
export BINARY = /<path-to-installation>/mpi/pt2pt/osu_latency

#Activate Latency file from OMB Benchmark and ibrun for parallel processing
ibrun -v $BINARY 

```
On the above batch script, 1 core from each node, comet-10-[01-02], exchange data and the latency is recorded in ```results.out```. Any coding error will be recorded on ```results.err```. When the calculation is done, an email will sent to email address specified on ```<User Email>```. We will be running our tests on the ```use300``` projects group. Notice that we specified a ```BINARY``` path to our MVAPICH installation directory. Comet does not allow us to have root installation without admin level previledges. As a result, we create our own binary on the login node. 

Here is a [PBS/Torque](https://kb.iu.edu/d/avmy) batch script for running the same test on Gordon or TSCC:

```

#!/bin/bash

#PBS -o results.out
#PBS -e results.err
#PBS -l nodes=2:ppn=1:ib
#PBS -l nodes=comet-10-01, comet-10-02
#PBS -l walltime=[01:00:00]
#PBS -M <User Email>
#PBS -m abe
#PBS -A use300

#We dont have a root binary for latency and hence using our own
export BINARY = /<path-to-installation>/mpi/pt2pt/osu_latency

#Activate Latency file from OMB Benchmark and ibrun for parallel processing
ibrun -v $BINARY `

```

The entire process of performing OMB Benchmark Latency tests on CPU nodes at L1 switch level is 
automated by the [latency.py](https://github.com/SDSC-HPC-Consultants/Latency_Test/blob/master/latency.py) script.
