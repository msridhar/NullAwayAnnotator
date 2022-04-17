import numpy as np
import matplotlib.pyplot as plt

data = [[np.random.rand(100)] for i in range(3)]
plt.boxplot(data)
plt.xticks([1, 2, 3], ['mon', 'tue', 'wed'])
