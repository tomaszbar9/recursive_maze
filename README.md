# Recursive Maze Generator

Python program generating a maze recursively.

A maze is displayed using turtle module.

Due to the limit of recursion, by default set to 1000 in Python, a possible size of a maze is restricted.

The generator will surely create a maze when the product of width and height does not exceed 1000, but in fact larger sizes are also possible.

For example, in 10 000 attempts the program generated a maze of size 40 x 40 in 99.8% of tries. The probability for 50 x 50 maze is almost 18%, but when the size is 57 x 57 the chance is less than 1%.

The program itself makes by default up to 10 attempts before it gives up.

The default size of a maze is 40 x 20 and the side of each cell is 15px.

All parameters may be changed by passing additional command-line arguments:

--attempts `int`

-s, --size `int` `int`

-c, --cell `int`

--close (closes the turtle window when the maze is finished).
