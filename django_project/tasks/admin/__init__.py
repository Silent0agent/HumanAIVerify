__all__ = (
    "TextTaskAdmin",
    "TextTaskCheckAdmin",
    "ImageTaskAdmin",
    "ImageTaskCheckAdmin",
)

from tasks.admin.image import ImageTaskAdmin, ImageTaskCheckAdmin
from tasks.admin.text import TextTaskAdmin, TextTaskCheckAdmin
