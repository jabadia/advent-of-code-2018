from collections import namedtuple, defaultdict
import re
import inspect

TestCase = namedtuple('TestCase', 'case expected')

INPUT1 = """
Before: [1, 2, 3, 2]
3 1 3 0
After:  [1, 2, 3, 2]

Before: [1, 1, 1, 3]
5 1 3 0
After:  [3, 1, 1, 3]

Before: [2, 3, 0, 2]
0 1 0 2
After:  [2, 3, 6, 2]

Before: [1, 2, 2, 3]
11 0 3 3
After:  [1, 2, 2, 0]

Before: [0, 0, 3, 3]
9 0 0 1
After:  [0, 0, 3, 3]

Before: [1, 0, 1, 2]
10 1 2 0
After:  [1, 0, 1, 2]

Before: [0, 2, 0, 2]
13 1 1 1
After:  [0, 1, 0, 2]

Before: [3, 1, 1, 1]
6 1 0 1
After:  [3, 3, 1, 1]

Before: [2, 3, 2, 0]
4 1 2 2
After:  [2, 3, 1, 0]

Before: [1, 2, 0, 2]
3 1 3 2
After:  [1, 2, 1, 2]

Before: [0, 1, 3, 3]
2 1 0 2
After:  [0, 1, 1, 3]

Before: [0, 3, 1, 3]
6 2 1 2
After:  [0, 3, 3, 3]

Before: [3, 1, 1, 1]
6 1 0 2
After:  [3, 1, 3, 1]

Before: [0, 2, 3, 2]
3 1 3 0
After:  [1, 2, 3, 2]

Before: [0, 0, 1, 3]
7 2 1 0
After:  [1, 0, 1, 3]

Before: [3, 1, 2, 3]
15 2 3 1
After:  [3, 3, 2, 3]

Before: [3, 2, 3, 2]
3 1 3 3
After:  [3, 2, 3, 1]

Before: [0, 2, 1, 2]
3 1 3 0
After:  [1, 2, 1, 2]

Before: [1, 0, 1, 1]
1 1 0 1
After:  [1, 1, 1, 1]

Before: [3, 2, 2, 2]
3 1 3 1
After:  [3, 1, 2, 2]

Before: [2, 3, 2, 3]
8 2 2 3
After:  [2, 3, 2, 4]

Before: [2, 1, 0, 2]
8 0 1 0
After:  [3, 1, 0, 2]

Before: [1, 1, 2, 3]
5 0 3 1
After:  [1, 3, 2, 3]

Before: [1, 0, 3, 1]
1 1 0 0
After:  [1, 0, 3, 1]

Before: [0, 1, 3, 1]
14 3 2 1
After:  [0, 3, 3, 1]

Before: [3, 3, 1, 1]
0 1 0 1
After:  [3, 9, 1, 1]

Before: [2, 3, 0, 3]
15 0 3 2
After:  [2, 3, 3, 3]

Before: [2, 2, 3, 3]
15 1 3 2
After:  [2, 2, 3, 3]

Before: [1, 1, 3, 2]
12 0 2 3
After:  [1, 1, 3, 3]

Before: [2, 1, 1, 3]
15 0 3 3
After:  [2, 1, 1, 3]

Before: [0, 2, 3, 2]
9 0 0 2
After:  [0, 2, 0, 2]

Before: [3, 2, 1, 0]
6 2 0 0
After:  [3, 2, 1, 0]

Before: [3, 3, 3, 2]
13 1 0 0
After:  [1, 3, 3, 2]

Before: [3, 2, 2, 3]
8 2 2 3
After:  [3, 2, 2, 4]

Before: [1, 0, 2, 3]
1 1 0 2
After:  [1, 0, 1, 3]

Before: [1, 0, 2, 0]
8 2 2 2
After:  [1, 0, 4, 0]

Before: [1, 3, 3, 2]
12 0 2 1
After:  [1, 3, 3, 2]

Before: [0, 1, 2, 2]
2 1 0 2
After:  [0, 1, 1, 2]

Before: [3, 0, 2, 3]
0 3 0 0
After:  [9, 0, 2, 3]

Before: [2, 0, 3, 1]
7 3 1 3
After:  [2, 0, 3, 1]

Before: [1, 2, 1, 3]
10 1 0 0
After:  [1, 2, 1, 3]

Before: [2, 3, 3, 0]
4 1 0 2
After:  [2, 3, 1, 0]

Before: [0, 1, 1, 2]
2 1 0 3
After:  [0, 1, 1, 1]

Before: [1, 0, 0, 2]
7 0 1 1
After:  [1, 1, 0, 2]

Before: [2, 3, 2, 2]
4 1 2 1
After:  [2, 1, 2, 2]

Before: [1, 2, 1, 0]
13 1 1 2
After:  [1, 2, 1, 0]

Before: [1, 0, 2, 2]
1 1 0 2
After:  [1, 0, 1, 2]

Before: [2, 2, 1, 3]
11 0 3 2
After:  [2, 2, 0, 3]

Before: [0, 1, 3, 1]
2 1 0 0
After:  [1, 1, 3, 1]

Before: [0, 1, 2, 2]
2 1 0 1
After:  [0, 1, 2, 2]

Before: [2, 3, 1, 1]
6 2 1 1
After:  [2, 3, 1, 1]

Before: [1, 2, 1, 0]
10 1 0 1
After:  [1, 1, 1, 0]

Before: [3, 1, 0, 3]
5 1 3 3
After:  [3, 1, 0, 3]

Before: [2, 1, 3, 1]
12 1 2 0
After:  [3, 1, 3, 1]

Before: [0, 0, 2, 3]
10 0 1 0
After:  [1, 0, 2, 3]

Before: [0, 1, 2, 0]
2 1 0 1
After:  [0, 1, 2, 0]

Before: [0, 1, 0, 3]
5 1 3 1
After:  [0, 3, 0, 3]

Before: [0, 1, 1, 1]
2 1 0 0
After:  [1, 1, 1, 1]

Before: [2, 0, 2, 1]
7 3 1 2
After:  [2, 0, 1, 1]

Before: [1, 0, 1, 0]
7 2 1 1
After:  [1, 1, 1, 0]

Before: [3, 2, 3, 3]
15 1 3 1
After:  [3, 3, 3, 3]

Before: [1, 2, 0, 3]
10 1 0 0
After:  [1, 2, 0, 3]

Before: [1, 2, 0, 0]
13 1 1 3
After:  [1, 2, 0, 1]

Before: [2, 3, 2, 3]
0 1 0 2
After:  [2, 3, 6, 3]

Before: [3, 3, 3, 1]
13 1 0 1
After:  [3, 1, 3, 1]

Before: [1, 2, 3, 1]
14 3 2 2
After:  [1, 2, 3, 1]

Before: [0, 0, 1, 3]
8 0 3 1
After:  [0, 3, 1, 3]

Before: [0, 2, 2, 3]
0 3 1 2
After:  [0, 2, 6, 3]

Before: [1, 1, 3, 3]
5 0 3 2
After:  [1, 1, 3, 3]

Before: [0, 1, 1, 0]
2 1 0 2
After:  [0, 1, 1, 0]

Before: [1, 0, 3, 0]
1 1 0 0
After:  [1, 0, 3, 0]

Before: [0, 1, 2, 0]
2 1 0 0
After:  [1, 1, 2, 0]

Before: [1, 1, 3, 2]
14 3 1 1
After:  [1, 3, 3, 2]

Before: [1, 3, 2, 2]
6 0 1 1
After:  [1, 3, 2, 2]

Before: [1, 0, 0, 2]
1 1 0 1
After:  [1, 1, 0, 2]

Before: [2, 3, 3, 0]
4 1 0 3
After:  [2, 3, 3, 1]

Before: [1, 0, 2, 1]
10 1 3 2
After:  [1, 0, 1, 1]

Before: [2, 1, 1, 1]
0 3 0 3
After:  [2, 1, 1, 2]

Before: [1, 0, 0, 1]
7 0 1 3
After:  [1, 0, 0, 1]

Before: [2, 0, 0, 1]
7 3 1 3
After:  [2, 0, 0, 1]

Before: [2, 3, 3, 2]
13 1 2 0
After:  [1, 3, 3, 2]

Before: [2, 2, 0, 1]
13 1 0 3
After:  [2, 2, 0, 1]

Before: [2, 3, 1, 3]
5 2 3 3
After:  [2, 3, 1, 3]

Before: [3, 2, 3, 2]
3 1 3 2
After:  [3, 2, 1, 2]

Before: [1, 3, 3, 1]
12 0 2 2
After:  [1, 3, 3, 1]

Before: [1, 0, 1, 3]
7 2 1 0
After:  [1, 0, 1, 3]

Before: [1, 3, 2, 0]
6 0 1 1
After:  [1, 3, 2, 0]

Before: [2, 0, 3, 1]
14 3 2 3
After:  [2, 0, 3, 3]

Before: [0, 1, 3, 1]
8 0 1 1
After:  [0, 1, 3, 1]

Before: [1, 1, 2, 3]
15 2 3 2
After:  [1, 1, 3, 3]

Before: [1, 2, 2, 2]
3 1 3 3
After:  [1, 2, 2, 1]

Before: [0, 1, 0, 2]
2 1 0 1
After:  [0, 1, 0, 2]

Before: [1, 2, 3, 3]
5 0 3 2
After:  [1, 2, 3, 3]

Before: [0, 0, 2, 0]
8 2 2 1
After:  [0, 4, 2, 0]

Before: [2, 3, 3, 1]
0 0 2 1
After:  [2, 6, 3, 1]

Before: [1, 0, 3, 2]
12 0 2 1
After:  [1, 3, 3, 2]

Before: [3, 1, 0, 3]
5 1 3 0
After:  [3, 1, 0, 3]

Before: [0, 0, 3, 1]
10 0 1 1
After:  [0, 1, 3, 1]

Before: [3, 3, 0, 2]
13 1 0 2
After:  [3, 3, 1, 2]

Before: [1, 1, 0, 3]
5 0 3 1
After:  [1, 3, 0, 3]

Before: [3, 3, 3, 1]
14 3 2 0
After:  [3, 3, 3, 1]

Before: [1, 3, 2, 3]
5 0 3 0
After:  [3, 3, 2, 3]

Before: [1, 0, 0, 3]
7 0 1 2
After:  [1, 0, 1, 3]

Before: [2, 2, 3, 1]
14 3 2 3
After:  [2, 2, 3, 3]

Before: [0, 1, 3, 1]
12 1 2 0
After:  [3, 1, 3, 1]

Before: [0, 1, 2, 3]
9 0 0 3
After:  [0, 1, 2, 0]

Before: [1, 3, 2, 3]
5 0 3 3
After:  [1, 3, 2, 3]

Before: [0, 2, 2, 3]
8 1 2 2
After:  [0, 2, 4, 3]

Before: [2, 3, 3, 0]
0 2 0 3
After:  [2, 3, 3, 6]

Before: [2, 3, 3, 1]
14 3 2 3
After:  [2, 3, 3, 3]

Before: [3, 1, 2, 2]
8 2 2 0
After:  [4, 1, 2, 2]

Before: [2, 3, 3, 3]
11 0 3 2
After:  [2, 3, 0, 3]

Before: [2, 2, 3, 2]
13 1 0 3
After:  [2, 2, 3, 1]

Before: [3, 0, 3, 3]
0 3 0 0
After:  [9, 0, 3, 3]

Before: [2, 3, 2, 3]
4 1 2 2
After:  [2, 3, 1, 3]

Before: [0, 0, 1, 1]
7 2 1 0
After:  [1, 0, 1, 1]

Before: [1, 0, 3, 0]
1 1 0 2
After:  [1, 0, 1, 0]

Before: [0, 1, 2, 3]
8 2 2 1
After:  [0, 4, 2, 3]

Before: [0, 1, 3, 0]
2 1 0 3
After:  [0, 1, 3, 1]

Before: [3, 3, 3, 1]
13 1 0 2
After:  [3, 3, 1, 1]

Before: [0, 1, 3, 0]
2 1 0 2
After:  [0, 1, 1, 0]

Before: [0, 0, 3, 1]
7 3 1 3
After:  [0, 0, 3, 1]

Before: [1, 0, 3, 0]
1 1 0 3
After:  [1, 0, 3, 1]

Before: [0, 3, 1, 2]
6 2 1 2
After:  [0, 3, 3, 2]

Before: [2, 1, 1, 3]
5 2 3 3
After:  [2, 1, 1, 3]

Before: [2, 0, 0, 3]
11 0 3 3
After:  [2, 0, 0, 0]

Before: [1, 0, 2, 1]
1 1 0 3
After:  [1, 0, 2, 1]

Before: [1, 3, 2, 3]
4 1 2 0
After:  [1, 3, 2, 3]

Before: [0, 2, 1, 2]
3 1 3 3
After:  [0, 2, 1, 1]

Before: [0, 0, 0, 0]
9 0 0 3
After:  [0, 0, 0, 0]

Before: [1, 0, 3, 3]
1 1 0 1
After:  [1, 1, 3, 3]

Before: [1, 1, 3, 1]
12 0 2 3
After:  [1, 1, 3, 3]

Before: [2, 3, 0, 0]
4 1 0 2
After:  [2, 3, 1, 0]

Before: [0, 1, 2, 3]
9 0 0 0
After:  [0, 1, 2, 3]

Before: [1, 0, 0, 3]
1 1 0 3
After:  [1, 0, 0, 1]

Before: [2, 2, 2, 0]
13 1 0 3
After:  [2, 2, 2, 1]

Before: [3, 3, 3, 3]
13 1 0 2
After:  [3, 3, 1, 3]

Before: [1, 2, 1, 3]
15 1 3 3
After:  [1, 2, 1, 3]

Before: [1, 3, 2, 1]
4 1 2 2
After:  [1, 3, 1, 1]

Before: [3, 3, 3, 3]
13 1 0 1
After:  [3, 1, 3, 3]

Before: [1, 0, 1, 1]
7 2 1 0
After:  [1, 0, 1, 1]

Before: [2, 1, 0, 3]
5 1 3 2
After:  [2, 1, 3, 3]

Before: [1, 0, 1, 2]
7 0 1 2
After:  [1, 0, 1, 2]

Before: [2, 1, 3, 2]
8 1 3 3
After:  [2, 1, 3, 3]

Before: [1, 2, 2, 3]
15 1 3 0
After:  [3, 2, 2, 3]

Before: [1, 0, 2, 3]
11 0 3 3
After:  [1, 0, 2, 0]

Before: [1, 3, 2, 2]
4 1 2 0
After:  [1, 3, 2, 2]

Before: [2, 2, 2, 3]
15 0 3 2
After:  [2, 2, 3, 3]

Before: [3, 1, 3, 1]
12 1 2 2
After:  [3, 1, 3, 1]

Before: [1, 0, 2, 1]
1 1 0 2
After:  [1, 0, 1, 1]

Before: [0, 3, 2, 0]
0 2 1 2
After:  [0, 3, 6, 0]

Before: [0, 2, 3, 2]
13 1 1 0
After:  [1, 2, 3, 2]

Before: [2, 3, 3, 2]
4 1 0 2
After:  [2, 3, 1, 2]

Before: [3, 3, 2, 1]
4 1 2 1
After:  [3, 1, 2, 1]

Before: [1, 3, 1, 2]
8 2 3 3
After:  [1, 3, 1, 3]

Before: [1, 3, 1, 1]
6 0 1 0
After:  [3, 3, 1, 1]

Before: [0, 3, 2, 1]
14 3 2 2
After:  [0, 3, 3, 1]

Before: [1, 0, 0, 3]
1 1 0 0
After:  [1, 0, 0, 3]

Before: [0, 0, 1, 1]
10 0 1 2
After:  [0, 0, 1, 1]

Before: [1, 1, 2, 2]
8 2 2 0
After:  [4, 1, 2, 2]

Before: [1, 2, 3, 2]
3 1 3 1
After:  [1, 1, 3, 2]

Before: [1, 2, 1, 2]
10 1 0 1
After:  [1, 1, 1, 2]

Before: [2, 3, 2, 0]
4 1 0 1
After:  [2, 1, 2, 0]

Before: [1, 0, 1, 0]
1 1 0 1
After:  [1, 1, 1, 0]

Before: [2, 0, 1, 2]
10 1 2 1
After:  [2, 1, 1, 2]

Before: [3, 3, 3, 0]
13 1 0 2
After:  [3, 3, 1, 0]

Before: [2, 0, 3, 3]
11 0 3 3
After:  [2, 0, 3, 0]

Before: [0, 1, 2, 3]
5 1 3 3
After:  [0, 1, 2, 3]

Before: [1, 0, 2, 3]
1 1 0 0
After:  [1, 0, 2, 3]

Before: [0, 0, 3, 3]
10 0 1 0
After:  [1, 0, 3, 3]

Before: [1, 0, 2, 2]
1 1 0 0
After:  [1, 0, 2, 2]

Before: [1, 0, 0, 2]
1 1 0 2
After:  [1, 0, 1, 2]

Before: [2, 3, 1, 1]
6 2 1 2
After:  [2, 3, 3, 1]

Before: [2, 2, 3, 1]
14 3 2 2
After:  [2, 2, 3, 1]

Before: [3, 3, 1, 3]
6 2 1 3
After:  [3, 3, 1, 3]

Before: [0, 1, 1, 2]
2 1 0 0
After:  [1, 1, 1, 2]

Before: [2, 0, 3, 3]
0 2 2 3
After:  [2, 0, 3, 9]

Before: [0, 1, 0, 0]
9 0 0 1
After:  [0, 0, 0, 0]

Before: [0, 1, 2, 1]
2 1 0 3
After:  [0, 1, 2, 1]

Before: [2, 2, 0, 3]
15 0 3 3
After:  [2, 2, 0, 3]

Before: [0, 3, 2, 1]
14 3 2 3
After:  [0, 3, 2, 3]

Before: [1, 2, 1, 3]
15 1 3 0
After:  [3, 2, 1, 3]

Before: [0, 3, 0, 2]
9 0 0 3
After:  [0, 3, 0, 0]

Before: [1, 2, 0, 1]
13 1 1 1
After:  [1, 1, 0, 1]

Before: [2, 3, 3, 1]
14 3 2 1
After:  [2, 3, 3, 1]

Before: [0, 2, 1, 3]
15 1 3 3
After:  [0, 2, 1, 3]

Before: [1, 0, 2, 1]
7 3 1 2
After:  [1, 0, 1, 1]

Before: [0, 2, 3, 2]
3 1 3 3
After:  [0, 2, 3, 1]

Before: [3, 3, 1, 3]
13 1 0 3
After:  [3, 3, 1, 1]

Before: [3, 2, 2, 2]
3 1 3 3
After:  [3, 2, 2, 1]

Before: [0, 1, 1, 1]
9 0 0 1
After:  [0, 0, 1, 1]

Before: [0, 1, 2, 3]
9 0 0 1
After:  [0, 0, 2, 3]

Before: [0, 1, 3, 2]
9 0 0 0
After:  [0, 1, 3, 2]

Before: [1, 1, 3, 3]
11 0 3 2
After:  [1, 1, 0, 3]

Before: [1, 1, 1, 3]
5 0 3 1
After:  [1, 3, 1, 3]

Before: [3, 1, 1, 2]
14 3 1 1
After:  [3, 3, 1, 2]

Before: [0, 3, 1, 0]
0 1 1 2
After:  [0, 3, 9, 0]

Before: [0, 1, 1, 1]
2 1 0 1
After:  [0, 1, 1, 1]

Before: [2, 2, 2, 1]
8 2 2 3
After:  [2, 2, 2, 4]

Before: [1, 2, 3, 0]
12 0 2 0
After:  [3, 2, 3, 0]

Before: [3, 3, 2, 1]
4 1 2 2
After:  [3, 3, 1, 1]

Before: [2, 2, 2, 1]
14 3 2 0
After:  [3, 2, 2, 1]

Before: [1, 1, 2, 1]
8 2 1 2
After:  [1, 1, 3, 1]

Before: [0, 3, 2, 2]
4 1 2 1
After:  [0, 1, 2, 2]

Before: [1, 0, 0, 0]
1 1 0 0
After:  [1, 0, 0, 0]

Before: [0, 1, 3, 2]
2 1 0 1
After:  [0, 1, 3, 2]

Before: [3, 3, 2, 0]
0 0 1 1
After:  [3, 9, 2, 0]

Before: [2, 3, 3, 3]
15 0 3 2
After:  [2, 3, 3, 3]

Before: [1, 0, 0, 2]
1 1 0 0
After:  [1, 0, 0, 2]

Before: [0, 3, 2, 3]
4 1 2 3
After:  [0, 3, 2, 1]

Before: [0, 1, 1, 2]
2 1 0 2
After:  [0, 1, 1, 2]

Before: [1, 2, 1, 2]
3 1 3 0
After:  [1, 2, 1, 2]

Before: [2, 2, 0, 3]
15 0 3 2
After:  [2, 2, 3, 3]

Before: [1, 3, 3, 0]
6 0 1 3
After:  [1, 3, 3, 3]

Before: [3, 2, 2, 3]
15 2 3 2
After:  [3, 2, 3, 3]

Before: [2, 2, 0, 2]
3 1 3 0
After:  [1, 2, 0, 2]

Before: [0, 1, 3, 1]
12 1 2 1
After:  [0, 3, 3, 1]

Before: [2, 0, 3, 3]
15 0 3 1
After:  [2, 3, 3, 3]

Before: [1, 1, 0, 2]
14 3 1 0
After:  [3, 1, 0, 2]

Before: [3, 3, 1, 2]
0 1 1 0
After:  [9, 3, 1, 2]

Before: [3, 1, 0, 0]
6 1 0 1
After:  [3, 3, 0, 0]

Before: [2, 2, 3, 1]
13 1 1 0
After:  [1, 2, 3, 1]

Before: [1, 0, 3, 2]
7 0 1 1
After:  [1, 1, 3, 2]

Before: [0, 1, 2, 1]
8 2 2 0
After:  [4, 1, 2, 1]

Before: [1, 0, 3, 1]
7 0 1 2
After:  [1, 0, 1, 1]

Before: [0, 3, 1, 1]
6 2 1 0
After:  [3, 3, 1, 1]

Before: [1, 0, 3, 3]
12 0 2 1
After:  [1, 3, 3, 3]

Before: [1, 3, 3, 3]
12 0 2 2
After:  [1, 3, 3, 3]

Before: [2, 1, 3, 1]
12 1 2 3
After:  [2, 1, 3, 3]

Before: [0, 2, 3, 2]
3 1 3 1
After:  [0, 1, 3, 2]

Before: [3, 2, 0, 1]
0 0 0 3
After:  [3, 2, 0, 9]

Before: [2, 0, 1, 3]
15 0 3 2
After:  [2, 0, 3, 3]

Before: [3, 1, 1, 2]
6 2 0 3
After:  [3, 1, 1, 3]

Before: [0, 0, 3, 1]
7 3 1 2
After:  [0, 0, 1, 1]

Before: [2, 2, 3, 3]
15 1 3 0
After:  [3, 2, 3, 3]

Before: [0, 0, 1, 1]
7 2 1 3
After:  [0, 0, 1, 1]

Before: [0, 1, 3, 2]
12 1 2 2
After:  [0, 1, 3, 2]

Before: [0, 1, 3, 3]
0 2 2 2
After:  [0, 1, 9, 3]

Before: [0, 0, 2, 3]
10 0 1 3
After:  [0, 0, 2, 1]

Before: [1, 3, 1, 1]
6 0 1 3
After:  [1, 3, 1, 3]

Before: [1, 0, 1, 2]
10 1 2 1
After:  [1, 1, 1, 2]

Before: [0, 1, 0, 2]
14 3 1 0
After:  [3, 1, 0, 2]

Before: [0, 1, 3, 2]
9 0 0 2
After:  [0, 1, 0, 2]

Before: [1, 0, 1, 2]
1 1 0 0
After:  [1, 0, 1, 2]

Before: [3, 0, 2, 1]
7 3 1 0
After:  [1, 0, 2, 1]

Before: [2, 2, 1, 3]
5 2 3 2
After:  [2, 2, 3, 3]

Before: [1, 3, 0, 3]
5 0 3 2
After:  [1, 3, 3, 3]

Before: [0, 1, 3, 1]
12 1 2 2
After:  [0, 1, 3, 1]

Before: [2, 3, 2, 3]
15 2 3 1
After:  [2, 3, 2, 3]

Before: [2, 1, 1, 3]
11 0 3 2
After:  [2, 1, 0, 3]

Before: [2, 2, 0, 2]
3 1 3 3
After:  [2, 2, 0, 1]

Before: [2, 3, 2, 3]
15 0 3 2
After:  [2, 3, 3, 3]

Before: [3, 2, 1, 3]
5 2 3 1
After:  [3, 3, 1, 3]

Before: [1, 0, 1, 3]
5 2 3 2
After:  [1, 0, 3, 3]

Before: [0, 1, 3, 1]
2 1 0 2
After:  [0, 1, 1, 1]

Before: [1, 0, 3, 2]
7 0 1 3
After:  [1, 0, 3, 1]

Before: [1, 2, 2, 2]
3 1 3 1
After:  [1, 1, 2, 2]

Before: [2, 3, 0, 3]
4 1 0 0
After:  [1, 3, 0, 3]

Before: [3, 3, 1, 1]
6 2 0 2
After:  [3, 3, 3, 1]

Before: [2, 3, 3, 1]
0 0 2 3
After:  [2, 3, 3, 6]

Before: [1, 1, 2, 1]
14 3 2 0
After:  [3, 1, 2, 1]

Before: [1, 3, 1, 3]
11 0 3 0
After:  [0, 3, 1, 3]

Before: [2, 2, 0, 3]
15 0 3 1
After:  [2, 3, 0, 3]

Before: [1, 2, 2, 0]
10 1 0 1
After:  [1, 1, 2, 0]

Before: [1, 0, 1, 0]
10 1 2 1
After:  [1, 1, 1, 0]

Before: [1, 2, 0, 3]
10 1 0 2
After:  [1, 2, 1, 3]

Before: [0, 1, 1, 1]
2 1 0 3
After:  [0, 1, 1, 1]

Before: [2, 0, 1, 0]
7 2 1 2
After:  [2, 0, 1, 0]

Before: [0, 3, 1, 3]
6 2 1 1
After:  [0, 3, 1, 3]

Before: [3, 1, 3, 3]
5 1 3 1
After:  [3, 3, 3, 3]

Before: [0, 3, 3, 1]
0 1 2 2
After:  [0, 3, 9, 1]

Before: [2, 3, 2, 2]
8 3 2 0
After:  [4, 3, 2, 2]

Before: [2, 3, 1, 2]
4 1 0 3
After:  [2, 3, 1, 1]

Before: [1, 0, 3, 2]
12 0 2 0
After:  [3, 0, 3, 2]

Before: [2, 1, 2, 2]
8 2 1 0
After:  [3, 1, 2, 2]

Before: [0, 0, 0, 0]
10 0 1 3
After:  [0, 0, 0, 1]

Before: [1, 3, 0, 3]
11 0 3 2
After:  [1, 3, 0, 3]

Before: [2, 0, 3, 1]
7 3 1 1
After:  [2, 1, 3, 1]

Before: [0, 0, 3, 0]
10 0 1 2
After:  [0, 0, 1, 0]

Before: [2, 3, 1, 3]
4 1 0 0
After:  [1, 3, 1, 3]

Before: [3, 3, 2, 0]
13 1 0 3
After:  [3, 3, 2, 1]

Before: [1, 2, 2, 2]
10 1 0 1
After:  [1, 1, 2, 2]

Before: [3, 1, 3, 3]
12 1 2 1
After:  [3, 3, 3, 3]

Before: [3, 3, 2, 1]
14 3 2 0
After:  [3, 3, 2, 1]

Before: [2, 3, 2, 1]
4 1 2 1
After:  [2, 1, 2, 1]

Before: [0, 2, 2, 3]
15 2 3 3
After:  [0, 2, 2, 3]

Before: [3, 2, 3, 1]
0 2 0 1
After:  [3, 9, 3, 1]

Before: [0, 2, 0, 2]
3 1 3 3
After:  [0, 2, 0, 1]

Before: [3, 2, 3, 0]
0 2 2 3
After:  [3, 2, 3, 9]

Before: [0, 2, 1, 3]
9 0 0 1
After:  [0, 0, 1, 3]

Before: [0, 0, 0, 2]
9 0 0 1
After:  [0, 0, 0, 2]

Before: [1, 0, 3, 1]
1 1 0 1
After:  [1, 1, 3, 1]

Before: [1, 0, 1, 1]
7 3 1 3
After:  [1, 0, 1, 1]

Before: [0, 3, 3, 2]
9 0 0 0
After:  [0, 3, 3, 2]

Before: [1, 0, 1, 1]
1 1 0 2
After:  [1, 0, 1, 1]

Before: [3, 2, 1, 3]
6 2 0 0
After:  [3, 2, 1, 3]

Before: [2, 3, 2, 0]
4 1 2 0
After:  [1, 3, 2, 0]

Before: [1, 0, 2, 2]
1 1 0 1
After:  [1, 1, 2, 2]

Before: [1, 2, 1, 3]
11 0 3 1
After:  [1, 0, 1, 3]

Before: [0, 0, 2, 1]
7 3 1 2
After:  [0, 0, 1, 1]

Before: [1, 3, 1, 0]
6 2 1 1
After:  [1, 3, 1, 0]

Before: [1, 0, 1, 3]
1 1 0 0
After:  [1, 0, 1, 3]

Before: [3, 2, 2, 3]
15 2 3 0
After:  [3, 2, 2, 3]

Before: [1, 0, 1, 3]
11 0 3 1
After:  [1, 0, 1, 3]

Before: [3, 2, 1, 1]
13 1 1 2
After:  [3, 2, 1, 1]

Before: [1, 3, 0, 3]
5 0 3 1
After:  [1, 3, 0, 3]

Before: [2, 2, 2, 3]
8 0 2 1
After:  [2, 4, 2, 3]

Before: [0, 0, 3, 0]
9 0 0 3
After:  [0, 0, 3, 0]

Before: [1, 0, 2, 2]
1 1 0 3
After:  [1, 0, 2, 1]

Before: [0, 0, 3, 2]
10 0 1 3
After:  [0, 0, 3, 1]

Before: [0, 0, 0, 1]
10 1 3 1
After:  [0, 1, 0, 1]

Before: [0, 3, 3, 2]
0 3 1 2
After:  [0, 3, 6, 2]

Before: [2, 1, 3, 3]
12 1 2 1
After:  [2, 3, 3, 3]

Before: [0, 0, 2, 0]
8 0 2 1
After:  [0, 2, 2, 0]

Before: [3, 1, 1, 2]
14 3 1 3
After:  [3, 1, 1, 3]

Before: [0, 3, 2, 1]
4 1 2 2
After:  [0, 3, 1, 1]

Before: [3, 0, 1, 3]
5 2 3 0
After:  [3, 0, 1, 3]

Before: [1, 0, 3, 2]
0 3 2 2
After:  [1, 0, 6, 2]

Before: [2, 1, 3, 3]
11 0 3 3
After:  [2, 1, 3, 0]

Before: [1, 0, 0, 2]
1 1 0 3
After:  [1, 0, 0, 1]

Before: [3, 0, 1, 1]
7 3 1 0
After:  [1, 0, 1, 1]

Before: [2, 1, 2, 3]
5 1 3 3
After:  [2, 1, 2, 3]

Before: [1, 2, 0, 1]
10 1 0 3
After:  [1, 2, 0, 1]

Before: [2, 1, 0, 3]
15 0 3 0
After:  [3, 1, 0, 3]

Before: [1, 3, 3, 1]
12 0 2 3
After:  [1, 3, 3, 3]

Before: [2, 2, 3, 2]
3 1 3 1
After:  [2, 1, 3, 2]

Before: [2, 3, 3, 2]
4 1 0 1
After:  [2, 1, 3, 2]

Before: [3, 0, 1, 0]
7 2 1 1
After:  [3, 1, 1, 0]

Before: [1, 1, 0, 2]
14 3 1 2
After:  [1, 1, 3, 2]

Before: [2, 3, 1, 2]
6 2 1 3
After:  [2, 3, 1, 3]

Before: [2, 0, 0, 1]
10 1 3 2
After:  [2, 0, 1, 1]

Before: [1, 3, 1, 3]
5 0 3 0
After:  [3, 3, 1, 3]

Before: [0, 0, 1, 0]
7 2 1 2
After:  [0, 0, 1, 0]

Before: [1, 2, 1, 3]
11 0 3 2
After:  [1, 2, 0, 3]

Before: [2, 3, 0, 0]
4 1 0 3
After:  [2, 3, 0, 1]

Before: [1, 3, 1, 1]
6 2 1 0
After:  [3, 3, 1, 1]

Before: [0, 2, 2, 2]
3 1 3 2
After:  [0, 2, 1, 2]

Before: [3, 0, 3, 1]
10 1 3 3
After:  [3, 0, 3, 1]

Before: [2, 2, 1, 2]
13 1 1 1
After:  [2, 1, 1, 2]

Before: [0, 1, 3, 0]
9 0 0 3
After:  [0, 1, 3, 0]

Before: [2, 3, 0, 3]
4 1 0 3
After:  [2, 3, 0, 1]

Before: [0, 3, 2, 2]
4 1 2 2
After:  [0, 3, 1, 2]

Before: [2, 3, 3, 0]
4 1 0 0
After:  [1, 3, 3, 0]

Before: [0, 2, 3, 3]
15 1 3 1
After:  [0, 3, 3, 3]

Before: [0, 0, 2, 2]
8 0 2 3
After:  [0, 0, 2, 2]

Before: [1, 2, 2, 3]
11 0 3 0
After:  [0, 2, 2, 3]

Before: [0, 1, 0, 3]
2 1 0 3
After:  [0, 1, 0, 1]

Before: [3, 2, 3, 2]
3 1 3 0
After:  [1, 2, 3, 2]

Before: [3, 3, 1, 0]
0 0 0 2
After:  [3, 3, 9, 0]

Before: [1, 0, 0, 3]
7 0 1 1
After:  [1, 1, 0, 3]

Before: [0, 0, 0, 1]
7 3 1 1
After:  [0, 1, 0, 1]

Before: [1, 0, 0, 3]
1 1 0 1
After:  [1, 1, 0, 3]

Before: [1, 0, 2, 1]
14 3 2 2
After:  [1, 0, 3, 1]

Before: [1, 3, 2, 1]
14 3 2 2
After:  [1, 3, 3, 1]

Before: [2, 3, 3, 2]
0 2 2 3
After:  [2, 3, 3, 9]

Before: [0, 1, 2, 1]
2 1 0 2
After:  [0, 1, 1, 1]

Before: [1, 0, 3, 1]
1 1 0 3
After:  [1, 0, 3, 1]

Before: [3, 0, 3, 0]
0 2 2 2
After:  [3, 0, 9, 0]

Before: [0, 1, 2, 0]
2 1 0 3
After:  [0, 1, 2, 1]

Before: [2, 2, 3, 3]
11 0 3 0
After:  [0, 2, 3, 3]

Before: [0, 1, 0, 0]
2 1 0 1
After:  [0, 1, 0, 0]

Before: [0, 1, 0, 3]
2 1 0 0
After:  [1, 1, 0, 3]

Before: [3, 0, 2, 3]
15 2 3 2
After:  [3, 0, 3, 3]

Before: [0, 3, 1, 3]
9 0 0 1
After:  [0, 0, 1, 3]

Before: [3, 3, 2, 2]
0 2 0 3
After:  [3, 3, 2, 6]

Before: [1, 0, 2, 3]
1 1 0 3
After:  [1, 0, 2, 1]

Before: [1, 3, 3, 0]
12 0 2 2
After:  [1, 3, 3, 0]

Before: [3, 1, 3, 1]
12 1 2 3
After:  [3, 1, 3, 3]

Before: [2, 0, 1, 1]
7 3 1 0
After:  [1, 0, 1, 1]

Before: [0, 2, 0, 2]
3 1 3 1
After:  [0, 1, 0, 2]

Before: [1, 2, 1, 2]
8 0 3 3
After:  [1, 2, 1, 3]

Before: [3, 1, 1, 3]
6 1 0 2
After:  [3, 1, 3, 3]

Before: [1, 1, 3, 3]
5 0 3 1
After:  [1, 3, 3, 3]

Before: [0, 1, 3, 0]
2 1 0 1
After:  [0, 1, 3, 0]

Before: [0, 1, 2, 3]
2 1 0 2
After:  [0, 1, 1, 3]

Before: [0, 2, 0, 2]
13 1 1 3
After:  [0, 2, 0, 1]

Before: [1, 0, 1, 3]
1 1 0 2
After:  [1, 0, 1, 3]

Before: [1, 1, 0, 3]
5 0 3 3
After:  [1, 1, 0, 3]

Before: [1, 2, 3, 1]
14 3 2 1
After:  [1, 3, 3, 1]

Before: [2, 3, 2, 3]
15 2 3 2
After:  [2, 3, 3, 3]

Before: [1, 1, 2, 2]
8 2 1 1
After:  [1, 3, 2, 2]

Before: [1, 2, 1, 2]
3 1 3 2
After:  [1, 2, 1, 2]

Before: [0, 0, 1, 3]
5 2 3 2
After:  [0, 0, 3, 3]

Before: [2, 3, 0, 1]
4 1 0 2
After:  [2, 3, 1, 1]

Before: [0, 1, 3, 0]
9 0 0 2
After:  [0, 1, 0, 0]

Before: [3, 0, 0, 1]
7 3 1 0
After:  [1, 0, 0, 1]

Before: [1, 1, 3, 2]
12 1 2 1
After:  [1, 3, 3, 2]

Before: [1, 2, 3, 2]
3 1 3 3
After:  [1, 2, 3, 1]

Before: [2, 0, 1, 2]
10 1 2 3
After:  [2, 0, 1, 1]

Before: [3, 1, 3, 1]
6 1 0 2
After:  [3, 1, 3, 1]

Before: [3, 2, 2, 3]
13 1 1 2
After:  [3, 2, 1, 3]

Before: [1, 2, 0, 2]
3 1 3 3
After:  [1, 2, 0, 1]

Before: [0, 1, 0, 1]
2 1 0 3
After:  [0, 1, 0, 1]

Before: [3, 1, 1, 1]
6 1 0 3
After:  [3, 1, 1, 3]

Before: [3, 0, 3, 0]
0 2 0 3
After:  [3, 0, 3, 9]

Before: [1, 0, 1, 2]
1 1 0 2
After:  [1, 0, 1, 2]

Before: [0, 1, 2, 1]
8 2 1 1
After:  [0, 3, 2, 1]

Before: [3, 0, 2, 1]
7 3 1 2
After:  [3, 0, 1, 1]

Before: [0, 1, 1, 3]
2 1 0 1
After:  [0, 1, 1, 3]

Before: [1, 1, 2, 2]
8 1 2 2
After:  [1, 1, 3, 2]

Before: [3, 1, 3, 3]
6 1 0 0
After:  [3, 1, 3, 3]

Before: [1, 0, 3, 1]
12 0 2 3
After:  [1, 0, 3, 3]

Before: [1, 3, 3, 2]
6 0 1 1
After:  [1, 3, 3, 2]

Before: [0, 0, 3, 1]
10 1 3 1
After:  [0, 1, 3, 1]

Before: [3, 2, 3, 2]
3 1 3 1
After:  [3, 1, 3, 2]

Before: [3, 3, 1, 2]
6 2 0 2
After:  [3, 3, 3, 2]

Before: [0, 1, 0, 2]
2 1 0 2
After:  [0, 1, 1, 2]

Before: [2, 1, 2, 3]
8 0 1 1
After:  [2, 3, 2, 3]

Before: [3, 3, 1, 0]
6 2 0 3
After:  [3, 3, 1, 3]

Before: [1, 3, 3, 2]
13 1 2 1
After:  [1, 1, 3, 2]

Before: [0, 0, 2, 3]
15 2 3 0
After:  [3, 0, 2, 3]

Before: [0, 1, 1, 1]
2 1 0 2
After:  [0, 1, 1, 1]

Before: [0, 0, 0, 2]
10 0 1 2
After:  [0, 0, 1, 2]

Before: [0, 1, 1, 0]
2 1 0 1
After:  [0, 1, 1, 0]

Before: [0, 0, 2, 2]
8 3 2 2
After:  [0, 0, 4, 2]

Before: [2, 3, 1, 1]
4 1 0 3
After:  [2, 3, 1, 1]

Before: [1, 0, 0, 0]
1 1 0 3
After:  [1, 0, 0, 1]

Before: [1, 0, 3, 3]
7 0 1 2
After:  [1, 0, 1, 3]

Before: [1, 0, 3, 2]
1 1 0 1
After:  [1, 1, 3, 2]

Before: [0, 1, 1, 0]
9 0 0 0
After:  [0, 1, 1, 0]

Before: [3, 0, 3, 1]
14 3 2 2
After:  [3, 0, 3, 1]

Before: [2, 2, 2, 3]
15 1 3 1
After:  [2, 3, 2, 3]

Before: [0, 3, 3, 0]
9 0 0 0
After:  [0, 3, 3, 0]

Before: [0, 1, 3, 3]
2 1 0 3
After:  [0, 1, 3, 1]

Before: [1, 2, 2, 3]
15 2 3 2
After:  [1, 2, 3, 3]

Before: [3, 2, 2, 2]
0 3 0 2
After:  [3, 2, 6, 2]

Before: [0, 2, 3, 3]
13 1 1 3
After:  [0, 2, 3, 1]

Before: [0, 3, 2, 3]
4 1 2 1
After:  [0, 1, 2, 3]

Before: [0, 0, 3, 1]
10 0 1 3
After:  [0, 0, 3, 1]

Before: [2, 0, 2, 3]
15 0 3 2
After:  [2, 0, 3, 3]

Before: [1, 1, 3, 2]
12 1 2 3
After:  [1, 1, 3, 3]

Before: [1, 0, 2, 1]
7 0 1 3
After:  [1, 0, 2, 1]

Before: [0, 1, 3, 0]
0 2 2 3
After:  [0, 1, 3, 9]

Before: [2, 2, 2, 1]
14 3 2 2
After:  [2, 2, 3, 1]

Before: [0, 1, 0, 1]
2 1 0 0
After:  [1, 1, 0, 1]

Before: [0, 0, 2, 3]
15 2 3 1
After:  [0, 3, 2, 3]

Before: [1, 3, 0, 1]
6 0 1 2
After:  [1, 3, 3, 1]

Before: [1, 2, 2, 3]
10 1 0 3
After:  [1, 2, 2, 1]

Before: [0, 2, 3, 3]
13 1 1 2
After:  [0, 2, 1, 3]

Before: [0, 0, 0, 1]
10 1 3 0
After:  [1, 0, 0, 1]

Before: [2, 2, 3, 2]
3 1 3 0
After:  [1, 2, 3, 2]

Before: [0, 1, 2, 2]
14 3 1 1
After:  [0, 3, 2, 2]

Before: [0, 1, 3, 3]
2 1 0 1
After:  [0, 1, 3, 3]

Before: [3, 3, 3, 3]
0 2 0 0
After:  [9, 3, 3, 3]

Before: [1, 3, 2, 2]
8 0 3 1
After:  [1, 3, 2, 2]

Before: [2, 2, 0, 3]
15 1 3 2
After:  [2, 2, 3, 3]

Before: [1, 1, 2, 3]
5 0 3 0
After:  [3, 1, 2, 3]

Before: [2, 3, 3, 3]
11 0 3 3
After:  [2, 3, 3, 0]

Before: [2, 3, 2, 3]
4 1 0 1
After:  [2, 1, 2, 3]

Before: [2, 0, 0, 3]
11 0 3 1
After:  [2, 0, 0, 3]

Before: [3, 3, 1, 3]
5 2 3 1
After:  [3, 3, 1, 3]

Before: [1, 0, 3, 0]
12 0 2 2
After:  [1, 0, 3, 0]

Before: [1, 1, 3, 3]
5 1 3 2
After:  [1, 1, 3, 3]

Before: [1, 2, 0, 2]
3 1 3 1
After:  [1, 1, 0, 2]

Before: [2, 2, 3, 2]
3 1 3 2
After:  [2, 2, 1, 2]

Before: [3, 1, 2, 1]
6 1 0 1
After:  [3, 3, 2, 1]

Before: [0, 1, 3, 0]
2 1 0 0
After:  [1, 1, 3, 0]

Before: [1, 0, 1, 3]
8 1 3 2
After:  [1, 0, 3, 3]

Before: [1, 1, 2, 3]
11 0 3 2
After:  [1, 1, 0, 3]

Before: [0, 3, 2, 3]
9 0 0 0
After:  [0, 3, 2, 3]

Before: [3, 2, 2, 0]
13 1 1 0
After:  [1, 2, 2, 0]

Before: [1, 0, 0, 1]
1 1 0 1
After:  [1, 1, 0, 1]

Before: [2, 0, 0, 3]
15 0 3 0
After:  [3, 0, 0, 3]

Before: [3, 2, 0, 2]
3 1 3 3
After:  [3, 2, 0, 1]

Before: [1, 0, 1, 3]
5 2 3 1
After:  [1, 3, 1, 3]

Before: [2, 3, 3, 1]
4 1 0 1
After:  [2, 1, 3, 1]

Before: [2, 2, 1, 3]
5 2 3 1
After:  [2, 3, 1, 3]

Before: [0, 1, 0, 0]
9 0 0 2
After:  [0, 1, 0, 0]

Before: [0, 1, 0, 1]
2 1 0 2
After:  [0, 1, 1, 1]

Before: [0, 1, 0, 2]
2 1 0 3
After:  [0, 1, 0, 1]

Before: [1, 2, 2, 2]
13 1 1 1
After:  [1, 1, 2, 2]

Before: [1, 2, 1, 2]
3 1 3 3
After:  [1, 2, 1, 1]

Before: [1, 0, 2, 3]
11 0 3 1
After:  [1, 0, 2, 3]

Before: [0, 2, 0, 3]
15 1 3 0
After:  [3, 2, 0, 3]

Before: [1, 2, 3, 3]
15 1 3 2
After:  [1, 2, 3, 3]

Before: [0, 0, 1, 1]
10 1 2 2
After:  [0, 0, 1, 1]

Before: [1, 3, 1, 3]
5 2 3 3
After:  [1, 3, 1, 3]

Before: [1, 3, 1, 3]
6 0 1 2
After:  [1, 3, 3, 3]

Before: [0, 1, 2, 2]
2 1 0 0
After:  [1, 1, 2, 2]

Before: [2, 2, 2, 2]
3 1 3 0
After:  [1, 2, 2, 2]

Before: [0, 1, 3, 2]
2 1 0 3
After:  [0, 1, 3, 1]

Before: [2, 2, 3, 1]
13 1 0 1
After:  [2, 1, 3, 1]

Before: [2, 0, 2, 1]
7 3 1 0
After:  [1, 0, 2, 1]

Before: [1, 0, 3, 3]
12 0 2 0
After:  [3, 0, 3, 3]

Before: [0, 0, 3, 3]
10 0 1 3
After:  [0, 0, 3, 1]

Before: [0, 2, 0, 2]
9 0 0 0
After:  [0, 2, 0, 2]

Before: [1, 2, 0, 3]
11 0 3 0
After:  [0, 2, 0, 3]

Before: [2, 0, 0, 3]
11 0 3 0
After:  [0, 0, 0, 3]

Before: [0, 2, 0, 2]
3 1 3 0
After:  [1, 2, 0, 2]

Before: [1, 3, 1, 3]
6 0 1 1
After:  [1, 3, 1, 3]

Before: [0, 1, 3, 2]
2 1 0 2
After:  [0, 1, 1, 2]

Before: [1, 0, 3, 1]
1 1 0 2
After:  [1, 0, 1, 1]

Before: [1, 0, 2, 0]
7 0 1 1
After:  [1, 1, 2, 0]

Before: [2, 3, 1, 3]
15 0 3 3
After:  [2, 3, 1, 3]

Before: [1, 2, 0, 3]
11 0 3 1
After:  [1, 0, 0, 3]

Before: [1, 3, 0, 1]
6 0 1 0
After:  [3, 3, 0, 1]

Before: [2, 2, 1, 2]
3 1 3 2
After:  [2, 2, 1, 2]

Before: [1, 0, 3, 3]
1 1 0 2
After:  [1, 0, 1, 3]

Before: [3, 1, 0, 3]
5 1 3 2
After:  [3, 1, 3, 3]

Before: [0, 1, 2, 3]
8 2 1 1
After:  [0, 3, 2, 3]

Before: [0, 2, 2, 2]
3 1 3 1
After:  [0, 1, 2, 2]

Before: [1, 1, 2, 2]
0 0 3 1
After:  [1, 2, 2, 2]

Before: [2, 3, 1, 3]
11 0 3 1
After:  [2, 0, 1, 3]

Before: [3, 3, 2, 3]
4 1 2 0
After:  [1, 3, 2, 3]

Before: [3, 1, 3, 3]
5 1 3 2
After:  [3, 1, 3, 3]

Before: [2, 2, 1, 0]
13 1 1 1
After:  [2, 1, 1, 0]

Before: [0, 1, 3, 2]
2 1 0 0
After:  [1, 1, 3, 2]

Before: [3, 2, 0, 3]
15 1 3 0
After:  [3, 2, 0, 3]

Before: [2, 3, 0, 2]
0 1 0 0
After:  [6, 3, 0, 2]

Before: [2, 3, 0, 2]
4 1 0 1
After:  [2, 1, 0, 2]

Before: [1, 0, 1, 2]
1 1 0 3
After:  [1, 0, 1, 1]

Before: [2, 3, 3, 2]
0 3 2 1
After:  [2, 6, 3, 2]

Before: [0, 1, 3, 1]
2 1 0 3
After:  [0, 1, 3, 1]

Before: [2, 0, 0, 3]
15 0 3 3
After:  [2, 0, 0, 3]

Before: [2, 1, 3, 3]
5 1 3 3
After:  [2, 1, 3, 3]

Before: [3, 1, 3, 2]
12 1 2 3
After:  [3, 1, 3, 3]

Before: [0, 2, 1, 2]
3 1 3 1
After:  [0, 1, 1, 2]

Before: [0, 1, 0, 0]
2 1 0 3
After:  [0, 1, 0, 1]

Before: [0, 2, 3, 1]
14 3 2 0
After:  [3, 2, 3, 1]

Before: [3, 2, 2, 1]
13 1 1 1
After:  [3, 1, 2, 1]

Before: [3, 3, 1, 3]
6 2 0 3
After:  [3, 3, 1, 3]

Before: [3, 0, 3, 1]
14 3 2 3
After:  [3, 0, 3, 3]

Before: [2, 3, 2, 3]
11 0 3 0
After:  [0, 3, 2, 3]

Before: [2, 0, 1, 3]
5 2 3 2
After:  [2, 0, 3, 3]

Before: [1, 3, 1, 3]
11 0 3 1
After:  [1, 0, 1, 3]

Before: [1, 0, 1, 1]
7 3 1 1
After:  [1, 1, 1, 1]

Before: [1, 2, 2, 1]
14 3 2 0
After:  [3, 2, 2, 1]

Before: [1, 0, 2, 3]
8 1 2 1
After:  [1, 2, 2, 3]

Before: [1, 0, 1, 0]
7 2 1 0
After:  [1, 0, 1, 0]

Before: [2, 2, 1, 0]
13 1 1 2
After:  [2, 2, 1, 0]

Before: [1, 0, 1, 2]
7 2 1 2
After:  [1, 0, 1, 2]

Before: [2, 2, 2, 2]
3 1 3 2
After:  [2, 2, 1, 2]

Before: [2, 1, 0, 3]
11 0 3 1
After:  [2, 0, 0, 3]

Before: [2, 1, 2, 3]
11 0 3 1
After:  [2, 0, 2, 3]

Before: [0, 0, 1, 1]
7 3 1 1
After:  [0, 1, 1, 1]

Before: [1, 1, 0, 2]
14 3 1 1
After:  [1, 3, 0, 2]

Before: [1, 0, 1, 0]
7 0 1 3
After:  [1, 0, 1, 1]

Before: [0, 1, 2, 2]
8 3 2 1
After:  [0, 4, 2, 2]

Before: [1, 3, 0, 2]
6 0 1 0
After:  [3, 3, 0, 2]

Before: [1, 0, 1, 2]
7 0 1 0
After:  [1, 0, 1, 2]

Before: [3, 0, 3, 1]
7 3 1 2
After:  [3, 0, 1, 1]

Before: [0, 2, 0, 0]
9 0 0 0
After:  [0, 2, 0, 0]

Before: [1, 1, 2, 3]
8 1 2 2
After:  [1, 1, 3, 3]

Before: [0, 1, 2, 1]
2 1 0 1
After:  [0, 1, 2, 1]

Before: [1, 3, 3, 3]
11 0 3 1
After:  [1, 0, 3, 3]

Before: [3, 3, 1, 0]
6 2 0 0
After:  [3, 3, 1, 0]

Before: [2, 2, 0, 3]
11 0 3 3
After:  [2, 2, 0, 0]

Before: [3, 0, 1, 0]
7 2 1 0
After:  [1, 0, 1, 0]

Before: [1, 0, 3, 3]
1 1 0 0
After:  [1, 0, 3, 3]

Before: [1, 3, 3, 1]
14 3 2 3
After:  [1, 3, 3, 3]

Before: [2, 2, 0, 0]
13 1 0 1
After:  [2, 1, 0, 0]

Before: [2, 2, 2, 3]
15 2 3 0
After:  [3, 2, 2, 3]

Before: [3, 3, 0, 3]
0 0 0 3
After:  [3, 3, 0, 9]

Before: [2, 2, 1, 3]
15 1 3 0
After:  [3, 2, 1, 3]

Before: [2, 1, 3, 2]
0 2 0 3
After:  [2, 1, 3, 6]

Before: [0, 1, 1, 3]
2 1 0 2
After:  [0, 1, 1, 3]

Before: [2, 0, 1, 1]
7 2 1 0
After:  [1, 0, 1, 1]

Before: [1, 0, 2, 3]
8 1 3 2
After:  [1, 0, 3, 3]

Before: [0, 1, 0, 3]
2 1 0 1
After:  [0, 1, 0, 3]

Before: [0, 1, 2, 2]
2 1 0 3
After:  [0, 1, 2, 1]

Before: [1, 0, 1, 3]
1 1 0 3
After:  [1, 0, 1, 1]

Before: [2, 3, 1, 3]
4 1 0 3
After:  [2, 3, 1, 1]

Before: [2, 3, 2, 1]
4 1 0 3
After:  [2, 3, 2, 1]

Before: [1, 1, 1, 2]
0 0 3 0
After:  [2, 1, 1, 2]

Before: [0, 0, 0, 1]
9 0 0 0
After:  [0, 0, 0, 1]

Before: [1, 0, 3, 3]
5 0 3 1
After:  [1, 3, 3, 3]

Before: [0, 1, 1, 0]
2 1 0 3
After:  [0, 1, 1, 1]

Before: [1, 2, 1, 3]
10 1 0 3
After:  [1, 2, 1, 1]

Before: [0, 2, 0, 2]
3 1 3 2
After:  [0, 2, 1, 2]

Before: [2, 2, 1, 2]
3 1 3 3
After:  [2, 2, 1, 1]

Before: [2, 1, 3, 2]
12 1 2 3
After:  [2, 1, 3, 3]

Before: [2, 1, 2, 3]
15 2 3 3
After:  [2, 1, 2, 3]

Before: [0, 1, 2, 2]
9 0 0 2
After:  [0, 1, 0, 2]

Before: [0, 2, 2, 2]
8 0 2 0
After:  [2, 2, 2, 2]

Before: [0, 3, 2, 3]
4 1 2 0
After:  [1, 3, 2, 3]

Before: [1, 1, 3, 2]
8 0 3 0
After:  [3, 1, 3, 2]

Before: [1, 1, 3, 1]
12 1 2 1
After:  [1, 3, 3, 1]

Before: [2, 1, 1, 3]
5 1 3 3
After:  [2, 1, 1, 3]

Before: [3, 1, 1, 2]
6 1 0 1
After:  [3, 3, 1, 2]

Before: [1, 2, 2, 3]
15 2 3 0
After:  [3, 2, 2, 3]

Before: [3, 1, 3, 2]
6 1 0 1
After:  [3, 3, 3, 2]

Before: [2, 2, 0, 2]
3 1 3 1
After:  [2, 1, 0, 2]

Before: [3, 0, 1, 3]
5 2 3 3
After:  [3, 0, 1, 3]

Before: [3, 3, 1, 2]
8 2 3 2
After:  [3, 3, 3, 2]

Before: [2, 1, 2, 0]
8 3 2 2
After:  [2, 1, 2, 0]

Before: [1, 2, 3, 0]
12 0 2 2
After:  [1, 2, 3, 0]

Before: [3, 2, 0, 2]
3 1 3 1
After:  [3, 1, 0, 2]

Before: [1, 2, 1, 3]
5 0 3 2
After:  [1, 2, 3, 3]

Before: [0, 1, 0, 3]
9 0 0 0
After:  [0, 1, 0, 3]

Before: [1, 2, 3, 3]
10 1 0 2
After:  [1, 2, 1, 3]

Before: [2, 2, 1, 1]
13 1 0 3
After:  [2, 2, 1, 1]

Before: [2, 0, 2, 3]
15 2 3 0
After:  [3, 0, 2, 3]

Before: [2, 0, 0, 1]
10 1 3 1
After:  [2, 1, 0, 1]

Before: [1, 0, 2, 1]
1 1 0 1
After:  [1, 1, 2, 1]

Before: [3, 0, 1, 3]
10 1 2 3
After:  [3, 0, 1, 1]

Before: [1, 1, 3, 3]
5 1 3 1
After:  [1, 3, 3, 3]

Before: [1, 1, 2, 3]
5 0 3 3
After:  [1, 1, 2, 3]

Before: [3, 0, 1, 0]
6 2 0 3
After:  [3, 0, 1, 3]

Before: [1, 2, 0, 0]
10 1 0 3
After:  [1, 2, 0, 1]

Before: [0, 1, 0, 2]
2 1 0 0
After:  [1, 1, 0, 2]

Before: [0, 1, 2, 0]
9 0 0 1
After:  [0, 0, 2, 0]

Before: [1, 1, 0, 3]
8 2 3 1
After:  [1, 3, 0, 3]

Before: [2, 3, 1, 3]
4 1 0 1
After:  [2, 1, 1, 3]

Before: [0, 1, 3, 3]
9 0 0 3
After:  [0, 1, 3, 0]

Before: [0, 0, 1, 3]
10 0 1 0
After:  [1, 0, 1, 3]

Before: [2, 0, 1, 1]
10 1 3 3
After:  [2, 0, 1, 1]

Before: [3, 3, 0, 0]
0 0 1 1
After:  [3, 9, 0, 0]

Before: [1, 3, 2, 0]
4 1 2 0
After:  [1, 3, 2, 0]

Before: [0, 1, 1, 3]
9 0 0 0
After:  [0, 1, 1, 3]

Before: [0, 1, 2, 0]
2 1 0 2
After:  [0, 1, 1, 0]

Before: [2, 3, 3, 0]
0 2 1 1
After:  [2, 9, 3, 0]

Before: [0, 0, 1, 2]
10 1 2 3
After:  [0, 0, 1, 1]

Before: [2, 2, 0, 2]
13 1 0 3
After:  [2, 2, 0, 1]

Before: [1, 0, 1, 1]
10 1 2 0
After:  [1, 0, 1, 1]

Before: [3, 3, 2, 2]
13 1 0 1
After:  [3, 1, 2, 2]

Before: [1, 0, 2, 1]
8 0 2 1
After:  [1, 3, 2, 1]

Before: [1, 1, 2, 2]
8 2 2 2
After:  [1, 1, 4, 2]

Before: [0, 0, 1, 3]
5 2 3 3
After:  [0, 0, 1, 3]

Before: [2, 3, 1, 0]
6 2 1 3
After:  [2, 3, 1, 3]

Before: [1, 3, 1, 0]
6 2 1 3
After:  [1, 3, 1, 3]

Before: [1, 0, 2, 3]
7 0 1 2
After:  [1, 0, 1, 3]

Before: [2, 0, 3, 1]
0 3 0 0
After:  [2, 0, 3, 1]

Before: [2, 2, 3, 2]
3 1 3 3
After:  [2, 2, 3, 1]

Before: [0, 1, 0, 3]
2 1 0 2
After:  [0, 1, 1, 3]

Before: [3, 1, 1, 3]
6 1 0 1
After:  [3, 3, 1, 3]

Before: [1, 2, 2, 3]
13 1 1 1
After:  [1, 1, 2, 3]

Before: [2, 2, 1, 3]
15 0 3 2
After:  [2, 2, 3, 3]

Before: [1, 0, 0, 0]
1 1 0 1
After:  [1, 1, 0, 0]

Before: [2, 2, 0, 3]
11 0 3 0
After:  [0, 2, 0, 3]

Before: [1, 0, 3, 2]
1 1 0 0
After:  [1, 0, 3, 2]

Before: [1, 0, 3, 0]
1 1 0 1
After:  [1, 1, 3, 0]

Before: [0, 2, 2, 0]
9 0 0 3
After:  [0, 2, 2, 0]

Before: [0, 3, 3, 3]
0 3 1 0
After:  [9, 3, 3, 3]

Before: [3, 2, 1, 2]
3 1 3 2
After:  [3, 2, 1, 2]

Before: [3, 1, 2, 2]
14 3 1 3
After:  [3, 1, 2, 3]

Before: [3, 1, 3, 1]
12 1 2 1
After:  [3, 3, 3, 1]

Before: [3, 3, 3, 3]
0 3 0 0
After:  [9, 3, 3, 3]

Before: [1, 3, 3, 2]
12 0 2 2
After:  [1, 3, 3, 2]

Before: [2, 0, 1, 3]
11 0 3 1
After:  [2, 0, 1, 3]

Before: [1, 0, 1, 0]
1 1 0 2
After:  [1, 0, 1, 0]

Before: [1, 2, 0, 2]
3 1 3 0
After:  [1, 2, 0, 2]

Before: [1, 0, 1, 3]
11 0 3 2
After:  [1, 0, 0, 3]

Before: [2, 0, 2, 1]
7 3 1 3
After:  [2, 0, 2, 1]

Before: [0, 2, 3, 2]
3 1 3 2
After:  [0, 2, 1, 2]

Before: [3, 1, 2, 1]
14 3 2 3
After:  [3, 1, 2, 3]

Before: [1, 0, 2, 3]
1 1 0 1
After:  [1, 1, 2, 3]

Before: [0, 1, 3, 1]
2 1 0 1
After:  [0, 1, 3, 1]

Before: [1, 0, 2, 0]
1 1 0 3
After:  [1, 0, 2, 1]

Before: [1, 2, 0, 3]
13 1 1 3
After:  [1, 2, 0, 1]

Before: [0, 2, 2, 2]
9 0 0 3
After:  [0, 2, 2, 0]

Before: [0, 2, 0, 1]
13 1 1 3
After:  [0, 2, 0, 1]

Before: [1, 2, 2, 3]
13 1 1 0
After:  [1, 2, 2, 3]

Before: [1, 0, 1, 2]
7 0 1 3
After:  [1, 0, 1, 1]

Before: [2, 3, 2, 3]
15 2 3 3
After:  [2, 3, 2, 3]

Before: [2, 3, 0, 3]
4 1 0 1
After:  [2, 1, 0, 3]

Before: [1, 0, 0, 1]
7 0 1 0
After:  [1, 0, 0, 1]

Before: [0, 1, 3, 2]
12 1 2 3
After:  [0, 1, 3, 3]

Before: [2, 2, 1, 3]
11 0 3 1
After:  [2, 0, 1, 3]

Before: [0, 3, 2, 2]
0 2 1 3
After:  [0, 3, 2, 6]

Before: [3, 0, 3, 1]
14 3 2 1
After:  [3, 3, 3, 1]

Before: [3, 3, 2, 0]
4 1 2 0
After:  [1, 3, 2, 0]

Before: [2, 0, 3, 3]
15 0 3 3
After:  [2, 0, 3, 3]

Before: [1, 0, 2, 0]
1 1 0 0
After:  [1, 0, 2, 0]

Before: [2, 3, 1, 1]
6 2 1 0
After:  [3, 3, 1, 1]

Before: [0, 1, 0, 0]
2 1 0 0
After:  [1, 1, 0, 0]

Before: [0, 2, 1, 2]
9 0 0 2
After:  [0, 2, 0, 2]

Before: [0, 2, 2, 1]
14 3 2 3
After:  [0, 2, 2, 3]

Before: [2, 3, 2, 1]
4 1 2 0
After:  [1, 3, 2, 1]

Before: [3, 3, 0, 3]
8 2 3 1
After:  [3, 3, 0, 3]

Before: [3, 3, 3, 0]
13 1 0 0
After:  [1, 3, 3, 0]

Before: [1, 3, 0, 3]
0 3 1 0
After:  [9, 3, 0, 3]

Before: [1, 0, 1, 0]
1 1 0 3
After:  [1, 0, 1, 1]

Before: [0, 0, 1, 3]
5 2 3 1
After:  [0, 3, 1, 3]

Before: [3, 1, 3, 2]
12 1 2 1
After:  [3, 3, 3, 2]

Before: [1, 3, 2, 1]
6 0 1 3
After:  [1, 3, 2, 3]

Before: [2, 0, 2, 1]
8 0 2 1
After:  [2, 4, 2, 1]

Before: [2, 0, 2, 2]
8 1 2 2
After:  [2, 0, 2, 2]

Before: [0, 0, 1, 1]
7 3 1 2
After:  [0, 0, 1, 1]

Before: [3, 0, 2, 2]
8 1 2 1
After:  [3, 2, 2, 2]

Before: [3, 1, 3, 3]
5 1 3 3
After:  [3, 1, 3, 3]

Before: [0, 1, 0, 2]
9 0 0 0
After:  [0, 1, 0, 2]

Before: [3, 1, 2, 2]
6 1 0 0
After:  [3, 1, 2, 2]

Before: [3, 0, 1, 0]
6 2 0 0
After:  [3, 0, 1, 0]

Before: [0, 1, 1, 1]
9 0 0 2
After:  [0, 1, 0, 1]

Before: [1, 2, 0, 3]
15 1 3 2
After:  [1, 2, 3, 3]

Before: [2, 3, 1, 0]
4 1 0 2
After:  [2, 3, 1, 0]

Before: [2, 1, 2, 2]
14 3 1 1
After:  [2, 3, 2, 2]

Before: [3, 2, 0, 3]
15 1 3 3
After:  [3, 2, 0, 3]

Before: [1, 3, 0, 0]
6 0 1 0
After:  [3, 3, 0, 0]

Before: [0, 1, 1, 3]
2 1 0 0
After:  [1, 1, 1, 3]

Before: [0, 3, 3, 1]
14 3 2 0
After:  [3, 3, 3, 1]

Before: [1, 3, 3, 3]
13 1 2 1
After:  [1, 1, 3, 3]

Before: [0, 3, 2, 0]
4 1 2 1
After:  [0, 1, 2, 0]

Before: [1, 0, 3, 1]
12 0 2 0
After:  [3, 0, 3, 1]

Before: [1, 1, 2, 2]
14 3 1 2
After:  [1, 1, 3, 2]

Before: [2, 1, 1, 3]
5 2 3 2
After:  [2, 1, 3, 3]

Before: [0, 2, 2, 3]
15 1 3 1
After:  [0, 3, 2, 3]

Before: [3, 3, 2, 2]
4 1 2 3
After:  [3, 3, 2, 1]

Before: [0, 1, 3, 1]
9 0 0 2
After:  [0, 1, 0, 1]

Before: [3, 1, 1, 3]
5 2 3 0
After:  [3, 1, 1, 3]

Before: [1, 0, 1, 3]
1 1 0 1
After:  [1, 1, 1, 3]

Before: [1, 0, 0, 3]
1 1 0 2
After:  [1, 0, 1, 3]

Before: [3, 2, 1, 2]
3 1 3 1
After:  [3, 1, 1, 2]

Before: [3, 2, 3, 3]
15 1 3 0
After:  [3, 2, 3, 3]

Before: [1, 2, 3, 3]
0 2 2 2
After:  [1, 2, 9, 3]

Before: [3, 0, 0, 1]
7 3 1 3
After:  [3, 0, 0, 1]

Before: [0, 1, 0, 1]
2 1 0 1
After:  [0, 1, 0, 1]

Before: [2, 1, 1, 3]
5 2 3 0
After:  [3, 1, 1, 3]

Before: [0, 1, 1, 2]
2 1 0 1
After:  [0, 1, 1, 2]

Before: [0, 0, 2, 3]
9 0 0 0
After:  [0, 0, 2, 3]

Before: [0, 2, 1, 2]
8 2 3 3
After:  [0, 2, 1, 3]

Before: [1, 0, 1, 1]
1 1 0 3
After:  [1, 0, 1, 1]

Before: [1, 0, 1, 3]
8 1 3 0
After:  [3, 0, 1, 3]

Before: [3, 1, 3, 2]
14 3 1 0
After:  [3, 1, 3, 2]

Before: [2, 2, 0, 0]
13 1 0 2
After:  [2, 2, 1, 0]

Before: [3, 1, 3, 1]
12 1 2 0
After:  [3, 1, 3, 1]

Before: [0, 3, 3, 0]
13 1 2 1
After:  [0, 1, 3, 0]

Before: [3, 1, 3, 3]
12 1 2 0
After:  [3, 1, 3, 3]

Before: [1, 2, 2, 3]
8 0 2 1
After:  [1, 3, 2, 3]

Before: [3, 0, 1, 0]
7 2 1 3
After:  [3, 0, 1, 1]

Before: [0, 1, 2, 3]
2 1 0 3
After:  [0, 1, 2, 1]

Before: [0, 0, 1, 0]
9 0 0 1
After:  [0, 0, 1, 0]

Before: [3, 2, 3, 1]
13 1 1 1
After:  [3, 1, 3, 1]

Before: [2, 2, 0, 2]
3 1 3 2
After:  [2, 2, 1, 2]

Before: [3, 3, 3, 2]
0 2 0 0
After:  [9, 3, 3, 2]

Before: [0, 0, 2, 3]
10 0 1 1
After:  [0, 1, 2, 3]

Before: [2, 3, 2, 2]
8 0 2 3
After:  [2, 3, 2, 4]

Before: [3, 3, 2, 1]
14 3 2 1
After:  [3, 3, 2, 1]

Before: [0, 0, 1, 1]
9 0 0 1
After:  [0, 0, 1, 1]

Before: [0, 2, 2, 2]
3 1 3 0
After:  [1, 2, 2, 2]

Before: [2, 2, 1, 2]
3 1 3 1
After:  [2, 1, 1, 2]

Before: [2, 1, 2, 3]
11 0 3 2
After:  [2, 1, 0, 3]

Before: [1, 2, 2, 2]
3 1 3 2
After:  [1, 2, 1, 2]

Before: [1, 3, 2, 0]
4 1 2 2
After:  [1, 3, 1, 0]

Before: [1, 1, 3, 3]
12 1 2 2
After:  [1, 1, 3, 3]

Before: [1, 2, 0, 3]
15 1 3 3
After:  [1, 2, 0, 3]

Before: [1, 2, 3, 3]
12 0 2 3
After:  [1, 2, 3, 3]

Before: [0, 2, 1, 2]
3 1 3 2
After:  [0, 2, 1, 2]

Before: [1, 1, 1, 2]
8 1 3 1
After:  [1, 3, 1, 2]

Before: [1, 1, 2, 1]
14 3 2 1
After:  [1, 3, 2, 1]

Before: [1, 0, 1, 1]
1 1 0 0
After:  [1, 0, 1, 1]

Before: [2, 1, 1, 3]
15 0 3 0
After:  [3, 1, 1, 3]

Before: [2, 1, 1, 3]
11 0 3 1
After:  [2, 0, 1, 3]

Before: [2, 3, 1, 3]
11 0 3 0
After:  [0, 3, 1, 3]

Before: [0, 3, 1, 1]
9 0 0 0
After:  [0, 3, 1, 1]

Before: [1, 0, 2, 1]
7 0 1 2
After:  [1, 0, 1, 1]

Before: [1, 0, 0, 0]
1 1 0 2
After:  [1, 0, 1, 0]

Before: [1, 0, 2, 1]
1 1 0 0
After:  [1, 0, 2, 1]

Before: [0, 3, 3, 0]
13 1 2 2
After:  [0, 3, 1, 0]

Before: [3, 2, 0, 2]
0 0 0 2
After:  [3, 2, 9, 2]

Before: [2, 1, 2, 3]
5 1 3 0
After:  [3, 1, 2, 3]

Before: [2, 2, 2, 2]
3 1 3 3
After:  [2, 2, 2, 1]

Before: [1, 3, 2, 3]
5 0 3 1
After:  [1, 3, 2, 3]

Before: [2, 1, 3, 2]
0 1 0 0
After:  [2, 1, 3, 2]

Before: [1, 0, 0, 1]
1 1 0 2
After:  [1, 0, 1, 1]

Before: [3, 3, 3, 0]
0 2 2 0
After:  [9, 3, 3, 0]

Before: [2, 2, 3, 3]
15 0 3 3
After:  [2, 2, 3, 3]

Before: [0, 3, 2, 3]
15 2 3 2
After:  [0, 3, 3, 3]

Before: [1, 2, 0, 2]
13 1 1 1
After:  [1, 1, 0, 2]

Before: [0, 3, 1, 1]
9 0 0 2
After:  [0, 3, 0, 1]

Before: [0, 1, 2, 2]
8 2 2 3
After:  [0, 1, 2, 4]

Before: [0, 0, 2, 1]
9 0 0 1
After:  [0, 0, 2, 1]

Before: [2, 3, 0, 3]
4 1 0 2
After:  [2, 3, 1, 3]

Before: [1, 0, 2, 2]
7 0 1 0
After:  [1, 0, 2, 2]

Before: [3, 1, 3, 3]
0 3 2 0
After:  [9, 1, 3, 3]

Before: [2, 3, 2, 3]
11 0 3 1
After:  [2, 0, 2, 3]

Before: [1, 0, 3, 0]
7 0 1 0
After:  [1, 0, 3, 0]

Before: [1, 3, 2, 3]
15 2 3 0
After:  [3, 3, 2, 3]

Before: [1, 3, 3, 0]
6 0 1 0
After:  [3, 3, 3, 0]

Before: [3, 0, 1, 2]
7 2 1 1
After:  [3, 1, 1, 2]

Before: [0, 3, 1, 1]
6 2 1 1
After:  [0, 3, 1, 1]

Before: [3, 3, 3, 0]
0 2 1 3
After:  [3, 3, 3, 9]

Before: [3, 2, 1, 1]
6 2 0 3
After:  [3, 2, 1, 3]

Before: [1, 0, 3, 0]
12 0 2 0
After:  [3, 0, 3, 0]

Before: [1, 2, 1, 0]
10 1 0 2
After:  [1, 2, 1, 0]

Before: [1, 3, 2, 1]
0 1 1 1
After:  [1, 9, 2, 1]

Before: [2, 3, 1, 3]
11 0 3 2
After:  [2, 3, 0, 3]

Before: [0, 1, 1, 0]
2 1 0 0
After:  [1, 1, 1, 0]

Before: [2, 2, 3, 3]
15 1 3 1
After:  [2, 3, 3, 3]

Before: [2, 3, 0, 1]
0 3 0 1
After:  [2, 2, 0, 1]

Before: [1, 0, 1, 0]
1 1 0 0
After:  [1, 0, 1, 0]

Before: [2, 2, 0, 0]
13 1 1 2
After:  [2, 2, 1, 0]

Before: [2, 0, 3, 1]
14 3 2 0
After:  [3, 0, 3, 1]

Before: [2, 1, 3, 1]
14 3 2 2
After:  [2, 1, 3, 1]

Before: [3, 3, 1, 3]
6 2 1 2
After:  [3, 3, 3, 3]

Before: [1, 2, 1, 2]
3 1 3 1
After:  [1, 1, 1, 2]

Before: [1, 2, 2, 3]
10 1 0 0
After:  [1, 2, 2, 3]

Before: [0, 1, 3, 3]
5 1 3 2
After:  [0, 1, 3, 3]

Before: [2, 1, 2, 1]
14 3 2 3
After:  [2, 1, 2, 3]

Before: [3, 3, 2, 3]
4 1 2 3
After:  [3, 3, 2, 1]

Before: [1, 3, 2, 3]
11 0 3 0
After:  [0, 3, 2, 3]

Before: [1, 2, 0, 2]
0 0 3 1
After:  [1, 2, 0, 2]

Before: [2, 2, 2, 2]
13 1 0 3
After:  [2, 2, 2, 1]

Before: [1, 3, 2, 1]
6 0 1 1
After:  [1, 3, 2, 1]

Before: [1, 3, 2, 1]
14 3 2 0
After:  [3, 3, 2, 1]

Before: [2, 3, 3, 1]
14 3 2 0
After:  [3, 3, 3, 1]

Before: [1, 2, 1, 3]
5 2 3 0
After:  [3, 2, 1, 3]

Before: [1, 1, 3, 3]
11 0 3 1
After:  [1, 0, 3, 3]

Before: [3, 1, 2, 1]
6 1 0 3
After:  [3, 1, 2, 3]

Before: [1, 0, 1, 0]
7 0 1 2
After:  [1, 0, 1, 0]

Before: [3, 0, 1, 2]
8 2 3 0
After:  [3, 0, 1, 2]

Before: [2, 3, 0, 2]
4 1 0 3
After:  [2, 3, 0, 1]

Before: [0, 2, 2, 2]
8 1 2 0
After:  [4, 2, 2, 2]

Before: [3, 2, 2, 0]
8 3 2 1
After:  [3, 2, 2, 0]

Before: [2, 1, 2, 0]
8 0 2 1
After:  [2, 4, 2, 0]

Before: [3, 1, 3, 1]
14 3 2 2
After:  [3, 1, 3, 1]

Before: [3, 3, 1, 2]
0 0 0 3
After:  [3, 3, 1, 9]

Before: [2, 1, 0, 2]
0 1 0 3
After:  [2, 1, 0, 2]

Before: [3, 3, 1, 3]
0 0 0 2
After:  [3, 3, 9, 3]

Before: [1, 0, 2, 0]
1 1 0 1
After:  [1, 1, 2, 0]

Before: [1, 2, 1, 1]
10 1 0 0
After:  [1, 2, 1, 1]

Before: [1, 0, 1, 2]
1 1 0 1
After:  [1, 1, 1, 2]
"""

