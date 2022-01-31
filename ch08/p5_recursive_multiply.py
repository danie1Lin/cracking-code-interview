#limit: a & b > 0
def recursive_multiply(a: int, b: int):
    if a < 0 | b < 0:
        raise ValueError("must be positive function")
    if b == 0:
        return 0 
    return a + recursive_multiply(a, b - 1)

def recursive_multiply_bitshift(a: int, b: int):
    r = 0
    if b == 0:
        return r
    if b & 0b1:
        r += a
    left_bit_multiply = recursive_multiply_bitshift(a, b >> 1)
    r += left_bit_multiply + left_bit_multiply
    return r

def test_recursive_multiply():
    assert 5 * 8 == recursive_multiply(5, 8)
    assert 0 * 8 == recursive_multiply(0, 8)
    assert 8 * 0 == recursive_multiply(8, 0)

def test_recursive_multiply_bitshift():
    assert 5 * 8 == recursive_multiply_bitshift(5, 8)
    assert 0 * 8 == recursive_multiply_bitshift(0, 8)
    assert 8 * 0 == recursive_multiply_bitshift(8, 0)

