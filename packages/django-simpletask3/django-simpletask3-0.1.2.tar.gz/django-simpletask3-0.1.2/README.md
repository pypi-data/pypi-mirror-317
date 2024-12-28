# django-simpletask3

基于Redis及SimQ的异步任务处理。

## 安装

```shell
pip install django-simpletask3
```

## 使用

### SimQ引擎设置

在*pro/settings.py*中设置，或在环境变量中设置：`DJANGO_SIMPLETASK3_SIMQ_REDIS_URL`。一般来说，各业务系统都需要根据业务系统实际情况设置该配置项值。

### 在*pro/settings.py*中引入`django_simpletask3`

```python
INSTALLED_APPS = [
    ...
    "django_simpletask3",
    ...
]
```

### 在*app/models.py*中定义异步任务列表

```python
from django.db import models
from django_simpletask3.models import SimpleTask


class Task1(SimpleTask):

    # 每个工作节点启动的工作线程数
    django_simpletask3_worker_number = 2

    task_biz_field = models.CharField(max_length=64, null=True, blank=True)

    def do_task(self):
        """异步任务处理主函数。
        """
        self.task_biz_field = "task biz data"
        return "OK"
```

### 启动工作节点

```shell
python manage.py django-simpletask3-server
```

### 异步任务执行过程

- 当任务保存时，并自动往SimQ队列中推送一个消息。
- 工作节点取得消息后，执行异步任务处理主函数。
- 如果异步任务处理主函数没有抛出异常，则认为任务被成功处理，处理主函数的返回结果将被记录在`result_data`字段中。
- 如果异步任务处理主函数中抛出异常，则认为任务处理失败，错误信息将被记录任务的`error_data`字段中。

## 配置选项


- DJANGO_SIMPLETASK3_SIMQ_REDIS_URL = "redis://localhost:6379/0"
    - （配置项别名）
    - DJANGO_SIMPLETASK3_SIMQ_REDIS
    - SIMQ_REDIS_URL
    - SIMQ_REDIS
    - REDIS_URL
    - REDIS
- DJANGO_SIMPLETASK3_SIMQ_POP_TIMEOUT = 5
    - 工作线程从SimQ中获取消息的超时时长。如果设置很长，则结束节点时需要等待的时长也会很长。
- DJANGO_SIMPLETASK3_DEFAULT_SIMQ_WORKER_NUMBER = 5
    - 未在异步任务列表模型中指定`django_simpletask3_worker_number`时默认的每节点工作线程数。
- DJANGO_SIMPLETASK3_SIMQ_TIMEOUT_TASK_RECOVERY_INTERVAL = 60 * 2
    - 超时任务回收频率。默认每两分钟执行一次任务扫描，并回收已经超时的任务。
- DJANGO_SIMPLETASK3_SIMQ_DEFAULT_RUNNING_TIMEOUT_ACTION = "recover"
    - 超时任务处理策略。默认为：recover表示回收。
    - 其它选项有：drop表示丢弃。
- DJANGO_SIMPLETASK3_SIMQ_PREFIX = "simq"
- DJANGO_SIMPLETASK3_SIMQ_ACK_EVENT_EXPIRE = 60 * 60 * 24
- DJANGO_SIMPLETASK3_SIMQ_DONE_ITEM_EXPIRE = 60 * 60 * 24 * 7
- DJANGO_SIMPLETASK3_SIMQ_WORKER_STATUS_EXPIRE = 60 * 5
- DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT = 60 * 5
- DJANGO_SIMPLETASK3_SIMQ_RUNNING_TIMEOUT_HANDLER_POLICIES = None
- DJANGO_SIMPLETASK3_EVENT_QUEUE_CHANNEL_TEMPLATE = "django-simpletask3:{app_label}.{model_name}"
- DJANGO_SIMPLETASK3_TASK_ID_TEMPLATE = "django-simpletask3:{app_label}.{model_name}:{id}"

## 版本记录

### v0.1.0

- 版本首发。
- 基于Redis及SimQ的异步任务处理框架基础功能。

### v0.1.1

- 添加SimpleTaskAdmin基础类。
- 添加django_simpletask3_execute_for_selected和django_simpletask3_reset_for_selected批处理动作。
- 修改SimpleTask.execute执行机制。

### v0.1.2

- `SimpleTaskAdmin`中添加相关`actions`。
