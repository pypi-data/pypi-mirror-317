import json
import os

from cagu_toolkit.common.config import config


# 初始化配置环境（创建目录和文件）
def init_config_env():
    if not os.path.exists(config.config_file):  # 如果配置文件不存在，创建空的配置文件
        with open(config.config_file, 'w') as f:
            json.dump({}, f, indent=4)


# 读取配置文件
def load_config():
    init_config_env()  # 确保目录和文件已初始化
    with open(config.config_file, 'r') as f:
        return json.load(f)


# 保存配置文件
def save_config(my_config):
    init_config_env()  # 确保目录和文件已初始化
    with open(config.config_file, 'w') as f:
        json.dump(my_config, f, indent=4)
