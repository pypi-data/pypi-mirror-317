import unittest
from lambda_utils import LambdaBuilder, CollectionUtils, FunctionalUtils

class TestLambdaUtils(unittest.TestCase):
    def test_compose(self):
        f = lambda x: x * 2
        g = lambda x: x + 1
        composed = LambdaBuilder.compose(f, g)
        self.assertEqual(composed(3), 8)  # (3 + 1) * 2
    
    def test_map_dict(self):
        d = {'a': 1, 'b': 2, 'c': 3}
        result = CollectionUtils.map_dict(lambda x: x * 2, d)
        self.assertEqual(result, {'a': 2, 'b': 4, 'c': 6})
    
    def test_compose_predicates(self):
        is_even = lambda x: x % 2 == 0
        is_positive = lambda x: x > 0
        pred = FunctionalUtils.compose_predicates(is_even, is_positive)
        self.assertTrue(pred(2))
        self.assertFalse(pred(-2))
        self.assertFalse(pred(3))

    def test_chainable_lambda(self):
        @LambdaBuilder.chainable_lambda()
        def create_multiplier(x):
            return lambda y: x * y
        
        double = create_multiplier(2)
        self.assertEqual(double(3), 6)

    def test_curried_lambda(self):
        @LambdaBuilder.curried_lambda()
        def add(x, y, z):
            return x + y + z
        
        self.assertEqual(add(1)(2)(3), 6)

    def test_composable_lambda(self):
        @LambdaBuilder.composable_lambda()
        def double(x):
            return x * 2
        
        @LambdaBuilder.composable_lambda()
        def add_one(x):
            return x + 1
        
        composed = double >> add_one
        self.assertEqual(composed(3), 7)

    def test_pipeline_lambda(self):
        @LambdaBuilder.pipeline_lambda()
        def process_data():
            return (
                lambda x: x * 2,
                lambda x: x + 1,
                lambda x: str(x)
            )
        
        pipeline = process_data()
        self.assertEqual(pipeline(3), "7")

    def test_recursive_lambda(self):
        @LambdaBuilder.recursive_lambda()
        def factorial(n):
            return lambda: 1 if n <= 1 else n * factorial(n-1)()
        
        self.assertEqual(factorial(5), 120)

    def test_monadic_lambda(self):
        @LambdaBuilder.monadic_lambda()
        def safe_divide(x, y):
            return None if y == 0 else x / y
        
        result = safe_divide(10, 2).then(lambda x: x * 2)
        self.assertEqual(result.get_or_else(0), 10)
        
        result = safe_divide(10, 0).then(lambda x: x * 2)
        self.assertEqual(result.get_or_else(0), 0)

    def test_lambda_syntax_sugar(self):
        # 测试λ语法
        f = LambdaBuilder.λ("x -> x * 2")
        self.assertEqual(f(3), 6)
        
        # 测试管道
        process = LambdaBuilder.pipe(
            "x -> x * 2",
            "x -> x + 1",
            str
        )
        self.assertEqual(process(3), "7")
        
        # 测试模式匹配
        classify = LambdaBuilder.match(
            (LambdaBuilder.λ("x -> x > 0"), LambdaBuilder.λ("x -> 'positive'")),
            (LambdaBuilder.λ("x -> x < 0"), LambdaBuilder.λ("x -> 'negative'")),
            (LambdaBuilder.λ("x -> True"), LambdaBuilder.λ("x -> 'zero'"))
        )
        self.assertEqual(classify(5), "positive")
        
        # 测试链式操作
        result = (LambdaBuilder.chain(5)
                 。map("x -> x * 2")
                 。filter("x -> x > 5")
                 。value())
        self.assertEqual(result, 10)
        
        # 测试中缀表达式
        add = LambdaBuilder.infix(lambda x, y: x + y)
        self.assertEqual(1 |add| 2, 3)
        
        # 测试快速lambda
        double = LambdaBuilder.quick("* 2")
        self.assertEqual(double(5), 10)
        
        # 测试简化组合
        f = LambdaBuilder.compose_simple("* 2", "+ 1", str)
        self.assertEqual(f(3), "7")

if __name__ == '__main__':
    unittest.main() 
