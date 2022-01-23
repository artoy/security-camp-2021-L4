import random

# 「Mersenne Twisterの出力を推測してみる」 ももいろテクノロジー https://inaz2.hatenablog.com/entry/2016/03/07/194147

def untemper(x):
    x = unBitshiftRightXor(x, 18)
    x = unBitshiftLeftXor(x, 15, 0xefc60000)
    x = unBitshiftLeftXor(x, 7, 0x9d2c5680)
    x = unBitshiftRightXor(x, 11)
    return x


def unBitshiftRightXor(x, shift):
    i = 1
    y = x
    while i * shift < 32:
        z = y >> shift
        y = x ^ z
        i += 1
    return y


def unBitshiftLeftXor(x, shift, mask):
    i = 1
    y = x
    while i * shift < 32:
        z = y << shift
        y = x ^ (z & mask)
        i += 1
    return y

# ------------------------------------------------------------------------------------------------------


def reloadState(state):
    for i in range(227):
        state[i] = twist(state[i + 397], state[i], state[i + 1])
    for i in range(227, 623):
        state[i] = twist(state[i - 227], state[i], state[i + 1])

    state[623] = twist(state[396], state[623], state[0])

    return state


def twist(m, u, v):
    if v & 1:
        return m ^ (((u & 0x80000000) | (v & 0x7FFFFFFF)) >> 1) ^ 0x9908b0df
    else:
        return m ^ (((u & 0x80000000) | (v & 0x7FFFFFFF)) >> 1)


def temper(x):
    x ^= (x >> 11)
    x ^= (x << 7) & 0x9d2c5680
    x ^= (x << 15) & 0xefc60000
    x ^= (x >> 18)

    return x


def main():
    rand = [0] * 1249
    pred = [0] * 624
    state = [0] * 624
    predState = [0] * 624
    actual = [0] * 624

    for i in range(1248):
        rand[i] = random.getrandbits(32) >> 1

    for i in range(624):
        actual[i] = random.getrandbits(32) >> 1

    for i in range(624):
        for T397_0 in range(2):
            for T0_0 in range(2):
                for T1_0 in range(2):
                    S397 = untemper((rand[i + 397] << 1) | T397_0)
                    S0 = untemper((rand[i] << 1) | T0_0)
                    S1 = untemper((rand[i + 1] << 1) | T1_0)

                    S624 = twist(S397, S0, S1)

                    if temper(S624) >> 1 != rand[i + 624]:
                        continue

                    state[i] = S1

    state = reloadState(state)
    predState[0] = state[623]
    predState[1:] = reloadState(state)[0:623]

    for i in range(624):
        pred[i] = temper(predState[i]) >> 1

    print(pred)
    print(actual)
    print(pred == actual)


if __name__ == "__main__":
    main()
