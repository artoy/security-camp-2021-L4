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


def initialState(seed):
    state = [0] * 624

    state[0] = seed & 0xffffffff

    for i in range(623):
        state[i + 1] = (1812433253 * (state[i] ^
                        (state[i] >> 30)) + (i + 1)) & 0xffffffff

    return state


def reloadState(state):
    for i in range(227):
        state[i] = twist(state[i + 397], state[i], state[i + 1])
    for i in range(227, 623):
        state[i] = twist(state[i - 227], state[i], state[i + 1])

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


def previousState(s, i):
    x = (2520285293 * (s - i)) & 0xffffffff
    return x ^ (x >> 30)


def recoveryState(T0, T227, offset, initialFlag, S228_31):
    clue = T0 ^ T227

    S228_0 = clue >> 31

    if S228_0 == 1:
        clue ^= 0x9908b0df

    S227_31 = clue >> 30

    if S227_31 == 1:
        S228_30_1 = (clue ^ (1 << 30)) << 1
    else:
        S228_30_1 = clue << 1

    S228 = (S228_31 << 31) | S228_30_1 | S228_0

    if initialFlag:
        S227 = previousState(S228, offset + 228)

        if S227 >> 31 != S227_31:
            return None

        seed = S227

        for i in range(offset + 227, 0, -1):
            seed = previousState(seed, i)

        return seed
    else:
        return S228


def main(state):
    for i in range(624):
        state[i] = untemper(state[i])

    state = reloadState(state)

    ans = [0] * 624

    for i in range(624):
        ans[i] = temper(state[i])

    return ans

for i in range(300):
    dummy =random.getrandbits(32)

predicted = [0] * 624

for i in range(624):
    predicted[i] = random.getrandbits(32)

print(main(predicted))

for i in range(624):
    predicted[i] = random.getrandbits(32)

print(predicted)




