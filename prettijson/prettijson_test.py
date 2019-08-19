import unittest

import azure.functions as func
import prettijson


class prettijsonTestCases(unittest.TestCase):
    def test_content_headers(self):
        request = func.HttpRequest(
            method="POST",
            body="{}",
            url="/api/prettijson",
            headers={"Content-Type": ""}
        )

        expected = func.HttpResponse(
            b"Content-Type header must be set to 'application/json'\n",
            status_code=400
        )

        resp = prettijson.main(request)
        self.assertEqual(resp.get_body(), expected.get_body())
        self.assertEqual(resp.status_code, expected.status_code)

    def test_http_methods(self):
        request = func.HttpRequest(
            body="",
            method="GET",
            url="/api/prettijson"
        )

        expected = func.HttpResponse(
            b"HTTP Method GET not allowed\n",
            status_code=400
        )

        resp = prettijson.main(request)
        self.assertEqual(resp.get_body(), expected.get_body())
        self.assertEqual(resp.status_code, expected.status_code)

    def test_invalid_json(self):
        request = func.HttpRequest(
            body=b"[[",
            method="POST",
            url="/api/prettijson",
            headers={"Content-Type": "application/json"}
        )
        
        expected = func.HttpResponse(
            b"Request was invalid JSON\n",
            status_code=400
        )

        resp = prettijson.main(request)
        self.assertEqual(resp.get_body(), expected.get_body())
        self.assertEqual(resp.status_code, expected.status_code)

    def test_options_method(self):
        request = func.HttpRequest(
            body="",
            method="OPTIONS",
            url="/api/prettijson"
        )

        expected = func.HttpResponse(
            b'["OPTIONS", "POST"]',
            status_code=200
        )

        resp = prettijson.main(request)
        self.assertEqual(resp.get_body(), expected.get_body())
        self.assertEqual(resp.status_code, expected.status_code)


    def test_valid_json(self):
        request = func.HttpRequest(
            method="POST",
            body=b'["a","b","c","d"]',
            url="/api/prettijson",
            headers={"Content-Type": "application/json"}
        )

        expected = func.HttpResponse(
            b'[\n  "a", \n  "b", \n  "c", \n  "d"\n]\n',
            status_code=200
        )

        resp = prettijson.main(request)
        self.assertEqual(resp.get_body(), expected.get_body())
        self.assertEqual(resp.status_code, expected.status_code)


if __name__ == "__main__":
    unittest.main()

