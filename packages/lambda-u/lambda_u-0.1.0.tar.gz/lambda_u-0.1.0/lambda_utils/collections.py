from typing import Any, Callable, List, Dict, Sequence, TypeVar, Set, Tuple
from functools import reduce
from itertools import chain

# 定义泛型类型变量
T = TypeVar('T')  # 集合元素类型
R = TypeVar('R')  # 转换后的类型

class CollectionUtils:
    """增强的集合操作工具
    
    提供了一系列用于处理集合的高阶函数，包括：
    - 深度字典映射
    - 链式映射操作
    - 序列分区
    - 自定义去重
    """
    
    @staticmethod
    def map_dict_deep(func: Callable[[Any], Any], d: Dict, depth: int = -1) -> Dict:
        """递归对嵌套字典的值进行映射
        
        Args:
            func: 映射函数
            d: 要处理的字典
            depth: 递归深度，-1表示无限递归
            
        Returns:
            处理后的新字典
            
        Example:
            >>> d = {'a': {'b': 1}, 'c': 2}
            >>> map_dict_deep(lambda x: x * 2, d)
            {'a': {'b': 2}, 'c': 4}
        """
        def _map_dict_deep(value: Any, current_depth: int) -> Any:
            if isinstance(value, dict) and (depth == -1 or current_depth < depth):
                return {k: _map_dict_deep(v, current_depth + 1) for k, v in value.items()}
            return func(value)
        return _map_dict_deep(d, 0)
    
    @staticmethod
    def chain_maps(*functions: Callable[[T], R], safe: bool = False) -> Callable[[Sequence[T]], List[R]]:
        """链式映射操作，可选安全模式
        
        Args:
            *functions: 要链式应用的函数序列
            safe: 是否启用安全模式（忽略错误）
            
        Returns:
            一个接受序列并返回处理结果的函数
            
        Example:
            >>> funcs = [lambda x: x + 1, lambda x: x * 2]
            >>> chain_maps(*funcs)([1, 2, 3])
            [4, 6, 8]
        """
        def chained(seq: Sequence[T]) -> List[R]:
            result = []
            for item in seq:
                try:
                    current = item
                    for f in functions:
                        current = f(current)
                    result.append(current)
                except Exception as e:
                    if not safe:
                        raise e
            return result
        return chained
    
    @staticmethod
    def partition(pred: Callable[[T], bool], seq: Sequence[T]) -> Tuple[List[T], List[T]]:
        """根据谓词函数将序列分区
        
        Args:
            pred: 谓词函数，返回True/False
            seq: 要分区的序列
            
        Returns:
            (满足条件的元素列表, 不满足条件的元素列表)
            
        Example:
            >>> partition(lambda x: x > 0, [-1, 2, -3, 4])
            ([2, 4], [-1, -3])
        """
        truthy = []
        falsy = []
        for item in seq:
            (truthy if pred(item) else falsy).append(item)
        return truthy, falsy
    
    @staticmethod
    def unique_by(key: Callable[[T], Any], seq: Sequence[T]) -> List[T]:
        """根据键函数去重
        
        Args:
            key: 用于生成唯一键的函数
            seq: 要去重的序列
            
        Returns:
            去重后的列表，保持原始顺序
            
        Example:
            >>> data = [{'id': 1}, {'id': 2}, {'id': 1}]
            >>> unique_by(lambda x: x['id'], data)
            [{'id': 1}, {'id': 2}]
        """
        seen = set()
        result = []
        for item in seq:
            k = key(item)
            if k not in seen:
                seen.add(k)
                result.append(item)
        return result 