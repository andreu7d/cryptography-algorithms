from sha256.utils import translate, hexify, fillZeros, chunker, initializer
from sha256.message_utils import preprocessMessage
from sha256.constants import initial_values, round_constants
from sha256.crypto_utils import *

message = "Hello World"


def sha256(message):

    k = initializer(round_constants())
    h0, h1, h2, h3, h4, h5, h6, h7 = initializer(initial_values())
    ## Cut the message into 512 bit chunks, and pad with the sha2 scheme
    chunks = preprocessMessage(message)

    for chunk in chunks:
        ## Message schedule
        ## Since the message is 512 bits, this leaves 16 x 32 bit words
        words = chunker(chunk, 32)

        ## Since we need 64 x 32 bit words for sha, we add 48 times 32 bit words that are zero
        words = words + [[0] * 32] * 48

        ## Starting at 16th word, the first fully 0 word, we run the algo, notice the lag
        for i in range(16, 64):
            lag2 = words[i - 2]
            lag7 = words[i - 7]
            lag15 = words[i - 15]
            lag16 = words[i - 16]

            sig0 = XORXOR(rotr(lag15, 7), rotr(lag15, 18), shr(lag15, 3))
            sig1 = XORXOR(rotr(lag2, 17), rotr(lag2, 19), shr(lag2, 10))

            words[i] = add(add(add(lag16, sig0), lag7), sig1)

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for j in range(64):
            Sig1 = XORXOR(rotr(e, 6), rotr(e, 11), rotr(e, 25))
            Choose = XOR(AND(e, f), AND(NOT(e), g))
            Temp1 = add(add(add(add(h, Sig1), Choose), k[j]), words[j])

            Sig0 = XORXOR(rotr(a, 2), rotr(a, 13), rotr(a, 22))
            Majority = XORXOR(AND(a, b), AND(a, c), AND(b, c))
            Temp2 = add(Sig0, Majority)

            a0 = add(Temp1, Temp2)
            d0 = add(d, Temp1)

            h = g
            g = f
            f = e
            e = d0
            d = c
            c = b
            b = a
            a = a0

        h0 = add(h0, a)
        h1 = add(h1, b)
        h2 = add(h2, c)
        h3 = add(h3, d)
        h4 = add(h4, e)
        h5 = add(h5, f)
        h6 = add(h6, g)
        h7 = add(h7, h)

    digest = ""
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += hexify(val)
    return digest


print(sha256(message))
