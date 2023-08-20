from enum import unique
import re
import os
from itertools import combinations
import numpy as np
import string    
import random  
import copy
import pyapproxmc


# FILE_NAME = 'AND6'
# UNROLL_DEPTH = 6
# OUTPUT_LENGTH = 3

FILE_NAME = "const_output_2bit_GLN"
DIRECTORY = FILE_NAME
UNROLL_DEPTH = 10
OUTPUT_LENGTH = 2

DIRECTORY = FILE_NAME

def generate_cnf(bench):
    net_map = {}
    clauses = []

    #Parse Output Nodes
    regex = r'OUTPUT\(([^()]+)\)'

    for out_node in re.findall(regex,bench):
        out_node = out_node.replace(" ","").replace("\n","").replace("\t","")
        net_map[out_node] = len(net_map)+1
        
    #Parse Input Nodes
    regex = r'INPUT\(([^()]+)\)'

    for in_node in re.findall(regex,bench):
        in_node = in_node.replace(" ","").replace("\n","").replace("\t","")
        net_map[in_node] = len(net_map)+1
        # if in_node == 'reset':
        #     reset_node = net_map[in_node] 
        #     clauses.append(f'{reset_node} 0')


    # Parse assignements and generate clauses
    regex = r'([\w]+)\s*=\s*([\w]+)\(([\w,\s]+)\)'

    for gate_out, gate, gate_ins in re.findall(regex,bench):
        
        out = gate_out.replace(" ","").replace("\n","").replace("\t","")
        
        inps = gate_ins.replace(" ","").replace("\n","").replace("\t","").split(",")
        
        if out not in net_map:
            net_map[out] = len(net_map)+1
        for inp in inps:
            if inp not in net_map:
                net_map[inp] = len(net_map)+1
                
        if gate == 'AND':
            exp = f'{net_map[out]}'
            
            for inp in inps:
                clauses.append(f'-{net_map[out]} {net_map[inp]} 0')
                exp += f' -{net_map[inp]}'
            exp += ' 0'
            clauses.append(exp)
            
        elif gate == 'NAND':
            exp = f'-{net_map[out]}'
            for inp in inps:
                clauses.append(f'{net_map[out]} {net_map[inp]} 0')
                exp += f' -{net_map[inp]}'
            exp += ' 0'
            clauses.append(exp)
            
        elif gate == 'OR':
            exp = f'-{net_map[out]}'
            for inp in inps:
                clauses.append(f'{net_map[out]} -{net_map[inp]} 0')
                exp += f' {net_map[inp]}'
            exp += ' 0'
            clauses.append(exp)

        elif gate == 'NOR':
            exp = f'{net_map[out]}'
            for inp in inps:
                clauses.append(f'-{net_map[out]} -{net_map[inp]} 0')
                exp += f' {net_map[inp]}'
            exp += ' 0'
            clauses.append(exp)

        elif gate == 'NOT':
            clauses.append(f'{net_map[out]} {net_map[inps[0]]} 0')
            clauses.append(f'-{net_map[out]} -{net_map[inps[0]]} 0')
        
        elif gate == 'BUFF':
            # print(inps[0])
            clauses.append(f'{net_map[out]} -{net_map[inps[0]]} 0')
            clauses.append(f'-{net_map[out]} {net_map[inps[0]]} 0')

        elif gate == 'XOR':
            while len(inps)>2:
                #create new net
                new_net = inps[-2]+inps[-1]
                net_map[new_net] = len(net_map)+1

                # add constraints
                clauses.append(f'-{net_map[new_net]} -{net_map[inps[-1]]} -{net_map[inps[-2]]} 0')
                clauses.append(f'-{net_map[new_net]} {net_map[inps[-1]]} {net_map[inps[-2]]} 0')
                clauses.append(f'{net_map[new_net]} -{net_map[inps[-1]]} {net_map[inps[-2]]} 0')
                clauses.append(f'{net_map[new_net]} {net_map[inps[-1]]} -{net_map[inps[-2]]} 0')

                # remove last 2 nets
                inps = inps[:-2]

                # insert before out
                inps.insert(1,new_net)

            # add constraints
            clauses.append(f'-{net_map[out]} -{net_map[inps[-1]]} -{net_map[inps[-2]]} 0')
            clauses.append(f'-{net_map[out]} {net_map[inps[-1]]} {net_map[inps[-2]]} 0')
            clauses.append(f'{net_map[out]} -{net_map[inps[-1]]} {net_map[inps[-2]]} 0')
            clauses.append(f'{net_map[out]} {net_map[inps[-1]]} -{net_map[inps[-2]]} 0')
            
            
        elif gate == 'XNOR':
            while len(inps)>2:
                #create new net
                new_net = inps[-2]+inps[-1]
                net_map[new_net] = len(net_map)+1

                # add constraints
                clauses.append(f'-{net_map[new_net]} -{net_map[inps[-1]]} -{net_map[inps[-2]]} 0')
                clauses.append(f'-{net_map[new_net]} {net_map[inps[-1]]} {net_map[inps[-2]]} 0')
                clauses.append(f'{net_map[new_net]} -{net_map[inps[-1]]} {net_map[inps[-2]]} 0')
                clauses.append(f'{net_map[new_net]} {net_map[inps[-1]]} -{net_map[inps[-2]]} 0')

                # remove last 2 nets
                inps = inps[:-2]

                # insert before out
                inps.insert(1,new_net)

            #create new net
            new_net = out+'_xnor'
            net_map[new_net] = len(net_map)+1

            # add constraints
            clauses.append(f'-{net_map[new_net]} -{net_map[inps[-1]]} -{net_map[inps[-2]]} 0')
            clauses.append(f'-{net_map[new_net]} {net_map[inps[-1]]} {net_map[inps[-2]]} 0')
            clauses.append(f'{net_map[new_net]} -{net_map[inps[-1]]} {net_map[inps[-2]]} 0')
            clauses.append(f'{net_map[new_net]} {net_map[inps[-1]]} -{net_map[inps[-2]]} 0')
            clauses.append(f'{net_map[out]} {net_map[new_net]} 0')
            clauses.append(f'-{net_map[out]} -{net_map[new_net]} 0')

    return clauses, net_map

