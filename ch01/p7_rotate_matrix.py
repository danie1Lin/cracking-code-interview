
from typing import NewType, TypeVar

import unittest


Image = TypeVar('Image', bound=list[list[int]]) 
def RotateMatrix(img: Image) -> Image:
    dim = len(img)
    center = (dim - 1) / 2 # 常漏，因為是位置所以剪掉 1
    for i in range(int(center) + 1):
        for j in range(int(center) + 1):
            dis = (center - i, center -j)
            pos_of_quadrant = [
                (int(center - dis[0]), int(center - dis[1])),
                (int(center - dis[1]), int(center + dis[0])),
                (int(center + dis[0]), int(center + dis[1])),
                (int(center + dis[1]), int(center - dis[0]))
            ] 
            print(dis, pos_of_quadrant)
            img[pos_of_quadrant[0][0]][pos_of_quadrant[0][1]], img[pos_of_quadrant[1][0]][pos_of_quadrant[1][1]], img[pos_of_quadrant[2][0]][pos_of_quadrant[2][1]], img[pos_of_quadrant[3][0]][pos_of_quadrant[3][1]] = img[pos_of_quadrant[3][0]][pos_of_quadrant[3][1]], img[pos_of_quadrant[0][0]][pos_of_quadrant[0][1]], img[pos_of_quadrant[1][0]][pos_of_quadrant[1][1]], img[pos_of_quadrant[2][0]][pos_of_quadrant[2][1]]
    return img




class TestRotateImage(unittest.TestCase):
    def test(self):
        self.assertEqual(RotateMatrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]), [[13, 9 , 5, 1], [14,10 ,6,2], [15,11, 7, 3], [16 , 12, 8, 4]])

if __name__ == '__main__':
    unittest.main()
