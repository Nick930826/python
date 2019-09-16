'''
@Description: In User Settings Edit
@Author: your name
@Date: 2017-09-22 14:48:02
@LastEditTime: 2019-09-05 17:24:21
@LastEditors: Please set LastEditors
'''
# -*- coding: utf-8 -*-
# name = input('please enter your name: ')
# print('hello,', name)

# list和tuple
# classmates = ['炳奇', '薛冰', '凌霄']
# print (classmates)

# print (len(classmates))
# print (classmates[0])
# print (classmates[-1])
# # classmates[1]
# # classmates[2]

# classmates.append('静静')
# print (classmates)

# classmates.insert(1, '勇元')
# print (classmates)

# classmates.pop()
# print (classmates)

# 判断条件
# age = input('请输入年龄：')
# if int(age) > 18:
#     print ('老腊肉')
# else:
#     print ('小鲜肉')

# 循环
# classmates = ['炳奇', '薛冰', '凌霄']

# for name in classmates:
#     print(name)

# number = list(range(100))
# sum = 0

# for x in number:
#     sum = sum + x

# print(sum)

# all = 0
# n = 100
# while n > 0:
#     all = all + n
#     n = n - 1
# print(all)

a = [1,2,3,4]
b = ['aa', 'bb', 'cc', 'dd']

for k, m in zip(a,b):
    print(k, m)
    #print(m)