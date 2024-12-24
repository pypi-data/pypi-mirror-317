import logging
from django.db import transaction
from django_model_helper.models import WithSimplePRSFStatusFields
from django_model_helper.models import WithSimpleResultFields
from .settings import DJANGO_SIMPLETASK3_EVENT_QUEUE_CHANNEL_TEMPLATE
from .settings import DJANGO_SIMPLETASK3_TASK_ID_TEMPLATE
from .settings import DJANGO_SIMPLETASK3_DEFAULT_SIMQ_WORKER_NUMBER
from .simq import get_simq_client

_logger = logging.getLogger(__name__)


class SimpleTask(WithSimplePRSFStatusFields, WithSimpleResultFields):
    # 工作线程数。None表示使用应用全局设置。默认为：5。
    django_simpletask3_worker_number = None
    # 其它控制
    django_simpletask3_event_queue_channel_template = None
    django_simpletask3_task_id_template = None
    django_simpletask3_no_push_to_event_queue_flag_key = (
        "_django_simpletask3_no_push_to_event_queue_flag"
    )

    class Meta:
        abstract = True
        permissions = [
            ("django_simpletask3_execute", "执行任务"),
            ("django_simpletask3_reset", "重置任务"),
        ]

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if not hasattr(self, self.django_simpletask3_no_push_to_event_queue_flag_key):
            transaction.on_commit(self.push_to_event_queue)
        return result

    def clean_no_push_to_event_queue_flag(self):
        if hasattr(self, self.django_simpletask3_no_push_to_event_queue_flag_key):
            delattr(self, self.django_simpletask3_no_push_to_event_queue_flag_key)

    def mark_no_push_to_event_queue_flag(self):
        setattr(self, self.django_simpletask3_no_push_to_event_queue_flag_key, True)

    def push_to_event_queue(self):
        self.mark_no_push_to_event_queue_flag()
        channel = self.get_event_channel()
        simq_client = get_simq_client()
        simq_client.lpush(channel, self.get_task_data(), id=self.get_task_id())

    @classmethod
    def get_event_channel(cls):
        template = cls.django_simpletask3_event_queue_channel_template
        if not template:
            template = DJANGO_SIMPLETASK3_EVENT_QUEUE_CHANNEL_TEMPLATE
        app_label = cls._meta.app_label
        model_name = cls._meta.model_name
        return template.format(app_label=app_label, model_name=model_name)

    @classmethod
    def get_worker_number(cls):
        worker_number = cls.django_simpletask3_worker_number
        if worker_number is None:
            worker_number = DJANGO_SIMPLETASK3_DEFAULT_SIMQ_WORKER_NUMBER
        return worker_number

    def get_task_id(self):
        template = self.django_simpletask3_task_id_template
        if not template:
            template = DJANGO_SIMPLETASK3_TASK_ID_TEMPLATE
        return DJANGO_SIMPLETASK3_TASK_ID_TEMPLATE.format(
            app_label=self._meta.app_label,
            model_name=self._meta.model_name,
            id=self.pk,
        )

    def get_task_data(self):
        return {
            "app_label": self._meta.app_label,
            "model_name": self._meta.model_name,
            "id": self.id,
        }

    def set_result(self, result, save=True):
        self.set_success(save=False)
        return super().set_result(result, save=save)

    def set_error(self, error, save=True):
        self.set_failed(save=False)
        return super().set_error(error, save=save)

    def reset(self, push_to_event_queue=True, save=True):
        self.status = self.PENDING
        self.start_time = None
        self.done_time = None
        self.success = None
        self.result_data = None
        self.error_data = None
        self.result_time = None
        if not push_to_event_queue:
            self.mark_no_push_to_event_queue_flag()
        else:
            self.clean_no_push_to_event_queue_flag()
        if save:
            self.save()

    def execute(self, **kwargs):
        worker_index = kwargs.get("worker_index", None)
        _logger.debug(
            "django-simpletask3 execute start: app_label=%s, model_name=%s, worker_index=%s, id=%s",
            self._meta.app_label,
            self._meta.model_name,
            worker_index,
            self.id,
        )
        self.mark_no_push_to_event_queue_flag()
        try:
            result = self.do_task(**kwargs)
            self.set_result(result)
            _logger.debug(
                "django-simpletask3 execute success: app_label=%s, model_name=%s, worker_index=%s, id=%s, result=%s",
                self._meta.app_label,
                self._meta.model_name,
                worker_index,
                self.id,
                result,
            )
            return True
        except Exception as error:
            _logger.exception(
                "django-simpletask3 execute failed: app_label=%s, model_name=%s, worker_index=%s, id=%s, error=%s",
                self._meta.app_label,
                self._meta.model_name,
                worker_index,
                self.id,
                error,
            )
            self.set_error(error)
            return False

    def do_task(self, **kwargs):
        raise NotImplementedError("任务执行主体过程尚未实现")

    fields = [
        "status",
        "success",
        "result_data",
        "error_data",
        "start_time",
        "done_time",
        "result_time",
    ]

    @classmethod
    def get_fieldset(cls, title="任务信息", classes=None):
        if classes and isinstance(classes, str):
            classes = [classes]
        fieldset = (
            title,
            {
                "fields": cls.fields,
            },
        )
        if classes:
            fieldset[1]["classes"] = classes
        return fieldset
