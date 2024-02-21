from abc import ABC, abstractmethod
from typing import Optional
import json
import os
import threading
import redis
import time

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
    def __init__(self, cache_directory: str = 'cache'):
        if not os.path.exists(cache_directory):
            os.mkdir(cache_directory)
        self.cache_directory = cache_directory

    def get(self, key: str):
        file_path = os.path.join(self.cache_directory, key)
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            return self.get_structure(key, data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def set(self, key: str, value, ttl: Optional[int] = 0) -> None:
        file_path = os.path.join(self.cache_directory, key)
        # Store data in the cache file
        with open(file_path, "w") as file:
            json.dump(self.set_structure(value, ttl), file)

    def delete(self, key: str) -> None:
        file_path = os.path.join(self.cache_directory, key)
        try:
            # Delete the file
            os.remove(file_path)
        except FileNotFoundError:
            pass

    def update_ttl(self, key: str, ttl: int) -> None:
        file_path = os.path.join(self.cache_directory, key)
        try:
            # Update the timestamp to simulate an extension of the TTL
            with open(file_path, "r+") as file:
                data = json.load(file)
                file.seek(0)
                json.dump(self.set_structure(data['data'], ttl), file)
                file.flush()  # Flush the data to the file
                file.truncate()
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def exists(self, key: str) -> bool:
        file_path = os.path.join(self.cache_directory, key)
        return os.path.exists(file_path)
    
    def set_structure(self, value, expire=0):
        if expire > 0:
            expire = time.time() + expire
        return {'data': value, 'expire': expire}
    
    def get_structure(self, key, data):
        if data['expire'] == 0:
            return data['data']
        else:
            if data['expire'] > time.time():
                return data['data']
            else:
                self.delete(key)
        return None

class RedisCache(BaseCache):
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, password: Optional[str] = None):
        # 初始化 Redis 连接
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, password=password)

    def get(self, key: str):
        # 实现 Redis 缓存的获取逻辑
        value = self.redis_client.get(key)
        if value is not None:
            # 如果值存在，则进行反序列化
            return json.loads(value)
        return None

    def set(self, key: str, value, ttl: Optional[int] = None) -> None:
        # 实现 Redis 缓存的设置逻辑
        serialized_value = json.dumps(value)
        if ttl is None:
            self.redis_client.set(key, serialized_value)
        else:
            self.redis_client.setex(key, ttl, serialized_value)

    def delete(self, key: str) -> None:
        # 实现 Redis 缓存的删除逻辑
        self.redis_client.delete(key)

    def update_ttl(self, key: str, ttl: int) -> None:
        # 实现 Redis 缓存的更新 ttl 逻辑
        # 注意：Redis 中更新 TTL 的操作通常需要重新设置键的过期时间
        if self.redis_client.exists(key):
            self.redis_client.expire(key, ttl)

    def exists(self, key: str) -> bool:
        # 实现 Redis 缓存的判断是否存在逻辑
        return self.redis_client.exists(key) == 1

def create_cache(cache_type: str, **kwargs) -> BaseCache:
    if cache_type == "file":
        return FileCache(**kwargs)
    elif cache_type == "redis":
        return RedisCache(**kwargs)
    # 可以添加其他缓存类型的判断和创建逻辑
    else:
        raise ValueError("Unsupported cache type")

# # 创建 Redis 缓存时传递连接参数
# redis_cache = create_cache('redis', host='localhost', port=6379, db=0, password='bhb123456')

# # 示例：创建 File 缓存
# file_cache = create_cache('file')

# #
# redis_cache.set('key', 1)

# print(redis_cache.get('key'))
