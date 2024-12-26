import unittest

from Transformer import (
    ComplexProxy,
    DictProxy,
    DynamicProxy,
    FloatProxy,
    FrozensetProxy,
    IntProxy,
    StrProxy,
    Transformer,
    TupleProxy,
)


class TestTransformer(unittest.TestCase):

    def setUp(self):
        self.transformer = Transformer()

    def test_basic_types(self):
        # Test integers
        int_val = self.transformer.transform(42)
        self.assertIsInstance(int_val, IntProxy)
        self.assertEqual(int_val + 1, 43)

        # Test floats
        float_val = self.transformer.transform(3.14)
        self.assertIsInstance(float_val, FloatProxy)
        self.assertAlmostEqual(float_val * 2, 6.28)

        # Test strings
        str_val = self.transformer.transform("hello")
        self.assertIsInstance(str_val, StrProxy)
        self.assertEqual(str_val + " world", "hello world")

        # Test complex numbers
        complex_val = self.transformer.transform(1 + 2j)
        self.assertIsInstance(complex_val, ComplexProxy)
        self.assertEqual(complex_val * 2, (2 + 4j))

    def test_container_types(self):
        # Test lists
        list_val = self.transformer.transform([1, 2, 3])
        self.assertIsInstance(list_val, DynamicProxy)
        list_val.append(4)
        self.assertEqual(list_val._obj, [1, 2, 3, 4])

        # Test tuples
        tuple_val = self.transformer.transform((1, 2, 3))
        self.assertIsInstance(tuple_val, TupleProxy)
        self.assertEqual(tuple_val + (4, ), (1, 2, 3, 4))

        # Test sets
        set_val = self.transformer.transform({1, 2, 3})
        self.assertIsInstance(set_val, DynamicProxy)
        set_val.add(4)
        self.assertEqual(set_val._obj, {1, 2, 3, 4})

        # Test frozensets
        frozenset_val = self.transformer.transform(frozenset([1, 2, 3]))
        self.assertIsInstance(frozenset_val, FrozensetProxy)
        self.assertEqual(frozenset_val | {4}, frozenset([1, 2, 3, 4]))

    def test_dict_operations(self):
        dict_val = self.transformer.transform({"a": 1, "b": {"c": 2}})
        self.assertIsInstance(dict_val, DictProxy)

        # Test attribute-style access
        self.assertEqual(dict_val.a, 1)
        self.assertEqual(dict_val.b.c, 2)

        # Test item-style access
        self.assertEqual(dict_val["a"], 1)
        self.assertEqual(dict_val["b"]["c"], 2)

        # Test path-based access
        self.assertEqual(dict_val["b.c"], 2)

        # Test setting values
        dict_val.d = 3
        self.assertEqual(dict_val.d, 3)
        dict_val["e.f.g"] = 4
        nested_val = dict_val["e"]["f"]["g"]
        self.assertEqual(nested_val, 4)

    def test_nested_structures(self):
        nested = self.transformer.transform({
            "list": [1, {
                "a": 2
            }, (3, 4)],
            "dict": {
                "set": {5, 6},
                "tuple": (7, 8)
            },
            "complex": {
                "real": 1.0,
                "imag": 2.0
            }
        })

        self.assertEqual(nested.list[1].a, 2)
        self.assertIsInstance(nested.list[2], TupleProxy)
        self.assertTrue(5 in nested.dict.set)
        self.assertEqual(nested.dict.tuple[1], 8)

    def test_type_conversions(self):
        # Test numeric conversions
        num = self.transformer.transform(42)
        self.assertEqual(float(num), 42.0)
        self.assertEqual(complex(num), 42 + 0j)
        self.assertEqual(str(num), "42")

        # Test string conversions
        text = self.transformer.transform("123")
        self.assertEqual(int(text), 123)
        self.assertEqual(float(text), 123.0)

    def test_method_interception(self):
        list_val = self.transformer.transform([1, 2, 3])
        list_val.append(4)
        list_val.extend([5, 6])
        list_val.insert(0, 0)
        self.assertEqual(list_val._obj, [0, 1, 2, 3, 4, 5, 6])

    def test_error_handling(self):
        obj = self.transformer.transform({})

        # Test invalid path access
        with self.assertRaises(KeyError):
            _ = obj["nonexistent.path"]

        # Test invalid type operation
        with self.assertRaises(TypeError):
            _ = obj + 1

        # Test invalid attribute access
        with self.assertRaises(AttributeError):
            _ = obj.nonexistent

    def test_custom_class_wrapping(self):

        class TestClass:

            def __init__(self, value):
                self.value = value

            def get_value(self):
                return self.value

        WrappedClass = self.transformer.wrap_class(TestClass)
        obj = WrappedClass(42)
        self.assertEqual(obj.value, 42)
        self.assertEqual(obj.get_value(), 42)

    def test_reference_tracking(self):
        original = {"value": 42}
        transformed = self.transformer.transform(original)
        self.transformer.reshape_references(original, transformed)

        # Test that the original reference was replaced
        self.assertIs(transformed._obj, original)

    def test_immutable_operations(self):
        # Test operations that return new objects
        str_val = self.transformer.transform("hello")
        upper_str = str_val.upper()
        self.assertIsInstance(upper_str, StrProxy)
        self.assertEqual(upper_str, "HELLO")

        int_val = self.transformer.transform(5)
        squared = int_val**2
        self.assertIsInstance(squared, IntProxy)
        self.assertEqual(squared, 25)

    def test_advanced_container_operations(self):
        # Test list slicing
        list_val = self.transformer.transform([1, 2, 3, 4, 5])
        self.assertEqual(list_val[1:4], [2, 3, 4])
        list_val[1:4] = [20, 30, 40]
        self.assertEqual(list_val._obj, [1, 20, 30, 40, 5])

        # Test dict merging
        dict1 = self.transformer.transform({"a": 1})
        dict2 = {"b": 2}
        dict1.update(dict2)
        self.assertEqual(dict1._obj, {"a": 1, "b": 2})

    def test_special_methods(self):
        # Test comparison operations
        num1 = self.transformer.transform(5)
        num2 = self.transformer.transform(10)
        self.assertTrue(num1 < num2)
        self.assertFalse(num1 > num2)
        self.assertNotEqual(num1, num2)

        # Test container methods
        list_val = self.transformer.transform([1, 2, 3])
        self.assertTrue(2 in list_val)
        self.assertFalse(4 in list_val)
        self.assertEqual(len(list_val), 3)


if __name__ == "__main__":
    unittest.main()
