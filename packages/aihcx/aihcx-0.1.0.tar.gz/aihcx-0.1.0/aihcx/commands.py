import json
import click
from typing import Optional
from .client import expando_to_dict, get_client, AIJobConfig
from tabulate import tabulate
import yaml
import time

def get_pool_id(pool: Optional[str] = None) -> str:
    """获取资源池ID，优先使用参数传入的值，否则使用配置文件中的值"""
    if pool:
        return pool
        
    config = AIJobConfig()
    pool_id = config.get('pool')
    if not pool_id:
        raise click.UsageError("需要指定资源池ID。可以通过 --pool 参数指定，或使用 'aihcctl config --pool <pool-id>' 设置默认值")
    return pool_id

def get_queue_name(queue: Optional[str] = None) -> str:
    """获取队列ID，优先使用参数传入的值，否则使用配置文件中的值"""
    if queue:
        return queue

    return 'default'

def get_framework_type(framework: Optional[str] = None) -> str:
    """获取框架类型，优先使用参数传入的值，否则使用默认值"""
    if framework:
        return framework

    return 'PyTorchJob'

@click.command()
@click.option('--host', help='设置API域名')
@click.option('--access-key', help='设置AK')
@click.option('--secret-key', help='设置SK')
@click.option('--pool', help='默认资源池')
@click.option('--path', help='默认文件保存路径')
@click.option('--show', is_flag=True, help='显示当前配置')
def config(host, access_key, secret_key, pool, show, path):
    """配置CLI工具"""
    config = AIJobConfig()
    
    if show:
        click.echo("当前配置:")
        click.echo(f"Pool: {config.get('pool')}")
        click.echo(f"Host: {config.get('host')}")
        click.echo(f"Access Key: {config.get('access_key')}")
        click.echo(f"Secret Key: {'*' * 8 if config.get('secret_key') else 'Not Set'}")
        return
        
    if host:
        config.set('host', host)
        click.echo(f"已设置Host: {host}")
        
    if access_key:
        config.set('access_key', access_key)
        click.echo(f"已设置Access Key: {access_key}")
        
    if secret_key:
        config.set('secret_key', secret_key)
        click.echo("已设置Secret Key")

    if pool:
        config.set('pool', pool)
        click.echo("已设置Pool")
    
    if path:
        config.set('path', path)
        click.echo(f"已设置Path: {path}")

# 列出资源池
@click.command()
def list_pool():
    """列出资源池列表"""
    client = get_client()
    res = client.get_all_pools()
    pool_list = []
    for pool in res.result.resourcePools:
        pool_dic = {
            'NAME': pool.metadata.name,
            'ID': pool.metadata.id,
            'STATUS': pool.status.phase,
            'NODE_COUNT': f"{pool.status.nodeCount.used}/{pool.status.nodeCount.total}",
            'GPU_COUNT': f"{pool.status.gpuCount.used}/{pool.status.gpuCount.total}",
            'CREATED_AT': pool.metadata.createdAt
        }
        pool_list.append(pool_dic)
        
    click.echo(tabulate(pool_list, headers="keys", tablefmt="plain"))

# 获取资源池详情
@click.command()
@click.argument('id', required=False)
def get_pool(id):
    """获取资源池详情
    
    如果不指定资源池ID，则获取默认资源池信息
    """
    client = get_client()
    
    if not id:
        # 如果没有传入ID，使用配置中的默认资源池
        config = AIJobConfig()
        id = config.get('pool')
        if not id:
            raise click.UsageError("未指定资源池ID，且未配置默认资源池。请通过参数指定ID或使用 'aihcctl config --pool <pool-id>' 设置默认值")
    
    res = client.get_pool(id)
    resource_pool = expando_to_dict(res.result)
    pool_info = yaml.dump(resource_pool, allow_unicode=True)
    click.echo(pool_info)

