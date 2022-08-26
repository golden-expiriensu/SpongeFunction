import math

# Int order to operate input through algoritm call 'operate' method
# For better variables and algoritm explanation, check: https://en.wikipedia.org/wiki/Sponge_function
class Sponge:
    def __init__(self, r, c, f):
        self.r = r # bitrate (first part of the S)
        self.c = c # capacity (second part of the S)
        self.b = r + c # store bit length

        self.S = 0 # store
        self.f = f # mixing funtion, will be applied to S
        self.CMask = (1 << c) - 1 # bitmask to get C (first part of the S)

    # help view functions

    def extractR(self, S):
        return S >> self.c

    def extractC(self, S):
        return S & self.CMask

    def concatRC(self, R, C):
        C = self.constrainByBitlen(C, self.c)
        return (R << self.c) | C

    def appendBits(self, to, bits, bitlen):
        return (to << bitlen) | bits

    def constrainByBitlen(self, value, bitlen):
        mask = (1 << bitlen) - 1
        return value & mask

    def splitToBitBlocks(self, value, bitBlockLen):
        mask = (1 << bitBlockLen) - 1
        blocks = []

        numOfBlocks = math.ceil(value.bit_length() / bitBlockLen)

        for i in range(numOfBlocks):
            block = (value >> (bitBlockLen * i)) & mask
            blocks.append(block)
        
        return blocks

    # sponge operations

    def operate(self, M, outputBitLen):
        self.S = 0
        self.absorb(M)
        return self.squeeze(outputBitLen)

    def absorb(self, M):
        rBlocks = self.splitToBitBlocks(M, self.r)
        
        for B in rBlocks:
            newR = self.extractR(self.S) ^ B
            newS = self.concatRC(newR, self.extractC(self.S))
            self.S = self.f(newS)

    def squeeze(self, outputBitLen):
        result = 0
        while outputBitLen > 0:
            extracted = self.extractR(self.S)
            constraned = self.constrainByBitlen(extracted, outputBitLen)

            bitlenConstrained = min(self.r, outputBitLen)
            result = self.appendBits(result, constraned, bitlenConstrained)

            self.S = self.f(self.S)
            outputBitLen -= self.r
        return result