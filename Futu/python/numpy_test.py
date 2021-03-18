# -*- coding: utf-8 -*-

import numpy as np

numpy1 = np.array([[10, -8, 1, 5], [-9, 9, 2, 6]])
numpy2 = np.array([1, 2, 3, 4])

print(numpy1)
print(type(numpy1))
print(numpy1.T)
print(numpy2 * numpy1)
print(numpy1 * numpy2)
print(numpy1.dot(numpy2))
