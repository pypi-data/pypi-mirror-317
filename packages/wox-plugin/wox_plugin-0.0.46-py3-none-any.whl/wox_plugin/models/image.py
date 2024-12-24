from dataclasses import dataclass, field
from enum import Enum
import json


class WoxImageType(str, Enum):
    """Image type enum for Wox"""

    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    BASE64 = "base64"
    SVG = "svg"
    LOTTIE = "lottie"  # only support lottie json data
    EMOJI = "emoji"
    URL = "url"
    THEME = "theme"


@dataclass
class WoxImage:
    """Image model for Wox"""

    image_type: WoxImageType = field(default=WoxImageType.ABSOLUTE)
    image_data: str = field(default="")

    def to_json(self) -> str:
        """Convert to JSON string with camelCase naming"""
        return json.dumps(
            {
                "Data": self.image_data,
                "Type": self.image_type,
            }
        )

    @classmethod
    def from_json(cls, json_str: str) -> "WoxImage":
        """Create from JSON string with camelCase naming"""
        data = json.loads(json_str)

        if data.get("Type") == "":
            data["Type"] = WoxImageType.ABSOLUTE

        return cls(
            image_type=WoxImageType(data.get("Type")),
            image_data=data.get("Data", ""),
        )

    @classmethod
    def new_base64(cls, data: str) -> "WoxImage":
        """Create a new base64 image"""
        return cls(image_type=WoxImageType.BASE64, image_data=data)

    @classmethod
    def new_svg(cls, data: str) -> "WoxImage":
        """Create a new svg image"""
        return cls(image_type=WoxImageType.SVG, image_data=data)

    @classmethod
    def new_lottie(cls, data: str) -> "WoxImage":
        """Create a new lottie image"""
        return cls(image_type=WoxImageType.LOTTIE, image_data=data)

    @classmethod
    def new_emoji(cls, data: str) -> "WoxImage":
        """Create a new emoji image"""
        return cls(image_type=WoxImageType.EMOJI, image_data=data)

    @classmethod
    def new_url(cls, data: str) -> "WoxImage":
        """Create a new url image"""
        return cls(image_type=WoxImageType.URL, image_data=data)

    @classmethod
    def new_absolute(cls, data: str) -> "WoxImage":
        """Create a new absolute image"""
        return cls(image_type=WoxImageType.ABSOLUTE, image_data=data)

    @classmethod
    def new_relative(cls, data: str) -> "WoxImage":
        """Create a new relative image"""
        return cls(image_type=WoxImageType.RELATIVE, image_data=data)

    @classmethod
    def new_theme(cls, data: str) -> "WoxImage":
        """Create a new theme image"""
        return cls(image_type=WoxImageType.THEME, image_data=data)

    def __str__(self) -> str:
        """Convert image to string"""
        return f"{self.image_type}:{self.image_data}"
