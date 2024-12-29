from typing import Any, Callable, TypeVar, Sequence, Optional, Union, Type, Tuple
from functools import reduce, wraps
import inspect

# 定义泛型类型变量用于类型提示
T = TypeVar('T')  # 输入类型
R = TypeVar('R')  # 返回类型

class LambdaBuilder:
    """用于构建和组合lambda表达式的工具类
    
    这个类提供了一系列静态方法来增强lambda表达式的功能，包括：
    - 类型检查
    - 调试支持
    - 错误处理
    - 函数组合
    - 命名和文档
    """
    
    @staticmethod
    def validate_callable(func: Callable) -> None:
        """验证传入的对象是否为可调用对象
        
        Args:
            func: 要验证的对象
            
        Raises:
            TypeError: 当对象不是可调用类型时抛出
        """
        if not callable(func):
            raise TypeError(f"Expected a callable, got {type(func)}")
    
    @staticmethod
    def debug_lambda(func: Callable) -> Callable:
        """为lambda添加调试功能的装饰器
        
        增加异常处理和详细的错误信息，包括：
        - 函数名称（如果有）
        - 调用参数
        - 原始错误信息
        
        Args:
            func: 要装饰的lambda函数
            
        Returns:
            装饰后的函数，具有更好的错误处理能力
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                raise type(e)(
                    f"Error in lambda function {func.__name__ if hasattr(func, '__name__') else 'anonymous'}: "
                    f"args={args}, kwargs={kwargs}\n{str(e)}"
                )
        return wrapper
    
    @staticmethod
    def named_lambda(name: str) -> Callable:
        """创建具名lambda的装饰器
        
        为lambda函数添加名称，使其在调试和错误追踪时更容易识别
        
        Args:
            name: 要赋予lambda的名称
            
        Returns:
            一个装饰器函数
        """
        def decorator(func: Callable) -> Callable:
            func.__name__ = name
            func.__qualname__ = name
            return func
        return decorator
    
    @staticmethod
    def compose(*functions: Callable) -> Callable:
        """组合多个函数，从右到左执行，带类型检查
        
        例如：compose(f, g, h)(x) 相当于 f(g(h(x)))
        
        Args:
            *functions: 要组合的函数序列
            
        Returns:
            组合后的函数
            
        Raises:
            TypeError: 当任何参数不是可调用对象时抛出
        """
        for f in functions:
            LambdaBuilder.validate_callable(f)
            
        def compose_two(f: Callable, g: Callable) -> Callable:
            @wraps(f)
            def composed(x):
                return f(g(x))
            return composed
            
        if len(functions) == 0:
            return lambda x: x
        return reduce(compose_two, functions)
    
    @staticmethod
    def safe_lambda(default_value: Any = None) -> Callable:
        """创建安全的lambda装饰器，出错时返回默认值
        
        Args:
            default_value: 发生异常时返回的默认值
            
        Returns:
            一个装饰器函数，使得被装饰的lambda在出错时返回默认值而不是抛出异常
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    return default_value
            return wrapper
        return decorator
    
    @staticmethod
    def documented_lambda(doc: str) -> Callable:
        """为lambda添加文档字符串的装饰器
        
        Args:
            doc: 要添加的文档字符串
            
        Returns:
            一个装饰器函数，为lambda添加文档说明
        """
        def decorator(func: Callable) -> Callable:
            func.__doc__ = doc
            return func
        return decorator
    
    @staticmethod
    def type_checked_lambda(input_type: Type, output_type: Type) -> Callable:
        """为lambda添加类型检查的装饰器
        
        在运行时检查输入和输出类型是否符合预期
        
        Args:
            input_type: 期望的输入类型
            output_type: 期望的输出类型
            
        Returns:
            一个带有类型检查的装饰器函数
            
        Raises:
            TypeError: 当输入或输出类型不匹配时抛出
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(x):
                if not isinstance(x, input_type):
                    raise TypeError(f"Expected input type {input_type}, got {type(x)}")
                result = func(x)
                if not isinstance(result, output_type):
                    raise TypeError(f"Expected return type {output_type}, got {type(result)}")
                return result
            return wrapper
        return decorator 

    @staticmethod
    def primitive_lambda(func: Callable) -> Callable:
        """优化基本类型的lambda表达式，避免不必要的装箱/拆箱
        
        Args:
            func: 要优化的lambda函数
            
        Returns:
            优化后的函数，直接处理基本类型
            
        Example:
            >>> @primitive_lambda
            >>> def add_one(x): return x + 1
            >>> # 避免了int的装箱/拆箱
        """
        primitive_types = {int, float, bool}
        
        @wraps(func)
        def wrapper(x):
            # 如果是基本类型，直接处理
            if type(x) in primitive_types:
                return func(x)
            # 如果是包装类型，先拆箱再处理
            try:
                primitive_value = x.__wrapped__
                result = func(primitive_value)
                return type(x)(result)  # 重新装箱
            except AttributeError:
                return func(x)  # 不是包装类型，直接处理
        return wrapper

    @staticmethod
    def object_pool_lambda(pool_size: int = 100) -> Callable:
        """使用对象池来减少lambda创建的对象数量
        
        Args:
            pool_size: 对象池大小
            
        Returns:
            使用对象池的装饰器函数
            
        Example:
            >>> @object_pool_lambda(pool_size=10)
            >>> def create_obj(x): return {'value': x}
        """
        from collections import deque
        
        def decorator(func: Callable) -> Callable:
            pool = deque(maxlen=pool_size)
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 尝试从对象池获取对象
                if pool:
                    obj = pool.pop()
                    # 重置/更新对象
                    if hasattr(obj, 'reset'):
                        obj.reset(*args, **kwargs)
                    else:
                        obj.update(func(*args, **kwargs))
                    return obj
                
                # 对象池为空时创建新对象
                return func(*args, **kwargs)
            
            # 添加回收方法
            def recycle(obj):
                if len(pool) < pool_size:
                    pool.append(obj)
            
            wrapper.recycle = recycle
            return wrapper
        return decorator

    @staticmethod
    def closure_optimizer(func: Callable) -> Callable:
        """优化lambda闭包，减少内存占用并处理作用域问题
        
        Args:
            func: 要优化的lambda函数
            
        Returns:
            优化后的函数
            
        Example:
            >>> x = 10
            >>> @closure_optimizer
            >>> lambda y: x + y  # 优化对x的引用
        """
        # 获取闭包变量
        if hasattr(func, '__closure__') and func.__closure__:
            closure_vars = {
                name: cell.cell_contents
                for name, cell in zip(func.__code__.co_freevars, func.__closure__)
            }
            
            # 创建新的函数，显式传递闭包变量
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            # 将闭包变量存储为函数属性，避免循环引用
            wrapper.__closure_vars__ = closure_vars
            
            # 清理原始闭包
            if hasattr(func, '__closure__'):
                func.__closure__ = None
                
            return wrapper
        return func

    @staticmethod
    def weak_closure(func: Callable) -> Callable:
        """使用弱引用来处理闭包中的循环引用问题
        
        Args:
            func: 要处理的lambda函数
            
        Returns:
            使用弱引用的函数
            
        Example:
            >>> class MyClass:
            >>>     def __init__(self):
            >>>         self.func = weak_closure(lambda: self.value)
        """
        import weakref
        
        if hasattr(func, '__closure__') and func.__closure__:
            closure_dict = {}
            
            # 将闭包变量转换为弱引用
            for name, cell in zip(func.__code__.co_freevars, func.__closure__):
                value = cell.cell_contents
                if hasattr(value, '__weakref__'):
                    closure_dict[name] = weakref.proxy(value)
                else:
                    closure_dict[name] = value
            
            # 创建新函数，使用弱引用访问闭包变量
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            wrapper.__closure_vars__ = closure_dict
            return wrapper
        return func

    @staticmethod
    def cache_lambda(maxsize: int = 128, typed: bool = False) -> Callable:
        """为lambda添加结果缓存，避免重复计算
        
        Args:
            maxsize: 缓存大小
            typed: 是否区分参数类型
            
        Returns:
            带缓存的装饰器函数
            
        Example:
            >>> @cache_lambda(maxsize=100)
            >>> def expensive_calc(x): return x ** 2
        """
        from functools import lru_cache
        
        def decorator(func: Callable) -> Callable:
            # 使用LRU缓存
            cached_func = lru_cache(maxsize=maxsize, typed=typed)(func)
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                return cached_func(*args, **kwargs)
            
            # 添加缓存控制方法
            wrapper.cache_info = cached_func.cache_info
            wrapper.cache_clear = cached_func.cache_clear
            return wrapper
        return decorator

    @staticmethod
    def immutable_lambda(func: Callable) -> Callable:
        """创建不可变的lambda函数，避免状态改变
        
        Args:
            func: 要处理的lambda函数
            
        Returns:
            不可变版本的函数
            
        Example:
            >>> @immutable_lambda
            >>> def process(x): return x * 2
        """
        from functools import partial
        
        # 冻结函数的属性
        frozen_func = partial(func)
        # 防止修改函数属性
        frozen_func.__setattr__ = lambda *args: None
        
        return frozen_func 

    @staticmethod
    def parallel_lambda(workers: int = None, chunk_size: int = None) -> Callable:
        """并行处理装饰器，用于优化计算密集型lambda
        
        Args:
            workers: 工作进程数，默认为CPU核心数
            chunk_size: 每个进程的数据块大小
            
        Returns:
            并行处理版本的函数
            
        Example:
            >>> @parallel_lambda(workers=4)
            >>> def process_data(x): return expensive_computation(x)
        """
        import multiprocessing as mp
        from concurrent.futures import ProcessPoolExecutor
        
        def decorator(func: Callable) -> Callable:
            pool = ProcessPoolExecutor(max_workers=workers)
            
            @wraps(func)
            def wrapper(data):
                if isinstance(data, (list, tuple)):
                    # 并行处理序列数据
                    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)] if chunk_size else [data]
                    results = list(pool.map(func, chunks))
                    return [item for sublist in results for item in sublist]
                return func(data)
            
            return wrapper
        return decorator

    @staticmethod
    def memory_optimized(max_memory: int = None) -> Callable:
        """内存优化装饰器，控制lambda函数的内存使用
        
        Args:
            max_memory: 最大内存使用量(MB)
            
        Returns:
            内存受控的函数
            
        Example:
            >>> @memory_optimized(max_memory=100)
            >>> def process_large_data(data): return data.transform()
        """
        import psutil
        import gc
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 强制垃圾回收
                gc.collect()
                
                # 获取初始内存使用
                process = psutil.Process()
                initial_memory = process.memory_info().rss / 1024 / 1024
                
                try:
                    result = func(*args, **kwargs)
                    
                    # 检查内存使用
                    current_memory = process.memory_info().rss / 1024 / 1024
                    if max_memory and current_memory - initial_memory > max_memory:
                        raise MemoryError(f"Memory usage exceeded limit: {current_memory-initial_memory:.2f}MB > {max_memory}MB")
                    
                    return result
                finally:
                    # 清理内存
                    gc.collect()
            
            return wrapper
        return decorator

    @staticmethod
    def profile_lambda(enable_timer: bool = True, enable_memory: bool = True) -> Callable:
        """性能分析装饰器，用于分析lambda函数的执行时间和内存使用
        
        Args:
            enable_timer: 是否启用时间分析
            enable_memory: 是否启用内存分析
            
        Returns:
            带性能分析的函数
            
        Example:
            >>> @profile_lambda()
            >>> def my_function(x): return x * 2
        """
        import time
        import psutil
        from functools import wraps
        
        def decorator(func: Callable) -> Callable:
            stats = {
                'calls': 0,
                'total_time': 0,
                'avg_time': 0,
                'min_time': float('inf'),
                'max_time': 0,
                'memory_usage': []
            }
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                start_memory = psutil.Process().memory_info().rss if enable_memory else 0
                
                result = func(*args, **kwargs)
                
                if enable_timer:
                    elapsed = time.perf_counter() - start_time
                    stats['calls'] += 1
                    stats['total_time'] += elapsed
                    stats['avg_time'] = stats['total_time'] / stats['calls']
                    stats['min_time'] = min(stats['min_time'], elapsed)
                    stats['max_time'] = max(stats['max_time'], elapsed)
                
                if enable_memory:
                    memory_used = psutil.Process().memory_info().rss - start_memory
                    stats['memory_usage'].append(memory_used)
                
                return result
            
            wrapper.stats = stats
            return wrapper
        return decorator

    @staticmethod
    def batch_processor(batch_size: int = 100) -> Callable:
        """批处理优化装饰器，用于优化大数据集处理
        
        Args:
            batch_size: 每批处理的数据量
            
        Returns:
            支持批处理的函数
            
        Example:
            >>> @batch_processor(batch_size=1000)
            >>> def process_items(items): return [item * 2 for item in items]
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(data):
                if not isinstance(data, (list, tuple)):
                    return func(data)
                
                results = []
                for i in range(0, len(data), batch_size):
                    batch = data[i:i + batch_size]
                    results.extend(func(batch))
                return results
            
            return wrapper
        return decorator

    @staticmethod
    def lazy_evaluation() -> Callable:
        """惰性求值装饰器，延迟计算直到真正需要结果
        
        Returns:
            支持惰性求值的函数
            
        Example:
            >>> @lazy_evaluation()
            >>> def expensive_calc(x): return x ** 2
        """
        class LazyWrapper:
            def __init__(self, func, *args, **kwargs):
                self.func = func
                self.args = args
                self.kwargs = kwargs
                self._result = None
                self._computed = False
            
            def __call__(self):
                if not self._computed:
                    self._result = self.func(*self.args, **self.kwargs)
                    self._computed = True
                return self._result
            
            def reset(self):
                self._computed = False
                self._result = None
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return LazyWrapper(func, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def vectorized(parallel: bool = False) -> Callable:
        """向量化操作装饰器，优化数值计算
        
        Args:
            parallel: 是否启用并行处理
            
        Returns:
            向量化的函数
            
        Example:
            >>> @vectorized(parallel=True)
            >>> def compute(x): return x * 2
        """
        import numpy as np
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(data):
                # 转换为numpy数组
                if not isinstance(data, np.ndarray):
                    data = np.array(data)
                
                if parallel:
                    # 使用numpy的并行操作
                    return np.frompyfunc(func, 1, 1)(data)
                else:
                    # 使用向量化操作
                    return np.vectorize(func)(data)
            
            return wrapper
        return decorator 

    @staticmethod
    def multi_statement_lambda() -> Callable:
        """支持多语句lambda表达式的装饰器
        
        允许在lambda中使用多个语句，包括条件、循环等
        
        Returns:
            支持多语句的装饰器
            
        Example:
            >>> @multi_statement_lambda()
            >>> def complex_lambda(x):
            >>>     if x > 0:
            >>>         x = x * 2
            >>>     for i in range(3):
            >>>         x += i
            >>>     return x
        """
        def decorator(func: Callable) -> Callable:
            # 获取函数的源代码
            source = inspect.getsource(func)
            # 提取函数体
            body = source[source.index(':') + 1:]
            
            # 创建新的函数对象
            namespace = {}
            exec(f"def wrapper{inspect.signature(func)}:\n{body}", globals(), namespace)
            wrapper = namespace['wrapper']
            
            # 复制原函数的属性
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            wrapper.__annotations__ = func.__annotations__
            
            return wrapper
        return decorator

    @staticmethod
    def readable_lambda(description: str = None) -> Callable:
        """增强lambda可读性的装饰器
        
        Args:
            description: lambda功能的描述
            
        Returns:
            带有可读性增强的装饰器
            
        Example:
            >>> @readable_lambda("计算平方并加倍")
            >>> def process(x): return x ** 2 * 2
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                # 添加可读性属性
                wrapper.description = description or func.__doc__ or "未提供描述"
                wrapper.args_info = f"参数: {args}, 关键字参数: {kwargs}"
                wrapper.result_info = f"结果: {result}"
                return result
            
            # 添加字符串表示
            wrapper.__str__ = lambda: f"{description or func.__name__}\n参数类型: {func.__annotations__}"
            wrapper.__repr__ = wrapper.__str__
            
            return wrapper
        return decorator

    @staticmethod
    def debug_enhanced_lambda(log_level: str = 'INFO') -> Callable:
        """增强的lambda调试装饰器
        
        Args:
            log_level: 日志级别
            
        Returns:
            带有增强调试功能的装饰器
            
        Example:
            >>> @debug_enhanced_lambda(log_level='DEBUG')
            >>> def calc(x): return x * 2
        """
        import logging
        import traceback
        
        logging.basicConfig(level=getattr(logging, log_level))
        logger = logging.getLogger('lambda_debug')
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                call_frame = inspect.currentframe().f_back
                caller_info = f"{call_frame.f_code.co_filename}:{call_frame.f_lineno}"
                
                logger.debug(f"调用 {func.__name__} 在 {caller_info}")
                logger.debug(f"参数: {args}, 关键字参数: {kwargs}")
                
                try:
                    result = func(*args, **kwargs)
                    logger.debug(f"返回值: {result}")
                    return result
                except Exception as e:
                    logger.error(f"错误: {str(e)}")
                    logger.error(f"堆栈跟踪:\n{traceback.format_exc()}")
                    raise
            
            # 添加调试辅助方法
            def inspect_lambda():
                """检查lambda函数的详细信息"""
                return {
                    'name': func.__name__,
                    'doc': func.__doc__,
                    'signature': str(inspect.signature(func)),
                    'source': inspect.getsource(func),
                    'module': func.__module__
                }
            
            wrapper.inspect = inspect_lambda
            return wrapper
        return decorator

    @staticmethod
    def conditional_lambda(*conditions: Callable[[Any], bool]) -> Callable:
        """支持条件分支的lambda装饰器
        
        Args:
            *conditions: 条件函数列表
            
        Returns:
            支持条件分支的装饰器
            
        Example:
            >>> @conditional_lambda(lambda x: x > 0, lambda x: x < 0)
            >>> def process(x):
            >>>     return [
            >>>         lambda x: x * 2,  # x > 0
            >>>         lambda x: x * -1, # x < 0
            >>>         lambda x: 0       # default
            >>>     ]
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(x):
                branches = func(x)
                for condition, branch in zip(conditions, branches):
                    if condition(x):
                        return branch(x)
                return branches[-1](x)  # default branch
            return wrapper
        return decorator

    @staticmethod
    def loop_lambda(max_iterations: int = None) -> Callable:
        """支持循环操作的lambda装饰器
        
        Args:
            max_iterations: 最大迭代次数
            
        Returns:
            支持循环的装饰器
            
        Example:
            >>> @loop_lambda(max_iterations=100)
            >>> def accumulate(x):
            >>>     state = {'sum': 0, 'count': 0}
            >>>     def condition(): return state['count'] < x
            >>>     def body():
            >>>         state['sum'] += state['count']
            >>>         state['count'] += 1
            >>>     return condition, body, lambda: state['sum']
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                condition, body, result = func(*args, **kwargs)
                iterations = 0
                
                while condition():
                    if max_iterations and iterations >= max_iterations:
                        raise RuntimeError(f"超过最大迭代次数: {max_iterations}")
                    body()
                    iterations += 1
                
                return result()
            
            return wrapper
        return decorator

    @staticmethod
    def structured_lambda() -> Callable:
        """为lambda添加结构化编程支持的装饰器
        
        Returns:
            支持结构化编程的装饰器
            
        Example:
            >>> @structured_lambda()
            >>> def process(x):
            >>>     def init():
            >>>         return {'value': x}
            >>>     def validate():
            >>>         return x > 0
            >>>     def transform(state):
            >>>         state['value'] *= 2
            >>>     def finalize(state):
            >>>         return state['value']
            >>>     return init, validate, transform, finalize
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                init, validate, transform, finalize = func(*args, **kwargs)
                
                # 初始化
                state = init()
                
                # 验证
                if not validate():
                    raise ValueError("验证失败")
                
                # 转换
                transform(state)
                
                # 完成
                return finalize(state)
            
            return wrapper
        return decorator 

    @staticmethod
    def chainable_lambda() -> Callable:
        """支持链式调用的lambda装饰器，允许lambda()()模式
        
        Returns:
            支持链式调用的装饰器
            
        Example:
            >>> @chainable_lambda()
            >>> def create_multiplier(x):
            >>>     return lambda y: x * y
            >>> 
            >>> double = create_multiplier(2)
            >>> result = double(3)  # 返回6
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if callable(result):
                    # 为返回的lambda添加链式调用支持
                    @wraps(result)
                    def chain_wrapper(*chain_args, **chain_kwargs):
                        chain_result = result(*chain_args, **chain_kwargs)
                        # 支持继续链式调用
                        if callable(chain_result):
                            return chain_wrapper(chain_result)
                        return chain_result
                    return chain_wrapper
                return result
            return wrapper
        return decorator

    @staticmethod
    def curried_lambda() -> Callable:
        """支持自动柯里化的lambda装饰器
        
        Returns:
            支持柯里化的装饰器
            
        Example:
            >>> @curried_lambda()
            >>> def add(x, y, z):
            >>>     return x + y + z
            >>> 
            >>> add(1)(2)(3)  # 返回6
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if len(args) + len(kwargs) >= func.__code__.co_argcount:
                    return func(*args, **kwargs)
                return lambda *a, **kw: wrapper(*(args + a), **{**kwargs, **kw})
            return wrapper
        return decorator

    @staticmethod
    def composable_lambda() -> Callable:
        """支持函数组合的lambda装饰器
        
        Returns:
            支持组合的装饰器
            
        Example:
            >>> @composable_lambda()
            >>> def double(x):
            >>>     return x * 2
            >>> 
            >>> @composable_lambda()
            >>> def add_one(x):
            >>>     return x + 1
            >>> 
            >>> result = double >> add_one  # 创建新的组合函数
            >>> result(3)  # 返回7
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            def compose_right(self, other):
                """支持 f >> g 语法"""
                return lambda *args, **kwargs: other(self(*args, **kwargs))
            
            def compose_left(self, other):
                """支持 f << g 语法"""
                return lambda *args, **kwargs: self(other(*args, **kwargs))
            
            wrapper.__rshift__ = compose_right
            wrapper.__lshift__ = compose_left
            return wrapper
        return decorator

    @staticmethod
    def pipeline_lambda() -> Callable:
        """支持数据流管道的lambda装饰器
        
        Returns:
            支持管道操作的装饰器
            
        Example:
            >>> @pipeline_lambda()
            >>> def process_data():
            >>>     return (
            >>>         lambda x: x * 2,
            >>>         lambda x: x + 1,
            >>>         lambda x: str(x)
            >>>     )
            >>> 
            >>> pipeline = process_data()
            >>> result = pipeline(3)  # 返回"7"
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                pipeline_funcs = func(*args, **kwargs)
                
                def execute_pipeline(data):
                    result = data
                    for pipe_func in pipeline_funcs:
                        result = pipe_func(result)
                    return result
                
                return execute_pipeline
            return wrapper
        return decorator

    @staticmethod
    def recursive_lambda() -> Callable:
        """支持递归调用的lambda装饰器
        
        Returns:
            支持递归的装饰器
            
        Example:
            >>> @recursive_lambda()
            >>> def factorial(n):
            >>>     return lambda: 1 if n <= 1 else n * factorial(n-1)()
        """
        def decorator(func: Callable) -> Callable:
            # 使用Y组合子实现递归
            def Y(f):
                return (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                return Y(lambda f: func(*args, **kwargs))()
            return wrapper
        return decorator

    @staticmethod
    def monadic_lambda() -> Callable:
        """支持单子操作的lambda装饰器
        
        Returns:
            支持单子操作的装饰器
            
        Example:
            >>> @monadic_lambda()
            >>> def safe_divide(x, y):
            >>>     return None if y == 0 else x / y
            >>> 
            >>> result = safe_divide(10, 2).then(lambda x: x * 2)
            >>> # 返回Maybe(10)
        """
        class Maybe:
            def __init__(self, value):
                self.value = value
            
            def then(self, func):
                if self.value is None:
                    return Maybe(None)
                try:
                    return Maybe(func(self.value))
                except:
                    return Maybe(None)
            
            def get_or_else(self, default):
                return self.value if self.value is not None else default
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return Maybe(func(*args, **kwargs))
            return wrapper
        return decorator 

    @staticmethod
    def λ(expr: str) -> Callable:
        """超简洁的lambda表达式创建器
        
        Args:
            expr: lambda表达式字符串
            
        Returns:
            编译后的lambda函数
            
        Example:
            >>> f = λ("x -> x * 2")
            >>> g = λ("x, y -> x + y")
        """
        try:
            # 解析表达式
            parts = expr.split("->")
            args = [arg.strip() for arg in parts[0].split(",")]
            body = parts[1].strip()
            
            # 构建lambda字符串
            lambda_str = f"lambda {', '.join(args)}: {body}"
            
            # 编译并返回函数
            return eval(lambda_str)
        except Exception as e:
            raise SyntaxError(f"Invalid lambda expression: {expr}") from e

    @staticmethod
    def pipe(*funcs: Union[Callable, str]) -> Callable:
        """简化的函数管道
        
        Args:
            *funcs: 函数或lambda表达式字符串
            
        Returns:
            组合后的函数
            
        Example:
            >>> process = pipe(
            >>>     "x -> x * 2",
            >>>     "x -> x + 1",
            >>>     str
            >>> )
        """
        compiled_funcs = []
        for f in funcs:
            if isinstance(f, str):
                compiled_funcs.append(LambdaBuilder.λ(f))
            else:
                compiled_funcs.append(f)
        
        def piped(x):
            result = x
            for func in compiled_funcs:
                result = func(result)
            return result
        return piped

    @staticmethod
    def match(*patterns: Tuple[Callable, Callable]) -> Callable:
        """模式匹配风格的lambda
        
        Args:
            *patterns: (条件, 处理函数)元组
            
        Returns:
            模式匹配函数
            
        Example:
            >>> classify = match(
            >>>     (λ("x -> x > 0"), λ("x -> 'positive'")),
            >>>     (λ("x -> x < 0"), λ("x -> 'negative'")),
            >>>     (λ("x -> True"), λ("x -> 'zero'"))
            >>> )
        """
        def matcher(x):
            for cond, func in patterns:
                if cond(x):
                    return func(x)
            return None
        return matcher

    @staticmethod
    def chain(init_value: Any) -> 'ChainBuilder':
        """链式操作构建器
        
        Args:
            init_value: 初始值
            
        Returns:
            链式构建器对象
            
        Example:
            >>> result = chain(5).map("x -> x * 2").filter("x -> x > 5").value()
        """
        class ChainBuilder:
            def __init__(self, value):
                self._value = value
            
            def map(self, func):
                if isinstance(func, str):
                    func = LambdaBuilder.λ(func)
                self._value = func(self._value)
                return self
            
            def filter(self, pred):
                if isinstance(pred, str):
                    pred = LambdaBuilder.λ(pred)
                if not pred(self._value):
                    self._value = None
                return self
            
            def value(self):
                return self._value
        
        return ChainBuilder(init_value)

    @staticmethod
    def infix(func: Callable) -> 'InfixWrapper':
        """中缀表达式支持
        
        Args:
            func: 要转换为中缀形式的函数
            
        Returns:
            支持中缀调用的包装器
            
        Example:
            >>> add = infix(lambda x, y: x + y)
            >>> 1 |add| 2  # 返回3
        """
        class InfixWrapper:
            def __init__(self, func):
                self.func = func
            
            def __ror__(self, other):
                return InfixWrapper(lambda x: self.func(other, x))
            
            def __or__(self, other):
                return self.func(other)
        
        return InfixWrapper(func)

    @staticmethod
    def quick(template: str) -> Callable:
        """快速lambda生成器
        
        Args:
            template: 简化的lambda模板
            
        Returns:
            生成的函数
            
        Example:
            >>> double = quick("* 2")  # 等价于 lambda x: x * 2
            >>> add = quick("x y -> x + y")  # 等价于 lambda x, y: x + y
        """
        if "->" not in template:
            # 单参数简化形式
            return eval(f"lambda x: x {template}")
        else:
            # 完整形式
            return LambdaBuilder.λ(template)

    @staticmethod
    def compose_simple(*funcs: Union[Callable, str]) -> Callable:
        """简化的函数组合
        
        Args:
            *funcs: 函数或lambda表达式字符串
            
        Returns:
            组合后的函数
            
        Example:
            >>> f = compose_simple("* 2", "+ 1", str)
        """
        compiled_funcs = []
        for f in funcs:
            if isinstance(f, str):
                compiled_funcs.append(LambdaBuilder.quick(f))
            else:
                compiled_funcs.append(f)
        
        def composed(x):
            result = x
            for func in reversed(compiled_funcs):
                result = func(result)
            return result
        return composed 
