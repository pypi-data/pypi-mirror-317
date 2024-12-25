import logging
import select
import threading
import time
from selectors import DefaultSelector, EVENT_READ

import socket
import traceback
from typing import Dict, List, Set

from common.logger_factory import LoggerFactory
from common.register_append_data import ResisterAppendData
from constant.system_constant import SystemConstant

"""
这里只监听了 socket  的可读状态 
"""
import socket
from typing import Dict, Callable

class SocketThread(threading.Thread):
    def __init__(self, s: socket.socket, callback: Callable[[socket.socket, ResisterAppendData], None], data: ResisterAppendData):
        super().__init__()
        self.s = s
        self.callback = callback
        self.data = data
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            try:
                # Wait for the socket to be ready for reading without blocking
                ready_to_read, _, _ = select.select([self.s], [], [], 1)
                if ready_to_read:
                    self.callback(self.s, self.data)
            except Exception as e:
                LoggerFactory.get_logger().error(traceback.format_exc())
                break

class SelectPool:

    def __init__(self):
        self.is_running = True
        self.fileno_to_client: Dict[int, socket.socket] = dict()
        self.socket_threads: Dict[int, threading.Thread] = {}
        self.socket_to_lock: Dict[socket.socket, threading.Lock] = {}
        self.waiting_register_socket: Set[socket.socket] = set()

    def stop(self):
        self.is_running = False
        for thread in self.socket_threads.values():
            if thread.is_alive():
                thread.join()  # Wait for all threads to finish

    def clear(self):
        for s in list(self.socket_threads.keys()):
            self.unregister(s)
        self.fileno_to_client.clear()
        self.waiting_register_socket.clear()
        self.socket_to_lock.clear()

    def register(self, s: socket.socket, data: ResisterAppendData):
        self.socket_to_lock[s] = threading.Lock()
        self.fileno_to_client[s.fileno()] = s

        def socket_listener():
            while s in self.socket_to_lock:
                try:
                    ready_to_read, _, _ = select.select([s], [], [], 1)
                    if ready_to_read:
                        data.callable_(s, data)
                except Exception as e:
                    LoggerFactory.get_logger().error(traceback.format_exc())
                    break

        thread = threading.Thread(target=socket_listener, daemon=True)
        self.socket_threads[s.fileno()] = thread
        thread.start()

    def unregister_and_register_delay(self, s: socket.socket, data: ResisterAppendData, delay_time: int):
        """取消注册, 并在指定秒后注册"""
        self.unregister(s)

        def _register_again():
            try:
                time.sleep(delay_time)
                if s not in self.socket_to_lock:
                    return
                is_exceed, remain = data.speed_limiter.is_exceed()
                if is_exceed:
                    if LoggerFactory.get_logger().isEnabledFor(logging.DEBUG):
                        LoggerFactory.get_logger().debug('delay register again, maybe next: %.2f seconds "  ' % (remain / data.speed_limiter.max_speed))
                    threading.Timer(delay_time, _register_again).start()
                    return
                self.register(s, data)
            except Exception:
                LoggerFactory.get_logger().error(traceback.format_exc())
                raise

        threading.Timer(delay_time, _register_again).start()

    def unregister(self, s: socket.socket):
        fileno = s.fileno()
        if fileno in self.socket_threads:
            thread = self.socket_threads.pop(fileno)
            if thread.is_alive():
                # There's no direct way to stop a thread. We rely on the condition inside the thread.
                pass
        if s in self.socket_to_lock:
            with self.socket_to_lock[s]:
                if s in self.waiting_register_socket:
                    self.waiting_register_socket.remove(s)
                if fileno in self.fileno_to_client:
                    self.fileno_to_client.pop(fileno)
                self.socket_to_lock.pop(s)

    def run(self):
        while self.is_running:
            time.sleep(1)  # Keep the