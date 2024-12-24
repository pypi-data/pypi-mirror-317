from moirai_engine.actions.action import Action, ActionStatus


class EndAction(Action):
    def __init__(
        self, id: str = "end", label: str = "End Action", description: str = ""
    ):
        super().__init__(id, label, description)
        self.on_success = None

    def execute(self):
        self.status = ActionStatus.COMPLETED
