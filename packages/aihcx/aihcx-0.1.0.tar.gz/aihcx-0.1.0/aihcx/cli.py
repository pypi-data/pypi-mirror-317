import click
from . import commands
import os

@click.group()
def cli():
    """AI训练平台命令行工具"""
    pass

@cli.command()
@click.argument('shell', required=False, type=click.Choice(['bash', 'zsh', 'fish']))
def completion(shell=None):
    """生成自动补全脚本"""
    if not shell:
        shell = os.environ.get('SHELL', '').split('/')[-1]
        if shell not in ['bash', 'zsh', 'fish']:
            click.echo("无法检测到shell类型，请手动指定: aihcx completion [bash|zsh|fish]")
            return
            
    if shell == 'bash':
        click.echo("""
eval "$(_AIHCX_COMPLETE=bash_source aihcx)"
""")
    elif shell == 'zsh':
        click.echo("""
eval "$(_AIHCX_COMPLETE=zsh_source aihcx)"
""")
    elif shell == 'fish':
        click.echo("""
eval (env _AIHCX_COMPLETE=fish_source aihcx)
""")

# 创建job子命令组
@cli.group()
def job():
    """训练任务管理"""
    pass

# 创建pool子命令组
@cli.group()
def pool():
    """资源池管理"""
    pass

# 创建queue子命令组
@cli.group()
def queue():
    """队列管理"""
    pass

# 创建node子命令组
@cli.group()
def node():
    """节点管理"""
    pass

# 将命令添加到job子命令组
job.add_command(commands.list_job, name='list')
job.add_command(commands.get_job, name='get')
job.add_command(commands.create_job, name='create')
job.add_command(commands.delete_job, name='delete')
job.add_command(commands.update_job, name='update')
job.add_command(commands.stop_job, name='stop')
job.add_command(commands.get_job_status, name='status')
job.add_command(commands.job_logs, name='logs')
job.add_command(commands.job_exec, name='exec')
job.add_command(commands.job_export, name='export')
job.add_command(commands.list_pod, name='pods')
job.add_command(commands.job_events, name='events')

# 将命令添加到pool子命令组
pool.add_command(commands.list_pool, name='list') 
pool.add_command(commands.get_pool, name='get')

# 将命令添加到queue子命令组
queue.add_command(commands.list_queue, name='list')
queue.add_command(commands.get_queue, name='get')

# 将命令添加到node子命令组
node.add_command(commands.list_node, name='list')

# 配置命令放在顶层
cli.add_command(commands.config)

if __name__ == '__main__':
    cli()