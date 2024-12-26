import logging
import logging.config
import os
from typing import AnyStr

from mag_tools.model.log_type import LogType
from mag_tools.utils.common.string_utils import StringUtils


class Logger:
    __instance = None

    def __init__(self, app: os.PathLike[AnyStr], root_dir: str):
        """
        初始化 Logger 实例，配置日志记录器和日志文件路径。

        :param app: 应用程序路径
        :param root_dir: 根目录路径
        """
        app_name = os.path.splitext(os.path.basename(app))[0]
        self.__root_dir = root_dir

        log_dir = os.path.join(self.__root_dir, "data", app_name, "logs")
        os.makedirs(log_dir, exist_ok=True)

        logging.config.fileConfig(f"{self.__root_dir}\\data\\logging.conf", defaults={'logdir': str(log_dir)})

        self.root_logger = logging.getLogger()

        self.frame_logger = logging.getLogger('frame')

        self.service_logger = logging.getLogger('service')

        self.performance_logger = logging.getLogger('performance')

        Logger.__instance = self

    @staticmethod
    def initialize(app: os.PathLike[AnyStr], root_dir: str):
        """
        初始化 Logger 单例实例。

        :param app: 应用程序路径
        :param root_dir: 根目录路径
        """
        if Logger.__instance is None:
            Logger(app, root_dir)

    @staticmethod
    def debug(*args):
        """
        记录调试级别的日志信息。

        :param args: 日志信息参数，可以是单个消息或 (logger_type, message) 元组
        """
        if Logger.__instance is None:
            raise ValueError("Logger not initialized. Please call initialize first.")

        if len(args) == 1:
            message = args[0]
            Logger.__instance.__debug(LogType.FRAME, message)
        elif len(args) == 2:
            log_type, message = args
            Logger.__instance.__debug(log_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    @staticmethod
    def info(*args):
        """
        记录信息级别的日志信息。

        :param args: 日志信息参数，可以是单个消息、(logger_type, message) 或 (logger_type, message, is_highlight) 元组
        """
        if Logger.__instance is None:
            raise ValueError("Logger not initialized. Please call initialize first.")

        if len(args) == 1:
            message = args[0]
            Logger.__instance.__info(LogType.FRAME, message)
        elif len(args) == 2:
            logger_type, message = args
            Logger.__instance.__info(logger_type, message)
        elif len(args) == 3:
            logger_type, message, is_highlight = args
            if is_highlight:
                Logger.__instance.__info(logger_type, '*'*(StringUtils.get_print_width(message)+8))
                Logger.__instance.__info(logger_type, f'*** {message} ***')
                Logger.__instance.__info(logger_type, '*'*(StringUtils.get_print_width(message)+8))
            else:
                Logger.__instance.__info(logger_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    @staticmethod
    def warning(*args):
        """
        记录警告级别的日志信息。

        :param args: 日志信息参数，可以是单个消息或 (logger_type, message) 元组
        """
        if Logger.__instance is None:
            raise ValueError("Logger not initialized. Please call initialize first.")

        if len(args) == 1:
            message = args[0]
            Logger.__instance.__warning(LogType.FRAME, message)
        elif len(args) == 2:
            logger_type, message = args
            Logger.__instance.__warning(logger_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    @staticmethod
    def error(*args):
        """
        记录错误级别的日志信息。

        :param args: 日志信息参数，可以是单个消息或 (logger_type, message) 元组
        """
        if Logger.__instance is None:
            raise ValueError("Logger not initialized. Please call initialize first.")

        if len(args) == 1:
            message = str(args[0]) if isinstance(args[0], Exception) else args[0]
            Logger.__instance.__error(LogType.FRAME, message)
        elif len(args) == 2:
            logger_type, message = args
            message = str(message) if isinstance(message, Exception) else message
            Logger.__instance.__error(logger_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    def __debug(self, logger_type: LogType, message: str):
        """
        内部方法，记录调试级别的日志信息。

        :param logger_type: 日志类型
        :param message: 日志消息
        """
        self.root_logger.debug(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.debug(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.debug(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.debug(message)

    def __info(self, logger_type: LogType, message: str):
        """
        内部方法，记录信息级别的日志信息。

        :param logger_type: 日志类型
        :param message: 日志消息
        """
        self.root_logger.info(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.info(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.info(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.info(message)

    def __warning(self, logger_type: LogType, message: str):
        """
        内部方法，记录警告级别的日志信息。

        :param logger_type: 日志类型
        :param message: 日志消息
        """
        self.root_logger.warning(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.warning(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.warning(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.warning(message)

    def __error(self, logger_type: LogType, message: str):
        """
        内部方法，记录错误级别的日志信息。

        :param logger_type: 日志类型
        :param message: 日志消息
        """
        self.root_logger.error(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.error(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.error(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.error(message)