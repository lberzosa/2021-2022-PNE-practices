def fib(n):
    n1 = 0
    n2 = 1
    if n == 1:
        return n1
    elif n == 2:
        return n2
    else:
        for i in range(2, n + 1): #never write a return inside a loop
            num = n1 + n2
            n1 = n2
            n2 = num
        return num

print("5th fibonacci term:", fib(5))
print("11th fibonacci term:", fib(11))
print("55th fibonacci term:", fib(55))