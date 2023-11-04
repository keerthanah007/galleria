print("hello world")

x=4
print(x)
print(type(x))

x='sss'
print(x)
print(type(x))

list1=["apple","orange","grapes",3]
print(list1)
print(type(list1))

print(list1[2])
print(list1[-1])
print(list1[0:2])
print(list1[-2])

list1.insert(2,"fox")
list1.append("dog")
print(list1)
list1.remove(list1[3])
list1.remove("fox")
print(list1)


tp=("ron","herm","harry",94,94)
print(tp)
print(type(tp))

x=list(tp)
print(x)
print(type(x))



set={'eee','dddd',4.32}
print(set)
print(type(set))

dict={"keya":90,"keyb":34,"keyc":56,11:"hello"}
print(dict)
print(type(dict))

a=3
b=3
if a>b:
	print("this is if")
elif a==b:
	print("this is elif")
else:
	print("this is else")

for i in range(1,6,1):
	print(i)

for i in x:
	print(i)

c=1
while c<10:
	print(c)
	c+=1