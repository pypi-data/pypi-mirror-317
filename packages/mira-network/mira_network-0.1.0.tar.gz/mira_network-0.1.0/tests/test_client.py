import unittest
from mira_network.client import MiraNetwork


class TestMiraNetwork(unittest.TestCase):
    def test_init(self):
        api_key = "test_api_key"
        client = MiraNetwork(api_key)
        self.assertEqual(client.api_key, api_key)

    def test_generate_with_valid_api_key(self):
        api_key = "test_api_key"
        client = MiraNetwork(api_key)
        result = client.generate()
        self.assertIsInstance(result, dict)

    def test_generate_with_invalid_api_key(self):
        client = MiraNetwork("")
        with self.assertRaises(ValueError):
            client.generate()


if __name__ == "__main__":
    unittest.main()

# pypi-AgEIcHlwaS5vcmcCJGUzODI5NjhjLWQ4MTQtNDFhZi1iYjhlLTlmYWYyNDcyZjQ3ZgACKlszLCJjMzJhNWQ1NS1kYjYyLTRiYzEtOWZlMS0xNzEzNGIyZjVjNmQiXQAABiBQXeHWfLbWZOZA8Yw9XyZmDdyy_OonAp3XUeqCJTwBwA
