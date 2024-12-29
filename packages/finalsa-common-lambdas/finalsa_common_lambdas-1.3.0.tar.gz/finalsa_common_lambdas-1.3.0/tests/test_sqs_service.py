from finalsa.common.lambdas.sqs import SqsHandler, SqsEvent
from finalsa.common.models import SqsMessage
from json import dumps
from finalsa.sqs.client import SqsServiceTest
from pydantic import BaseModel


def test_sqs_event_parsing():
    event = {
        "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
        "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
        "body": "test",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
        "messageAttributes": {},
        "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
        "eventSource": "aws:sqs",
        "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
        "awsRegion": "us-west-2",
    }

    event = SqsEvent.from_sqs_lambda_event(event)

    assert event.message_id == "c80e8021-a70a-42c7-a470-796e1186f753"
    assert event.receipt_handle == "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a..."
    assert event.body == "test"
    assert event.attributes["ApproximateReceiveCount"] == "1"
    assert event.attributes["SentTimestamp"] == "1523232000000"
    assert event.attributes["SenderId"] == "123456789012"
    assert event.attributes["ApproximateFirstReceiveTimestamp"] == "1523232000001"
    assert event.message_attributes == {}
    assert event.md5_of_body == "098f6bcd4621d373cade4e832627b4f6"
    assert event.event_source == "aws:sqs"
    assert event.event_source_arn == "arn:aws:sqs:us-west-2:123456789012:MyQueue"
    assert event.aws_region == "us-west-2"


def test_sqs_event_parsing_with_sns_message():

    body = {"phone_number": "5523408612", "text_message": "asdfghj"}
    payload_body = {"id": "fb275956-2666-427d-afa6-4a0b8311e5b7", "topic": "free-form-messages-topic",
                    "payload": body, "correlation_id": "slack-bot-EW4L", "timestamp": "2024-09-27T06:15:30.526717+00:00"}
    sns_body = {
        "Type": "Notification",
        "MessageId": "4ee0673a-d465-5c0e-8264-384a9ba76fc7",
        "TopicArn": "arn:aws:sns:us-east-1:472541902293:free-form-messages-topic",
        "Message": payload_body,
        "Timestamp": "2024-09-27T06:15:30.756Z",
        "SignatureVersion": "1",
        "Signature": "FgbUOwA+MpAtjhX2o2zcGy73eT7NS2dG1FAzV5RyZffYV/iQ8jVGmwIwxDFKDZnEdQK5vn7xJaW91kZI1F60cbCtWHHohb8EY8qoUh8NTR/dX78ST53JygQCZdjRbuaWfkHmcE/AiyISYvdMa/qnbh4AgWwnrCrXGPk0egh5Z6oMXc0YJfumi6EEui/oCI+W1QTerK+Vu9Dy4XZMXXjCCuwCW3DysyDmRJQAqLng53Cf+VCBzpPAKwTBzznlW4LM3XkPcET/xQ3JEpRMtx4M61M5fHZQy0n8XGBa8nYU3lAIqeJ+zTumaFdXRBxQwT1TP0cW/PzkqlSkrfAOwKKI3Q==",
        "SigningCertURL": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-60eadc530605d63b8e62a523676ef735.pem",
        "UnsubscribeURL": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:472541902293:free-form-messages-topic:b8e4850d-28d5-45f5-b286-b26f4220d185",
        "MessageAttributes": {
            "trace_id": {"Type": "String", "Value": "597de260-bb55-4889-880b-a19c524f8d6a"},
            "span_id": {"Type": "String", "Value": "6e776aaf-5a36-4476-9f4f-732c49a0919e"},
            "correlation_id": {"Type": "String", "Value": "slack-bot-EW4L"}
        }
    }

    event = {
        "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
        "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
        "body": dumps(sns_body),
        "attributes": {
            "ApproximateReceiveCount": "1",
            "SentTimestamp": "1523232000000",
            "SenderId": "123456789012",
            "ApproximateFirstReceiveTimestamp": "1523232000001",
        },
        "messageAttributes": {},
        "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
        "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
        "eventSource": "aws:sqs",
        "awsRegion": "us-west-2",
    }

    event = SqsEvent.from_sqs_lambda_event(event)

    assert event.message_id == "c80e8021-a70a-42c7-a470-796e1186f753"
    assert event.receipt_handle == "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a..."
    assert event.body == dumps(sns_body)
    assert event.attributes["ApproximateReceiveCount"] == "1"
    assert event.attributes["SentTimestamp"] == "1523232000000"
    assert event.attributes["SenderId"] == "123456789012"
    assert event.attributes["ApproximateFirstReceiveTimestamp"] == "1523232000001"
    assert event.message_attributes == {}
    assert event.md5_of_body == "098f6bcd4621d373cade4e832627b4f6"
    assert event.event_source == "aws:sqs"
    assert event.event_source_arn == "arn:aws:sqs:us-west-2:123456789012:MyQueue"
    assert event.aws_region == "us-west-2"

    parsed_body = event.try_parse()

    assert parsed_body == payload_body

    assert event.message_attributes['correlation_id'] is not None