# 列出节点列表
@click.command()
@click.option('--pool', help='资源池ID(可选)')
def list_node(pool):
    """列出资源池节点列表"""
    client = get_client()
    pool_id = get_pool_id(pool)
    res = client.get_all_nodes(resourcePoolId=pool_id)
    nodes = res.result.nodes
    node_list = []
    for node in nodes:
        # print(node.name, node.nodeId, node.status, node.createdAt)
        # 格式化输出 node.name, node.nodeId, node.status, node.createdAt
        # print(node)
        node = expando_to_dict(node)
        node = {k.strip(): v for k, v in node.items()}
        node_info = {
            'nodeName': node['nodeName'],
            'statusPhase': node['statusPhase'],
            'instanceName': node['instanceName'],
            'instanceId': node['instanceId'],
            'gpuTotal': node['gpuTotal'],
            'gpuAllocated': node['gpuAllocated'],
            'region': node['region'],
            'zone': node['zone'],
        }
        node_list.append(node_info)
    
    click.echo(tabulate(node_list, headers="keys", tablefmt="plain")) 

# 获取队列列表
@click.command()
@click.option('--pool', help='资源池ID(可选)')
def list_queue(pool):
    """列出队列列表"""
    client = get_client()
    pool_id = get_pool_id(pool)
    res = client.get_all_queues(resourcePoolId=pool_id)
    queues = res.result.queues
    queue_list = []
    for queue in queues:
        # print(queue.name, queue.queueId, queue.status, queue.createdAt)
        # 格式化输出 queue.name, queue.queueId, queue.status, queue.createdAt
        queue_info = {
            'name': queue.name,
            'state': queue.state,
            'queueType': queue.queueType,
            'reclaimable': queue.reclaimable,
            'disableOversell': queue.disableOversell,
            'createdTime': queue.createdTime
        }
        queue_list.append(queue_info)
    
    click.echo(tabulate(queue_list, headers="keys", tablefmt="plain"))

# 获取队列详情
@click.command()
@click.argument('name', required=False)
@click.option('--pool', help='资源池ID(可选)')
def get_queue(pool, name):
    """获取队列详情"""
    client = get_client()
    pool_id = get_pool_id(pool)
    name = get_queue_name(name)
    res = client.get_queue(pool_id, queueName=name)
    queue_info = expando_to_dict(res.result)
    queue = yaml.dump(queue_info, allow_unicode=True)
    click.echo(queue)

# 获取任务列表
@click.command()
@click.option('--pool', help='资源池ID(可选)')
@click.option('--order', default='desc', help='排序方式')
@click.option('--page', default=1, help='页码')
@click.option('--size', default=10, help='每页大小')
def list_job(pool, order, page, size):
    """列出训练任务"""
    client = get_client()
    pool_id = get_pool_id(pool)
    size = int(size) if size else 50
    resp = client.get_all_aijobs(pool_id, pageSize=size)
    jobs = resp.result.jobs
    job_list = []
    for job in jobs:
        job_info = {
            'NAME': job.name,
            'ID': job.jobId,
            'STATUS': job.status,
            'CREATED_AT': job.createdAt
        }
        job_list.append(job_info)
    
    click.echo(tabulate(job_list, headers="keys", tablefmt="plain"))

# 获取任务详情
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
def get_job(id, pool):
    """获取训练任务详情"""
    client = get_client()
    pool_id = get_pool_id(pool)
    resp = client.get_aijob(pool_id, id)
    job_info = expando_to_dict(resp.result)
    job_info = yaml.dump(job_info, allow_unicode=True)
    click.echo(job_info)

