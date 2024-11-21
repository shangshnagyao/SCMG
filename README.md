SCMG: Scalable and Configurable FPGA-based Multiplier Generator using Integer Linear Programming
=====================
SCMG is a tool leveraging Integer Linear Programming (ILP) to generate high-performance Field-Programmable Gate Array (FPGA)-based multipliers capable of producing both precise and approximate designs. 

The ILP problem is solved using Gurobi; therefore, prior to use, verify that Gurobi is correctly installed and its license is activated. 

### Installing Gurobi

Go to [Gurobi website](https://www.gurobi.com/) to register and request an academic license, and download the Gurobi library.
In bin subdirectory of Gurobi directory, please run 
```Bash
./grbgetkey <key-you-obtained>
``` 
to activate your Gurobi, detailed in [Gurobi installation guide](https://www.gurobi.com/documentation/9.0/quickstart_linux/software_installation_guid.html#section:Installation).

After Gurobi is activated, please run
```Bash
mkdir lib
ln $GUROBI_HOME/linux64/lib/gurobi.jar lib/
``` 
in this directory to use the Gurobi library in this project.

## Quick Start
Make sure Gurobi is successfully installed.
### Multiplier Graph generation
Navigate to the ./gurobi directory and execute graph_gen.py. Before execution, adjust the parameters size (specifying the multiplier's bit width) and step (defining the number of logic levels in the compression tree process). 
```Bash
python graph_gen.py --size 8 --step 4
``` 

### Accurate Multiplier generation
To generate an accurate multiplier, simply run mult_gen.py.
```Bash
python mult_gen.py
``` 
  
### Approximate Multiplier generation
For approximate multipliers, modify the LUT target utilization within mult_gen4approx.py before execution. 
```Bash
python mult_gen4approx.py --target 45
``` 

The generated multiplier examples are located in the src/rtl directory, while the corresponding testbench files, used for verifying the correctness of the generated multipliers, reside in the src/tb directory.


