## 我的Lisp解释器（`MyNewLisp`）:

#### 主要完成功能：

`MyNewLisp`是一个简易的Lisp解释器，主要实现了以下功能：

1. 对表达式求值，并且表达式可以嵌套。

   ```lisp
   In[1]:  (+ (* 3 4) (-3 2) (/ 3 2))
   Out[1]: 14.5
   In[2]:  (* PI (* 3 3))
   Out[2]: 28.274333882308138
   ```

2. 变量定义。

   ```lisp
   In[3]:  (setf A (+ 3 3))
   Out[3]: 6
   ```

3. 函数定义使用。

   ```lisp
   In[4]:  (defun A (lambda (x) (+ x 3)))
   ```

4. if语句等。

   ```lisp
   In[5]:  (if (> 3 1) (+1 2) (- 1 2))
   ```

   。。。。。。

#### 程序简要分析：

`MyNewLisp`程序由以下部分组成：

- `Read`：分析输入内容,建立抽象语法树

- `FnAndCon`：实现Lisp环境内置函数并定义内置常量

- `Eval`：负责执行相关语句

- `InAndOut`：实现输入输出功能

  

`Read`:

​      输入的字符串先经过`tokenize`处理得到由token组成的列表。

```python
def tokenize(inp_str):
    return inp_str.replace('(', ' ( ').replace(')', ' ) ').split()
```

​      接下来创建`READ`对象：

```python
class READ:
    def __init__(self, tokens, position=0):
        self.tokens = tokens
        self.position = position

    def now(self):
        return self.tokens[self.position]

    def next(self):
        self.position += 1
        return None
```

​     `tokens`为处理好的`list`,`position`指向`list`当前的位置，`now`函数返回当前位置的`token`，`next`使位置加1。`tokens`被送入`read_tokens`函数中，对每一个token进行处理，用正则表达式匹配输入，转换成相应的`str`.`int`.`float`.`True`.`False`.`None`等类型，同时把`lisp`中的`list`转换为`python`中的`list`。

 `FnAndCon`:

​      此文件主要包括两个类。`DIC`主要为`Lisp`相关函数和变量常量的储存和查找，`add`方法用于增加自定义的变量和函数定义，`find`用于查找定义，如果内层查找找不到就跳转到外层查找。

```python
class DIC:
    def __init__(self, key=None, value=None, outer=None):
        self.dic = dict()
        self.outer = outer

    def add(self, key, value):
        self.dic[key] = value
        return self.dic[key]

    def find(self, key):
        if key in self.dic:
            return self.dic
        elif self.outer is not None:
            return self.outer.find(key)
        else:
            return None
```

`DeFun`用于自定义函数。当用户定义的函数被调用时，将直接调用`__call__方法`处理。

```Python
class DeFun:
    def __init__(self, name, body, env):
        self.name = name
        self.body = body
        self.env = env

    def __call__(self, *args):
        Eval.fac.add(self.name, args)
        return Eval.new_eval(self.args)
```

在函数`fac(Functions And Consts)`中，将所有内置函数与常量以字典形式存储，为方便函数调用，使用了`operator`模块，为进行多个参数的处理，使用`map`.`reduce`等高阶函数。

`Eval`:

​     此文件主要对输入的命令调用`FnAndcon`内的方法变量并且执行。同时处理`if`.`quote`等命令。

`InAndOut`:

​     `io`函数负责控制输入输出环境，`new_out`用于处理输出，把`Python`的列表的形式改为`Lisp`的风格。

#### 感受：

​     自学了两个礼拜，写了一个多星期，我的第一个`Lisp`解释器终于完成了（原谅我太笨）。。。刚看到题目时，连解释器是什么都还不知道，`Lisp`都没有听过。。。然后然后`Baidu`各种查资料，一点一点，最终就写成了这样子。。虽然感觉还很粗糙，很多功能没有实现。。。。

​     这次作业最大的收获在于很多自己一开始感觉很难的知识学下来感觉也并没有那么难，学下来也还是能学懂一些的。还有就是感觉自己的`Python`真熟练了不少。。。



​     



​     

