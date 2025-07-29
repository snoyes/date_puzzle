blocks_text = """
000
 00

000
00

111
1 1

111
1 1

2222
2

2222
   2

3
3
3
3

3
3
3
3

444
4
4

444
4
4

5
55
 5
 5

555
  55

6
66
 6

66
 66

7
7
77

77
7
7

8
888
8

8
888
8

9
999
  9

99
 9
 99
""".strip()

BLOCKS = {x: [set() for _ in range(8)] for x in range(10)}
seen = 1
for block in blocks_text.split('\n\n'):
    seen = 1 - seen
    for imag, line in enumerate(block.split('\n')):
        for real, c in enumerate(line):
            if c.isdigit():
                BLOCKS[int(c)][0+4*seen].add(complex(real, imag))
                BLOCKS[int(c)][1+4*seen].add(complex(imag, -real))
                BLOCKS[int(c)][2+4*seen].add(complex(-real, -imag))
                BLOCKS[int(c)][3+4*seen].add(complex(-imag, real))

#TODO: better symmetry detection
for k in BLOCKS:
    if len(BLOCKS[k][4]) == 0:
        BLOCKS[k] = BLOCKS[k][:4]
BLOCKS[1] = BLOCKS[1][:4]
BLOCKS[3] = BLOCKS[3][:2]
BLOCKS[4] = BLOCKS[4][:4]
BLOCKS[6] = BLOCKS[6][0:2] + BLOCKS[6][4:6]
BLOCKS[8] = BLOCKS[8][:4]
BLOCKS[9] = BLOCKS[9][0:2] + BLOCKS[9][4:6]

if __name__ == "__main__":
    from pprint import pprint
    pprint(BLOCKS)
