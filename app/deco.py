import logging
import typing as t


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def traced(func: t.Callable):
    def _inner(*args, **kwargs):
        logger.debug(f"start:{func.__name__}")
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as ex:
            logger.exception("trace_logger caught exception in callable")
            raise
        finally:
            logger.debug(f"start:{func.__name__}")
        return result

    return _inner
