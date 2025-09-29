from numpy import array
# 数组加
mm = array((1,2,3))
nn = array((1,1,1))

sum = mm + nn
sum2 = sum ** 2
print(sum2)

# 多维数组乘法

mul_arr = array([[1,2,3],[1,1,1]])
print(mul_arr)
print(mul_arr[0],mul_arr[1])
a1 = array([1,2,3])
a2 = array([3,4,5])
a12 = a1 * a2
print(a12)