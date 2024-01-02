import unittest
from py_utils.reliable_post import Message


class MessageTestCase(unittest.TestCase):

    def setUp(self):
        self.url = "http://test.com"
        self.body = {"one": 1, "2": "two"}
        self.txt = '{"url": "http://test.com", "body": {"one": 1, "2": "two"}, "state": "pending"}'
        self.state = "pending"

    def test_dumps(self):
        msg = Message(self.url, self.body)
        txt = msg.dumps()
        self.assertEqual(txt, self.txt)

    def test_loads(self):
        new_msg = Message.loads(self.txt)
        self.assertEqual(new_msg.url, self.url)
        self.assertEqual(new_msg.body, self.body)
        self.assertEqual(new_msg.state, self.state)


if __name__ == '__main__':
    unittest.main()
