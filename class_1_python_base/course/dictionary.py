# key只能是可哈希的不可变类型，如int,str,tuple,frozenset

test_dict = {
    'time':'时间',
    'machine':'机器',
    'course':'课程'
}

print(test_dict['time'])

# 另一种构造字典的方式
new_dict = {}
new_dict['stuff'] = 'start'
print(new_dict)

#字典的属性可以是字典
rec = {
    'name':{'first':'Bob','last':'Smith'},
    'job':['dev','mgr'],
    'age':40.5
}
print(rec)
sort_rec = sorted(rec)
# sorted返回的是一个已排序好的key的新列表，不会改变原容器
print(sort_rec)

rec = 0
# 当变量的最后一次引用完成时，内存自动释放