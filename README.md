# UnBlock Me Solver
A python solver for the popular puzzle game Unblock Me on iOS
The program is an implementation of the best-first search algorithm, also known as the A* algorithm. Using two different heuristics, the program attempts
to solve a given Rush Hour puzzle. The user can specifiy which heuristic they want the program to use when solving a given Rush Hour puzzle.
## Two Heuristics
1. Blocking Heuristic:
  This heuristic works by calculating how many cars are blocking the XX car from the exit. The only cars considered are the ones directly in the third row  and in front of the XX car. The move that results in the least number of cars that block the XX car is chosen.
2. Blocking Blocking Heuristic:
  This heuristic is inspired from the blocking heuristic. It calculates how many cars are in front of the XX car, just like in the blocking heuristic, and it calculates the cars that are blocking the cars blocking the XX car.
