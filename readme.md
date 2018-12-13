
# travis 私钥管理

## 安装
```bash
sudo gem install travis
```

## 登录
```bash
travis login --pro  # travis-ci.com

travis login --org  # travis-ci.org
```

## 上传秘钥
在工程目录里面执行
```bash
travis encrypt-file '<your private key paty>' --add
```