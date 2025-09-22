TestList = [10001,'中文内容','En Info',[1,2,3,4,5,6]]
print(TestList)

print("当前列表长度",len(TestList))

for info in TestList:
    print(info)

TestList.append(1.234)
TestList.append("最后一个元素")

print(TestList)
print("当前列表长度为:%d \n" % len(TestList))
# %占位符语法,基本格式为
# "包含多个占位符的字符串" % (值1, 值2, ..., 值N)

TestList.append("string")
print(TestList)

# 与list类似的类型，tuple也叫元组或者切片，定义规则同list。可以理解为常量list
tup1 = ('Google','Runoob',1997,2000)

