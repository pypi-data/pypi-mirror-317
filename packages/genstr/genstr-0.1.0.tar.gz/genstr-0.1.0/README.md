# pygenstr

按指定规则生成字符串。   

<a href="https://pypi.org/project/genstr" target="_blank">
    <img src="https://img.shields.io/pypi/v/genstr.svg" alt="Package version">
</a>

<a href="https://pypi.org/project/genstr" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/genstr.svg" alt="Supported Python versions">
</a>

## 特征
1. 可生成 **纯数字**
2. 可生成 **纯字母**、
3. 可生成 **纯数字+纯字母**
4. 可生成 **数字与字母混合**
5. 可生成 **排除纯数字和纯字母**
6. 可生成 **自定义字符**
7. 可生成 **自定义字符（排除纯数字和纯字母）**
8. 可生成 **自定义字符（纯数字和纯字母）**

## 使用
```python
from genstr import Genstr
from genstr import Mode

list = Genstr(
    length: int,
    mode: Mode = Mode.PURE_NUMBERS,
    alphabets: str = '',
    prefix: str = '',
    suffix: str = '',
    is_range: bool = False
).combine().list()

print(type(list), list)
```

```bash
<class 'list'>
[]
```

|参数|类型|默认值|描述|
|:---|:---|:---|:---|
| `length` | int | 无 | 组合长度 |
| `mode` | `Mode`（枚举） | Mode.PURE_NUMBERS | 域名组合模式: <br/>1. 纯数字 2. 纯字母 3. 纯数字+纯字母 4. 数字与字母混合 5. 排除纯数字和纯字母 6. 自定义字符 7. 自定义字符（排除纯数字和纯字母） 8. 自定义字符（纯数字和纯字母）|    
| `alphabets` | str | 空 | 自定义组合字母表，mode 6/7/8 必填      
| `prefix` | str | 空 | 组合前缀，如 -P a，则生成 a*
| `suffix` | str | 空 | 组合后缀，如 -S z，则生成 *z
| `is_range` | bool | False | 范围，如长度为 3 时，则范围为 1-3 内的数据

## 仓库镜像

- https://git.jetsung.com/idev/pygenstr
- https://framagit.org/idev/pygenstr
- https://gitcode.com/idev/pygenstr
- https://github.com/idevsig/pygenstr