from moirai_engine.sockets.socket import Socket, SocketType, SocketStatus


class OutputSocket(Socket):
    def __init__(self, id: str, label: str, type: SocketType, parent=None):
        super().__init__(id, label, type)
        self._value = None
        self.parent = parent

    def resolve(self):
        if self.status == SocketStatus.PENDING:
            self.status = SocketStatus.RESOLVING
            self.parent.run()

    def get_full_path(self):
        return super().get_full_path("outputs")
