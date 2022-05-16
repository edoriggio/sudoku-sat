from operator import ne
import sys
from subprocess import Popen
from subprocess import PIPE
import re
import random
import os

def var_name(r,c,n):
    return f"{n} at row {r} and col {c}"

def gen_vars():
    '''
    Generate two mappings:
    var_name(i,j,n) -> n : from the readable name of a variable, to its integer representation
    n -> (i,j,n) : from the integer representation, to the tuple representing a number in a specific cell
    '''
    nextVar = 1
    varMap = {}

    varToVals = {}

    for r in range(9):
        for c in range(9):
            for n in range(1,10):
                name = var_name(r,c,n)
                varMap[name] = nextVar
                varToVals[nextVar] = (r,c,n)
                nextVar += 1

    return varMap, varToVals, nextVar-1

def set_constraints(variables):

    clauses = []

    # Every cell has at least one number
    # [[1 OR 2] AND [5 OR 3] AND [7 OR 9]]
    for r in range(9):
        for c in range(9):
            clauses.append([variables[var_name(r,c,n)] for n in range(1,10)])

    # Every	cell contains at most one number:
    for r in range(9):
        for c in range(9):
            for x in range(1,9):
                for y in range(x+1, 10):
                    clause = [-variables[var_name(r,c,x)], -variables[var_name(r,c,y)]]
                    clauses.append(clause)

    # Every row contains every number:	
    for r in range(9):
        for n in range(1,10):
            clauses.append([variables[var_name(r,c,n)] for c in range(9)])

    for c in range(9):
        for n in range(1,10):
            clauses.append([variables[var_name(r,c,n)] for r in range(9)])

    for square_1 in range(3):
        for square_2 in range(3):
            for n in range(1,10):
                clause = []
                for r in range(3):
                    for c in range(3):
                        # p(3r + i, 3s + j, n)
                        clause.append(variables[var_name(3*square_1+r, 3*square_2+c, n)])
                clauses.append(clause)



    return clauses


def print_matrix(mat):
    for i in range(9):
        for j in range(9):
            print(mat[i][j], end='')
            if j != 8:
                if (j+1) % 3 == 0:
                    print(' | ', end='')
                else:
                    print(' ', end='')
        print('')
        if (i+1)%3 == 0:
            print(''.join(['-'  for x in range(21)]))
        
def get_header(vars, clauses):
    return "p cnf {} {}".format(vars, clauses)

def get_clauses(cls):
        return "\n".join(map(lambda x: "%s 0" % " ".join(map(str, x)), cls))

if __name__ == '__main__':
    variables, varToVals, var_count = gen_vars()
    clauses = set_constraints(variables)
    
    header = get_header(var_count, len(clauses))
    rules = get_clauses(clauses)

    fl = open("tmp_prob_sudoku.cnf", "w")
    fl.write("\n".join([header, rules]))
    fl.close()

    # print_matrix()
    ms_out = Popen(["z3 tmp_prob_sudoku.cnf"], stdout=PIPE, shell=True).communicate()[0]


    res = ms_out.decode('utf-8')
    # Print output
    # print(res)
    res = res.strip().split('\n')

    # Print the variables that are necessary to satify the problem
    mat = []
    for row in range(9):
        mat.append([0] * 9)
    
    if res[0] == "sat":   
        sat_vars = res[1].split(' ')
        for c in sat_vars:
            c_int = int(c)
            if c_int > 0:
                # print(varToVals[c_int])
                tupla = varToVals[c_int]
                mat[tupla[0]][tupla[1]] = tupla[2]
    # print(mat)
    print_matrix(mat)

