This toolbox computes QIF(Quantitative Information Flow)* of a sequential hardware module written in verilog. The QIF is computed as the logarithm of the number of unique outputs of a primary output which quantifies the amount of information flowing (Shannon's Entropy) from secret to the observable output. 
Assumption:
The hardware module is modeled as an information-theoretic channel with secrets as inputs and observable output as the output of the channel. If the hardware module is deterministic and the input distribution is uniform then according to [1], QIF is log2(number of unique outputs). The RTL design (verilog) has to be synthesized into gate-level netlist using 15nm open cell NAND library. For more details see [2].

Dependencies: 
1. Approxmc model counter tool for counting the number of solutions. Can be installed using: "pip install pyapproxmc". For more details: https://github.com/meelgroup/approxmc

Usage:
1. Synthesize the RTL module into a gate-level netlist using the 15nm open cell NAND library.
2. Run unroll_seq_test.py to unroll the netlist to the desired sequential depth and convert it into bench format.
3. Run bench2cnf_approxmc.py with the unrolled bench file to get the number of unique solutions
	a. define unroll depth
	b. define the length of output in bits.
4. You can also set/reset control bits of the module to run the FSM in the desired mode.

[1] Smith, Geoffrey. "On the foundations of quantitative information flow." International Conference on Foundations of Software Science and Computational Structures. Berlin, Heidelberg: Springer Berlin Heidelberg, 2009.
[2] https://uflorida-my.sharepoint.com/:p:/g/personal/monjil_m_ufl_edu/ERZ9tIFuOnZKn1rH7fZoPuQBFKUx-4Z0zgX3GG6rEDileA?e=tCLQGq
