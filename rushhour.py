"""
Class definitions for solving Rush Hour puzzle: \n
Option 0: Best-first search with blocking heuristic: cars directly blocking XX from goal \n
Option 1: Best-first search with own heuristic: cars blocking XX plus cars blocking the cars blocking XX \n

The program will convert the list of strings into a single string for easier manipulation and faster run time. \n

Written by Taher Jamali
"""
from queue import PriorityQueue
from typing import List




def rushhour(heuristic: int, boardList: List[str]):
    """
     main function that will run the rushhour program and print out result

     @:param heuristic: the type of heuristic, blocking or custom. Only values 0 and 1 are acceptable
     @:param boardList: the board which will be a List of strings
     @:return None: The function will not return anything. Results will be printed to the console
    """
    # convert boardList into appropriate format, which is a single string
    start = ''.join(boardList)
    # get the locations of all the cars on the board
    pos = boardLoc(start)
    # run the search, result will be a tuple from search function
    howMany, path = search(start, pos, heuristic)
    # print the results
    # printResults(howMany, path, heuristic)
    return howMany, path


"""Class objects used in the program --------------------------------------------------------------------------------"""


class State:
    """
    Class State()
    This class represents the state and its g(n) and h(n) values. It also contains operator overloads for equal
    to, less than and greater than operators

    Update: I never really ended up using the operator overloads, but I decided to keep them just in case

    .board is the board at the given state and is a string
    .gn is g(n) value and is an integer
    .hn is the h(n) value and is an integer
    """

    def __init__(self, board='', gn=0, hn=0):
        self.board = board
        self.gn = gn
        self.hn = hn

    # operator overload for greater than
    def __gt__(self, other):
        return self.hn > other.hn

    # operator overload for less than
    def __lt__(self, other):
        return self.hn < other.hn

    # operator overload for equal to
    def __eq__(self, other):
        return self.hn == other.hn

    # function to print out State object. Only used for debugging purposes
    def __str__(self):
        return 'Board: % s, g(n): % s, h(n): % s' % (self.board, self.gn, self.hn)





class Car:
    """
    Class Car()
    This class represents a vehicle on the board.

    .name is the letter that represents the car
    .orient is the orientation of the car, either H for horizontal or V for vertical
    .size is how many pieces on the board the car takes up. The length
    """
    def __init__(self, name='', orient='', size=0):
        self.name = name
        self.orient = orient
        self.size = size

    # function to print the car to the console. Just used for debugging purposes
    def __str__(self):
        return 'Name: % s, Orientation: % s, Size: % s' % (self.name, self.orient, self.size)


"""End of Class objects used in the program -------------------------------------------------------------------------"""




def search(start: str, carInfo: dict, heuristic: int) -> (int, List[str]):
    """
    Search function that does the main stuff. Using a priority queue, it implements the A* algorithm and returns the
    number of explored states and the path the function took to get from the start state to the goal state

    @:param start: the start state of the board
    @:param carInfo: a dictionary with all the Car objects on the board
    @:param heuristic: the heuristic that has been chosen for the search algorithm. Either a 1 or a 0
    @:return: a tuple with the total number of explored states and the path the search function took to reach goal state
    """
    # initialize the variables
    path, priorityQ, explored = list(), PriorityQueue(), dict()
    howMany, startState = 0, State(board=start)
    lastState = ''  # was giving a warning if I didn't declare lastState here
    # add the start state to the dict and to the queue
    explored[startState.board] = None
    priorityQ.put((0, startState))

    # go through the queue
    while not priorityQ.empty():
        howMany += 1
        # pop from the queue. get() returns tuple so only save the State object
        topState = priorityQ.get()[1]
        if isGoal(topState.board):
            lastState = topState.board
            break
        else:
            newStates = makeNewStates(topState.board, carInfo)
            # print(f'{howMany=} and {len(newStates)=}')
            for state in newStates:
                # get the heuristic value based on the chosen heuristic, blocking or own heuristic
                hVal = blockingH(state) if heuristic == 0 else ownH(state)
                if checkCycles(state, topState.board, explored):
                    # place the new states in the queue
                    temp = State(board=state, gn=topState.gn + 1, hn=hVal)
                    fn = temp.gn + temp.hn
                    priorityQ.put((fn, temp))
    # back track to get the whole path
    path.append(lastState)
    lastState = explored.get(lastState)  # for dict, if key does not exist, get will return None
    # print(f'{lastState=} {len(explored.keys())=}')
    while lastState is not None:
        path.append(lastState)
        lastState = explored.get(lastState)
    # reverse path to get from start to goal
    path.reverse()
    return howMany, path


