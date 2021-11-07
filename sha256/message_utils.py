from sha256.utils import translate, fillZeros, chunker


def preprocessMessage(message):
    bits = translate(message)
    length = len(bits)
    message_len = [int(b) for b in bin(length)[2:].zfill(64)]
    if length < 448:
        bits.append(1)
        bits = fillZeros(bits, 448, "LE")
        bits = bits + message_len
        return [bits]
    elif length == 448:
        bits.append(1)
        bits = fillZeros(bits, 1024, "LE")
        bits[-64:] = message_len
        return chunker(bits, 512)
    else:
        bits.append(1)
        while len(bits) % 512 != 0:
            bits.append(0)
        bits[-64:] = message_len
    return chunker(bits, 512)
