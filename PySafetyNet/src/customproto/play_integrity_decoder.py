class PlayIntegrityDecoder:
    message: bytes
    state: dict
    play_integrity_action = ["integrity"]

    def __init__(self):
        super().__init__()

    def perform_pi_action(self):
        content_type = self.state.get("r_type")
        content = self.state.get("content")
        if self.state.get("action") == "integrity":
            ...
