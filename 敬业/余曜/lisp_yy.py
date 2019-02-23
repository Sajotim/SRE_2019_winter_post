#这是一个scheme语言解释器

#这是一个十分简陋的解释器，本人有充分的理由相信里面有一大堆潜在的bug，请尽量包涵；

#运行的话，(大概)是交互型的那种模式，直接输入(if(> 1 2) '(hi)'(hello))这种命令

#目前只完成了可怜巴巴的最基础的一部分内容，数据类型只完成了字符和数字两种，而功能仅限于四则运算、条件判断、set!、begin那么几个。

#感觉总体思路上不够清晰(我怎么知道一个正确的解释器怎么写哇Σ(っ°Д°;)っ)，导致代码写得很慢，逻辑越往后面也越发混杂了。

#先交一次作业，后面几天再努力地完善和更正一下。




def split_input( input_str ): 
#预处理，接受输入的字符串，切割并以列表的形式返回

	return input_str.replace('(', ' ( ').replace(')', ' ) ').split()
	#左右括号的两侧都要加空格先

	
def before_deal_str_list( input_list ):
#二次预处理	
	the_list = input_list[:]
	
	_list = ["begin","then","else"]
	
	for i in reversed(the_list):
		if i in _list:
			the_list.remove(i)
	
	return the_list
	
	
def deal_str_list( input_list ):
#最主要的函数，进行处理
	global env_dict
	
	the_list = input_list[:]
	
	end = False
	new_list = []
	env_dict = {}
	
	while not end : #只要上一轮还能找到括号，就继续循环
		
		left_pos = -1
		right_pos = -1
		
		for i in range( len(the_list) ): #遍历切割过的列表
		
			if the_list[i] == '(':
				left_pos = i
			elif the_list[i] == ')':
				right_pos = i

			if i==len(the_list)-1:#遍历所有元素都没能找到一对括号
				end = True
				
			if (left_pos!=-1) and (right_pos!=-1): #找到了一对括号
			
				#new_list.append( the_list[left_pos:right_pos+1] )
				
				number_of_left = check_if_left(the_list,left_pos)
				
				if number_of_left:
					for i in range( right_pos+1-left_pos+number_of_left ):
					
						new_list.append(the_list[left_pos-number_of_left])
						#将括号内的东西以及括号左的字符串添加到新列表中
						
						the_list.pop(left_pos-number_of_left)
						#将旧列表的括号内的东西以及括号左的字符串删除
					
					the_return = answer_new_list_of_left(new_list)
					
					if the_return:
						the_list.insert(left_pos-number_of_left,the_return)
					#将新列表内的东西的结果算出来				，并添加到旧列表当中（如果效果是print之类的，直接执行效果就不用返回值）	
					
					new_list = []
					break
					
				else:
					for i in range( right_pos+1-left_pos ):
					
						new_list.append(the_list[left_pos])
						#将括号内的东西添加到新列表中
						
						the_list.pop(left_pos)
						#将旧列表的括号内的东西删除
					
					the_return = answer_new_list(new_list)
					
					if the_return != None:
						the_list.insert(left_pos,the_return)
					#将新列表内的东西的结果算出来				，并添加到旧列表当中（如果效果是print之类的，直接执行效果就不用返回值）	
					
					new_list = []
					break
					
	if the_list:		
		print(";value:",the_list[0]) #输出结果
	else:
		print(";value: 无")
	

def check_if_left(the_list,left_pos): 
#检查是否是 函数+() 的类型,譬如if(..)	
	
	left_list = [ "quote", "\'", "if", "True", "False"]
	
	if left_pos >= 1:
		if the_list[left_pos-1] in left_list :
			a=1		
			
			while (left_pos>=a) and (the_list[left_pos-a] in left_list):			
				a+=1
			return (a-1) #a-1是左端函数的个数
	
	
	
def answer_new_list_of_left(new_list): 
#处理 函数+() 的类型
	global env_dict
	
	
	if (new_list[0] == "quote") or (new_list[0] == "\'"): #引用

		for i in new_list[2:-1]:
			print(i,end=' ')			
			
	if new_list[0] == "if" :    #条件判断
		if answer_new_list(new_list[1:]):
			return("True")
		else:
			return("False")
		
	if 	new_list[0] == "True" : 
		deal_str_list( new_list[1:] )
		return("False")
		
	elif new_list[0] == "False" :
		pass
	
	
def answer_new_list(new_list):
#处理单纯的括号内部的形式，譬如(+ 2 3)、(< 2 1)
	global env_dict
	
	the_list = new_list[1:-1]
	
	for i in range( len(the_list) ): #将可以转化的都转化了
		if new_list[i+1] != None:
			try: 
				the_list[i] = int(new_list[i+1])
			except ValueError:
				try: 
					the_list[i] = float(new_list[i+1])
				except ValueError:
					the_list[i] = new_list[i+1]

				
	for i in the_list: #为了方便变量，将所有的数据都存在字典当中
		if i not in env_dict:
			env_dict.setdefault(i,i)	
		
	if the_list:
	
		if isinstance(env_dict[the_list[0]],int) or isinstance(env_dict[the_list[0]],float):  #是否是常数
			return env_dict[the_list[0]]
			
			
		if (the_list[0]=="define") or (the_list[0]=="set!"):  #给变量赋值
			env_dict[the_list[1]] = env_dict[the_list[2]]		

			
		if env_dict[the_list[0]]=="+": #四则运算
			_ = env_dict[the_list[1]]
			for i in the_list[2:]:
				_ += env_dict[i]
			return _
			
		elif env_dict[the_list[0]]=="-":	
			_ = env_dict[the_list[1]]
			for i in the_list[2:]:
				_ -= env_dict[i]
			return _

		elif env_dict[the_list[0]]=="*":	
			_ = env_dict[the_list[1]]
			for i in the_list[2:]:
				_ *= env_dict[i]
			return _

		elif env_dict[the_list[0]]=="/":	
			_ = env_dict[the_list[1]]
			for i in the_list[2:]:
				_ /= env_dict[i]
			return _

			
		if env_dict[the_list[0]]=="<":	#比较大小
			return ([the_list[1]] < [the_list[2]])		

		elif env_dict[the_list[0]]==">":	
			return ([the_list[1]] > [the_list[2]])	
						
		if env_dict[the_list[0]]=="<=":	#比较大小
			return ([the_list[1]] <= [the_list[2]])	
			
		elif env_dict[the_list[0]]==">=":	
			return ([the_list[1]] >= [the_list[2]])					
	

		if env_dict[the_list[0]]=="=":	#比较大小
			return ([the_list[1]] == [the_list[2]])		
	
			
		if the_list[0]=="display":	#print输出
			print(the_list[1][1:-1]) #去掉字符串的对应引号
		

		if the_list[0]=="newline":	#输出一个空行
			print(" ")
		

def if_left_and_right_number_equal(input_str):
#判定字符串的(和)数目是否相等

	left_number = 0
	right_number = 0
	for i in input_str:
		if i=="(":
			left_number+=1
		elif i==")":
			right_number+=1		
	
	if (left_number==right_number): #括号数目相等，返回True
		return 1
	else:
		return 0

	
def main():
		
	input_str = input()
		
	while not (if_left_and_right_number_equal(input_str)):
	#以括号数目为判定依据，多次调用input()完成多行输入
	
		input_str += ' '
		input_str += input()

	deal_str_list(  before_deal_str_list(split_input(input_str))  )

	
	
main()	
	
	
	
		
	








