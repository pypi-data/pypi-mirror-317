# Lambda-U

Lambda-U 是一个轻量级的 Python 函数式编程工具库，提供了丰富的函数式编程工具和集合操作方法，帮助开发者写出更简洁、优雅的代码。

## ✨ 主要特性

- 🛠 丰富的函数式编程工具（compose、pipe、curry 等）
- 📦 强大的集合操作（group_by、flatten、chunk 等）
- ⛓ 支持优雅的链式调用
- 🎯 完整的类型提示支持
- 🧪 全面的单元测试覆盖
- 📝 详细的文档说明

## 🚀 快速开始

### 安装

```bash
pip install lambda-u
```

### 使用

```python
from lambda_u import LambdaBuilder, CollectionUtils, FunctionalUtils
```

### 函数组合

```python
f = lambda x: x * 2
g = lambda x: x + 1
composed = LambdaBuilder.compose(f, g)
print(composed(3))  # 输出: 8
```

### 函数管道

```python
result = pipe(
1,
lambda x: x + 1,
lambda x: x 2
) # 输出: 4
```

### 柯里化
```python
@curry
def add(x, y):
return x + y
add_one = add(1)
result = add_one(2) # 输出: 3
```

### 集合操作

## 分组
```python
users = [
{"name": "Alice", "age": 20},
{"name": "Bob", "age": 20},
{"name": "Charlie", "age": 25}
]
by_age = group_by(users, key="age")
# 输出: {20: [{'name': 'Alice', 'age': 20}, {'name': 'Bob', 'age': 20}], 25: [{'name': 'Charlie', 'age': 25}]}
```
## 展平嵌套列表
```python
nested = [[1, 2], [3, 4]]
flat = flatten(nested) # 输出: [1, 2, 3, 4]
# 输出: [1, 2, 3, 4, 5, 6]
```

## 分块
```python
numbers = [1, 2, 3, 4, 5, 6]
chunks = chunk(numbers, size=2) # 输出: [[1, 2], [3, 4], [5, 6]]
```
## 📚 API 文档

### functional 模块

- `compose(*functions)`: 从右到左组合多个函数
- `pipe(value, *functions)`: 将值通过一系列函数传递
- `curry(func)`: 函数柯里化装饰器

### collections 模块

- `group_by(items, key)`: 根据键对集合进行分组
- `flatten(items)`: 展平嵌套列表
- `chunk(items, size)`: 将列表分割成固定大小的块

更多 API 详情请查看[完整文档](#)。

## 🤝 贡献指南

欢迎提交 Pull Request 和 Issue！在提交之前，请确保：

1. 更新或添加相应的测试
2. 更新相关文档
3. 遵循项目的代码风格

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

- [问题反馈](https://github.com/your-username/lambda-u/issues)
- [更新日志](CHANGELOG.md)

## ⭐️ 致谢

感谢所有贡献者对项目的支持！