def generate_constraint_single(clauses,var_numbers,output_length, unroll_depth):
    
    
    subfolder_path = os.path.join(DIRECTORY, "CNFs")
    if not os.path.isdir(subfolder_path):
        os.mkdir(subfolder_path)

    for i in range(1,unroll_depth+1):
        file_path = os.path.join(subfolder_path, "unroll_"+str(i)+".cnf")


        projection_scope = "c ind "


        for j in range(1+(i-1)*output_length, i*output_length+1):
            projection_scope = projection_scope+str(j)+" "

        projection_scope = projection_scope+"0"+"\n"

        with open(file_path, "w") as f:
        
            f.write(projection_scope+'p cnf '+str(var_numbers)+' '+str(len(clauses))+' 0'+'\n')
            for clause in clauses:
                f.write(clause + '\n')

def generate_constraint_plural(clauses,net_map,output_length, unroll_depth):  

    subfolder_path = os.path.join(DIRECTORY, "CNFs")
    if not os.path.isdir(subfolder_path):
        os.mkdir(subfolder_path)

    output_indices = np.arange(1,unroll_depth+1)

    for i in range(2,unroll_depth+1):
        coupling_indices = combinations(output_indices, i)
        
        for couple in coupling_indices:
            # print(couple)
            #couple_length = len(list(couples))

            projection_scope = "c ind "
            couple = list(couple)
        
            print("---------")
            for output_id in couple:
                
                for var_ids in range(1+(output_id-1)*output_length, output_id*output_length+1):
                    projection_scope = projection_scope+str(var_ids)+" "
                    
            # projection scope for the plural terms    
            projection_scope = projection_scope+"0"+"\n"
            # print(projection_scope)

            print('couple = ',couple)

            # Need to have separate CNFs for each term
            # print(clauses)
            # print(len(clauses))
            clause_w_constraint = copy.copy(clauses)
            net_map_w_constraint = copy.copy(net_map)
            

            for i in range(0,len(couple)-1):               # take every two output ids
                # generate variable ids for perform equality constraint 
                var_1_list = np.ones(output_length)*(couple[i]-1)*output_length + np.arange(1,output_length+1)
                var_2_list = np.ones(output_length)*(couple[i+1]-1)*output_length + np.arange(1,output_length+1)
                # print(var_1_list)
                # print(var_2_list)
                # print("Time to create clause")

                for var_1, var_2 in zip(var_1_list,var_2_list):

                    var_1 = int(var_1)
                    var_2 = int(var_2)
                    # print(var_1)
                    # print(var_2)
                    
                    # generate random string to name the new net for the equality/xnor constraint 
                    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k = 3))    
                    new_net = str(var_1)+'_'+str(var_2)+'_'+random_string+'_xnor_constraint'
                    net_map_w_constraint[new_net] = len(net_map_w_constraint)+1
                    
                    
                    
                    clause_w_constraint.append(f' {net_map_w_constraint[new_net]} -{var_1} -{var_2} 0')
                    clause_w_constraint.append(f' {net_map_w_constraint[new_net]} {var_1} {var_2} 0')
                    clause_w_constraint.append(f' -{net_map_w_constraint[new_net]} {var_1} -{var_2} 0')
                    clause_w_constraint.append(f' -{net_map_w_constraint[new_net]} -{var_1} {var_2} 0')

                    
                    # print(new_net)
                    # print(f' {net_map[new_net]} -{var_1} -{var_2} 0')
                    # print(f' {net_map[new_net]} {var_1} {var_2} 0')
                    # print(f' -{net_map[new_net]} {var_1} -{var_2} 0')
                    # print(f' -{net_map[new_net]} -{var_1} {var_2} 0')
            
            #generating name for cnfs
            file_name = '_'.join(map(str, couple))
            file_path = os.path.join(subfolder_path, file_name+".cnf")

            with open(file_path, "w") as f:
                f.write(projection_scope+'p cnf '+str(len(net_map_w_constraint))+' '+str(len(clause_w_constraint))+' 0'+'\n')
                for clause in clause_w_constraint:
                    f.write(clause + '\n')
    
