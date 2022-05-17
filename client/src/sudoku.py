from math import sqrt
from subprocess import Popen, PIPE
import sys

# Constants for game
ROWS = 9
COLUMNS = 9
NUMBERS = 9
SQUARE_SIDE = int(sqrt(ROWS))


def var_name(row, col, n):
    return f"{n} at row {row} and col {col}"


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


def set_constraints(variables, file_name=None):
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
    if file_name:

        f = open(file_name, 'r')
        for line in f.readlines():
            row = line[1]
            col = line[4]
            n = line[7]
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


def get_header(variables, clauses):
    return "p cnf {} {}".format(variables, clauses)


def get_clauses(cls):
    return "\n".join(map(lambda x: "%s 0" % " ".join(map(str, x)), cls))


if __name__ == '__main__':
    variables, varToVals, var_count = gen_vars()

    if len(sys.argv) > 1:
        final_clauses = set_constraints(variables, sys.argv[1])
    else:
        final_clauses = set_constraints(variables)
    
    header = get_header(var_count, len(final_clauses))
    rules = get_clauses(final_clauses)

    fl = open("tmp_prob_sudoku.cnf", "w")
    fl.write("\n".join([header, rules]))
    fl.close()

    ms_out = Popen(["z3 tmp_prob_sudoku.cnf"], stdout=PIPE, shell=True).communicate()[0]

    res = ms_out.decode('utf-8')
    # Print output
    res = res.strip().split('\n')

    # Print the variables that are necessary to satisfy the problem
    mat = []

    for row in range(ROWS):
        mat.append([0] * ROWS)

    if res[0] == "s SATISFIABLE":
        sat_vars = res[1][2:].split(' ')

        for c in sat_vars:
            c_int = int(c)

            if c_int > 0:
                element = varToVals[c_int]
                mat[element[0]][element[1]] = element[2]

    print_matrix(mat)

