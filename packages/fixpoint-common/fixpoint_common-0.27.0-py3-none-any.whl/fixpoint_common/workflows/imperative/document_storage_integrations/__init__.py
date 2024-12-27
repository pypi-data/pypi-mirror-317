"""Document storage integrations for workflows"""

__all__ = ["OnDiskDocStorage", "ApiDocStorage"]

from .on_disk import OnDiskDocStorage
from .api import ApiDocStorage
