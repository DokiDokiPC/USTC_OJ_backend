# Users

### GET /users/\<string:username\>

获取当前用户信息

**jwt_required**

##### success

```json
jsonify(current_user), 200-OK
```

##### error

```json
['err_msg', ...]
```

### POST /users

创建一个新用户

##### request

```json
{'username': 'xxx', 'password': 'xxx', 'email': 'xxx'}
```

##### success

```json
201-CREATED
```

##### error

```json
['err_msg', ...]
```

### POST /users/\<string:username\>

更新当前用户信息

**jwt_required**

##### request

```json
{'password': 'xxx'}
```

##### success

```json
200-OK
Set-Cookie: access_token_cookie=new_jwt, OK, if password changed
```

##### error

```json
['err_msg', ...]
```

### DELETE /users/\<string:username\>

删除当前用户

**jwt_required**

##### success

```json
204-NO_CONTENT
```

##### error

```json
['err_msg', ...]
```

# Tokens

### POST /tokens

获取一个JWT

##### request

```json
{'username': 'xxx', 'password': 'xxx'}
```

##### success

```json
200-OK, Set-Cookie: access_token_cookie=jwt
```

##### error

```json
['err_msg', ...]
```

### DELETE /tokens

删除JWT

##### success

```json
200-OK, Set-Cookie: access_token_cookie=;
```

### HEAD /tokens

测试是否登录

##### success

```json
200-OK
```

##### error

```json
401-UNAUTHORIZED
```
