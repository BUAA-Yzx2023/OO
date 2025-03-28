import random
import sys
from random import randint

def genExpr(depth,alpha):
    expr = []
    Mlen = max(1,maxExprLength-(depth))
    length = randint(1,Mlen+1)

    for i in range(length):
        expr.append(genTerm(depth,alpha))
        if i < length - 1:  # 避免最后一个 '+' 多余
            if randint(0,1)==0:
                expr.append(' + ')
            else:
                expr.append(' - ')
    return ''.join(expr)  # 将列表转换为字符串

def genTerm(depth,alpha):
    term = []
    Mlen = max(1,maxTermLength-depth)
    length = randint(1, Mlen)
    for i in range(length):
        if i==0:
            sign = randint(0,3)
            if sign==0:
                term.append('+ ')
            elif sign==1:
                term.append('- ')
        term.append(genFactor(depth,alpha))
        if i < length - 1:  # 避免最后一个 '+' 多余
            term.append(' * ')
    return ''.join(term)  # 将列表转换为字符串

def genFactor(depth,alpha):
    global nowFuncnt
    i = randint(0, 6)
    if i == 0 and depth < maxDepth:
        return genExprFactor(depth + 1,alpha)
    elif i == 1 and depth < maxDepth:
        return genTrainFactor(depth + 1,alpha)
    elif i == 2 and recurFunc==1 and isDefine==0 and nowFuncnt<maxFuncnt and depth < maxDepth :
        nowFuncnt += 1
        return genFuncFactor(depth + 1, alpha)
    elif i == 3 and (normalArgs['g']!=0 or normalArgs['h']!=0) and depth < maxDepth :
        j = randint(0,1)
        if normalArgs[name[j]]!=0:
            return genNormalFuncFactor(depth+1,name[j],alpha)
        else:
            return genNormalFuncFactor(depth + 1, name[1-j], alpha)
    elif i == 4 and isDefine==0 and depth < (maxDepth+2):
        return genDeriveFactor(depth+1, alpha)
    elif i == 5 :
        return genNumFactor(depth)
    else:
        return genVarFactor(depth, alpha)

def genNumFactor(depth):
    num = str(genInteger())
    i = randint(0,2)
    if i == 0:
        return num  # 返回原始数字
    elif i == 1:
        return f"+{num}"  # 返回带正号的数字
    else:
        return f"-{num}"  # 返回带负号的数字

def genVarFactor(depth,alpha):
    if alpha == 'z':
        if randint(0,1)==0:
            var = ['x']
        else:
            var = ['y']
    else:
        var = [alpha]
    if randint(0, 1) == 0:
        var.append('^')
        var.append(genIndex())
    return ''.join(var)  # 将列表转换为字符串

def genExprFactor(depth,alpha):
    expr = ['(']
    expr.append(genExpr(depth,alpha))
    expr.append(')')
    if randint(0, 1) == 0:
        expr.append('^')
        if randint(0,1)==0:
            expr.append('+')
        expr.append(genIndex())
    return ''.join(expr)  # 将列表转换为字符串

def genTrainFactor(depth,alpha):
    if randint(0,1) == 0:
        train = ['sin(']
    else:
        train = ['cos(']
    train.append(genFactor(depth,alpha))
    train.append(')')
    if randint(0, 1) == 0:
        train.append('^')
        if randint(0,1)==0:
            train.append('+')
        train.append(genIndex())
    return ''.join(train)

def genDeriveFactor(depth,alpha):
    derive = []
    derive.append(f'dx({genExpr(depth, alpha)})')
    return ''.join(derive)

def genInteger():
    num = []
    length = randint(1,maxIndex)
    for i in range(length):
        num.append(str(randint(0, 9)))
    return ''.join(num)  # 将列表转换为字符串

def genIndex():
    return str(randint(0, maxIndex))

def genFuncFactor(depth,alpha):
    func = []
    i = randint(0,maxFuncDepth)
    if args==2:
        func.append(f"f{{{i}}}({genFactor(depth+1,alpha)},{genFactor(depth+1,alpha)})")
    else:
        func.append(f"f{{{i}}}({genFactor(depth + 1, alpha)})")
    return ''.join(func)

