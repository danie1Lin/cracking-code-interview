# We have 20 GB file with one string per line
# We have limit memory to load part of data a time

# Solution 1.
# 1. Load n line once sort and write to a file or in-place modify until all lines are partially sorted
# 2. now we have m file, use int[m] to store the cursor of file, we load the first line of every file. if smallest we pick that line and increase its cursor

# Solution 2. Bucket Sort if we know the charset size
# 1. We load a part of file once, place it into file call (like: 0-a) by its first alphabet.
# 2. after the first step, if the file (0-a) small enough we can sort it in memory. If it is not, we have to do first step again, but we check the second character to place it into file call 1-a, 1-b etc.

# if charset size is small like ascii, we can use solution 2. But if is unicode and word range is very wide we will not have efficiency.
# use the first solution might perform averagely well.
def sort_big_file():
    # TODO: implement it.
    pass
