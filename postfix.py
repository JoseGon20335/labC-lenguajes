def passToPostFix(redexPre):
    specials = {'(': 1, "(": 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}
    alfabetoA = [str(i) for i in range(256)]
    resultPostFix = []
    fixRedex = []
    stack = []
    redex = []

    littleString = ''
    checker = False
    for i, c in enumerate(redexPre):
        if c == '"':
            if checker:
                checker = False
                redex.append(littleString)
                littleString = ''
            else:
                checker = True
                continue
        if checker:
            littleString += c
        elif c == '(' or c == ')' or c == '|' or c == '*' or c == '+' or c == '?' or c == '.':
            if littleString != '':
                redex.append(littleString)
            redex.append(c)
            littleString = ''
        else:
            littleString += c
    if littleString != '' or littleString != ' ' or littleString != '"':
        redex.append(littleString)

    for i, c in enumerate(redex):
        if i+1 != len(redex) and c in alfabetoA and redex[i+1] in alfabetoA:
            fixRedex.append(c)
            fixRedex.append('.')
        elif i+1 != len(redex) and c in alfabetoA and redex[i+1] == '(':
            fixRedex.append(c)
            fixRedex.append('.')
        elif i+1 != len(redex) and c == ')' and redex[i+1] in alfabetoA:
            fixRedex.append(c)
            fixRedex.append('.')
        elif i+1 != len(redex) and c == ')' and redex[i+1] == '(':
            fixRedex.append(c)
            fixRedex.append('.')
        elif i+1 != len(redex) and c == '?' and redex[i+1] in alfabetoA:
            fixRedex.append(c)
            fixRedex.append('.')
        elif i+1 != len(redex) and c == '?' and redex[i+1] == '(':
            fixRedex.append(c)
            fixRedex.append('.')
        elif i+1 != len(redex) and c == '*' and redex[i+1] in alfabetoA:
            fixRedex.append(c)
            fixRedex.append('.')
        elif i+1 != len(redex) and c == '*' and redex[i+1] == '(':
            fixRedex.append(c)
            fixRedex.append('.')
        elif i+1 != len(redex) and c == '+' and redex[i+1] in alfabetoA:
            fixRedex.append(c)
            fixRedex.append('.')
        elif i+1 != len(redex) and c == '+' and redex[i+1] == '(':
            fixRedex.append(c)
            fixRedex.append('.')
        elif c != '"':
            if c != '':
                fixRedex.append(c)

    for i, c in enumerate(fixRedex):
        if c in alfabetoA or c[:1] == '#':
            resultPostFix.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                resultPostFix.append(stack.pop())
            stack.pop()
        else:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                resultPostFix.append(stack.pop())
            stack.append(c)

    while stack:
        resultPostFix.append(stack.pop())

    return resultPostFix
