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

## Create the environment
We used a custom Conda environment in order to run the webserver. This environment can be recreated by using the following commands:

```bash
conda env create -f ./environment.yml
conda activate sudoku
```

In order to remove the virtual environment, use the following commands:

```bash
conda deactivate
conda remove --name sudoku --all
```

## Requirements
The project uses the following additional packages:
- Django (version 3.2.5)
- Z3 (version 4.8.16)

## How to run
In order to run the webserver, navigate to the root folder of this project and run the following command:

```bash
./manage.py runserver
```

Once te server is up and running, navigate to http://127.0.0.1:8000.
