import os
import unittest

from whatsappchattodf import WhatsappChatToDF


class TestWhatsappChatToDF(unittest.TestCase):

    def setUp(self):
        # Get the file path for test_chat.txt
        self.test_file_path = os.path.join(os.path.dirname(__file__), "test_chat.txt")

    def test_run(self):
        wctd = WhatsappChatToDF(self.test_file_path)
        df = wctd.run()
        self.assertIsNotNone(df)
        self.assertIn("Timestamp", df.columns)
        self.assertIn("User", df.columns)
        self.assertIn("Message", df.columns)
        self.assertGreater(len(df), 0)  # Ensure the DataFrame is not empty


if __name__ == "__main__":
    unittest.main()