def genDefine(x,y):
    actions = [
        lambda: print(genFn(x, y)),
        lambda: print(genF01(1, x, y)),
        lambda: print(genF01(0, x, y))
    ]
    # 随机打乱执行顺序
    random.shuffle(actions)
    for action in actions:
        action()
    isDefine = 0

def genFn(x,y):
    Fn = []
    if y is not None:
        Fn.append(f'f{{n}}({x},{y}) = ')
        alpha = 'z'
    else:
        Fn.append(f'f{{n}}({x}) = ')
        alpha = x

    Fn.append(genInteger())
    Fn.append(' * ')

    if y is not None:
        Fn.append(f'f{{n-1}}({genFactor(maxDepth-1,alpha)},{genFactor(maxDepth-1,alpha)})')
    else:
        Fn.append(f'f{{n-1}}({genFactor(maxDepth - 1, alpha)})')

    if randint(0,1)==0:
        Fn.append(' - ')
    else:
        Fn.append(' + ')

    Fn.append(genInteger())
    Fn.append(' * ')
    if y is not None:
        Fn.append(f'f{{n-2}}({genFactor(maxDepth - 1, alpha)},{genFactor(maxDepth - 1, alpha)})')
    else:
        Fn.append(f'f{{n-2}}({genFactor(maxDepth - 1, alpha)})')

    if randint(0,2)>0:
        Fn.append(' + ')
        Fn.append(genExpr(maxDepth-1,alpha))
    return ''.join(Fn)

def genF01(i,x,y):
    F01 = []

    if y is not None:
        F01.append(f'f{{{i}}}({x},{y}) = ')
        alpha = 'z'
    else:
        F01.append(f'f{{{i}}}({x}) = ')
        alpha = x
    F01.append(genExpr(maxDepth-1,alpha))
    return ''.join(F01)

def genNormalDefine(name,x,y):
    func = []
    if y is not None:
        func.append(f'{name}({x},{y}) = ')
        alpha = 'z'
    else:
        func.append(f'{name}({x}) = ')
        alpha = x
    func.append(genExpr(maxDepth - 1, alpha))

    if y is not None:
        normalArgs[name] = 2
    else:
        normalArgs[name] = 1
    return ''.join(func)

def genNormalFuncFactor(depth,name,alpha):
    func = []
    if normalArgs[name] == 2:
        func.append(f'{name}({genFactor(depth+1,alpha)},{genFactor(depth+1, alpha)})')
    else:
        func.append(f'{name}({genFactor(depth + 1, alpha)})')
    return ''.join(func)





# maxDepth = 3  # 全局变量
# maxTermLength = 3
# maxExprLength = 3
# maxFuncDepth = 3
# maxIndex = 3
# maxFuncnt = 5

maxDepth = int(sys.argv[1])
maxExprLength = int(sys.argv[2])
maxTermLength = int(sys.argv[3])
maxIndex = int(sys.argv[4])
maxFuncDepth = int(sys.argv[5])
maxFuncnt = int(sys.argv[6])

nowFuncnt = 0
isDefine = 1

normalFunc = randint(0,2)
normalFunc = 2
recurFunc = randint(0,1)
group = [['x','y'],['y','x'],['x',None],['y',None]]
name = ['g','h']
normalArgs = dict([['g',0],['h',0]])
print(normalFunc)
if normalFunc == 1:
    i = randint(0,1)
    j = randint(0,3)
    print(genNormalDefine(name[i],group[j][0],group[j][1]))
elif normalFunc == 2:
    i = randint(0, 1)
    j = randint(0, 3)
    print(genNormalDefine(name[i], group[j][0], group[j][1]))
    j = randint(0, 3)
    print(genNormalDefine(name[1-i], group[j][0], group[j][1]))


print(recurFunc)
if recurFunc == 1:
    j = randint(0,3)
    group = [['x', 'y'], ['x', None],['y', 'x'],  ['y', None]]
    args = 2-(j%2)
    genDefine(group[j][0],group[j][1])

isDefine = 0
print(genExpr(0,'x'))