# limit: a & b > 0
def recursive_multiply(a: int, b: int):
    # recursive function call is more expensive so we place smaller number at second argument
    bigger = max(a, b)
    smaller = min(a, b)
    if a < 0 | b < 0:
        raise ValueError("must be positive function")
    if smaller == 0:
        return 0 
    if smaller == 1:
        return bigger
    # use bitshift to n function call to log(n) function call 
    result = recursive_multiply(bigger, smaller >> 1)
    result += result
    if smaller % 2: result += bigger
    return result

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

