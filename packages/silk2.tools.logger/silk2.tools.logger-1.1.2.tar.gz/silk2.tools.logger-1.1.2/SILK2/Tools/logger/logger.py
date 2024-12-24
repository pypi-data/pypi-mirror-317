from logbook import Logger, StreamHandler, lookup_level
import sys
import logbook

class Log:
    def __init__(self, name:str, log_level="INFO"):
        '''  Initialize a logging record with interesting information.
        :param name: log name
        :param log_level: log level(DEBUG, INFO, WARNING, ERROR), default is INFO
        '''
        self.__name__ = name
        logbook.set_datetime_format("local")
        log_level_up = log_level.upper()
        self.log_level = "INFO"
        if log_level_up in ("DEBUG","INFO","WARNING", "ERROR"):
            self.log_level = log_level_up

        self.logger = Logger(self.__name__, level=lookup_level(self.log_level))
        self.logger.enable()

        
        console_handler = StreamHandler(sys.stdout)
        log_format = '{record.time:%Y-%m-%d %H:%M:%S} [{record.channel}] [{record.level_name}] {record.message}'
        console_handler.format_string = log_format  # 设置格式
        console_handler.push_application()

        if self.log_level != log_level_up:
            self.logger.warning(f"Can not find log level: {log_level_up}, USE default INFO!")
    
    def set_log_level(self, log_level:str):
        """  设置日志等级  """
        log_level_up = log_level.upper()
        if log_level_up in ("DEBUG","INFO","WARNING", "ERROR"):
            self.log_level = log_level_up
        else:
            self.logger.warning(f"Can not find log level: {log_level_up}, log level not change!")
        self.logger.level_name=lookup_level(self.log_level)

    def get_log_level(self):
        return self.log_level

    def debug(self, *args, **kwargs):
        """Logs a :class:`~logbook.LogRecord` with the level set
        to :data:`~logbook.DEBUG`.
        """
        return self.logger.debug(*args,**kwargs)
    
    def info(self, *args, **kwargs):
        """Logs a :class:`~logbook.LogRecord` with the level set
        to :data:`~logbook.INFO`.
        """
        return self.logger.info(*args,**kwargs)
        
    def warning(self, *args, **kwargs):
        """Logs a :class:`~logbook.LogRecord` with the level set
        to :data:`~logbook.WARNING`.
        """
        return self.logger.warning(*args,**kwargs)
    
    def error(self, *args, **kwargs):
        """Logs a :class:`~logbook.LogRecord` with the level set
        to :data:`~logbook.ERROR`.
        """
        return self.logger.error(*args,**kwargs)
