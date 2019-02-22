 
## 目录：

+ 对lisp的基本了解
+ 写一个解释器的框架
+ 代码实现的功能
+ Q&A
+ 一点体会


### 对lisp的基本了解：
####lisp的特点
>1.lisp是一种表处理语言，列表是它的主要数据结构，lisp编码也主要是利用列表.
>2.lisp代码计算过程:
>- 读取器转换字符到lisp对象— s表达式（由三个有效对象：原子、列表、字符串组成）
>- 求值器定义将s表达式转化为lisp内置的语法形式(lisp形式可以是一个原子、空或非名单、有符号作为他的第一个元素的任何列表)
>
>3.lisp尝试计算一切，包括函数的参数和列表的成员
4.lisp通常使用前缀表达式
>5.lisp特有的一类元素称之为符号，当定义一个函数或者一个变量时，他们的内容会指向一个符号。符号形如‘a，而符号会被lisp解释器直接指向存储器的位置



​
####lisp的七个基本操作符

> 0.(quote a) or（’a）返回a值
1.(atom x)当x是一个atom或者空的list时返回原子t，否则返回NIL
2.(eq x y)当x和y指向相同的对象的时候返回t，否则返回NIL
3.(car x)要求x是一个表，它返回x中的第一个元素
4.(cdr x)同样要求x是一个表，它返回x中除第一个元素之外的所有元素组成的表
5.(cons x y)返回一个cons cell(x y)
6.(cond (p1 e1) ...(pn en))的求值规则如下。对“条件表达式p”依次求值直到有一个返回t.如果能找到这样的p表达式，相应的“结果表达式e”的值作为整个cond表达式的返回值

####lisp的变量

1.全局变量

```

(defvar var val)
or
(setq var val)
```

全局变量有永久值在整个lisp系统

2.局部变量

 ```
 (let((var1 val1)(var2 val2)(var3 val3))<s-expression>)
```
在计算s表达式时，用let结构创建局部变量，每个变量被分配各自的值
 
####lisp的条件和选择
1.cond
```

(cond(test1 action1)(test2 action2)......)
```

依次检查每个子句条件,如果为真则执行该条件下的action,并返回相应的值;如果是nil,则继续下一个子句的条件扫描
2.if
```
(setq a 10)(if(> a 20)then(format t"~% a is less than 20"))(format t "~% value of a is ~d"a)
```

返回结果是 
> a is less than 20 value of a is 20


#### lisp函数
命名函数宏用于定义函数,defun的语法是
```

(defun fun_name(parameter-list)body)
```



### lisp语言解释器的框架

