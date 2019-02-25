import Read
import Eval
import FnAndCon


def io():
	# 进行输入输出
	n = 1

	while True:
		print('In [', n, ']:  ', end='')
		inp = input()
		if inp == 'exit':
			print('Are you sure to exit? [Y|Others]')
			if input() == 'Y':
					print('Bye Bye!!!')
					break
			else:
				n += 1
		elif inp == '':
			n += 1
			continue
		else:
			out = new_out(Eval.new_eval(Read.read(inp)))
			print('Out[', n, ']: ', out, end='\n')
			n += 1


def new_out(output):
	# 将Python的列表形式转为Lisp的形式
	if type(output) == list:
		if len(output) == 1:
			return str(output[0])
		else:
			x = [str(x) for x in output]
			return str('(' + ' '.join(x)+')')
	else:
		return str(output)


if __name__ == '__main__':
	FnAndCon.fac()
	print('--------------------')
	print('Welcome To MyNewLisp')
	print('--------------------')
	io()