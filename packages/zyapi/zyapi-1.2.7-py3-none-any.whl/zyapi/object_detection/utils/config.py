# coding: utf-8
import os


# ------------------------------------算法常量------------------------------------ #

DBSCAN_EUCLIDEAN_EPS = os.environ.get('DBSCAN_EUCLIDEAN_EPS', 1.2)
SHARPNESS_LAPLACE = os.environ.get('SHARPNESS_LAPLACE', 100)
SHARPNESS_SMD2 = os.environ.get('SHARPNESS_SMD2', 1e7)
OCCLUSION_THRESHOLD = 0.9

# tf-serving服务地址
TF_SERVING_SERVER = os.environ.get('TF_SERVING_SERVER', '')


# ------------------------------------后端常量------------------------------------ #
TIMER_WILL_REPORT_SECONDS = os.environ.get('TIMER_WILL_REPORT_SECONDS', 60)  # 算法接口超时报警时间(s)
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')

# 日志配置
logging_config = {
    'version': 1,
    'incremental': False,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'class': 'logging.Formatter',
            'format': '[%(levelname)1.1s %(asctime)s %(filename)s->%(funcName)s:%(lineno)d]  %(message)s',
            'datefmt': '%F %X',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_DSN,
            'auto_log_stacks': True,
            'encoding': 'utf8'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['default', 'sentry'],
    },
}
HARDWARE_FINGERPRINT = None