# 查询任务状态
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
def get_job_status(id, pool):
    """获取训练任务状态"""
    client = get_client()
    pool_id = get_pool_id(pool)
    res = client.get_aijob(pool_id, id)
    job_info = expando_to_dict(res.result)

    job_status = [{
        'name': job_info['name'],
        'priority': job_info['priority'],
        'pool/queue': f"{job_info['resourcePoolId']}/{job_info['queue']}",
        'replicas': job_info['replicas'],
        'status': job_info['status'],
        'runningAt': job_info['runningAt'] if 'runningAt' in job_info else '--',
        'scheduledAt': job_info['scheduledAt'] if 'scheduledAt' in job_info else '--',
        'createdAt': job_info['createdAt'],
    }]
    click.echo(tabulate(job_status, headers="keys", tablefmt="plain"))

# 创建任务
@click.command()
@click.argument('name', required=False)
@click.option('--pool', help='资源池ID(可选)')
@click.option('--file', '-f', required=True, type=click.Path(exists=True), help='配置文件路径')
def create_job(name, pool, file):
    """创建训练任务"""
    client = get_client()
    pool_id = get_pool_id(pool)
    
    with open(file) as f:
        config = json.load(f)
        # click.echo(json.dumps(config, indent=2, ensure_ascii=False))
    
    if name:
        config['name'] = name
    client_token = str(int(time.time()))
    res = client.create_aijob(client_token, pool_id, config)
    result = expando_to_dict(res.result)

    click.echo(yaml.dump(result, allow_unicode=True))

# 删除任务
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
def delete_job(id, pool):
    """删除训练任务"""
    client = get_client()
    pool_id = get_pool_id(pool)
    res = client.delete_aijob(pool_id, id)
    job_info = expando_to_dict(res.result)
    job_info = yaml.dump(job_info, allow_unicode=True)
    click.echo(job_info)

# 停止任务
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
def stop_job(id, pool):
    """停止训练任务"""
    client = get_client()
    pool_id = get_pool_id(pool)
    try:
        res = client.stop_aijob(pool_id, id)
        job_info = expando_to_dict(res.result)
        job_info = yaml.dump(job_info, allow_unicode=True)
        click.echo(job_info)
    except Exception as e:
        click.echo(f"停止任务失败: {e}")

# 更新任务
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
@click.option('--priority', required=True, type=click.Choice(['high', 'normal', 'low']), help='优先级')
def update_job(id, pool, priority):
    """更新训练任务"""
    client = get_client()
    pool_id = get_pool_id(pool)
    result = client.update_job(pool_id, id, priority)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))

# 导出任务配置
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
@click.option('--path', help='保存路径')
def job_export(id, pool, path):
    """导出任务配置"""
    client = get_client()
    pool_id = get_pool_id(pool)
    resp = client.get_aijob(pool_id, id)
    job_info = expando_to_dict(resp.result)

    new_job_info = {
    "queue": "",
    "priority": "",
    "jobFramework": "",
    "name": "",
    "jobSpec": {
      "command": "",
      "image": "",
      "replicas": 0,
      "resources": [
        {
          "name": "baidu.com/a800_80g_cgpu",
          "quantity": 8
        }
      ],
      "enableRDMA": True,
      "envs": [
        {
          "name": "CUDA_DEVICE_MAX_CONNECTIONS",
          "value": "1"
        }
      ]
    },
    "datasources": [
      {
        "type": "pfs",
        "name": "",
        "mountPath": "/mnt/cluster"
      }
    ]
  } 
    new_job_info['name'] = job_info['name']
    new_job_info['queue'] = job_info['queue']
    new_job_info['priority'] = job_info['priority']
    new_job_info['jobFramework'] = 'PyTorchJob' if job_info['jobFramework'] == 'pytorch' else ''
    new_job_info['jobSpec']['command'] = job_info['command']
    new_job_info['jobSpec']['image'] = job_info['image']
    new_job_info['jobSpec']['replicas'] = job_info['replicas']
    new_job_info['jobSpec']['resources'] = job_info['resources']
    new_job_info['jobSpec']['enableRDMA'] = job_info['enableRDMA']
    new_job_info['jobSpec']['envs'] = job_info['envs']
    # 过滤掉"type": "emptydir"的数据
    datasources = job_info['datasources']
    datasources = [datasource for datasource in datasources if datasource['type'] != 'emptydir']
    new_job_info['datasources'] = datasources

    # 保存为JSON文件
    filename = f"{job_info['name']}-export.json"
    path = AIJobConfig().get('path') if not path else path
    if path:
        filename = f"{path}/{filename}"
        with open(filename, 'w') as f:
            json.dump(job_info, f, indent=2, ensure_ascii=False)
        
        new_job_info_filename = f"{path}/{new_job_info['name']}-copy.json"
        with open(new_job_info_filename, 'w') as f:
            json.dump(new_job_info, f, indent=2, ensure_ascii=False)

        click.echo(f"已导出配置到文件: \n原始任务信息：{filename}\n复制任务信息：{new_job_info_filename}")
    else:
        click.echo('未设置默认保存路径，请通过"--path"指定保存路径或"aihcctl config --path <path>" 设置默认路径')

