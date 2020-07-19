import unittest
from app import app, process1, process2, process3


class SetUpTests(unittest.TestCase):
    def setUp(self):
        self.logger = app.logger
        app.testing = True
        self.client = app.test_client()


class TestMainLogics(SetUpTests):
    def test_api_main_path(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            result = self.client.get('/api')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'{"message":"main page for api"}\n', result.data)
        self.assertListEqual(log.output, ['INFO:app:GET method for http://localhost/api, params: ""',
                                          'INFO:app:Process 1 is being performed',
                                          'INFO:app:Process 2 is being performed',
                                          'INFO:app:Process 3 is being performed',
                                          ])

    def test_api_wrong_path(self):
        with self.assertLogs(self.logger, level='ERROR') as log:
            result = self.client.get('/api/non_existing_path')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'{"message":"404. Sorry, we could not find the page"}\n', result.data)
        self.assertListEqual(log.output,
                             ["ERROR:app:GET method for http://localhost/api/non_existing_path, page not found"])

    def test_not_allowed_post_method(self):
        with self.assertLogs(self.logger, level='ERROR') as log:
            result = self.client.post('/api')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'{"message":"POST method is prohibited"}\n', result.data)
        self.assertListEqual(log.output, [
            "ERROR:app:POST method for http://localhost/api is prohibited"])

    def test_not_allowed_delete_method(self):
        with self.assertLogs(self.logger, level='ERROR') as log:
            result = self.client.delete('/api')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'{"message":"DELETE method is prohibited"}\n', result.data)
        self.assertListEqual(log.output, [
            "ERROR:app:DELETE method for http://localhost/api is prohibited"])


class TestErrorParams(SetUpTests):
    def test_api_get_invalid_param(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            result = self.client.get('/api?invalid=1')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'Parameter "invalid=1"', result.data)
        self.assertListEqual(log.output, ['INFO:app:GET method for http://localhost/api?invalid=1, params: "invalid=1"',
                                          'ERROR:app:Error params: "invalid=1" for http://localhost/api'])

    def test_api_delete_invalid_param(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            result = self.client.delete('/api?invalid=1')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'{"message":"DELETE method is prohibited"}\n', result.data)
        self.assertListEqual(log.output, ['ERROR:app:DELETE method for http://localhost/api?invalid=1 is prohibited'])

    def test_api_get_notawaiting_param(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            result = self.client.get('/api?notawaiting=1')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'Parameter "notawaiting=1"', result.data)
        self.assertListEqual(log.output,
                             ['INFO:app:GET method for http://localhost/api?notawaiting=1, params: "notawaiting=1"',
                              'INFO:app:Process 1 is being performed',
                              'INFO:app:Process 2 is being performed',
                              'ERROR:app:Error params: "notawaiting=1" for http://localhost/api'])

    def test_api_put_notawaiting_param(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            result = self.client.put('/api?notawaiting=1')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'{"message":"PUT method is prohibited"}\n', result.data)
        self.assertListEqual(log.output, ['ERROR:app:PUT method for http://localhost/api?notawaiting=1 is prohibited'])


class TestProcessStubs(SetUpTests):
    def test_process1(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            process1(None)
        self.assertListEqual(log.output, ['INFO:app:Process 1 is being performed'])

    def test_process2(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            with self.assertRaises(Exception) as e:
                process2({'notawaiting': '1'})
            self.assertEqual(e.exception.__str__(), 'Parameter "notawaiting=1"')
        self.assertListEqual(log.output, ['INFO:app:Process 2 is being performed'])

    def test_process2_notawaiting_3(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            process2({'notawaiting': '3'})
        self.assertListEqual(log.output, ['INFO:app:Process 2 is being performed'])

    def test_process3(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            process3(None)
        self.assertListEqual(log.output, ['INFO:app:Process 3 is being performed'])


if __name__ == "__main__":
    unittest.main(verbosity=2)