INPUT2 = """
5 1 0 0
12 0 2 0
5 0 0 2
12 2 3 2
5 0 0 3
12 3 1 3
0 3 0 0
5 0 3 0
8 0 1 1
2 1 1 3
14 2 3 2
14 0 2 1
14 1 1 0
2 0 2 0
5 0 1 0
8 3 0 3
2 3 3 1
14 2 1 3
14 1 1 2
14 2 0 0
3 0 3 2
5 2 1 2
5 2 3 2
8 1 2 1
2 1 1 3
5 2 0 1
12 1 2 1
14 1 1 0
14 2 3 2
2 0 2 2
5 2 3 2
8 3 2 3
2 3 0 2
14 1 1 1
5 2 0 0
12 0 2 0
14 2 1 3
14 3 0 3
5 3 1 3
8 2 3 2
5 0 0 3
12 3 2 3
14 1 0 0
14 0 3 1
8 0 0 0
5 0 1 0
8 2 0 2
2 2 3 1
14 0 3 3
14 0 0 2
14 3 0 0
7 0 2 2
5 2 2 2
8 1 2 1
2 1 0 2
14 2 0 3
14 2 3 1
14 2 2 0
3 0 3 3
5 3 3 3
8 3 2 2
2 2 1 0
14 0 0 1
5 2 0 2
12 2 0 2
14 1 0 3
12 3 1 3
5 3 1 3
8 3 0 0
2 0 2 2
14 1 3 3
14 2 2 0
14 2 0 1
4 0 3 3
5 3 1 3
5 3 3 3
8 2 3 2
2 2 0 1
14 0 1 0
14 2 3 2
14 0 3 3
11 3 2 3
5 3 3 3
8 3 1 1
2 1 3 2
14 2 2 3
14 1 1 1
14 2 2 0
0 1 0 1
5 1 1 1
8 2 1 2
2 2 2 3
5 1 0 1
12 1 3 1
14 0 2 2
13 0 1 1
5 1 3 1
8 1 3 3
5 1 0 0
12 0 3 0
14 2 3 1
14 2 0 2
9 0 1 0
5 0 1 0
5 0 3 0
8 3 0 3
2 3 1 2
14 0 3 1
5 3 0 3
12 3 1 3
14 0 3 0
14 3 0 0
5 0 1 0
8 2 0 2
14 1 2 1
14 2 3 0
4 0 3 1
5 1 3 1
8 2 1 2
2 2 3 3
14 3 0 0
14 0 2 2
14 3 1 1
1 2 0 0
5 0 1 0
8 0 3 3
2 3 0 2
14 3 2 3
5 0 0 0
12 0 2 0
14 1 2 1
9 3 0 0
5 0 1 0
8 0 2 2
2 2 1 3
14 0 2 2
14 0 1 1
14 3 0 0
1 2 0 0
5 0 2 0
8 0 3 3
2 3 0 0
14 2 1 3
14 2 2 1
10 2 3 1
5 1 2 1
8 0 1 0
14 3 3 1
10 2 3 3
5 3 3 3
8 3 0 0
2 0 1 3
14 1 2 0
14 2 3 2
2 0 2 2
5 2 1 2
8 3 2 3
2 3 1 1
14 3 0 3
14 2 0 2
2 0 2 0
5 0 1 0
5 0 1 0
8 0 1 1
14 2 1 0
14 2 0 3
5 2 0 2
12 2 0 2
10 2 3 2
5 2 3 2
8 2 1 1
5 1 0 3
12 3 3 3
14 0 2 2
14 3 3 0
1 2 0 3
5 3 1 3
8 3 1 1
2 1 2 3
14 3 2 2
14 2 2 0
14 1 1 1
6 0 2 1
5 1 1 1
8 3 1 3
2 3 2 1
5 3 0 2
12 2 2 2
14 1 2 0
14 0 3 3
2 0 2 3
5 3 3 3
8 3 1 1
5 0 0 2
12 2 0 2
14 0 0 3
8 0 0 3
5 3 3 3
8 3 1 1
14 2 0 3
0 0 3 2
5 2 1 2
5 2 2 2
8 1 2 1
14 0 2 2
14 3 0 0
1 2 0 2
5 2 3 2
8 2 1 1
2 1 1 0
14 2 1 2
14 3 3 1
14 3 1 3
13 2 1 1
5 1 1 1
8 1 0 0
2 0 0 1
14 0 1 2
14 3 0 0
14 1 1 3
1 2 0 2
5 2 1 2
5 2 2 2
8 1 2 1
2 1 1 0
14 3 0 2
14 0 2 1
5 3 2 3
5 3 3 3
8 3 0 0
2 0 0 2
14 2 1 3
14 1 2 1
14 2 0 0
3 0 3 1
5 1 1 1
8 1 2 2
2 2 3 1
14 2 0 2
14 1 2 3
4 0 3 0
5 0 1 0
8 0 1 1
14 1 1 0
2 0 2 2
5 2 3 2
8 2 1 1
14 3 2 3
14 2 0 0
14 3 1 2
6 0 2 2
5 2 3 2
8 2 1 1
2 1 0 0
14 2 3 2
14 1 2 1
14 0 1 3
11 3 2 2
5 2 3 2
8 0 2 0
2 0 0 1
14 1 0 0
14 3 1 3
14 3 3 2
14 2 3 2
5 2 3 2
5 2 2 2
8 1 2 1
2 1 2 2
14 2 2 0
5 1 0 3
12 3 1 3
14 2 1 1
8 3 3 1
5 1 3 1
5 1 2 1
8 2 1 2
14 3 3 1
5 3 0 0
12 0 1 0
8 0 0 3
5 3 1 3
5 3 3 3
8 3 2 2
2 2 2 1
5 2 0 2
12 2 0 2
14 2 0 3
5 1 0 0
12 0 2 0
3 0 3 2
5 2 3 2
8 2 1 1
14 0 3 2
14 1 2 0
0 0 3 3
5 3 1 3
8 3 1 1
2 1 1 3
14 1 0 2
14 1 0 1
8 1 0 0
5 0 3 0
8 0 3 3
14 1 3 0
14 2 0 2
14 3 3 1
2 0 2 0
5 0 1 0
8 3 0 3
2 3 3 1
14 0 0 3
14 3 1 2
14 1 2 0
10 3 2 0
5 0 3 0
5 0 2 0
8 1 0 1
14 2 2 0
5 2 0 2
12 2 1 2
14 2 0 3
3 0 3 0
5 0 3 0
8 0 1 1
2 1 3 0
14 3 3 2
5 2 0 1
12 1 0 1
14 3 1 3
7 3 2 2
5 2 3 2
8 2 0 0
2 0 3 1
14 0 1 0
14 2 2 3
14 0 0 2
10 2 3 0
5 0 3 0
5 0 3 0
8 0 1 1
2 1 3 0
5 0 0 1
12 1 2 1
14 3 0 3
7 3 2 1
5 1 3 1
8 1 0 0
2 0 3 1
5 3 0 0
12 0 3 0
14 1 1 3
5 1 0 2
12 2 3 2
5 3 2 0
5 0 1 0
8 0 1 1
2 1 3 3
14 3 2 1
14 2 1 0
1 0 2 0
5 0 3 0
8 3 0 3
2 3 1 1
14 1 0 0
14 0 1 3
14 2 0 2
2 0 2 0
5 0 1 0
8 0 1 1
2 1 0 0
5 3 0 1
12 1 3 1
11 3 2 2
5 2 1 2
8 2 0 0
14 3 1 2
14 2 0 1
14 2 3 3
15 1 3 2
5 2 1 2
8 2 0 0
2 0 3 3
14 3 3 1
14 2 1 0
5 2 0 2
12 2 2 2
9 1 0 1
5 1 3 1
5 1 1 1
8 3 1 3
2 3 0 2
14 1 3 1
14 1 3 0
14 2 1 3
8 1 0 0
5 0 3 0
8 0 2 2
2 2 2 3
5 3 0 1
12 1 2 1
14 0 0 2
5 3 0 0
12 0 1 0
5 0 2 0
5 0 3 0
8 3 0 3
2 3 1 1
14 2 2 0
14 2 0 3
14 3 3 2
6 0 2 0
5 0 2 0
8 0 1 1
2 1 2 2
14 0 1 3
14 1 1 0
14 3 0 1
12 0 1 3
5 3 3 3
8 2 3 2
2 2 3 3
5 3 0 0
12 0 2 0
14 0 2 2
14 1 1 1
0 1 0 0
5 0 3 0
8 0 3 3
2 3 3 2
14 2 0 0
14 2 0 3
5 2 0 1
12 1 3 1
13 0 1 0
5 0 1 0
5 0 2 0
8 2 0 2
2 2 3 3
14 2 1 2
14 1 1 0
14 2 1 1
2 0 2 1
5 1 3 1
8 1 3 3
5 2 0 2
12 2 3 2
5 3 0 1
12 1 3 1
14 0 2 0
7 1 2 2
5 2 3 2
8 2 3 3
2 3 0 1
14 1 2 3
14 3 0 2
5 3 2 0
5 0 1 0
8 0 1 1
5 0 0 3
12 3 2 3
14 1 1 0
14 1 1 2
0 0 3 0
5 0 3 0
8 0 1 1
2 1 1 2
14 0 2 1
14 2 1 0
3 0 3 0
5 0 2 0
8 2 0 2
2 2 1 0
5 0 0 2
12 2 2 2
14 3 0 1
5 3 0 3
12 3 0 3
15 2 3 2
5 2 2 2
8 2 0 0
2 0 3 2
14 1 2 1
14 2 3 0
14 3 1 3
9 3 0 3
5 3 3 3
8 2 3 2
5 0 0 1
12 1 3 1
14 1 0 3
4 0 3 3
5 3 3 3
5 3 1 3
8 3 2 2
2 2 0 1
14 2 1 3
5 3 0 2
12 2 0 2
14 3 2 0
10 2 3 3
5 3 2 3
8 1 3 1
2 1 2 0
14 1 3 2
5 1 0 3
12 3 0 3
14 0 2 1
14 3 2 2
5 2 1 2
5 2 2 2
8 0 2 0
14 1 3 1
14 0 3 2
5 1 2 1
5 1 2 1
5 1 1 1
8 1 0 0
5 1 0 2
12 2 3 2
14 2 3 1
6 1 2 2
5 2 1 2
8 2 0 0
2 0 2 3
14 1 2 0
14 0 2 2
5 0 2 2
5 2 3 2
8 2 3 3
14 0 3 1
5 2 0 2
12 2 2 2
2 0 2 2
5 2 2 2
8 3 2 3
2 3 0 0
14 2 0 2
14 1 2 1
14 0 2 3
15 2 3 3
5 3 1 3
8 3 0 0
2 0 1 1
14 2 0 3
14 1 3 0
14 1 1 2
0 0 3 2
5 2 2 2
8 2 1 1
2 1 0 3
5 3 0 1
12 1 1 1
14 3 3 2
5 0 2 2
5 2 3 2
8 3 2 3
2 3 2 1
14 0 2 3
5 0 0 0
12 0 2 0
14 3 1 2
6 0 2 3
5 3 3 3
8 3 1 1
2 1 2 3
14 1 3 1
14 2 2 2
0 1 0 0
5 0 1 0
8 0 3 3
14 2 3 0
14 3 2 2
1 0 2 2
5 2 2 2
8 2 3 3
2 3 0 1
14 1 3 2
14 1 0 3
14 1 3 0
8 0 0 3
5 3 1 3
5 3 3 3
8 3 1 1
2 1 3 3
14 3 0 1
14 2 2 2
14 3 2 0
6 2 0 2
5 2 1 2
5 2 3 2
8 2 3 3
2 3 3 1
14 2 3 2
5 2 0 3
12 3 0 3
11 3 2 2
5 2 2 2
8 1 2 1
14 3 0 2
10 3 2 3
5 3 2 3
5 3 3 3
8 3 1 1
2 1 2 3
14 2 2 2
14 3 0 1
6 2 0 0
5 0 1 0
5 0 3 0
8 0 3 3
2 3 2 1
14 2 1 0
14 1 1 3
14 1 2 2
4 0 3 2
5 2 3 2
8 1 2 1
2 1 1 2
14 0 2 3
14 3 2 1
15 0 3 1
5 1 2 1
5 1 2 1
8 1 2 2
14 3 1 0
14 1 3 3
14 0 2 1
12 3 1 3
5 3 2 3
5 3 1 3
8 2 3 2
2 2 1 1
14 0 1 0
14 3 0 3
14 3 3 2
14 2 3 3
5 3 2 3
5 3 3 3
8 3 1 1
14 3 3 3
14 2 1 0
14 0 1 2
14 2 3 3
5 3 2 3
8 1 3 1
2 1 2 3
14 3 3 2
14 3 3 0
14 2 2 1
6 1 0 1
5 1 3 1
8 1 3 3
2 3 2 1
14 3 2 3
14 2 0 2
13 2 0 2
5 2 1 2
8 2 1 1
2 1 2 0
14 1 0 3
14 3 3 1
14 3 3 2
14 2 1 1
5 1 1 1
5 1 2 1
8 0 1 0
2 0 3 3
5 0 0 1
12 1 1 1
14 0 1 2
14 3 0 0
1 2 0 1
5 1 1 1
5 1 2 1
8 3 1 3
2 3 1 1
5 2 0 2
12 2 2 2
14 3 1 3
6 2 0 3
5 3 3 3
5 3 2 3
8 1 3 1
5 3 0 2
12 2 0 2
14 2 1 3
5 2 0 0
12 0 2 0
3 0 3 3
5 3 2 3
8 3 1 1
2 1 2 2
5 1 0 0
12 0 3 0
14 1 1 3
14 3 2 1
12 3 1 1
5 1 2 1
5 1 1 1
8 1 2 2
2 2 1 1
14 2 0 2
5 2 0 3
12 3 0 3
5 0 0 0
12 0 1 0
11 3 2 0
5 0 3 0
8 1 0 1
2 1 1 2
5 3 0 1
12 1 1 1
14 2 0 3
5 2 0 0
12 0 2 0
3 0 3 3
5 3 1 3
5 3 1 3
8 2 3 2
2 2 1 1
14 0 2 0
5 3 0 2
12 2 3 2
14 0 1 3
14 2 3 2
5 2 3 2
8 2 1 1
2 1 2 3
14 2 3 1
14 2 1 0
5 0 0 2
12 2 3 2
6 1 2 0
5 0 2 0
8 3 0 3
2 3 1 1
14 0 0 2
5 0 0 3
12 3 1 3
14 2 3 0
8 3 3 0
5 0 3 0
8 1 0 1
5 0 0 0
12 0 2 0
14 3 2 2
14 2 2 3
3 0 3 2
5 2 2 2
8 2 1 1
14 3 2 2
3 0 3 3
5 3 1 3
5 3 1 3
8 1 3 1
2 1 3 3
14 0 3 2
14 0 0 1
5 0 0 0
12 0 1 0
8 0 0 2
5 2 2 2
8 2 3 3
2 3 0 1
5 3 0 3
12 3 2 3
14 0 0 2
14 2 3 0
10 2 3 0
5 0 3 0
8 0 1 1
14 2 3 2
14 1 2 0
8 0 0 0
5 0 2 0
5 0 3 0
8 0 1 1
2 1 2 3
14 2 3 1
14 1 2 0
8 0 0 0
5 0 3 0
8 0 3 3
2 3 0 1
5 2 0 3
12 3 2 3
14 1 3 0
2 0 2 3
5 3 2 3
8 1 3 1
2 1 0 2
14 2 1 1
14 3 1 3
14 3 3 0
6 1 0 3
5 3 3 3
8 2 3 2
14 0 2 3
14 1 0 0
5 0 0 1
12 1 0 1
14 3 0 0
5 0 2 0
8 0 2 2
2 2 1 0
14 2 0 2
14 1 2 1
11 3 2 1
5 1 3 1
5 1 2 1
8 1 0 0
2 0 0 2
14 1 0 3
14 2 3 0
5 0 0 1
12 1 0 1
4 0 3 3
5 3 2 3
5 3 1 3
8 2 3 2
2 2 3 0
5 0 0 2
12 2 3 2
14 1 3 1
14 1 1 3
14 3 1 3
5 3 2 3
8 3 0 0
2 0 0 2
5 0 0 3
12 3 2 3
14 0 3 1
14 2 2 0
3 0 3 1
5 1 3 1
5 1 3 1
8 2 1 2
5 1 0 1
12 1 2 1
14 3 0 0
9 0 1 3
5 3 1 3
8 2 3 2
2 2 2 1
14 2 3 0
14 2 2 3
14 3 0 2
6 0 2 3
5 3 1 3
5 3 1 3
8 1 3 1
2 1 0 3
14 3 3 0
14 2 2 1
9 0 1 1
5 1 1 1
8 1 3 3
14 1 0 2
14 3 0 1
14 1 0 0
7 1 2 0
5 0 3 0
5 0 2 0
8 3 0 3
5 1 0 0
12 0 3 0
14 1 0 1
7 0 2 2
5 2 1 2
8 3 2 3
2 3 1 2
14 2 3 3
14 1 2 0
0 1 3 1
5 1 2 1
8 2 1 2
2 2 3 1
5 1 0 0
12 0 2 0
14 0 3 2
3 0 3 0
5 0 3 0
5 0 3 0
8 1 0 1
2 1 2 2
14 2 2 0
14 0 3 1
14 0 1 3
14 3 0 0
5 0 2 0
8 0 2 2
2 2 2 3
14 1 3 0
5 1 0 1
12 1 1 1
14 0 2 2
8 1 0 1
5 1 3 1
5 1 1 1
8 1 3 3
2 3 0 0
"""


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
""", 1),
]


class Opcodes:
    @staticmethod
    def addr(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = inputs[A] + inputs[B]
        return tuple(outputs)

    @staticmethod
    def addi(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = inputs[A] + B
        return tuple(outputs)

    @staticmethod
    def mulr(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = inputs[A] * inputs[B]
        return tuple(outputs)

    @staticmethod
    def muli(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = inputs[A] * B
        return tuple(outputs)

    @staticmethod
    def banr(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = inputs[A] & inputs[B]
        return tuple(outputs)

    @staticmethod
    def bani(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = inputs[A] & B
        return tuple(outputs)

    @staticmethod
    def borr(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = inputs[A] | inputs[B]
        return tuple(outputs)

    @staticmethod
    def bori(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = inputs[A] | B
        return tuple(outputs)

    @staticmethod
    def setr(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = inputs[A]
        return tuple(outputs)

    @staticmethod
    def seti(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = A
        return tuple(outputs)

    @staticmethod
    def gtir(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = 1 if A > inputs[B] else 0
        return tuple(outputs)

    @staticmethod
    def gtri(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = 1 if inputs[A] > B else 0
        return tuple(outputs)

    @staticmethod
    def gtrr(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = 1 if inputs[A] > inputs[B] else 0
        return tuple(outputs)

    @staticmethod
    def eqir(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = 1 if A == inputs[B] else 0
        return tuple(outputs)

    @staticmethod
    def eqri(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = 1 if inputs[A] == B else 0
        return tuple(outputs)

    @staticmethod
    def eqrr(A, B, C, inputs):
        outputs = list(inputs)
        outputs[C] = 1 if inputs[A] == inputs[B] else 0
        return tuple(outputs)


def find_possible_opcodes(before, instruction, after):
    opcode, A, B, C = instruction
    possible = set()
    for name, method in inspect.getmembers(Opcodes):
        if name[0] != '_':
            outputs = method(A, B, C, before)
            if outputs == after:
                possible.add(name)

    return possible
    # print(before)
    # print(instruction)
    # print(after)


RE_NUMBER = re.compile('(\d+)')


def solve(samples, program):
    before, instruction, after = [], [], []
    possible_opcodes = {}
    for line in samples.strip().split('\n'):
        if 'Before:' in line:
            before = tuple(map(int, RE_NUMBER.findall(line)))
        elif 'After:' in line:
            after = tuple(map(int, RE_NUMBER.findall(line)))
            code, A, B, C = instruction
            opcodes = find_possible_opcodes(before, instruction, after)
            if code in possible_opcodes:
                possible_opcodes[code] = possible_opcodes[code].intersection(opcodes)
            else:
                possible_opcodes[code] = opcodes
        else:
            instruction = tuple(map(int, RE_NUMBER.findall(line)))

    while max(len(v) for v in possible_opcodes.values()) > 1:
        for code, opcodes in possible_opcodes.items():
            if len(opcodes) == 1:
                opcode = next(iter(opcodes))
                for code2, opcodes2 in possible_opcodes.items():
                    if opcode in opcodes2 and code != code2:
                        opcodes2.remove(opcode)
    opcodes = {code: next(iter(opcodes)) for code, opcodes in possible_opcodes.items()}

    print(possible_opcodes)
    registers = (0, 0, 0, 0)
    for line in program.strip().split('\n'):
        instruction = tuple(map(int, RE_NUMBER.findall(line)))
        code, A, B, C = instruction
        method = getattr(Opcodes, opcodes[code])
        registers = method(A, B, C, registers)

    return registers[0]


if __name__ == '__main__':
    # for case in TEST_CASES:
    #     result = solve(case.case)
    #     check_case(case, result)

    print(solve(INPUT1, INPUT2))
