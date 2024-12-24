import threading

# 创建一个线程局部存储
_local = threading.local()


def set_context(profile):
    """设置上下文"""
    _local.profile = profile


def get_context():
    """获取上下文"""
    return getattr(_local, 'profile', None)