一个语言解释器包括两部分:解析和执行
![图片1.png](https://upload-images.jianshu.io/upload_images/15605979-b343bd6ab1226d40.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##### - 解析:
(解析部分接收输入,将输入翻译成中间表示.中间表示一般是一种树结构,反映了源程序中表达式的嵌套结构.)

 
- 分解: 词法分析

将输入的字符串分解成一些词法单元
1. 在程序中tokens是token的列表,tokens是按照输入顺序排列的.分解的过程将输入划分成一个个小单元,并判定了这些小单元的类型
![图片4.png](https://upload-images.jianshu.io/upload_images/15605979-28c49284bc3f0d92.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

例如
```
set[a[+ 4 5]]
log a
```

由分解后,成为![图片2.png](https://upload-images.jianshu.io/upload_images/15605979-45fff935f5798d44.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



- 组织:语法分析

将词法单元组织成中间表示:抽象语法树![图片5.png](https://upload-images.jianshu.io/upload_images/15605979-6e85ee2a4e3bb582.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


语法分析的实现:

组织中有一个重要的过程是要记录数据结构,也就是建造抽象语法树
中括号从一个符号变成了具有抽象意义.
```

token_array = []
```
```
 elif e == '[':

            v, break_index = parser(tokens[i+1:])   #使用parser的递归来脱去括弧返回一个列表   
  
            

            counter = break_index

            token_array.append(v)

```

```
return token_array, break_index
```


#####- 执行:
接收抽象语法树.封装函数,实现模块的调用![图片7.png](https://upload-images.jianshu.io/upload_images/15605979-145c8da3f60f947c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



interpreter的作用是循环遍历抽象语法树,调用各类函数,对变量的存储和调用,最终返回一个计算结果.
###代码实现功能

1.基本的算术运算和数值比较(+-*/><!=)
2.变量赋值和函数定义
3.条件判断语句(if)
4.结果输出

###Q&A

##### -变量如何存储?如何调用变量的值?

变量存储在一个名为var的字典中 .为了保证变量赋值和调用的及时准确,因此每当向具有执行功能的函数中传入参数时,都要讲该字典一并传入函数中.调用也就是在字典中进行查找key.

```
def apply_op(tokens, vars):
```
```
def apply_compare(tokens, vars):
```

#####- 在算术运算和比较大小时,由于对象可能是token类(定义的词法单元)中的数字、变量,也有可能是一个list,那么如何做到同统一?

写一个函数,分别处理这三种操作数.如果是数字,就将token类转换为int型,变量涉及到取值.如果是list,一个可以求值的表达式,那么继续调用interpreter函数来求出子树的结果.统一的好处是简洁,也符合了操作符最终处理对象是int型的规则.
#####- 如何定义函数并记录函数体?如何实现函数调用并向参数传递数值?
由于函数和变量的相似,都有名称和值两部分,定义后全局有效.在和全局变量相同的字典中存进函数名和函数值(函数的参数列表和函数体).![图片8.png](https://upload-images.jianshu.io/upload_images/15605979-fb4e670877e1e1bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
函数的调用需要通过匹配实现,哪一部分是函数名,哪一部分是参数列表,函数体.![图片9.png](https://upload-images.jianshu.io/upload_images/15605979-d90040e6084424c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在调用函数时,一是要进行参数传递:写一个绑定函数,传递参数列表和实际值的列表,完成一一对应的绑定.作为局部变量存储在临时的字典中,再将这个字典和全局变量的字典进行合并;二是要进入函数体,实际上也就是调用interpreter.

#####- 在执行表达式时,表达式中既有操作符又有操作数,如何区分?如何实现操作符代表的功能?

由于每个表达式的第一个元素只可能是:算术运算符,比较符,关键字,变量名,函数名,这些我统称为操作符.在处理表达式时,只需要拿到第一个元素,根据操作符映射到相应的功能函数(字典实现),再调用.

#####- 在解释器的框架中可不可以不转化为词法单元(token类)?
不能.变成tokens的过程,就是给输入的每个字符判定类型的过程.同时,让他们都归属于相同的token类,统一的好处是便于执行时的判断这是一个子树还是叶子节点.子树的类型是list,叶节点的类型是token类.





###一点体会

这个解释器让我联系到我们手动计算时体现的步骤:我们拿到一个函数或者表达式,也是先整体扫描,每个符号也才有了意义(解析为词法单元);然后我们有顺序的计算,这就好像执行语法树;而根据我们已知的规则在脑海中形成计算先后顺序的结构,就像构建语法树的过程.因此,语法树作为数据结构能够将操作符和操作数有层次的联系起来,使原来的表达式具有结合性和优先性.在执行时,和函数调用的关系是从上下遍历,每一个节点就进入一个interpreter中特定的函数,如果有子树就继续调用interpreter.计算是在遍历过程之后,从叶节点开始向上走的.

######p.s.
刚看到题目时,表示完全不懂.然后逐渐了解有关lisp和解释器的一点东西,代码参考了GitHub上有关python实现lisp解释器的代码.在完成的过程中,熟悉了python的语法(在类中定义魔法方法,通过字典进行存储和查找,通过字典实现映射,利用python传递值和返回值的自由进行匹配……);熟悉了写一个解释器的基本框架;对语法树有一定的理解.本篇写的冗长,但对于自己的理解进行输出还是很有帮助的.