"""Heuristics are declared here -------------------------------------------------------------------------------------"""




def blockingH(curr: str) -> int:
    """
    Blocking heuristic
    Function returns the number of cars blocking xx from the exit
    All cars in 3rd row of board are totalled and the value is returned
    Curr is a single string so the 3rd row is from index 12 to 17

    @:param curr: the current board
    @:return howMany: the amount of cars blocking xx from exit
    """
    # if the current state is the goal state, return 0
    if isGoal(curr):
        return 0
    else:
        # need to keep track where on the third row the xx car is. A car can be behind xx but that is not blocking xx
        # from exit, so those cars are ignored.
        found = False
        howMany = 1
        for i in range(12, 18):
            if not found and curr[i] == 'X':
                found = True
            elif found and curr[i] != '-' and curr[i] != 'X':
                howMany += 1
        return howMany





def ownH(curr: str) -> int:
    """
    Own heuristic
    I built my heuristic off of the blocking heuristic. It calculates the total cars blocking xx from exit plus the cars
    that are blocking the cars that are blocking xx

    @:param curr: the current board
    @:return howMany: the amount of cars blocking xx from exit plus how many cars that are blocking those cars
    """
    # if curr is the goal state, return 0
    if isGoal(curr):
        return 0
    else:
        found = False  # to keep track of where the XX car is on the board
        blockedSeen = dict()
        howMany = 1
        for i in range(12, 18):
            if not found and curr[i] == 'X':
                found = True
                blockedSeen['X'] = True
            elif found and curr[i] != '-' and curr[i] not in blockedSeen:
                blockedSeen[curr[i]] = True
                howMany += 1
                # if there are cars above or below the blocking car, add 2
                if curr[i + 6] not in blockedSeen:
                    blockedSeen[curr[i + 6]] = True
                    howMany += 2
                elif curr[i - 6] not in blockedSeen:
                    blockedSeen[curr[i - 6]] = True
                    howMany += 2

            elif found and curr[i] != '-' and curr[i] in blockedSeen:
                # if there are cars above or below the blocking car, add 2
                if curr[i + 6] not in blockedSeen:
                    blockedSeen[curr[i + 6]] = True
                    howMany += 2
                elif curr[i - 6] not in blockedSeen:
                    blockedSeen[curr[i - 6]] = True
                    howMany += 2
        return howMany


"""End of heuristic functions ---------------------------------------------------------------------------------------"""




def makeNewStates(curr: str, carInfo: dict) -> List[str]:
    """
    Function that creates a list of new states to explore. New states are potential moves that can be made on the current
    board. The order of the potential moves is left, right, up, down. This makes the program find the goal state quicker.

    @:param curr: the board
    @:param carInfo: dictionary of the Car objects on the board
    @:return new: a list of the new potential moves that can be made
    """
    new, visited = list(), dict()
    for i, let in enumerate(curr):
        if let not in visited and let != '-':
            visited[let] = True
            car = carInfo[let]
            # car is horizontal so generate right and left moves
            if car.orient == 'H':
                # generate left move
                # shift to the left by moving let by one and changing the last edge of car to '-'
                # visually: '--cc--' -> '-cc---'
                if i % 6 > 0 and curr[i - 1] == '-':
                    # convert curr into a list
                    newBoard = list(curr)
                    newBoard[i - 1] = let
                    newBoard[i + car.size - 1] = '-'
                    new.append(''.join(newBoard))
                # generate right move
                # shift to the right by moving let by one and changing the last edge of car to '-'
                # visually: '--cc--' -> '---cc-'
                if i % 6 < (6 - car.size) and curr[i + car.size] == '-':
                    newBoard = list(curr)
                    newBoard[i + car.size] = let
                    newBoard[i] = '-'
                    new.append(''.join(newBoard))
            else:  # the car is vertical so generate up and down moves
                # generate up move
                if i > 5 and curr[i - 6] == '-':
                    newBoard = list(curr)
                    newBoard[i - 6] = let
                    newBoard[i + (car.size - 1) * 6] = '-'
                    new.append(''.join(newBoard))
                # generate down move
                if i < (36 - car.size * 6) and curr[i + car.size * 6] == '-':
                    newBoard = list(curr)
                    newBoard[i + car.size * 6] = let
                    newBoard[i] = '-'
                    new.append(''.join(newBoard))

    return new





