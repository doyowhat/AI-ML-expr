# 这里如果把文件命名为random.py的话就会循环导入报错
import numpy.random as nr

x = nr.rand(2,5)
y = nr.randn(1,10)

print(x)

print(y)