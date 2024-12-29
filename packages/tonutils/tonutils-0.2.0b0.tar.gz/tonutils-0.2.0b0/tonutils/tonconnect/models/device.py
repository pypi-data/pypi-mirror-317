from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DeviceInfo:
    platform: str
    app_name: str
    app_version: str
    max_protocol_version: int
    features: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DeviceInfo:
        return cls(
            platform=data["platform"],
            app_name=data["appName"],
            app_version=data["appVersion"],
            max_protocol_version=data["maxProtocolVersion"],
            features=data.get("features", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform": self.platform,
            "appName": self.app_name,
            "appVersion": self.app_version,
            "maxProtocolVersion": self.max_protocol_version,
            "features": self.features,
        }
