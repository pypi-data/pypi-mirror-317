# Readme of `yasiu-math`

Module with useful math functions that are missing in numpy or scipy.

# Installation

```shell
pip install yasiu-math
```
# Modules list
- `convolve` - Convolution functions

### Use example:

```py
from yasiu.math.convolve import moving_average

moving_average(Union[list, "1d np array"], radius=1, padding="try", kernel_type="avg", kernel_exp=2)
```

#### Example

![picure](https://raw.githubusercontent.com/GrzegorzKrug/yasiu-math/refs/heads/main/pics/convolveComparison.png)

# All packages

[1. Native Package](https://pypi.org/project/yasiu-native/)

[2. Math Package](https://pypi.org/project/yasiu-math/)

[3. Image Package](https://pypi.org/project/yasiu-image/)

[4. Visualisation Package](https://pypi.org/project/yasiu-vis/)
