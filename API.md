# Users

### GET /users/\<string:username\>

获取当前用户信息

**jwt_required**

##### success

```
jsonify(current_user), 200-OK
```

##### error

```
['err_msg', ...]
```

### POST /users

创建一个新用户

##### request

```
{'username': 'xxx', 'password': 'xxx', 'email': 'xxx'}
```

##### success

```
201-CREATED
```

##### error

```
['err_msg', ...]
```

### POST /users/\<string:username\>

更新当前用户信息

**jwt_required**

##### request

```
{'password': 'xxx'}
```

##### success

```
200-OK
Set-Cookie: access_token_cookie=new_jwt, OK, if password changed
```

##### error

```
['err_msg', ...]
```

### DELETE /users/\<string:username\>

删除当前用户

**jwt_required**

##### success

```
204-NO_CONTENT
```

##### error

```
['err_msg', ...]
```

# Tokens

### POST /tokens

获取一个JWT

##### request

```
{'username': 'xxx', 'password': 'xxx'}
```

##### success

```
200-OK, Set-Cookie: access_token_cookie=jwt
```

##### error

```
['err_msg', ...]
```

### DELETE /tokens

删除JWT

##### success

```
200-OK, Set-Cookie: access_token_cookie=;
```

### HEAD /tokens

测试是否登录

##### success

```
200-OK
```

##### error

```
401-UNAUTHORIZED
```
