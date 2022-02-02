N = 11 #this is a constant, its value is not going to change. we create them at the beginning of the program
n1 = 0
n2 = 1
print(n1, end=" ")
print(n2, end=" ")
for i in range(2, N): # we start from 2 because we already have printed two numbers outside of the for, we need to print 9
    num = n1 + n2
    print(num, end=" ")
    n1 = n2
    n2 = num
print()