
# Introduction
## Install package
```shell
pip install maimai_cat
```
## Preparation

- create file `maimai_cookies.json`

- please use Chrome Extension `EditThisCookie` to export maimai cookies to `maimai_cookies.json`



##  Example Usage:

## - Basic

```python
# 第一步: 实例化
from maimai.api import MaimaiAPI

api = MaimaiAPI().connect()

# 获取用户组
api.pretty_print(api.group.read())

# 搜索keyword,指定页码，page从0开始，最多到30 
api.pretty_print(api.search.keyword("Google", page=0))

# 获取用户信息,参数为用户id
api.pretty_print(api.user.read(41962985))

# 把用户id加入到用户组,参数为用户id和用户组id
api.pretty_print(api.group.add_user_to_group(41962985, 1323029))

# 星标用户，参数为用户id
api.pretty_print(api.group.unstar(41962985))
```

