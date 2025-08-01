from collections import defaultdict

# Each block is rectangular; trailing spaces are important
blocks_text = """
000
 00

111
1 1

2222
2   

3333

444
4  
4  

555 
  55

66 
 66

777
7  

8  
888
8  

9  
999
  9
""".strip()

BLOCKS = defaultdict(set) # starts as a set to remove symmetries.
for i, block in enumerate(blocks_text.split('\n\n')):
    block = [list(line) for line in block.split('\n')]
    for _ in range(4):
        # transpose
        block = [list(row) for row in zip(*block)]
        base = min(col for col, cell in enumerate(block[0]) if cell != ' ')
        BLOCKS[i].add(frozenset({col+row*1j-base for row, line in enumerate(block) for col, cell in enumerate(line) if cell != ' '}))

        # invert
        block = block[::-1]
        base = min(col for col, cell in enumerate(block[0]) if cell != ' ')
        BLOCKS[i].add(frozenset({col+row*1j-base for row, line in enumerate(block) for col, cell in enumerate(line) if cell != ' '}))

    BLOCKS[i] = list(BLOCKS[i]) # now that symmetries are gone, convert to a list for consistent access

if __name__ == "__main__":
    from pprint import pprint
    pprint(BLOCKS)
