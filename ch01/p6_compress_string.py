import unittest

def compress_string(s: str)-> str:
    compress_str = "" 
    current_word = s[0]
    current_word_count = 1
    curr = 1
    while curr < len(s):
        if current_word != s[curr]:
            # compress_str += current_word + str(current_word_count)
            # 如果是 java 連接字串的速度其實很慢，用 string builder 更好
            # python best practice is join https://waymoot.org/home/python_string/
            # StringIO 算是第二快
            compress_str = "".join([compress_str, current_word, str(current_word_count)])
            current_word_count = 1
            current_word = s[curr]
        else:
            current_word_count += 1
        curr += 1
    compress_str = "".join([compress_str, current_word, str(current_word_count)])
    if len(compress_str) > len(s):
        return s
    else:
        return compress_str

class TestCompressString(unittest.TestCase):
    def test(self):
        self.assertEqual(compress_string("aabcccccaaa"), "a2b1c5a3")

if __name__ == '__main__':
    unittest.main()
