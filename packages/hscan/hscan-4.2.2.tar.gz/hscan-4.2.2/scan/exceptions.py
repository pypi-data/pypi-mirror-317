class ScanException(Exception):
    """基础异常类"""
    pass

class DownloadError(ScanException):
    """下载异常"""
    pass

class StorageError(ScanException):
    """存储异常"""
    pass

class ConfigError(ScanException):
    """配置异常"""
    pass

class TaskError(ScanException):
    """任务异常"""
    pass

