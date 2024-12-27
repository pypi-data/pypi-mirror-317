import threading

SITE = "sobeycloud-site"
PROJECT_CODE = "sobeycloud-project-code"
SOBEY_CLOUD_USER_CODE = "sobeycloud-user"
SOBEY_CLOUD_USER_NAME = "sobeycloud-user-name"
SOBEY_CLOUD_ROLE_CODE = "sobeycloud-role-code"
SOBEY_CLOUD_ORG_CODE = "sobeycloud-org-code"
SOBEY_CLOUD_PERMISSIONS = "sobeycloud-permissions"
SOBEY_CLOUD_CLIENT_ID = "sobeycloud-client-id"

# 上下文变量,注意,这个和JAVA的不一样.对于子线程不友好
__thread_local = threading.local()


def set_value(key: str, value: str):
    tmp = __thread_local.key if hasattr(__thread_local, 'key') and __thread_local.key is not None else {}

    tmp[key] = value
    __thread_local.key = tmp


def close():
    __thread_local.key = None


def remove_value(key: str):
    tmp: dict = __thread_local.key
    if tmp is None:
        return
    tmp.pop(key)
    if len(tmp) == 0:
        close()


def get_value(key: str) -> str:
    tmp: dict = __thread_local.key
    if tmp is not None:
        return tmp.get(key)
    return None
