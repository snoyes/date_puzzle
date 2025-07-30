import multiprocessing
from blocks import BLOCKS
from pprint import pprint
from copy import copy, deepcopy
import time
from datetime import date, timedelta
from date_frames import get_date_holes

def print_puzzle(rotations, bases, current_date):
    dateHoles = get_date_holes(current_date)
    trim = {6, 6+1j, 0+7j, 1+7j, 2+7j, 3+7j}
    #print(rotations)
    #print(bases)
    result = ''
    output = {x: set() for x in range(10)}
    for i in range(len(rotations)):
        block = BLOCKS[i][rotations[i]]
        base = bases[i]
        output[i] |= {base + vector for vector in block}
    for row in range(8):
        for col in range(7):
            char = '.' if complex(col, row) in dateHoles else '#' if complex(col, row) in trim else '?'
            for i in output:
                if complex(col, row) in output[i]:
                    char = str(i)
            result += char
    with open('results/' + str(current_date) + '.txt', 'a') as f:
        f.write(result + '\n')

def find_disconnected_regions(puzzleSpace):
#    regions = []
#    for space in puzzleSpace:
#        if not any(space in region for region in regions):
#            regions.append(set())
#            frontier = {space,}
#            while frontier:
#                space = frontier.pop()
#                regions[-1].add(space)
#                for d in (1, -1, 1j, -1j):
#                    if space + d in puzzleSpace and not any(space + d in region for region in regions):
#                        frontier.add(space + d)
#    return regions

    regions = []
    #copy_puzzleSpace = copy(puzzleSpace)
    copy_puzzleSpace = set().union(puzzleSpace)

    while copy_puzzleSpace:
        regions.append(set())
        space = copy_puzzleSpace.pop()
        frontier = {space,}
        while frontier:
            space = frontier.pop()
            regions[-1].add(space)
            for d in (1, -1, 1j, -1j):
                if space + d in copy_puzzleSpace:
                    frontier.add(space + d)
            copy_puzzleSpace -= frontier
    return regions

def adjust_regions(regions, attempt):
    regions = deepcopy(regions)
    #pprint(f'{regions=}')
    #pprint(f'{attempt=}')
    i = next(i for i in range(len(regions)) if regions[i] & attempt)
    region = regions[i]
    region -= attempt
    regions[i:i+1] = find_disconnected_regions(region)
    #print(f'{regions=}')
    #print()
    #return regions

def solve(puzzleSpace, rotation=None, BLOCKS=None, BLOCK_PLACES=None, ATTEMPTS=None, currentDate=None, blockNum=0, rotations=None, bases=None, regions=None):
    if rotations is None:
        rotations = []
    if bases is None:
        bases = []
    if regions is None:
        regions = [copy(puzzleSpace),]
    if blockNum >= len(BLOCKS):
        # found a solution
        print_puzzle(rotations, bases, currentDate)
        return 1

    assert set().union(*regions) == puzzleSpace

    #print_puzzle(rotations, bases)

    if MIN_BLOCK_SIZE > min(len(region) for region in regions):
        #print('too small', blockNum)
        return 0

    #return sum(
        #solve(puzzleSpace - attempt, blockNum+1)
        #for block in BLOCKS[blockNum]
        #for base in puzzleSpace
        #if (attempt := {base + vector for vector in block})
        #and attempt & puzzleSpace == attempt
    #)
    t = 0
    if rotation is None:
        source = enumerate(BLOCKS[blockNum])
    else:
        source = ([rotation, BLOCKS[blockNum][rotation]],)
    for b, block in source:
        #for base in sorted(puzzleSpace, key=lambda x: (x.imag, x.real)):
        for base in BLOCK_PLACES[blockNum][b]:
            #attempt = {base + vector for vector in block}
            attempt = ATTEMPTS[blockNum, b, base]
            if attempt & puzzleSpace == attempt:
                #print_puzzle(rotations, bases)
                i = next(i for i in range(len(regions)) if regions[i] & attempt)
                region = regions[i]
                region -= attempt
                newregions = find_disconnected_regions(region)
                regions[i:i+1] = newregions
                newregions_len = len(newregions)
                t += solve(puzzleSpace=puzzleSpace-attempt, rotation=None, BLOCKS=BLOCKS, BLOCK_PLACES=BLOCK_PLACES, ATTEMPTS=ATTEMPTS, currentDate=currentDate, blockNum=blockNum + 1, rotations=rotations+[b,], bases=bases+[base,], regions=regions)
                regions[i:i+newregions_len] = [set().union(*regions[i:i+newregions_len]) | attempt]
#            if t > 20:
#                exit()
    return t

MIN_BLOCK_SIZE = min(len(BLOCKS[x][0]) for x in range(len(BLOCKS)))

def get_block_places(puzzleSpace, BLOCKS):
    blockPlaces = {x: [set() for _ in range(len(BLOCKS[x]))] for x in BLOCKS}
    for k in BLOCKS:
        for b, block in enumerate(BLOCKS[k]):
            for base in sorted(puzzleSpace, key=lambda x: (x.imag, x.real)):
                attempt = {base + vector for vector in block}
                if attempt & puzzleSpace == attempt:
                    blockPlaces[k][b].add(base)
    return blockPlaces


if __name__ == '__main__':
    trim = {6, 6+1j, 0+7j, 1+7j, 2+7j, 3+7j}

    current_date = date(2025, 7, 25)
    end_date = date(2025, 12, 25)
    total_results = 0

    while current_date <= end_date:
        start = time.time()

        dateHoles = get_date_holes(current_date)
        puzzleSpace = {complex(col, row) for col in range(7) for row in range(8)} - trim - dateHoles
        BLOCK_PLACES = get_block_places(puzzleSpace, BLOCKS)

        ATTEMPTS = dict()
        for blockNum in range(10):
            for b, block in enumerate(BLOCKS[blockNum]):
                for base in BLOCK_PLACES[blockNum][b]:
                    ATTEMPTS[(blockNum, b, base)] = {base + vector for vector in block}


        numTrials = len(puzzleSpace) * 8

        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.starmap(solve, [(puzzleSpace, rotation, BLOCKS, BLOCK_PLACES, ATTEMPTS, current_date) for rotation in range(8)])

        end = time.time()
        total_results += sum(results)
        print(current_date)
        print(results)
        print(sum(results))
        print("elapsed:", end - start)
        print(flush=True)
        current_date += timedelta(days=1)
    print(f'{total_results=}')
