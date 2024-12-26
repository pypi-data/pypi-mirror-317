import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_name: str = "cagu-toolkit"
    base_dir: str = os.path.expanduser(f"~/.{app_name}")
    config_file: str = os.path.join(base_dir, "config.json")
    log_file: str = os.path.join(base_dir, "app.log")
    last_check_file: str = os.path.join(base_dir, "last-check")
    check_version_interval: int = 24 * 60 * 60

    def __init__(self, **kwargs):
        # 调用父类构造函数
        super().__init__(**kwargs)
        # 确保目录存在
        os.makedirs(self.base_dir, exist_ok=True)

# 全局配置实例
config = Config()
