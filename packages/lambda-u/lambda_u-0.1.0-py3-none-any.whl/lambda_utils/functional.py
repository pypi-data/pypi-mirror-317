from typing import Any, Callable, List, Sequence, TypeVar, Dict, Optional
from functools import reduce, partial, wraps
import inspect

# 定义泛型类型变量
T = TypeVar('T')  # 输入类型
R = TypeVar('R')  # 返回类型

class FunctionalUtils:
    """增强的函数式编程工具
    
    提供了一系列函数式编程工具，包括：
    - 谓词组合
    - 部分应用
    - 异步管道
    - 重试机制
    """
    
    @staticmethod
    def compose_predicates(*predicates: Callable[[T], bool], 
                          operator: str = 'and',
                          short_circuit: bool = True) -> Callable[[T], bool]:
        """增强的谓词组合，支持短路求值
        
        Args:
            *predicates: 要组合的谓词函数
            operator: 组合操作符，'and'或'or'
            short_circuit: 是否启用短路求值
            
        Returns:
            组合后的谓词函数
            
        Example:
            >>> is_even = lambda x: x % 2 == 0
            >>> is_positive = lambda x: x > 0
            >>> pred = compose_predicates(is_even, is_positive)
            >>> pred(2)  # True
        """
        if operator == 'and':
            def combined(x):
                for p in predicates:
                    if not p(x) and short_circuit:
                        return False
                return all(p(x) for p in predicates)
        elif operator == 'or':
            def combined(x):
                for p in predicates:
                    if p(x) and short_circuit:
                        return True
                return any(p(x) for p in predicates)
        else:
            raise ValueError("operator must be 'and' or 'or'")
        return combined
    
    @staticmethod
    def partial_right(func: Callable, *args, **kwargs) -> Callable:
        """从右侧进行部分应用
        
        Args:
            func: 要部分应用的函数
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            部分应用后的新函数
            
        Example:
            >>> def divide(x, y): return x / y
            >>> divide_by_2 = partial_right(divide, 2)
            >>> divide_by_2(10)  # 5.0
        """
        @wraps(func)
        def wrapper(*a, **kw):
            return func(*(a + args), **{**kw, **kwargs})
        return wrapper
    
    @staticmethod
    def pipe_async(*functions: Callable) -> Callable:
        """异步函数管道
        
        创建一个异步函数管道，支持混合同步和异步函数
        
        Args:
            *functions: 要管道化的函数序列
            
        Returns:
            异步管道函数
            
        Example:
            >>> async def process(x): return x + 1
            >>> pipeline = pipe_async(lambda x: x * 2, process)
            >>> await pipeline(2)  # 6
        """
        async def piped(x):
            result = x
            for f in functions:
                if inspect.iscoroutinefunction(f):
                    result = await f(result)
                else:
                    result = f(result)
            return result
        return piped
    
    @staticmethod
    def retry(max_attempts: int = 3, delay: float = 0) -> Callable:
        """为lambda添加重试机制的装饰器
        
        Args:
            max_attempts: 最大重试次数
            delay: 重试间隔（秒）
            
        Returns:
            带有重试机制的装饰器
            
        Example:
            >>> @retry(max_attempts=3, delay=1)
            >>> def unstable_function():
            >>>     # 可能失败的操作
            >>>     pass
        """
        import time
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if delay:
                            time.sleep(delay)
                raise last_exception
            return wrapper
        return decorator 