def checkCycles(child: str, parent: str, explored: dict) -> bool:
    """
    Function that checks if a state has been visited and returns a boolean value. If a state has not been visited,
    the function adds the curr state to the explored dictionary and returns True. If a state is already in the
    dictionary, it'll return false.

    @:param child: the current state that will be checked for cycles
    @:param parent: the parent state of the current state
    @:param explored: the dictionary that keeps track of the explored states
    @:return bool: if cycle -> False else True
    """
    if child in explored:
        return False
    else:
        explored[child] = parent
        return True




def boardLoc(currState) -> dict:
    """
    Function that returns the positions of all the cars on the board

    @:param currState: the board which contains all the cars
    @:return carInfo: a dict of all the cars' positions
    """

    carInfo = dict()
    # go through the string
    for idx, let in enumerate(currState):
        # first check if the current letter is in the dictionary and if it is an actual letter from alphabet
        if let not in carInfo and let.isalpha():
            # create a Car object to insert into carInfo dictionary
            temp = Car(name=let, size=1)
            # now to follow the piece across the board to get the size and orientation
            # first checking horizontal (right of the board)
            if idx % 6 < 5:  # the edge of the board
                jdx = idx + 1
                if let == currState[jdx]:
                    # the orientation is horizontal
                    temp.orient = 'H'
                    while jdx % 6 > 0:  # keep going right until we hit the edge of the board
                        if let == currState[jdx]:
                            temp.size += 1
                            jdx += 1
                        else:  # no longer same car so no need to continue, just break
                            break
            if idx < 30:  # checking the vertical axis
                jdx = idx + 6  # add 6 bc single string format means the next row is in +6 intervals
                if currState[jdx] == let:
                    temp.orient = 'V'
                    while jdx < 36:  # continue going downwards and follow the car
                        if currState[jdx] == let:
                            temp.size += 1
                            jdx += 6
                        else:
                            break
            # add temp to the dictionary
            carInfo[let] = temp
    # return the position dictionary
    return carInfo





def printResults(explored: int, path: List[str], heuristic: int) -> None:
    """
    Function that will print out the results from the search function

    @:param explored: the total number of states that were explored
    @:param path: the path that the program took from start state to goal state
    @:param heuristic: the heuristic type chosen for the search
    """
    # print which heuristic was used
    if heuristic == 1:
        print(f'Custom heuristic was used to solve this puzzle :)')
    else:
        print(f'Blocking heuristic was used to solve this puzzle')
    # print the path
    for state in path:
        for j in range(len(state)):
            print(state[j], end='')
            if j % 6 == 5:
                print()  # newline
        print()  # newline
    # print the length of the path and how many states were explored
    print(f'Total moves was {len(path) - 1} \nAnd the total states explored were {explored}')





def isGoal(currState: str) -> bool:
    """
    Simple function to just check if the current state is the goal state. It's easier to just have a function rather than
    recheck every time.
    The current state is a single string that represents the board and if the positions 16 and 17 are X, then current
    state is the goal state and function will return true. Otherwise, it will return false

    @:param currState: a single string that represents the current board
    @:return: Boolean value that represents if the current state is the goal state or not
    """
    return True if currState[16] == 'X' and currState[17] == 'X' else False
