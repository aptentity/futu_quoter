# -*- coding: utf-8 -*-

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.arange(8)
y = np.array([1, 5, 3, 6, 2, 4, 5, 6])
df = pd.DataFrame({'x-axis': x, 'y-axis': y})
sns.barplot('x-axis', 'y-axis', palette='RdBu_r', data=df)
plt.xticks(rotation=90)
plt.show()
