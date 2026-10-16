# 微信公众号机器人 Webhook

## 这是什么

一个简单的 Python 服务，接收微信公众号推送的用户消息并自动回复。
微信后台把用户消息 POST 到这个服务的 `/wechat` 地址，服务处理后返回回复内容。

## 本地运行（测试用）

```bash
cd ~/workspace/wechat-bot
pip install -r requirements.txt
TOKEN=你的token python app.py
```

服务会监听 5000 端口，地址是 `http://localhost:5000/wechat`。

## 部署到公网（微信要求）

微信要求配置的 URL 必须是公网可访问的。推荐用免费平台：

### 方案一：Railway（推荐新手）

1. 把代码推到 GitHub
2. 打开 https://railway.app ，用 GitHub 登录
3. New Project → Deploy from GitHub repo，选择这个仓库
4. 在 Variables 里加：`TOKEN=你自己定的token`（比如 `nova123456`）
5. 部署完成后，Railway 会给一个公网域名，如 `xxx.up.railway.app`
6. 微信后台 URL 填：`https://xxx.up.railway.app/wechat`

### 方案二：自己的云服务器

```bash
TOKEN=你的token gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

配合 Nginx 反向代理 + HTTPS 证书（可用 Let's Encrypt 免费证书）。

## 微信后台配置

1. 登录 https://mp.weixin.qq.com
2. 左侧菜单：开发 → 基本配置 → 服务器配置 → 修改配置
3. 填写：
   - **URL**：`https://你的域名/wechat`
   - **Token**：和部署时设置的 TOKEN 一致
   - **EncodingAESKey**：点“随机生成”
   - **消息加解密方式**：选“明文模式”（最简单）
4. 点提交，微信会发验证请求，服务返回正确就会显示“配置成功”
5. 最后点“启用”服务器配置

## 下一步：接入 AI 回复

现在机器人只会按关键词回复。想让它用 AI 智能回复，
把 `app.py` 里 `handle_message` 函数的逻辑换成调用大模型 API 即可。
