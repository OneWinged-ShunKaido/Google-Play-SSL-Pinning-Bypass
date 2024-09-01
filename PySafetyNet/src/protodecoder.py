from src.customproto.safetynet_decoder import SafetyNetDecoder
from src.customproto.play_integrity_decoder import PlayIntegrityDecoder
from src.droiguard.utils.droidguard_utils import DroidGuardUtils


class ProtoDecoder(SafetyNetDecoder, PlayIntegrityDecoder, DroidGuardUtils):
    """An interface between Safetynet & Play Integrity"""
    state: dict

    def __init__(self):
        super().__init__()

    def _on_state(self):
        if self.state.get("action") in self.safetynet_action:
            self.perform_sn_action()

        elif self.state.get("action") in self.play_integrity_action:
            self.perform_pi_action()

        else:
            return False

    def _on_response(self):
        ...












