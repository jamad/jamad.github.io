* code

```
import pygame
import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iterations=30):
    z = 0
    for i in range(max_iterations):
        if 2<abs(z):return i
        z=z*z+c
    return max_iterations 

def mandelbrot_set(size=512):
    x=np.linspace(-2    ,1  ,size)
    y=np.linspace(-1.5  ,1.5,size)
    mset=np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            c=complex(x[j],y[i])
            mset[i,j]=mandelbrot(c)
    return mset

plt.imshow(mandelbrot_set(),cmap='hot')
plt.show()
```
