# agent-team-sandbox

软件研发 Agent Team 的第一个项目仓库。团队方案在另一个仓库里；这个仓库是被开发的软件。

当前只有一个最小 HTTP 服务，用来走通「分支、Pull Request、测试、密钥扫描、本机 Compose」。

## 本地运行

```bash
docker compose up --build
```

服务监听 `http://localhost:8080/health`。启动和每次请求都把一行 JSON 日志打到标准输出，其中包含 `version`。

## 测试

```bash
PYTHONPATH=src python -m pytest
```
