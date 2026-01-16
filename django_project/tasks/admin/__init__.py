__all__ = (
    'TextTaskAdmin',
    'TextTaskCheckAdmin',
    'ImageTaskAdmin',
    'ImageTaskCheckAdmin',
    'AudioTaskAdmin',
    'AudioTaskCheckAdmin',
)

from tasks.admin.audio import AudioTaskAdmin, AudioTaskCheckAdmin
from tasks.admin.image import ImageTaskAdmin, ImageTaskCheckAdmin
from tasks.admin.text import TextTaskAdmin, TextTaskCheckAdmin
