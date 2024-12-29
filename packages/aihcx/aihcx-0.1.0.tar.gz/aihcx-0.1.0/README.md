# AI训练平台命令行工具

一个用于管理AI训练平台的命令行工具。

## 使用源码安装

```bash
pip install -r requirements.txt
pip install -e .
```

## 打包发布

### 打包和安装

1.	本地打包
    在项目根目录下运行：
    ```
    python setup.py sdist
    ```
    
    打包后的文件会保存在 dist/ 目录中，例如：dist/aihcx-0.1.0.tar.gz。

2.	本地安装
    使用 pip 安装：

    ```
    pip install dist/aihcx-0.1.0.tar.gz
    ```

3.	运行工具
    安装完成后，运行：
    ```
    aihcx
    ```

### 发布新版本

1. 更新版本号
   编辑 setup.py 中的 version 字段

2. 创建新的 tag
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

3. 构建分发包
   ```bash
   # 安装构建工具
   pip install build wheel
   
   # 构建源码包和wheel包
   python setup.py sdist bdist_wheel
   ```

4. 发布到PyPI（可选）
   ```bash
   # 安装发布工具
   pip install twine
   
   # 检查分发包
   twine check dist/*
   
   # 上传到 PyPI
   twine upload dist/*
   ```

   或者创建 GitHub Release，CI 会自动发布到 PyPI。

5. 安装新版本
   ```bash
   pip install --upgrade aihcx
   ```

### 发布到 PyPI（可选）
	
1.	安装 twine：
    ```
    pip install twine
    ```

2.	上传到 PyPI：
    ```
    twine upload dist/*
    ```

3. 发布后，用户可以通过以下命令直接安装：
    ```
    pip install aihcx
    ```

## 配置

### 基本配置

首次使用前需要配置认证信息:

```bash
# 设置配置信息
aihcx config \
    --host https://aihc.bj.baidubce.com \
    --access-key <your-access-key> \
    --secret-key <your-secret-key> \
    --pool <default-pool-id>

# 查看当前配置
aihcx config --show
```

### 命令补全

安装命令自动补全支持：

```bash
# 对于 zsh
aihcx completion zsh >> ~/.zshrc
source ~/.zshrc

# 对于 bash
aihcx completion bash >> ~/.bashrc
source ~/.bashrc

# 对于 fish
aihcx completion fish > ~/.config/fish/completions/aihcx.fish
```

补全支持：
- 命令补全（Tab键）
- 子命令补全
- 参数名补全
- 资源名补全（部分支持）

## 使用方法

所有命令都支持 `--help` 选项查看详细帮助信息。

### 训练任务管理

```bash
# 创建任务
aihcx job create <job-name> -f job.json  # 从配置文件创建任务

# 查看任务列表
aihcx job list  # 列出所有任务
aihcx job list --pool <pool-id>  # 指定资源池的任务
aihcx job list --page 2 --size 20  # 分页查询
aihcx job list --order desc  # 按时间降序排列

# 获取任务详情
aihcx job get <job-id>  # 获取任务详情
aihcx job status <job-id>  # 获取任务状态

# 任务操作
aihcx job delete <job-id>  # 删除任务
aihcx job update <job-id> --priority high  # 更新任务优先级(high/normal/low)

# 任务日志和终端
aihcx job logs <job-id> --podname <pod-name>  # 查看任务日志
aihcx job exec <job-id> --podname <pod-name> [command]  # 连接到任务实例
aihcx job exec <job-id> --podname <pod-name> -it bash  # 交互式终端

# 导出任务配置
aihcx job export <job-id>  # 导出任务配置到文件
```

### 资源池管理

```bash
# 查看资源池列表
aihcx pool list  # 显示所有资源池

# 获取资源池详情
aihcx pool get [pool-id]  # 不指定ID时使用默认资源池
```

### 队列管理

```bash
# 查看队列列表
aihcx queue list  # 显示所有队列
aihcx queue list --pool <pool-id>  # 指定资源池的队列

# 获取队列详情
aihcx queue get [queue-name]  # 不指定名称时使用default队列
aihcx queue get <queue-name> --pool <pool-id>  # 指定资源池的队列
```

### 节点管理

```bash
# 查看节点列表
aihcx node list  # 显示所有节点
aihcx node list --pool <pool-id>  # 指定资源池的节点
```

### Pod管理

```bash
# 查看Pod列表
aihcx pod list <job-id>  # 显示任务的所有Pod
```

### 命令格式说明

命令遵循以下格式:
```bash
aihcx [TYPE] [COMMAND] [NAME] [FLAGS]
```

- TYPE: 资源类型，如 job、pool、node、queue、pod
- COMMAND: 操作命令，如 create、list、get、delete 等
- NAME: 资源名称（部分命令需要）
- FLAGS: 命令参数

## 环境变量支持

可以通过环境变量设置常用配置：

```bash
export AIHC_HOST=https://aihc.bj.baidubce.com
export AIHC_ACCESS_KEY=your-access-key
export AIHC_SECRET_KEY=your-secret-key
export AIHC_DEFAULT_POOL=your-default-pool
```

## 注意事项

1. 请妥善保管AK/SK密钥对
2. 建议设置默认资源池，简化命令使用
3. 使用自动补全提高效率
4. 大型任务配置建议使用配置文件
5. 导出任务配置后可用于快速复制任务
6. 使用 --help 查看每个命令的详细用法

## 项目结构

```
aihcx-cli/
├── README.md           # 本文档
├── requirements.txt    # 依赖包
├── setup.py           # 安装配置
└── aihcx/             # 源代码
    ├── __init__.py    # 包初始化
    ├── cli.py         # CLI入口
    ├── commands.py    # 命令实现
    └── client.py      # API客户端
```
