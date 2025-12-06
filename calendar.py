from algorithm_x import AlgorithmX

"""
Find all arrangments of a set of shapes which leave exposed a particular
month, day, and weekday in this calendar:

###############################
# Jan Feb Mar Apr May Jun #####
# Jul Aug Sep Oct Nov Dec #####
#   1   2   3   4   5   6   7 #
#   8   9  10  11  12  13  14 #
#  15  16  17  18  19  20  21 #
#  22  23  24  25  26  27  28 #
#  29  30  31 Sun Mon Tue Wed #
################# Thu Fri Sat #
###############################

For the purpose of Algorithm X, the calendar is a grid numbered like:
 0  1  2  3  4  5  6 
 7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31 32 33 34
35 36 37 38 39 40 41
42 43 44 45 46 47 48
49 50 51 52 53 54 55
"""

WIDTH = 7
HEIGHT = 8

FRAME_RULES = [6, 13, 49, 50, 51, 52]


def get_date_rules(month, day, weekday):
    if month < 7:
        month -= 1
    day = day + 13

    # Mon=0, Sun=6
    weekday = [46, 47, 48, 53, 54, 55, 45][weekday]

    return [month, day, weekday]


SHAPES = {
    0: ["000", "00 "],
    1: ["111", "1 1"],
    2: ["2222", "2   "],
    3: ["3333"],
    4: ["444", "4  ", "4  "],
    5: ["555 ", "  55"],
    6: ["66 ", " 66"],
    7: ["777", "7  "],
    8: ["8  ", "888", "8  "],
    9: ["9  ", "999", "  9"],
}


def all_rotations(numshape):
    maxwidth = max(x for row in numshape for x in row)
    mirror = tuple(tuple(maxwidth - x for x in row[::-1]) for row in numshape)
    return [numshape, mirror, numshape[::-1], mirror[::-1]]


def transpose(shape):
    return list(zip(*shape))


def shape_to_numeric(shape):
    # "x x
    #  xxx"
    #
    # becomes
    #
    # (0, 2),
    # (0, 1, 2)
    return tuple(tuple(i for i, cell in enumerate(row) if cell != " ") for row in shape)


def numeric_to_shape(numshape, character="#"):
    maxwidth = max(x for row in numshape for x in row) + 1
    result = "\n".join(
        "".join(character if i in line else " " for i in range(maxwidth))
        for line in numshape
    )
    return result


def get_shape_rules():
    rule_list = []
    for shape_id, shape in SHAPES.items():
        rotations = set(
            all_rotations(shape_to_numeric(shape))
            + all_rotations(shape_to_numeric(transpose(shape)))
        )

        for rotation_num, rotation in enumerate(rotations):
            shapewidth = max(max(row) for row in rotation)
            shapeheight = len(rotation)
            for start_row in range(HEIGHT - shapeheight + 1):
                for start_col in range(WIDTH - shapewidth):
                 
                    rules = [shape_id + 56] # each shape must appear once

                    for r, row in enumerate(rotation):
                        for c in row:
                            rules.append((start_row + r) * WIDTH + start_col + c)

                    rule_list.append(
                        (
                            rules,
                            f"Position {start_row} {start_col}\n{numeric_to_shape(rotation, str(shape_id))}",
                        )
                    )
    return rule_list


def get_solutions(date):
    solver = AlgorithmX(WIDTH * HEIGHT + len(SHAPES))

    solver.appendRow(FRAME_RULES, "Frame")

    dateRules = get_date_rules(*date)
    solver.appendRow(dateRules, f"Date")

    noShapesHere = set(FRAME_RULES + dateRules)
    shapeRules = get_shape_rules()
    for rules, label in shapeRules:
        if set(rules).isdisjoint(noShapesHere):
            solver.appendRow(rules, label)

    return solver.solve()


def count_solutions(date):
    solutions = get_solutions(date)
    print(*date, len(list(solutions)), sep="\t")


if __name__ == "__main__":
    from multiprocessing import Pool
    from itertools import product

    print("Month", "Day", "Weekday", "Solutions", sep="\t")
    with Pool() as p:
        p.map(count_solutions, product(range(1, 13), range(1, 32), range(7)))
