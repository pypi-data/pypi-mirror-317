from qtstrap import *
from qtpy.QtWebSockets import *
from qtpy.shiboken import isValid
import json
import queue
import logging


@singleton
class GodotSocket(QObject):
    status_changed = Signal(str)
    message_received = Signal(dict)
    raw_message_received = Signal(str)
    socket_connected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.log = logging.getLogger(__name__)

        self.id = 0
        self.active = False
        self.we_closed = False
        self.reconnect_attempts = 0
        self.max_attempts = 5

        self.url = ''

        self.socket = QWebSocket()
        self.socket.connected.connect(self.connected)
        self.socket.disconnected.connect(self.disconnected)
        self.socket.textMessageReceived.connect(self.recieve)

        self.queue = queue.Queue()
        self.history = {}
        self.callbacks = {}

    def set_status(self, status):
        self.status_changed.emit(status)
        if status == 'active':
            self.reconnect_attempts = 0
            self.active = True
            self.socket_connected.emit()
            self.process_queue()

        elif status == 'inactive':
            self.reconnect_attempts = 0
            self.active = False

        elif status == 'failed':
            self.active = False

        elif status == 'reconnecting':
            self.active = False

    def connected(self):
        def auth_cb(msg):
            if msg['authRequired']:
                pass
            else:
                self.set_status('active')

        self._send({'request-type': 'GetAuthRequired'}, auth_cb)

    def disconnected(self):
        if self.we_closed:
            self.we_closed = False
            self.set_status('inactive')
            return
        self.set_status('reconnecting')
        self.retry()

    def retry(self):
        self.reconnect_attempts += 1
        if self.reconnect_attempts >= self.max_attempts:
            self.log.info('Max retry attempts reached, aborting')
            self.set_status('inactive')
            return

        self.set_status('reconnecting')
        if isValid(self.socket):
            self.socket.close()
            self.log.info('Attempting to reconnect')
            self.socket.open(self.url)

    def open(self, url, port, password=''):
        self.url = QUrl(f'ws://{url}:{port}')
        self.log.info(f'Attempting to connect to Godot at: {self.url}')
        self.password = password
        self.socket.open(self.url)

    def close(self):
        self.log.info(f'Closing socket')
        self.socket.close()

    def _send(self, payload, callback=None):
        payload['message-id'] = str(self.id)
        self.history[self.id] = payload

        self.log.info(f'TX: {payload}')

        if callback:
            self.callbacks[str(self.id)] = callback

        message = json.dumps(payload)
        self.socket.sendTextMessage(message)
        self.id += 1

    def send(self, payload, callback=None):
        if self.active:
            self._send(payload, callback)
        else:
            self.queue.put((payload, callback))

    def process_queue(self):
        while not self.queue.empty():
            payload, callback = self.queue.get()
            self._send(payload, callback)

    def recieve(self, message):
        self.raw_message_received.emit(message)
        msg = json.loads(message)
        self.message_received.emit(msg)

        self.log.info(f'RX: {message}')

        # process callbacks
        if 'message-id' in msg:
            if msg['message-id'] in self.callbacks:
                self.callbacks[msg['message-id']](msg)
