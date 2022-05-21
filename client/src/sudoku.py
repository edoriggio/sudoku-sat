import os
import shutil
from math import sqrt
from subprocess import Popen, PIPE

# Constants for game
ROWS = 9
COLUMNS = 9
NUMBERS = 9
SQUARE_SIDE = int(sqrt(ROWS))


def var_name(row, col, n):
    return f'{n} at row {row} and col {col}'


def gen_vars():
    """
    Generate two mappings:
    var_name(i,j,n) -> n : from the readable name of a variable, to its integer representation
    n -> (i,j,n) : from the integer representation, to the tuple representing a number in a specific cell
    """
    next_var = 1
    var_map = {}

    var_to_vals = {}

    for row in range(ROWS):
        for col in range(COLUMNS):
            for n in range(1, NUMBERS+1):
                name = var_name(row, col, n)
                var_map[name] = next_var
                var_to_vals[next_var] = (row, col, n)
                next_var += 1

    return var_map, var_to_vals, next_var - 1


def set_constraints(variables, input_file=None):
    clauses = []

    # Every cell has at least one number
    for row in range(ROWS):
        for col in range(COLUMNS):
            clauses.append([variables[var_name(row, col, n)] for n in range(1, NUMBERS+1)])

    # Every	cell contains at most one number
    for row in range(ROWS):
        for col in range(COLUMNS):
            for n in range(1, NUMBERS):
                for m in range(n+1, NUMBERS+1):
                    clause = [-variables[var_name(row, col, n)], -variables[var_name(row, col, m)]]
                    clauses.append(clause)

    # Every row contains every number
    for row in range(ROWS):
        for n in range(1, NUMBERS+1):
            clauses.append([variables[var_name(row, col, n)] for col in range(COLUMNS)])

    # Every column contains every number
    for col in range(COLUMNS):
        for n in range(1, NUMBERS+1):
            clauses.append([variables[var_name(row, col, n)] for row in range(ROWS)])

    # Every nxn square contains every number
    for square_1 in range(SQUARE_SIDE):
        for square_2 in range(SQUARE_SIDE):
            for n in range(1, NUMBERS+1):
                clause = []

                for row in range(SQUARE_SIDE):
                    for col in range(SQUARE_SIDE):
                        clause.append(variables[var_name(3 * square_1 + row, 3 * square_2 + col, n)])
                clauses.append(clause)

    # Every line in the input file
    if input_file:

        file_clauses = input_file.split('\n')
        for clause in file_clauses:
            clause = clause.split(',')
            row = int(clause[0]) - 1
            col = int(clause[1]) - 1
            n = clause[2]
            clauses.append([variables[var_name(row, col, n)]])

    return clauses


def print_matrix(matrix):
    for i in range(ROWS):
        for j in range(COLUMNS):
            print(matrix[i][j], end='')
            if j != COLUMNS-1:
                if (j+1) % SQUARE_SIDE == 0:
                    print(' | ', end='')
                else:
                    print(' ', end='')
        print()

        if (i+1) % SQUARE_SIDE == 0:
            print(''.join(['-' for _ in range(21)]))


def check_solution(mat):
    checks = []
    # check rows
    for i in range(9):
        r_set = set()
        for j in range(9):
            r_set.add(mat[i][j])
            checks.append((i,j))

        for n in range(1,10):
            if n not in r_set:
                return checks, False
    
    # check columns
    for j in range(9):
        c_set = set()
        for i in range(9):
            c_set.add(mat[i][j])
            checks.append((i,j))

        for n in range(1,10):
            if n not in c_set:
                return checks, False

    #check boxes
    for b1 in range(3):
        for b2 in range(3):
            b_set = set()
            for i in range(3):
                for j in range(3):
                    b_set.add(mat[3*b1 + i][3*b2 + j])
                    checks.append((3*b1 + i, 3*b2 + j))
                    # print(3*b1 + i, 3*b2 + j)
            for n in range(1,10):
                if n not in b_set:
                    return checks, False
    
    return checks, True

            



def get_header(variables, clauses):
    return 'p cnf {} {}'.format(variables, clauses)


def get_clauses(cls):
    return '\n'.join(map(lambda x: '%s 0' % ' '.join(map(str, x)), cls))


def solve(input_file=None):
    mat = []
    variables, var_to_vals, var_count = gen_vars()

    if input_file:
        final_clauses = set_constraints(variables, input_file)
    else:
        final_clauses = set_constraints(variables)

    header = get_header(var_count, len(final_clauses))
    rules = get_clauses(final_clauses)

    os.mkdir(os.path.join(os.path.dirname(__file__), '../tmp'))
    with open(os.path.join(os.path.dirname(__file__), '../tmp/tmp_prob_sudoku.cnf'), 'x') as file:
        file.write('\n'.join([header, rules]))

    ms_out = Popen(['z3 ./client/tmp/tmp_prob_sudoku.cnf'], stdout=PIPE, shell=True).communicate()[0]
    shutil.rmtree(os.path.join(os.path.dirname(__file__), '../tmp'), ignore_errors=True)

    res = ms_out.decode('utf-8')
    res = res.strip().split('\n')

    for row in range(ROWS):
        mat.append([0] * ROWS)

    if res[0][2:] == 'SATISFIABLE':
        sat_vars = res[1][2:].split(' ')

        for c in sat_vars:
            c_int = int(c)

            if c_int > 0:
                element = var_to_vals[c_int]
                mat[element[0]][element[1]] = element[2]

    return mat
