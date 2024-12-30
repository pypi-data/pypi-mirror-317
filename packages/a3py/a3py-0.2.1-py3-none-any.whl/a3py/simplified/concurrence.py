# -*- coding: utf-8 -*-
import logging
import os
import signal
import traceback
from threading import Event, Thread
from typing import List

logger = logging.getLogger(__name__)


def force_exit_from_threads(reason: str, code: int = -1):
    logger.critical(f"About to be forced to exit, reason being: {reason}")
    os._exit(code)  # noqa


# 适合有阻塞wait的情况
class GracefulExitThread(Thread):
    def __init__(self, exit_event: Event, **params):
        super().__init__(**params)
        self.exit_event = exit_event


def run_threads_until_any_exits(thread_list: List[Thread], exit_event: Event):
    def _wrap_run(raw_run, event: Event):
        def _wrapper():
            self = raw_run.__self__
            try:
                raw_run()
                logger.info(f"A thread has finished: {self}")
            except SystemExit:
                logger.warning(f"A thread has exited: {self}")
            except Exception as e:
                logger.critical(
                    f"A thread has aborted by exception: {self}, {e}, traceback:\n {traceback.format_exc()}"
                )
            event.set()

        return _wrapper

    for thread in thread_list:
        thread.run = _wrap_run(thread.run, exit_event)
        thread.start()

    for thread in thread_list:
        if not thread.daemon:
            thread.join()


def set_exit_signals(exit_event: Event, signal_list: List[int] | None = None):
    def _signal_handler(sig: int, frame):
        logger.info(f"Received exit signal: {sig}, frame: {frame}")
        exit_event.set()

    signal_list = signal_list or [signal.SIGINT, signal.SIGTERM]
    for s in signal_list:
        signal.signal(s, _signal_handler)
