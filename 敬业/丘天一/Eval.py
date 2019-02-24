import FnAndCon
fac = FnAndCon.fac()


def new_eval(exp):
	'执行输入内容'
	if type(exp) != list:
		if type(exp) == str:
			fd = fac.find(exp)
			if fd is not None:
				return fd[exp]
			else:
				return None
		else:
			return exp
	else:
		if exp[0] == 'if':
			if exp[1] is True:
				return new_eval(exp[2])
			else:
				if len(exp) == 3:
					return None
				else:
					return new_eval(exp[3])
		elif exp[0] == 'setf':
			return fac.add(exp[1], exp[2])
		elif exp[0] == 'quote':
			return exp[1]
		elif exp[0] == 'list':
			return list(map(new_eval, exp[1:]))
		elif exp[0] == 'listq':
			return True if type(exp[1]) == list else False
		elif exp[0] == 'defun':
			fac.add(exp[0], new_eval(exp[1]))
		elif exp[0] == 'lambda':
			return FnAndCon.DeFun(exp[1], exp[2], fac)
		else:
			fn = new_eval(exp[0])
			return fn(exp[1:])
