import sys
from random import randint


def genExpr(depth):
    expr = []
    if Long == 1:
        length = randint(3, 12)
    else:
        length = randint(2, 4)

    for i in range(length):
        expr.append(genTerm(depth))
        for j in range(randint(0, 2)):
            expr.append(' ')
        if i < length - 1:  # 避免最后一个 '+' 多余
            if randint(0,1)==0:
                expr.append('+')
            else:
                expr.append('-')
    return ''.join(expr)  # 将列表转换为字符串

def genTerm(depth):
    term = []
    if Long == 1:
        length = randint(1, 5)
    else:
        length = randint(1, 3)

    for i in range(length):
        if i==0:
            sign = randint(0,3)
            if sign==0:
                term.append('+')
            elif sign==1:
                term.append('-')

        term.append(genFactor(depth))
        if(randint(0,2)==0):
            term.append('\t')
        if i < length - 1:  # 避免最后一个 '+' 多余
            term.append('*')
    return ''.join(term)  # 将列表转换为字符串

def genFactor(depth):
    i = randint(0, 3)
    if i == 0 and depth < maxDepth:
        return genExprFactor(depth + 1)
    elif i == 1:
        return genVarFactor(depth)
    else:
        return genNumFactor(depth)

def genNumFactor(depth):
    num = str(genInteger())
    # if randint(0, 1) == 0:
    #     num.append('^')
    #     num.append(genIndex())
    i = randint(0,2)
    if i == 0:
        return num  # 返回原始数字
    elif i == 1:
        return f"+{num}"  # 返回带正号的数字
    else:
        return f"-{num}"  # 返回带负号的数字

def genVarFactor(depth):
    var = ['x']
    if randint(0, 1) == 0:
        var.append('^')
        var.append(genIndex())
    return ''.join(var)  # 将列表转换为字符串

def genExprFactor(depth):
    expr = ['(']
    expr.append(genExpr(depth))
    expr.append(')')
    if randint(0, 1) == 0:
        expr.append('^')
        if randint(0,1)==0:
            expr.append('+')
        expr.append(genIndex())
    return ''.join(expr)  # 将列表转换为字符串

def genInteger():
    num = []
    if Big==1:
        length = randint(1, 16)
    else:
        length = randint(1,3)
    for i in range(length):
        num.append(str(randint(0, 9)))
    return ''.join(num)  # 将列表转换为字符串

def genIndex():
    if Long == 1:
        return str(randint(0, 8))
    else:
        return str(randint(0, 3))

maxDepth = 1  # 全局变量
Long = int(sys.argv[1])
Big = int(sys.argv[2])
print(genExpr(0))