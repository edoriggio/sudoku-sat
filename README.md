# Sudoku SAT Solver

The Sudoku SAT Solver project aims at developing a way of solving the popular Japanese game "Sudoku" by using the SAT solver Z3. More specifically, the game rules are implemented through a Boolean satisfiability problem, represented as a conjunction of clauses.

## How does it work
In order to solve a Sudoku game, drag a .txt file to the website and click on the **solve** button. The .txt file must contain the initial numbers that need to be added to the Sudoku grid. This file must be formatted in the following way:

```
1,2,1
3,2,2
```

The first number in the line is the $x$ position, the second number is the $y$ position, and the third number is the number that needs to be put in the cell. N.B., there must be only 1 line for a cell; there mustn't be any spaces at the end of the lines or the end of the file.

The user can also check the correctness of a solution. After a solution has been generated, click on the **check** button and watch as the solution is verified.

## How to run
In order to run the webserver, navigate to the root folder of this project and run the following command:

```bash
./manage.py runserver
```

Once te server is up and running, navigate to http://127.0.0.1:8000.