def test_sqs_handler():

    app = SqsHandler.test()

    @app.handler("queue")
    def test_handler():
        return "test"

    @app.default()
    def default_handler():
        return "default"

    assert app.handlers["queue"] == test_handler
    assert app.handlers["default"] == default_handler


def test_process_default():

    app = SqsHandler.test()
    app.sqs_client = SqsServiceTest()

    @app.default()
    def default_handler():
        return "default"

    response = app.process({
        "eventSource": "aws:sqs",
        "Records": [
            {
                "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": "test",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
                "messageAttributes": {},
                "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
                "awsRegion": "us-west-2",
            }
        ]

    }, {})

    assert response == ["default"]

    response = app.process({
        "eventSource": "aws:sqs",
        "Records": [
            {
                "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": dumps({
                    "topic": "queue"
                }),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
                "messageAttributes": {},
                "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
                "awsRegion": "us-west-2",
            }
        ]

    }, {})

    assert response == ["default"]


def test_sqs_body_parse():

    app = SqsHandler.test()
    app.sqs_client = SqsServiceTest()

    class TestRequest(BaseModel):
        test: str

    @app.default()
    def default_handler(body: TestRequest):
        return body.test

    response = app.process({
        "eventSource": "aws:sqs",
        "Records": [
            {
                "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": dumps({
                    "test": "test"
                }),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
                "messageAttributes": {},
                "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
                "awsRegion": "us-west-2",
            }
        ]

    }, {})

    assert response == ["test"]


def test_from_sqs_message():
    real_payload = {
        "test": "123e4567-e89b-12d3-a456-426614174000"
    }

    sqs_message = SqsMessage(
        id="c80e8021-a70a-42c7-a470-796e1186f753",
        topic="mytopic",
        payload=dumps(real_payload),
        correlation_id="123e4567-e89b-12d3-a456-426614174000",

    )
    sns_payload = {
        'Type': 'Notification',
        'TopicArn': 'mytopic1',
        'Message': sqs_message.model_dump_json(),
        'MessageAttributes': {'correlation_id': {
            'Type': 'String', 'Value': '123e4567-e89b-12d3-a456-426614174000'
        }}
    }

    app = SqsHandler.test()
    app.sqs_client = SqsServiceTest()

    @app.handler("mytopic")
    def test_handler(message: dict):
        return message

    response = app.process({
        "eventSource": "aws:sqs",
        "Records": [
            {
                "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": dumps(sns_payload),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
                "messageAttributes": {},
                "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
                "awsRegion": "us-west-2",
            }
        ]

    }, {})

    assert response == [real_payload]


def test_from_sqs_message():
    real_payload = {
        "test": "123e4567-e89b-12d3-a456-426614174000"
    }

    sqs_message = SqsMessage(
        id="c80e8021-a70a-42c7-a470-796e1186f753",
        topic="mytopic",
        payload=dumps(real_payload),
        correlation_id="123e4567-e89b-12d3-a456-426614174000",

    )
    sns_payload = {
        'Type': 'Notification',
        'TopicArn': 'mytopic1',
        'Message': sqs_message.model_dump_json(),
        'MessageAttributes': {'correlation_id': {
            'Type': 'String', 'Value': '123e4567-e89b-12d3-a456-426614174000'
        }}
    }

    app = SqsHandler.test()
    app.sqs_client = SqsServiceTest()

    @app.handler("mytopic")
    def test_handler(message: dict):
        return message

    response = app.process({
        "eventSource": "aws:sqs",
        "Records": [
            {
                "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": dumps(sns_payload),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
                "messageAttributes": {},
                "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
                "awsRegion": "us-west-2",
            }
        ]

    }, {})

    assert response == [real_payload]
