import os
import translate
from unroll_seq import *


if __name__ == '__main__':
    # TODO: Make the path reference correctly by using path functions

    # Remove these two lines for debug purpose.
    # f = open('attack_log.txt', 'w')  # FIXME: add back if you want to output to log
    # sys.stdout = f  # FIXME: add back if you want to output to log


    
    netlist = 'const_output_2bit_GLN.v'
    func_level = 10
    
    print('\n*****************************************\n')
    # Create a temporary folder to store intermmediate files
    
    current_path = os.getcwd()
 
    output_path = os.path.join(current_path,'output',netlist.replace('.v', "")) 
    
    if not os.path.exists(output_path):
    # Create the directory if it doesn't exist
        os.makedirs(output_path)
        print('Output path: %s' % output_path)
    	
    print('Original netlist: %s' % netlist)
    print('Unroll level: %d' % func_level)

    # Verilog to Bench
    translate.translate(netlist, output_path)
    print('Original netlist: Verilog to Bench finished.')

    unroll(output_path + '/' + netlist.replace('.v', "") + '.bench', output_path + '/' + netlist.replace('.v', "") + '_unrolled.bench',func_level)
    print('Unrolling finished.')
    

