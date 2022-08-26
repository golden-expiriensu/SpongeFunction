import unittest

from sponge import Sponge

class SpongeTest(unittest.TestCase):
    def setUp(self):
        self.r = 16
        self.c = 48
        self.f = lambda x: x
        self.sponge = Sponge(self.r, self.c, self.f)
    
    def test_extractR(self):
        S = 0b0110101010100001010111100001010001001111011010010001111101001110
        expectR = 0b0110101010100001
        self.assertEqual(self.sponge.extractR(S), expectR)

    def test_extractC(self):
        S = 0b0110101010100001010111100001010001001111011010010001111101001110
        expectC = 0b010111100001010001001111011010010001111101001110
        self.assertEqual(self.sponge.extractC(S), expectC)

    def test_concatRC(self):
        R = 0b0110101010100001
        C = 0b010111100001010001001111011010010001111101001110
        expectS = 0b0110101010100001010111100001010001001111011010010001111101001110
        self.assertEqual(self.sponge.concatRC(R, C), expectS)

    def test_appendBits(self):
        to = 0b1010011011101001000100010111101011
        bits = 0b11010101010111110100001

        expect23 = 0b101001101110100100010001011110101111010101010111110100001
        expect32 = 0b101001101110100100010001011110101100000000011010101010111110100001

        self.assertEqual(self.sponge.appendBits(to, bits, 23), expect23)
        self.assertEqual(self.sponge.appendBits(to, bits, 32), expect32)

    def test_constrainByBitlen(self):
        value = 0b111110001000011000101100010

        expect24 = 0b110001000011000101100010
        expect16 = 0b11000101100010

        self.assertEqual(self.sponge.constrainByBitlen(value, 24), expect24)
        self.assertEqual(self.sponge.constrainByBitlen(value, 16), expect16)

    def test_splitToBitBlocks(self):
        input = 0b101110100010110110111101000001100101110100010101110111010010000101101100
        expect = [
            0b0010000101101100,
            0b0001010111011101,
            0b0000011001011101,
            0b0010110110111101,
            0b10111010
        ]
        self.assertEqual(self.sponge.splitToBitBlocks(input, 16), expect)
    
    def test_absorb(self):
        input = 123456756368139847192816889
        expect = 0b1011111010110010000000000000000000000000000000000000000000000000
        self.sponge.absorb(input)
        self.assertEqual(self.sponge.S, expect)

    def test_squeeze(self):
        input = 123456756368139847192816889
        after = 0b1011111010110010000000000000000000000000000000000000000000000000
    
        expect32 = 0b10111110101100101011111010110010
        expect39 = 0b101111101011001010111110101100100110010

        self.assertEqual(self.sponge.operate(input, 32), expect32)
        self.assertEqual(self.sponge.operate(input, 39), expect39)

if __name__ == "__main__":
    unittest.main()