"""Consciousness-aware data filtering and flash event logic."""

from typing import Any, Dict, List


class FlashEventManager:
    """Manage flash insight events."""

    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    def trigger_insight_flash(self, pattern_recognition_event: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger an insight flash from a pattern recognition event."""
        flash = {
            "event": pattern_recognition_event,
            "flash_triggered": True,
        }
        self.events.append(flash)
        return flash


class FilterFlash:
    """Filter incoming data using a consciousness threshold."""

    def __init__(self, consciousness_threshold: float = 0.5) -> None:
        self.consciousness_threshold = consciousness_threshold
        self.event_manager = FlashEventManager()

    def filter_data(self, data: Any, cognitive_load: float = 0.0) -> Any:
        """Filter data based on the current cognitive load."""
        if cognitive_load > self.consciousness_threshold:
            return []

        if self._detect_pattern(data):
            self.event_manager.trigger_insight_flash({"data": data})

        return data

    @staticmethod
    def _detect_pattern(data: Any) -> bool:
        """Simple pattern detection placeholder."""
        return isinstance(data, dict) and data.get("pattern") is True
