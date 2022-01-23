import sys


def next(oldSeed):
    return (oldSeed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)


def main(oldNum, nextNum, act):
    for i in range(2 ** 16):
        oldSeed = (oldNum << 16) + i

        nextNumAct = next(oldSeed) >> 16

        if((nextNumAct) >> 31 & 1):
            nextNumAct = -((nextNumAct ^ ((1 << 32) - 1)) + 1)

        if nextNum == nextNumAct:
            break

    pred = next(next(oldSeed)) >> 16

    if((pred >> 31) & 1):
        pred = -((pred ^ ((1 << 32) - 1)) + 1)

    print("predict: " + str(pred))
    print("actual: " + str(act))
    print(act == pred)


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Usage:")
		print(f' {sys.argv[0]} <rand_n> <rand_n+1> <rand_n+2 (This program predict it)>')
	else:
		main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
