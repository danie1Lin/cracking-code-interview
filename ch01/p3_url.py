import unittest


def url_encode(s: list[str], length: int) -> list[str]:
    i = 0
    while i < length:
        print(s, i, length)
        if s[i] == ' ':
            # 這邊容易多1，原本是 length -1 往後移兩個是 length + 1
            for j in range(length+1, i, -1):
                s[j] = s[j-2]
            s[i:i+3] = '%20'
            length += 2
            i += 3 
            continue
        i += 1
    return s



class TestUrlEncode(unittest.TestCase):
    def test(self):
        self.assertEqual(url_encode(list("Mr John Smith    "), 13), list("Mr%20John%20Smith"))

if __name__ == '__main__':
    unittest.main()
