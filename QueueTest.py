import unittest
import requests

class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        self.localhost = __name__
        self.base_url = "http://localhost:5000"

    def test_create_queue1(self):
        URL = self.base_url + "/CreateQueue"
        data = {'queueName': 'test_queue'}
        response = requests.post(url=URL,data=data)
        self.assertEqual(response.json(), {'created': True})
    def test_create_queue2(self):
        URL = self.base_url + "/CreateQueue"
        data = {'queueName': 'test_queue2'}
        requests.post(url=URL, data=data)
        URL = self.base_url + "/CreateQueue"
        data = {'queueName': 'test_queue2'}
        response = requests.post(url=URL,data=data)
        self.assertEqual(response.json(), {'created': False})

    def test_send_message_1(self):
        # First create the queue
        url = self.base_url + "/CreateQueue"
        data = {'queueName': 'test_send1'}
        r = requests.post(url=url, data=data)
        self.assertEqual(r.json(), {'created': True})
        url = self.base_url + "/SendMessage"
        params = {'queueName': 'test_send1', 'delayInMS': 1, 'message': 'test_message'}
        response = requests.post(url=url, data=params)
        self.assertEqual(response.json(), {'messageId': 0})

    def test_send_message_2(self):
        # First create the queue
        url = self.base_url + "/CreateQueue"
        data = {'queueName': 'test_send2'}
        r = requests.post(url=url, data=data)
        self.assertEqual(r.json(), {'created': True})
        url = self.base_url + "/SendMessage"
        params = {'queueName': 'test_send2', 'delayInMS': 1, 'message': 'test_message'}
        requests.post(url=url, data=params)
        response = requests.post(url=url, data=params)
        self.assertEqual(response.json(), {'messageId': 1})

    def test_receive_message1(self):
        # First create the queue
        url = self.base_url + "/CreateQueue"
        data = {'queueName': 'test_queue_receive'}
        requests.post(url=url, data=data)

        # Then send a message to the queue
        url = self.base_url + "/SendMessage"
        data = {'queueName': 'test_queue_receive', 'delayInMS': 0, 'message': 'test_message'}
        requests.post(url, data=data)

        # Then receive the message from the queue
        url = self.base_url + "/ReceiveMessage"
        data = {'queueName': 'test_queue_receive'}
        response = requests.get(url, data=data)
        self.assertEqual(response.json(), {'messageId': 0, 'message': 'test_message'})

    def test_receive_message2(self):
        # First create the queue
        url = self.base_url + "/CreateQueue"
        data = {'queueName': 'test_queue_receive2'}
        requests.post(url=url, data=data)

        # Then send a message to the queue
        url = self.base_url + "/SendMessage"
        data = {'queueName': 'test_queue_receive2', 'delayInMS': 0, 'message': 'test_message'}
        requests.post(url, data=data)
        data = {'queueName': 'test_queue_receive2', 'delayInMS': 0, 'message': 'test_message'}
        requests.post(url, data=data)

        url = self.base_url + "/DeleteMessage"
        data = {'queueName': 'test_queue_receive2', 'messageId': 0}
        response = requests.delete(url, data=data)
        self.assertEqual(response.json(), {'wasDeleted': True})

        # Then receive the message from the queue
        url = self.base_url + "/ReceiveMessage"
        data = {'queueName': 'test_queue_receive2'}
        response = requests.get(url, data=data)
        self.assertEqual(response.json(), {'messageId': 1, 'message': 'test_message'})

    def test_delete_message(self):
        # First create the queue
        url = self.base_url + "/CreateQueue"
        data = {'queueName': 'test_queue_delete'}
        requests.post(url, data=data)

        # Then send a message to the queue
        url = self.base_url + "/SendMessage"
        data = {'queueName': 'test_queue_delete', 'delayInMS': 0, 'message': 'test_message'}
        requests.post(url, data=data)

        # Then delete the message from the queue
        url = self.base_url + "/DeleteMessage"
        data = {'queueName': 'test_queue_delete', 'messageId': 0}
        response = requests.delete(url, data=data)
        self.assertEqual(response.json(), {'wasDeleted': True})

    def test_delete_message2(self):
        # First create the queue
        url = self.base_url + "/CreateQueue"
        data = {'queueName': 'test_queue_delete2'}
        requests.post(url, data=data)

        # Then send a message to the queue
        url = self.base_url + "/SendMessage"
        data = {'queueName': 'test_queue_delete2', 'delayInMS': 0, 'message': 'test_message'}
        requests.post(url, data=data)

        # Then delete the message from the queue
        url = self.base_url + "/DeleteMessage"
        data = {'queueName': 'test_queue_delete2', 'messageId': 0}
        response = requests.delete(url, data=data)
        self.assertEqual(response.json(), {'wasDeleted': True})

        url = self.base_url + "/DeleteMessage"
        data = {'queueName': 'test_queue_delete2', 'messageId': 0}
        response = requests.delete(url, data=data)
        self.assertEqual(response.json(), {'wasDeleted': False})

if __name__ == '__main__':
    unittest.main()
