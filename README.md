SCMG is a tool leveraging Integer Linear Programming (ILP) to generate high-performance Field-Programmable Gate Array (FPGA)-based multipliers capable of producing both precise and approximate designs. 

The ILP problem is solved using Gurobi; therefore, prior to use, verify that Gurobi is correctly installed and its license is activated. 

The usage is simple: 
1) Navigate to the Gurobi directory and execute graph_gen.py. Before execution, adjust the parameters size (specifying the multiplier's bit width) and step (defining the number of logic levels in the compression process). 
2) To generate a precise multiplier, simply run mult_gen.py. For approximate multipliers, modify the EXPECT_LUT_NUM parameter within mult_gen4approx.py before execution. 
3) The generated multiplier examples are located in the src/rtl directory, while the corresponding testbench files, used for verifying the correctness of the generated multipliers, reside in the src/tb directory.


