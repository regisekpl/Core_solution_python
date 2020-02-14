# solution to the core puzzle written in python as an exercise

# I didn't solve also I didn't write algoritm on discord channel (@km user did) /
# - this python version helps me practice and understand solution

# first, the mapping, I took it from 0646 hint (mind that there are 2 possible versions)

# DG - dark green, P - purple, G - green, B - blue, numbers are width

mapping = {
    "DG1": '0',
    "DG2": '4',
    "DG3": '8',
    "DG4": 'C',
    "P1": '1',
    "P2": '5',
    "P3": '9',
    "P4": 'D',
    "G1": '2',
    "G2": '6',
    "G3": 'A',
    "G4": 'E',
    "B1": '3',
    "B2": '7',
    "B3": 'B',
    "B4": 'F'
}

# that's the core read from most inner circle.

core = [["DG1", "G2", "DG2", "G2"],
        ["P4", "G3", "DG4", "G4"],
        ["B2", "DG3", "B1", "P2"],
        ["P3", "P3", "DG2", "P3"],
        ["G2", "DG1", "P2", "B3"],
        ["DG4", "B1", "G4", "G4"],
        ["B1", "DG3", "P4", "B2"],
        ["P3", "B4", "P2", "G1"],
        ["G4", "P4", "B3", "G3"],
        ["B3", "B1", "G2", "DG2"],
        ["B1", "DG1", "DG2", "P1"],
        ["G2", "DG3", "G1", "B4"],
        ["B4", "G3", "DG3", "G1"],
        ["G4", "G1", "B4", "B4"],
        ["P2", "B2", "P3", "G2"],
        ["DG3", "B3", "P1", "DG3"]]


# second - I generate base for the key - I've build upon it later
# def generatebase():
#     result = []
#
#     for x in range(0,16):
#         for y in range(0,4):
#             result.append(mapping.get(core[x][y]))
#
#     print(result)
#
# generatebase()

# what I did wrong was to treat every hex bit individually - I should take whole ring each time, not the arcs.

# third step and most important - take each ring, rotate bits (not simple shift!) and substract previous ring


# function for rotating bits right - found on stack overflow by David Heffernan as answer to Jack Evans

def mask1(n):
    """Return a bitmask of length n (suitable for masking against an
      int to coerce the size to a given length)
   """
    if n >= 0:
        return 2 ** n - 1
    else:
        return 0


def ror(n, rotations=1):
    """Return a given number of bitwise right rotations of an integer n,
       for a given bit field width.
    """
    rotations %= 16  # width bytes give 8*bytes bits
    if rotations < 1:
        return n
    mask = mask1(16)  # store the mask
    n &= mask
    return (n >> rotations) | ((n << (16 - rotations)) & mask)  # apply the mask to result


def converttostr(input_seq, seperator):
    # Join all the strings in list
    final_str = seperator.join(input_seq)
    return final_str


# step 3.1 - create 16 rings from core mapping

def generatebase():
    # initializing 2 dimensional array
    w, h = 4, 16;
    Matrix = [[0 for x in range(w)] for y in range(h)]

    resultInt = []
    resultHex = []
    keyHex = []

    finalPK = ""

    # MAIN LOOP for every arc in every ring
    for x in range(0, 16):
        for y in range(0, 4):
            # translating arcs to base PK - we build upon it
            Matrix[x][y] = mapping.get(core[x][y])

        # ugly code to change table of chars to table of Int to table of 4-length Hex
        resultInt.append(int(converttostr(Matrix[x], ""), 16))
        #resultHex.append(hex(resultInt[x])) - nope - this cuts leading zeros :( Using code below
        resultHex.append(format(resultInt[x], '#06x'))

        # main algorithm (fi(xi,yi-1))
        if x == 0:
            keyHex.append(resultHex[x])
        else:
            temp = (ror(resultInt[x], x) - (resultInt[x - 1])) % 65536
            keyHex.append(hex(temp))


        # adding to finalPK and removing 0x
        finalPK = finalPK + str(keyHex[x])[len('0x'):]


    return finalPK


#calling the function
pk = ""
pk = generatebase()

print("final key is: ")
print(pk)
