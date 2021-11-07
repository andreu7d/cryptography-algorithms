def translate(message):
    charcodes = [ord(c) for c in message]
    bytes = [bin(char)[2:].zfill(8) for char in charcodes]
    bits = [int(bit) for byte in bytes for bit in byte]
    return bits


def hexify(value):
    value = "".join([str(x) for x in value])
    binaries = []
    for d in range(0, len(value), 4):
        binaries.append(f"0b{value[d:d+4]}")
    hexes = ""
    for b in binaries:
        hexes += hex(int(b, 2))[2:]
    return hexes


def fillZeros(bits, length=8, endian="LE"):
    l = len(bits)
    if endian == "LE":
        for i in range(l, length):
            bits.append(0)
    else:
        while l < length:
            bits.insert(0, 0)
            l = len(bits)
    return bits


def chunker(bits, chunk_length=8):
    # divides list of bits into desired byte/word chunks,
    # starting at LSB
    chunked = []
    for b in range(0, len(bits), chunk_length):
        chunked.append(bits[b : b + chunk_length])
    return chunked


def initializer(values):
    # convert from hex to python binary string (with cut bin indicator ('0b'))
    binaries = [bin(int(v, 16))[2:] for v in values]
    # convert from python string representation to a list of 32 bit lists
    words = []
    for binary in binaries:
        word = []
        for b in binary:
            word.append(int(b))
        words.append(fillZeros(word, 32, "BE"))
    return words
