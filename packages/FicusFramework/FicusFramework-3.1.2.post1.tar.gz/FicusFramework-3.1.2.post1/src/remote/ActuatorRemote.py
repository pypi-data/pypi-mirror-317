import time
import logging
from threading import Thread

from flask import jsonify
from redis.exceptions import RedisError

from cloudcelery import celery_redis_client
from . import remote

log = logging.getLogger('Ficus')


@remote.route('/actuator/info', methods=['GET'])
def actuator_info():
    return jsonify({"build": {"version": "3.1.2", "artifact": "sobeycube-ficus-framework-4-py",
                              "name": "FicusFramework", "group": "com.sobey.jcg"}})


# 缓存 Redis 状态
redis_status = {
    "status": "UNKNOWN",
    "last_checked": None
}
# 状态检查间隔（秒）
CHECK_INTERVAL = 10


def update_redis_status():
    """后台任务：定期检查 Redis 状态"""
    redis = celery_redis_client()
    global redis_status
    while True:
        try:
            redis.ping()
            new_status = "UP"
        except RedisError as e:
            new_status = "DOWN"
            log.error(f"Error connecting to Redis: {e}")

        # 记录状态变化
        if redis_status["status"] != new_status:
            log.info(f"Redis status changed: {redis_status['status']} -> {new_status}")

        redis_status = {"status": new_status, "last_checked": time.time()}

        time.sleep(CHECK_INTERVAL)


@remote.route('/actuator/health', methods=['GET'])
def actuator_health():
    health_status = {
        "status": "UP" if redis_status["status"] == "UP" else "DOWN",
        "components": {
            "redis": {
                "status": redis_status["status"],
                "lastChecked": redis_status["last_checked"]
            }
        }
    }
    return jsonify(health_status)


thread = Thread(target=update_redis_status, daemon=True)
thread.start()
