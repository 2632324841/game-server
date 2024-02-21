from abc import ABC, abstractmethod
from typing import Optional
import pickle
import json
import time
import os
import redis
from typing import Optional
import hashlib

class BaseCache(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value, ttl: Optional[int] = None) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def update_ttl(self, key: str, ttl: int) -> None:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass


class FileCache(BaseCache):
    def __init__(self, base_path: str = "./cache"):
        self.base_path = base_path

    def _get_file_path(self, key: str) -> str:
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.base_path, hashed_key[:2], hashed_key[2:4], hashed_key[4:])

    def get(self, key: str):
        file_path = self._get_file_path(key)
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                value = data["value"]
                ttl = data.get("ttl")
                if ttl is not None and time.time() > ttl:
                    # 如果 TTL 已过期，则删除文件并返回 None
                    self.delete(key)
                    return None
                return value
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def set(self, key: str, value, ttl: Optional[int] = None) -> None:
        file_path = self._get_file_path(key)
        data = {"value": value}
        if ttl is not None:
            data["ttl"] = time.time() + ttl

        # Ensure the directory structure exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            json.dump(data, file)

    def delete(self, key: str) -> None:
        file_path = self._get_file_path(key)
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

    def update_ttl(self, key: str, ttl: int) -> None:
        file_path = self._get_file_path(key)
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                data["ttl"] = time.time() + ttl
            with open(file_path, "w") as file:
                json.dump(data, file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def exists(self, key: str) -> bool:
        file_path = self._get_file_path(key)
        return os.path.exists(file_path)

class RedisCache(BaseCache):
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def get(self, key: str):
        return self.redis_client.get(key)

    def set(self, key: str, value, ttl: Optional[int] = None) -> None:
        self.redis_client.set(key, value, ex=ttl)

    def delete(self, key: str) -> None:
        self.redis_client.delete(key)

    def update_ttl(self, key: str, ttl: int) -> None:
        # 更新 TTL 的操作在 Redis 中通常是设置过期时间
        # 如果 Redis 中的 key 不存在，这个方法会忽略
        self.redis_client.expire(key, ttl)

    def exists(self, key: str) -> bool:
        return self.redis_client.exists(key)


def create_cache(cache_type: str) -> BaseCache:
    if cache_type == "file":
        return FileCache()
    elif cache_type == "redis":
        return RedisCache()
    # 可以添加其他缓存类型的判断和创建逻辑
    else:
        raise ValueError("Unsupported cache type")
