import unittest
import struct

# not fit the question requests. It is like 0.625 -> 0.101
def binary_to_string_wrong(n: float) -> str:
    packed = struct.pack('!f', n)
    binaries = [bin(i).replace('0b', '') for i in packed]
    s = "".join([s.rjust(8, '0') for s in binaries])
    if len(s) > 32:
        return 'ERROR'
    return s

def binary_to_string(n: float) -> str:
    x = 0
    while 2 ** x < n:
        x += 1
    x -= 1
    s = ""
    c = x
    while n > 0:
        if c == -1:
            if len(s) == 0:
                s += "0"
            s += "."
        if n >= 2 ** c: # >= 的等於漏掉了
            s += "1"
            n -= 2 ** c 
        else:
            s += "0"
        if x - c > 32:
            print(s, x, c)
            return 'ERROR'
        c -= 1
    return s 
class TestBinaryToString(unittest.TestCase):
    def test(self):
        self.assertEqual(binary_to_string(0.625), '0.101')
        self.assertEqual(binary_to_string(1.625), '1.101')
        self.assertEqual(binary_to_string(1.25), '1.01')
        self.assertEqual(binary_to_string(0.629), 'ERROR')

if __name__ == '__main__':
    unittest.main()
