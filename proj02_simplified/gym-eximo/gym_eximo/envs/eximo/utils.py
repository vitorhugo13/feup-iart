# addition of two tuples
# ex: (1, 4) + (3, 2) = (4, 6)
def add(t1: tuple, t2: tuple) -> tuple:
    return (t1[0] + t2[0], t1[1] + t2[1])

# multiply a tuple by a constant
# (2, 3) * 2 = (4, 6)
def mult(t: tuple, f: int) -> tuple:
    return (t[0] * f, t[1] * f)

# a simple enum for referencing move directions
class Direction:
    WEST = (0, 1)
    NORTHWEST = (1, 1)
    NORTH = (1, 0)
    NORTHEAST = (1, -1)
    EAST = (0, -1)
