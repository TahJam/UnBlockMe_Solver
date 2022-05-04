from rushhour import rushhour

if __name__ == '__main__':

    tests = [["---O--", "---O--", "XX-O--", "PQQQ--", "P-----", "P-----"],
             ["OOOP--", "--AP--", "XXAP--", "Q-----", "QGGCCD", "Q----D"],
             ["--OPPP", "--O--A", "XXO--A", "-CC--Q", "-----Q", "--RRRQ"],
             ["-ABBO-", "-ACDO-", "XXCDO-", "PJFGG-", "PJFH--", "PIIH--"],
             ['OOO--P', '-----P', '--AXXP', '--ABCC', 'D-EBFF', 'D-EQQQ']
             ]
    heuristics = ['blocking', 'custom']

    for j, heuristic in enumerate(heuristics):
        for i, test in enumerate(tests):
            print(f'Puzzle {i+1} using {heuristic} heuristic')
            howMany, path = rushhour(j, test)
            print(f'Total moves: {len(path) - 1} \nStates explored: {howMany}\n')
        print()
