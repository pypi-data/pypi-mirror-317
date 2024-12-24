"""SILK2 logbook python module
"""
import inspect
__all__ = []

try:
    import logbook
except ImportError:
    print('SILK2.Tools.logger requires "logbook" package.')
    print('Install it via command:')
    print('    pip3 install logbook')
    raise

from .logger import (Log)

def file_lineno():
    frame = inspect.currentframe()  # 获取当前帧
    line_number = frame.f_back.f_lineno    # 获取当前行号
    return f"[{frame.f_back.f_code.co_filename}:{line_number}]"