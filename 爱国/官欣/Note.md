## 2查询方式

1. 集成工具

   shell: whois/pwhois

   python: python-whois(直连TCP :43)

2. 网站解析（单/批量）：

   a.html静态爬虫

   - 西部数码 https://www.west.cn/jiaoyi/ #批量模式不支持`.gs`
   - 站长之家 http://whois.chinaz.com/  #批量，POST,js隐藏
   - http://secure.nic.gs/index.php #验证码

   b.api

   - 万网 http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=doucube.com #仅注册与否、不支持`.gs`
   - https://www.whoisxmlapi.com/  #收费/免费x500

#### 备注：

- 不同根域名返回的whois格式不同
- API接口每天查询量约100条，有付费版本。
- 需要ICANN支持？
- 批量查询: 扫米工具

|                                        | 免费     | 价格       |
| -------------------------------------- | ------ | -------- |
| https://www.jisuapi.com/api/whois/     | 1K     | 49/10K   |
| http://api.chinaz.com/ApiDetails/Whois | 0.5K   | 50/10K   |
| http://www.91cha.com/api/whois.html    | 50/day | 99/20K.. |

支持.gs?

- http://www.whoisip.cn/love.gs  #可BS4直接解析
- http://whois.ac/love.gs  #有缓存,最新验证码,返回raw
- https://t.caozha.com/ymgq/sm.php?q=idn.gs  #返回<tr>标签：[域名,注册日期,过期日期]

## 3 流程

#### B.var_HTTP

> 参考流程图

req_var_HTTP: 获取静态页面HTML，通过BS4解析后查找出<ul>下对应<label> 的<span>信息。存入二维列表后输出到文件。

```html
<body>
  <div class="page">
    <div class="content">
      <ul>
        list..here
      </ul>
    </div>
    <div class="content">
      raw..here
    </div>
  </div>
</body>
```

compute_time: 通过获取文件中每行的时间字符串，解析为`datetime.datetime`类，与生成的`datetime.now()` 运算，返回相差天数。并映射到字典中，按照`value` 升序排序后添加到行首，输出文件

send_var_SMTP: 配置SMTP后发送计算生成的文件附件。

#### A.var_module

DictCreator: 调用`itertools.product` 生成二维全排列列表，处理后写入`list.txt`

Lookup_var_module_multi: 尝试打开`existed.txt` ,使用数值标记存在条目后，逆序剔除掉原始序列中标记出的项。再进行多进程查询，附加到`existed.txt` 中。如果是第一次，不会剔除项。（多进程未加锁顺序随机）

## 4 错误解决

1) `readlines()`读取多行文件时，字串末尾有'\n'

#### B.var_HTTP

##### 1) bs4匹配结构时，使用常量确定信息位置

```python
wlist.append([lis[i].contents[2].string for i in (1,3,8)])
```

出现数据错位，超出索引范围等

措施：通过HTML结构特征每一条数据的平行节点<label> 确定，若未索引出完整数据判断为'Available'。

##### 2）bs4 解析时，单标签<br> 无法获取

措施：

```python
html.replace('<br>','\n')	#</br>,<br/>
```

##### 3) 计算时间差时，使用时间差为主键，数据为值，导致同样时间差出现覆盖

措施：

互换键-值顺序，数据为主键（唯一），时间差为值。并按值排序

#### A.var_module 

##### 4) 程序员碰到了一个问题，他决定用多进程解决。现在两个他问题了有

输出结果顺序混乱，出现错误无法确定数据索引。

措施（待定）：

通过将字母视作`26进制` 唯一确定位置，进行标记。使用运行中途生成的数据标记，筛选出未查询数据。进行多次运行补全列表。