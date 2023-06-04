def tokens(listaTokens):
	for tokenValue in listaTokens:
		token = tokenValue[1].replace("#","")
		if token == "id":
			return ID
		elif token == "+":
			return PLUS
		elif token == "*":
			return TIMES
		elif token == "(":
			return LPAREN
		elif token == ")":
			return RPAREN
		else: 
			print("error de sintaxis")