# Executed in Python 3.6
import re
import copy
from Ntk_Parser import *




###########################################################################
# Function name: seq_to_comb
# Note: Remove the DFFs in the netlist and output as a new file.
###########################################################################
def unroll(input_path, output_path,unroll_level):
    circuit_graph = ntk_parser(input_path)
    opt_file = open(output_path, "w")
    reset_initilization = True
    constant_0 = 'constant_0_0'
    constant_1 = 'constant_0_1'

    zipped = zip([node.name for node in circuit_graph.PI], circuit_graph.PI)
    zipped = sorted(zipped)
    sorted_PI = list(zip(*zipped))[1]

    #write input ports
    for cycle in range(1,unroll_level+1):
        for node in sorted_PI:
            # We omit the reset input and later replace all the gate connections with reset nodes with a constant 0
            if node.name!='reset':
                node_name_temp = node.name+'_'+str(cycle)
                opt_file.write("INPUT(%s)\n" % node_name_temp)
            
    
    # Create contatnt gate 1 and constant gate 0
    # create two constant gates, that will be used to load the initial states
    for node in sorted_PI:
        opt_file.write(node_name_temp + "_bar = NOT(" + node_name_temp + ")\n")
        opt_file.write("constant_1_0 = XOR(" + node_name_temp + ", " + node_name_temp + "_bar)\n")
        opt_file.write("constant_0_0 = NOT(constant_1_0)\n")
        const_gate_formed = True
        break




    zipped = zip([node.name for node in circuit_graph.PO], circuit_graph.PO)
    zipped = sorted(zipped)
    sorted_PO = list(zip(*zipped))[1]
    
    #write output ports
    for cycle in range(1,unroll_level+1):
        for node in sorted_PO:
            node_name_temp = node.name+'_'+str(cycle)
            opt_file.write("OUTPUT(%s)\n" % node_name_temp)
    # opt_file.write("breakpoint 1\n"
    

    
    for cycle in range(0,unroll_level+1):
        
        if cycle == 0:
            print("Load Initial State Values")
            # if reset_initilization:
            #     constant_gate = constant_0      # If the inital state is the reset state then the name of the constant gate is constant_0_0
        if cycle:
            for node in circuit_graph.object_list:

                # if node.power_node == 1 or node.power_node == 2:
                #     continue

                # if node.name == 'reset' and cycle > 1:
                #     opt_file.write("%s = BUFF( %s " % ('reset'+'_'+str(cycle), constant_gate))
                #     opt_file.write(") \n")

                
                if node.gate_type != circuit_graph.gateType['IPT']:
                    #create a new name of the node for comb. snaoshot of that cycle
                    if node.gate_type == circuit_graph.gateType['DFF']:
                       
                        if cycle == 1 and reset_initilization and const_gate_formed:
                            DFF_D_name = constant_0                  # D pin of flipflop connected to logic 0 which is the initial condition for reset
                        else:
                            DFF_D_name = node.fan_in_node[0].name+'_'+str(cycle-1)     #D pin of previous cycle, as it is DFF node, it has only one fan-in node

                        DFF_Q_name = node.name+'_'+str(cycle)   # Q pin of current cycle
                        opt_file.write("%s = BUFF( %s " % (DFF_Q_name, DFF_D_name)) # We establish a buffer gate between the Q of current cycle and D of previous cycle
                        opt_file.write(") \n")


                    elif node.gate_type != circuit_graph.gateType['DFF']:


                        node_name_temp = node.name+'_'+str(cycle)
                        opt_file.write("%s = %s(" % (node_name_temp, circuit_graph.gateType_reverse[node.gate_type])),
                        ipt_num = len(node.fan_in_node)
                    
                        for ipt_node in node.fan_in_node:
                            ipt_num -= 1

                            #Experimental.  We omitted the reset input and replace all the gate connections with reset nodes with a constant 0
                            if ipt_node.name == 'reset':
                                ipt_name_temp = constant_0
                            else:
                                ipt_name_temp = ipt_node.name +'_'+str(cycle)
                            # Experimental

                            #Original
                            # ipt_name_temp = ipt_node.name +'_'+str(cycle)
                            if ipt_num == 0:
                                opt_file.write("%s" % ipt_name_temp),
                            else:
                                opt_file.write("%s, " % ipt_name_temp),
                        

                        opt_file.write(") \n")
        
    opt_file.close()


