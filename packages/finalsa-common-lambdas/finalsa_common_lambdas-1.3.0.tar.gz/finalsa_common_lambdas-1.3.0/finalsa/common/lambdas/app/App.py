from finalsa.common.lambdas.app.AppEntry import AppEntry
from typing import Optional
from logging import Logger


class App(AppEntry):

    def __init__(
        self,
        app_name: Optional[str] = None,
        logger: Optional[Logger] = None
    ) -> None:
        self.app_name = app_name
        if logger is None:
            logger = Logger("root")
        super().__init__(app_name, logger)

    def register(self, app_entry: AppEntry) -> None:
        app_entry.set_app_name(self.app_name)
        if self.__is_test__:
            app_entry.set_test_mode()
        self.sqs.merge(app_entry.sqs)
        self.http.merge(app_entry.http)