# 查看任务日志
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
@click.option('--podname', required=True, help='Pod名称')
def job_logs(id, pool, podname):
    """查看任务日志"""
    client = get_client()
    pool_id = get_pool_id(pool)
    resp = client.get_aijob_logs(pool_id, id, podname)
    logs = expando_to_dict(resp.result)
    click.echo(yaml.dump(logs, allow_unicode=True))

def get_job_events(id, pool, framework):
    """查询任务事件"""
    client = get_client()
    pool_id = get_pool_id(pool)
    framework = get_framework_type(framework)
    resp = client.get_aijob_events(pool_id, id, framework)
    events = expando_to_dict(resp.result)
    click.echo(yaml.dump(events, allow_unicode=True))

def get_aijob_pod_events(id, pool, podName, jobFramework):
    """查询任务事件"""
    client = get_client()
    pool_id = get_pool_id(pool)
    res = client.get_aijob_pod_events(pool_id, id, podName, jobFramework)
    pod_events = expando_to_dict(res.result)
    click.echo(yaml.dump(pod_events, allow_unicode=True))

# 查询任务事件
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
@click.option('--framework', required=False, help='训练任务框架类型，当前支持 "PyTorchJob"')
@click.option('--podname', required=False, help='Pod名称')
def job_events(id, pool, framework, podname):
    """查询任务事件"""
    pool_id = get_pool_id(pool)
    framework = get_framework_type(framework)
    if podname is not None:
        get_aijob_pod_events(id, pool_id, podname, framework)
    else:
        get_job_events(id, pool_id, framework)

# 列出任务的Pod列表
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
def list_pod(id, pool):
    """列出任务的Pod列表"""
    client = get_client()
    pool_id = get_pool_id(pool)
    resp = client.get_aijob(pool_id, id)
    pods = resp.result.podList.pods
    pod_list = []
    for pod in pods:
        pod_info = {
            'replicaType': pod.replicaType,
            'name': pod.objectMeta.name,
            'namespace': pod.objectMeta.namespace,
            'podPhase': pod.podStatus.podPhase,
            'status': pod.podStatus.status,
            'creationTimestamp': pod.objectMeta.creationTimestamp
        }
        pod_list.append(pod_info)
    click.echo(tabulate(pod_list, headers="keys", tablefmt="plain"))

# 连接到任务实例
@click.command()
@click.argument('id')
@click.option('--pool', help='资源池ID(可选)')
@click.option('-it', '--interactive', is_flag=True, help='交互式终端')
@click.option('--podname', required=True, help='Pod名称')
@click.option('-c', '--container', help='容器名称')
@click.argument('cmd', nargs=-1)
def job_exec(id, pool, interactive, podname, container, cmd):
    """连接到任务实例"""
    client = get_client()
    pool_id = get_pool_id(pool)
    resp = client.get_webterminal(pool_id, id, podname)
    terminal_info = expando_to_dict(resp.result)
    click.echo(yaml.dump(terminal_info, allow_unicode=True))