def approx_solution_count(clauses,net_map,output_length, unroll_depth):
   
    solution_count = 0

    #solution count for single terms
    for i in range(1,unroll_depth+1):
        print("i =",i)
        projection_scope = []

        for j in range(1+(i-1)*output_length, i*output_length+1):
            projection_scope.append(j)

        c = pyapproxmc.Counter()

        for clause in clauses:
            c.add_clause(list(map(int, clause.strip().split()[:-1])))
        print("projection scope variables= ",projection_scope)
        count = c.count(projection_scope)
        solution_count = solution_count + count[0]*2**count[1]
        print("solution count = ",count[0]*2**count[1])
        

    # solution count for multiple terms

    output_indices = np.arange(1,unroll_depth+1)

    for i in range(2,unroll_depth+1):
        coupling_indices = combinations(output_indices, i)
        
        for couple in coupling_indices:
            
            couple = list(couple)
        
            print("---------")

            print('couple = ',couple)

            # Need to have separate CNFs for each term
            # print(clauses)
            # print(len(clauses))
            clause_w_constraint = copy.copy(clauses)
            net_map_w_constraint = copy.copy(net_map)
            

            for i in range(0,len(couple)-1):               # take every two output ids
                # generate variable ids for perform equality constraint 
                var_1_list = np.ones(output_length)*(couple[i]-1)*output_length + np.arange(1,output_length+1)
                var_2_list = np.ones(output_length)*(couple[i+1]-1)*output_length + np.arange(1,output_length+1)
                # print(var_1_list)
                # print(var_2_list)
                # print("Time to create clause")

                for var_1, var_2 in zip(var_1_list,var_2_list):

                    var_1 = int(var_1)
                    var_2 = int(var_2)
                    # print(var_1)
                    # print(var_2)
                    
                    # generate random string to name the new net for the equality/xnor constraint 
                    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k = 3))    
                    new_net = str(var_1)+'_'+str(var_2)+'_'+random_string+'_xnor_constraint'
                    net_map_w_constraint[new_net] = len(net_map_w_constraint)+1
                    
                    
                    
                    clause_w_constraint.append(f' {net_map_w_constraint[new_net]} -{var_1} -{var_2} 0')
                    clause_w_constraint.append(f' {net_map_w_constraint[new_net]} {var_1} {var_2} 0')
                    clause_w_constraint.append(f' -{net_map_w_constraint[new_net]} {var_1} -{var_2} 0')
                    clause_w_constraint.append(f' -{net_map_w_constraint[new_net]} -{var_1} {var_2} 0')


                    clause_w_constraint.append(f' {net_map_w_constraint[new_net]} 0')
            
            

            c = pyapproxmc.Counter()
            for clause in clause_w_constraint:
                c.add_clause(list(map(int, clause.strip().split()[:-1])))

            projection_scope = []
            for output_id in couple:
                for var_ids in range(1+(output_id-1)*output_length, output_id*output_length+1):
                    projection_scope.append(var_ids) 

            # print(projection_scope)
            count = c.count(projection_scope)
            plus_minus = (-1)**(len(couple)+1)
            print(plus_minus*count[0]*2**count[1])
            
            solution_count = solution_count + plus_minus*count[0]*2**count[1]


    return solution_count

def write_cnf(clauses, net_map, working_path):

    # if not os.path.isdir(DIRECTORY):
    #     os.mkdir(DIRECTORY)

    file_path = os.path.join(working_path, FILE_NAME+".cnf")

    with open(file_path, "w") as f:
        # Write each string in the list to the file, one per line
        f.write('p cnf '+str(len(net_map))+' '+str(len(clauses))+' 0'+'\n')
        for clause in clauses:
            f.write(clause + '\n')

def main():
    current_path = os.getcwd()
    working_path = os.path.join(current_path,'output', DIRECTORY) 

    with open(os.path.join(working_path, FILE_NAME+'_unrolled.bench'), 'r') as f:
        bench = f.read()

    clauses, net_map = generate_cnf(bench)
    print(net_map)
    clauses_ori = copy.copy(clauses)
    net_map_ori = copy.copy(net_map)

    write_cnf(clauses, net_map, working_path)
    


    output_length = OUTPUT_LENGTH
    unroll_depth = UNROLL_DEPTH

    # generate_constraint_single(clauses,var_number,output_length, unroll_depth)
    # generate_constraint_plural(clauses,net_map,output_length, unroll_depth)

    unique_solution_count =  approx_solution_count(clauses,net_map,output_length, unroll_depth)

 
    print("Approximate count is: ",unique_solution_count)


if __name__ == "__main__":
    main()
