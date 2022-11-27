import numpy
from stl import mesh

"""
1. Load data / convert into standardised format
2. Find hard edges & corners
3. Reduce hard corners that are too close
4. Distribute points on hard corners (verticies)
4. Distribute points on hard edges _while keeping distance to already generated points_
5. Distribute points on faces including soft edges and corners (verticies) (bluse noise sampling) _while keeping
   distance to already generated points_
6. Map colors to points
7. (Optional) perform checks
"""


