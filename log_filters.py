import logging


class DebugFilter(logging.Filter):
    def filter(self, record):
        # print('filtering')
        return not (record.levelname != "DEBUG")


class InfoFilter(logging.Filter):
    def filter(self, record):
        # print('filtering')
        return not (record.levelname != "INFO")


class WarningFilter(logging.Filter):
    def filter(self, record):
        # print('filtering')
        return not (record.levelname != "WARNING")


class ErrorFilter(logging.Filter):
    def filter(self, record):
        # print('filtering')
        return not (record.levelname != "ERROR")


class CriticalFilter(logging.Filter):
    def filter(self, record):
        # print('filtering')
        return not (record.levelname != "CRITICAL")
