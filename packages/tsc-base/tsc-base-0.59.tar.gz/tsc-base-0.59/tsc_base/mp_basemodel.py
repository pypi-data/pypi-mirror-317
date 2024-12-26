from pydantic import BaseModel, Field
from typing import Optional
from multiprocessing import Manager

# Description: 使用 Pydantic BaseModel 与 DictProxy 实现进程间数据同步与点访问


class DictProxy(dict):
    """这是一个模拟的 DictProxy 类，可以用于多进程共享字典。"""
    pass


class ProxyDictModel(BaseModel):
    """在 BaseModel 内部集成 DictProxy 实现进程间同步与点访问"""

    def __init__(self, proxy: DictProxy, **data):
        super().__init__(**data)
        setattr(self, "_proxy", proxy)
        self._proxy: DictProxy
        self._sync_to_proxy()

    def _sync_to_proxy(self):
        """同步 BaseModel 字段到 DictProxy"""
        for field in self.model_fields:
            self._proxy[field] = super().__getattribute__(field)
    
    def _sync_to_model(self):
        """同步 DictProxy 到 BaseModel 字段"""
        for field in self.model_fields:
            super().__setattr__(field, self._proxy[field])

    def __getattribute__(self, item):
        """从 DictProxy 获取值，支持点访问"""
        if item in {"model_fields", "__pydantic_fields__", "_proxy"}:
            return super().__getattribute__(item)
        if item in super().__getattribute__('model_fields'):
            value = super().__getattribute__('_proxy')[item]
            super().__setattr__(item, value)
            return value
        else:
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        """更新属性，并同步到 DictProxy"""
        super().__setattr__(key, value)
        if key in self.model_fields:
            self._proxy[key] = value

    def model_dump(self, **kwargs):
        """将 DictProxy/BaseModel 转换为字典返回"""
        self._sync_to_model()
        return super().model_dump(**kwargs)


class ConfigModel(BaseModel):
    """配置模型, 用于进程间同步的配置"""
    delete_task: bool = Field(False, description='是否删除任务, 主要用于外部进程强制终止任务')
    is_successful: Optional[bool] = Field(
        None, description='整个进程是否正常处理完成，主要内部控制')
    create_date: Optional[str] = Field(None, description='进程开始运行的时间')
    stop_date: Optional[str] = Field(None, description='任务截止时间')


class ConfigModelPD(ConfigModel, ProxyDictModel):
    """配置模型, 用于进程间同步配置"""


# 测试代码
if __name__ == "__main__":
    # 创建 Manager 和 DictProxy 对象
    manager = Manager()
    proxy = manager.dict()

    # 配置数据
    config_data = {
        "delete_task": True,
        "is_successful": None,
        "create_date": "2024-11-13T10:00:00",
        "stop_date": None
    }

    # 创建 ConfigModelPD 实例
    config_model_pd = ConfigModelPD(proxy=proxy, **config_data)

    # 打印初始化后的 proxy 内容
    print("Initial proxy:", dict(config_model_pd._proxy))

    # 访问属性，测试 __getattribute__
    print("Accessing 'delete_task' directly:", config_model_pd.delete_task)
    print("Accessing 'is_successful' directly:", config_model_pd.is_successful)

    # 修改属性，测试 __setattr__
    config_model_pd.delete_task = False
    print("Modified 'delete_task' via setter:", config_model_pd.delete_task)

    # 打印修改后的 proxy 内容
    print("Updated proxy:", dict(config_model_pd._proxy))

    # 获取模型的字典表示
    model_dict = config_model_pd.model_dump()
    print("Model dump:", model_dict)
