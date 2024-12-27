from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import asyncio
import logging
from project_info import ProjectInfo
from spider_metrics import SpiderMetrics
from response import Response

logger = logging.getLogger(__name__)

class BaseDownloader(ABC):
    """下载器基类"""

    def __init__(self):
        self.headers = {
            "User-Agent": ProjectInfo.default_user_agent
        }
        self.timeout = 30
        self.retry_times = 3
        self._metrics = SpiderMetrics()

    @abstractmethod
    async def fetch(self, url: str, **kwargs) -> Any:
        """发送请求并获取响应的抽象方法"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """关闭下载器的抽象方法"""
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """检查下载器健康状态"""
        pass

    async def _handle_response(self, response: Any) -> Response:
        """处理响应的通用方法"""
        resp = Response()
        resp.response = response
        resp.request_url = response.url
        return resp

    async def _handle_error(self, error: Exception, url: str) -> None:
        """错误处理的通用方法"""
        self._metrics.request_counter.labels(
            status="error"
        ).inc()
        logger.error(f"Request failed for {url}: {error}")

    
    def add_middleware(self, middleware: Any) -> None:
        """添加中间件"""
        self.middlewares.append(middleware)
    
    async def _process_request(self, request: dict) -> dict:
        """请求预处理"""
        for middleware in self.middlewares:
            request = await middleware.process_request(request)
        return request
        
    async def _process_response(self, response: Response) -> Response:
        """响应后处理"""
        for middleware in self.middlewares:
            response = await middleware.process_response(response)
        return response
    

    async def __aenter__(self):
        """异步上下文管理器支持"""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """自动关闭资源"""
        await self.close()
        
    @property
    def closed(self) -> bool:
        """下载器状态"""
        return self._closed
        
    async def close(self) -> None:
        """关闭资源"""
        if not self._closed:
            async with self._lock:
                if not self._closed:
                    await self._close()
                    self._closed = True