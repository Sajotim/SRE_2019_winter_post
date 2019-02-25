import operator as op
import Eval


class DIC:
    # 对函数变量查找或增加
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


class DeFun:
    # 对'defun'自定义函数的处理
    def __init__(self, name, body, env):
        self.name = name
        self.body = body
        self.env = env

    def __call__(self, args):
        for i in range(len(self.name)):
            Eval.fac.add(self.name[i], args[i])
        return Eval.new_eval(self.body)


def fac():
    # 储存内置函数与常量
    from functools import reduce
    import math
    global fac_class
    fac_dic = {
        '+': lambda parms: reduce(op.add, [Eval.new_eval(parm) for parm in parms]),
        '-': lambda parms: reduce(op.sub, [Eval.new_eval(parm) for parm in parms]),
        '*': lambda parms: reduce(op.mul, [Eval.new_eval(parm) for parm in parms]),
        '/': lambda parms: reduce(op.truediv, [Eval.new_eval(parm) for parm in parms]),
        '<': op.lt,
        '<=': op.le,
        '>': op.gt,
        '>=': op.ge,
        '=': op.eq,
        'abs': lambda parms: list(map(abs, [Eval.new_eval(parm) for parm in parms])),
        'acos': lambda parms: list(map(math.acos, [Eval.new_eval(parm) for parm in parms])),
        'acosh': lambda parms: list(map(math.acosh, [Eval.new_eval(parm) for parm in parms])),
        'asin': lambda parms: list(map(math.asin, [Eval.new_eval(parm) for parm in parms])),
        'asinh': lambda parms: list(map(math.asinh, [Eval.new_eval(parm) for parm in parms])),
        'atan': lambda x: lambda parms: list(map(math.atan, [Eval.new_eval(parm) for parm in parms])),
        'atan2': lambda parms: list(map(math.atan2, [Eval.new_eval(parm) for parm in parms])),
        'atanh': lambda x: lambda parms: list(map(math.atanh, [Eval.new_eval(parm) for parm in parms])),
        'ceil': lambda parms: list(map(math.ceil, [Eval.new_eval(parm) for parm in parms])),
        'cos': lambda parms: list(map(math.cos, [Eval.new_eval(parm) for parm in parms])),
        'cosh': lambda parms: list(map(math.cosh, [Eval.new_eval(parm) for parm in parms])),
        'degrees': lambda parms: list(map(math.degrees, [Eval.new_eval(parm) for parm in parms])),
        'erf': lambda parms: list(map(math.erf, [Eval.new_eval(parm) for parm in parms])),
        'erfc': lambda parms: list(map(math.erfc, [Eval.new_eval(parm) for parm in parms])),
        'exp': lambda parms: list(map(math.exp, [Eval.new_eval(parm) for parm in parms])),
        'expm1': lambda parms: list(map(math.expm1, [Eval.new_eval(parm) for parm in parms])),
        'fabs': lambda parms: list(map(math.fabs, [Eval.new_eval(parm) for parm in parms])),
        'factorial': lambda parms: list(map(math.factorial, [Eval.new_eval(parm) for parm in parms])),
        'floor': lambda parms: list(map(math.floor, [Eval.new_eval(parm) for parm in parms])),
        'fmod': math.fmod,
        'frexp': lambda parms: list(map(math.frexp, [Eval.new_eval(parm) for parm in parms])),
        'gamma': lambda parms: list(map(math.gamma, [Eval.new_eval(parm) for parm in parms])),
        'gcd': math.gcd,
        'hypot': math.hypot,
        'isclose': math.isclose,
        'isfinite': math.isfinite,
        'isinf': math.isinf,
        'isnan': math.isnan,
        'ldexp': math.ldexp,
        'lgamma': lambda parms: list(map(math.lgamma, [Eval.new_eval(parm) for parm in parms])),
        'log': lambda parms: list(map(math.log, [Eval.new_eval(parm) for parm in parms])),
        'log1p': lambda parms: list(map(math.log1p, [Eval.new_eval(parm) for parm in parms])),
        'log10': lambda parms: list(map(math.log10, [Eval.new_eval(parm) for parm in parms])),
        'log2': lambda parms: list(map(math.log2, [Eval.new_eval(parm) for parm in parms])),
        'modf': lambda parms: list(map(math.modf, [Eval.new_eval(parm) for parm in parms])),
        'pow': math.pow,
        'radians': lambda x: list(map(math.radians, x)),
        'sin': lambda parms: list(map(math.sin, [Eval.new_eval(parm) for parm in parms])),
        'sinh': lambda parms: list(map(math.sinh, [Eval.new_eval(parm) for parm in parms])),
        'sqrt': lambda parms: list(map(math.sqrt, [Eval.new_eval(parm) for parm in parms])),
        'tan': lambda parms: list(map(math.tan, [Eval.new_eval(parm) for parm in parms])),
        'tanh': lambda parms: list(map(math.tanh, [Eval.new_eval(parm) for parm in parms])),
        'trunc': math.trunc,
        'PI': 3.141592653589793,
        'E': 2.718281828459045,
        'TAU': 6.283185307179586,
        'inf': math.inf,
        'nan': math.nan,
        'nil': None,
        'nilq': lambda parms: True if parms is None else False,
        'true': True,
        'false': False,
        'symbolq': lambda parms: True if parms[0] in fac_dic else False,
        'numberq': lambda parms: True if type(parms[0]) == (int, float) else True,
        'first': lambda parms: parms[0],
        'car': lambda parms: parms[0][0],
        'cdr': lambda parms: parms[0][1:],
        'not': lambda parms: op.not_(Eval.new_eval(parms[0]))
    }
    fac_class = DIC()
    fac_class.dic = fac_dic.copy()
    return fac_class
