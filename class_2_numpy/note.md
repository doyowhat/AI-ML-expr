# Numpy库

最重要的一个特性就是 ndarray 多维数组对象，它区别于 python 的标准类，拥有对高维数组的处理能力，这也是数值计算过程中缺一不可的重要特性。主要通过以下途径创建数组： 

使用.astype()转换数值类型，使用.dtype直接查看数值类型

**tips:和pytorch库的很多接口是一样的**

## Numpy快速入门

### 数组Array
见./course/array.py

重点是**逐数组操作**

### 矩阵matrix
见./course/matrix.py

重点是**矩阵乘和构造方法**

## Numpy随机抽样库

numpy.random模块，主要包括
```python
import numpy.random as nr
x = nr.rand(0,1)
x = nr.randn(1,10) #标准正态分布
```
