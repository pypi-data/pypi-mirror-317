from finalsa.common.lambdas.app.App import App
from uuid import uuid4
from datetime import datetime, timezone
from typing import Dict, Union, List, Optional
from finalsa.traceability.functions import (
    HTTP_HEADER_CORRELATION_ID, HTTP_HEADER_TRACE_ID)
from json import dumps


class TestContext():

    def __init__(self):
        self.aws_request_id = f"test-{uuid4()}"


class Consumer():

    def __init__(self, app: App) -> None:
        self.app = app

    def consume(self, payload: Dict, topic: str) -> Union[List[Optional[Dict]], Dict]:

        if not self.app.__is_test__:
            raise Exception("Test mode not enabled")
        now = datetime.now(timezone.utc)
        if isinstance(payload, Dict):
            payload = dumps(payload)
        request = {
            "id": str(uuid4()),
            "topic": topic,
            "payload": payload,
            "correlation_id": str(uuid4()),
            "timestamp": now.isoformat(),
        }
        sns_event = {
            "Type": "Notification",
            "MessageId": str(uuid4()),
            "TopicArn": f"arn:aws:sns:us-east-1:123456789012:{topic}",
            "Message": dumps(request),
            "Timestamp": now.isoformat(),
            "SignatureVersion": "1",
            "Signature": "EXAMPLE",

        }
        data = {
            "Records": [
                {
                    "messageId": str(uuid4()),
                    "receiptHandle": "MessageReceiptHandle",
                    "body": dumps(sns_event),
                    "attributes": {
                        "ApproximateReceiveCount": "1",
                        "SentTimestamp": "1523232000000",
                        "SenderId": "123456789012",
                        "ApproximateFirstReceiveTimestamp": "1523232000001"
                    },
                }
            ]
        }
        context = TestContext()
        return self.app.execute(data, context)


class HttpClient():

    def __init__(self, app: App) -> None:
        self.app = app

    def fix_headers(self, headers: Dict) -> Dict:
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
        if HTTP_HEADER_CORRELATION_ID not in headers:
            headers[HTTP_HEADER_CORRELATION_ID] = f"test-{uuid4()}"
        if HTTP_HEADER_TRACE_ID not in headers:
            headers[HTTP_HEADER_TRACE_ID] = f"test-{uuid4()}"
        return headers

    def get(self, path: str, headers: Dict = {}) -> Dict:
        if not self.app.__is_test__:
            raise Exception("Test mode not enabled")
        data = {
            "httpMethod": "GET",
            "path": path,
            "headers": self.fix_headers(headers),
            "body": "",
        }
        return self.app.execute(data, TestContext())

    def post(self, path: str, payload: Dict, headers: Dict = {}) -> Dict:
        if not self.app.__is_test__:
            raise Exception("Test mode not enabled")
        if isinstance(payload, Dict):
            payload = dumps(payload)
        data = {
            "httpMethod": "POST",
            "path": path,
            "headers": self.fix_headers(headers),
            "body": payload,
        }
        return self.app.execute(data, TestContext())

    def put(self, path: str, payload: Dict, headers: Dict = {}) -> Dict:
        if not self.app.__is_test__:
            raise Exception("Test mode not enabled")
        if isinstance(payload, Dict):
            payload = dumps(payload)
        data = {
            "httpMethod": "PUT",
            "path": path,
            "headers": self.fix_headers(headers),
            "body": payload,
        }
        return self.app.execute(data, TestContext())

    def delete(self, path: str, headers: Dict = {}) -> Dict:
        if not self.app.__is_test__:
            raise Exception("Test mode not enabled")
        data = {
            "httpMethod": "DELETE",
            "path": path,
            "headers": self.fix_headers(headers),
            "body": "",
        }
        return self.app.execute(data, TestContext())

    def patch(self, path: str, payload: Dict, headers: Dict = {}) -> Dict:
        if not self.app.__is_test__:
            raise Exception("Test mode not enabled")
        if isinstance(payload, Dict):
            payload = dumps(payload)
        data = {
            "httpMethod": "PATCH",
            "path": path,
            "headers": self.fix_headers(headers),
            "body": payload,
        }
        return self.app.execute(data, TestContext())
