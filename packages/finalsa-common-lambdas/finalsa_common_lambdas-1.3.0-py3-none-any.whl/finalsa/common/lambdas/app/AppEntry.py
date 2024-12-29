from typing import Optional, Union, Dict, Any, List
from finalsa.common.lambdas.sqs.SqsHandler import SqsHandler
from finalsa.common.lambdas.http.HttpHandler import HttpHandler
from finalsa.sqs.client import SqsServiceTest
from logging import Logger, getLogger
from warnings import warn


class AppEntry():

    def __init__(
        self,
        app_name: Optional[str] = None,
        logger: Optional[Logger] = None
    ) -> None:
        self.app_name = app_name
        if logger is None:
            logger = getLogger("root")
        self.__is_test__ = False
        self.sqs = SqsHandler(self.app_name, logger)
        self.http = HttpHandler(self.app_name, logger)

    def set_app_name(self, app_name: str) -> str:
        self.app_name = app_name
        self.sqs.set_app_name(app_name)
        self.http.set_app_name(app_name)

    def sqs_excecution(self, event: Dict, context: Any) -> List[Optional[Dict]]:
        return self.sqs.process(event, context)

    def http_excecution(self, event: Dict, context: Any) -> Dict:
        return self.http.process(event, context)

    def default_excutor(self, event: Dict, context: Optional[Any] = None) -> Union[List[Optional[Dict]], Dict]:
        warn("Use execute instead", DeprecationWarning)
        return self.execute(event, context)

    def execute(self, event: Dict, context: Optional[Any] = None) -> Union[List[Optional[Dict]], Dict]:
        if context is None:
            context = {}
        is_sqs = event.get("Records", None)
        if is_sqs:
            return self.sqs_excecution(event, context)
        return self.http_excecution(event, context)

    def set_test_mode(self) -> None:
        self.__is_test__ = True
        self.sqs.get_sqs_client(default=SqsServiceTest)
