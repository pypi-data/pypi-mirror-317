import json
from pathlib import Path
from typing import Optional
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.aihc.aihc_client import AIHCClient

def expando_to_dict(obj):
    if isinstance(obj, dict):
        return {k: expando_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, '__dict__'):
        return {k: expando_to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [expando_to_dict(item) for item in obj]
    else:
        return obj

class AIJobConfig:
    def __init__(self):
        self.config_dir = Path.home() / '.aijob'
        self.config_file = self.config_dir / 'config.json'
        self._ensure_config_dir()
        self.config = self._load_config()
    
    def _ensure_config_dir(self):
        """确保配置目录存在"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return {}
    
    def save(self):
        """保存配置到文件"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def set(self, key: str, value: str):
        """设置配置项"""
        self.config[key] = value
        self.save()
    
    def get(self, key: str) -> Optional[str]:
        """获取配置项"""
        return self.config.get(key)
    
def expando_to_dict(obj):
    if isinstance(obj, dict):
        return {k: expando_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, '__dict__'):
        return {k: expando_to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [expando_to_dict(item) for item in obj]
    else:
        return obj

def get_client(host: Optional[str]=None, access_key: Optional[str]=None, secret_key: Optional[str]=None) -> AIHCClient:
    """创建API客户端"""
    config = AIJobConfig()
    host = host or config.get('host')
    access_key = access_key or config.get('access_key')
    secret_key = secret_key or config.get('secret_key')
    aihc_config = BceClientConfiguration(credentials=BceCredentials(access_key, secret_key), endpoint=host)
    client: AIHCClient = AIHCClient(aihc_config)
    return client

