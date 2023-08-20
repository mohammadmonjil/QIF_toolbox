This tool box computes QIF(Quantitative Information Flow)* of a sequential hardware module. The QIF is computed as the logarithm of number of unique outputs of a primary output which quantifies the amount of information flowing (Entropy) from secret to the observable output. 

Dependencies: 
1. approxmc model counter tool for counting the number of solutions. Can be installed using: "pip install pyapproxmc". For more details: https://github.com/meelgroup/approxmc

Usage:
1. Define a RTL module with secret inputs and observable output(s).
2. Synthesize the RTL module into Gate-level netlist using 15nm open cell NAND library.
3. Run unroll_seq_test.py to unroll the netlist to desired sequential depth and convert into bench format.
4. Run bench2cnf_approxmc.py with the unrolled bench file to get the number of unique solutions
	a. define unroll depth
	b. define length of output in bits.
5. You can also set/reset control bits of the module to run the FSM in desired mode.

*Smith, Geoffrey. "On the foundations of quantitative information flow." International Conference on Foundations of Software Science and Computational Structures. Berlin, Heidelberg: Springer Berlin Heidelberg, 2009.
