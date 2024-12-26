from enum import Enum, IntFlag


class ImageExtension(Enum):
    PNG = 0
    JPG = 1
    JPEG = 1  # noqa: PIE796
    GIF = 2
    WEBP = 3

    @property
    def mime_type(self) -> str:
        return {
            ImageExtension.PNG: 'image/png',
            ImageExtension.JPG: 'image/jpeg',
            ImageExtension.GIF: 'image/gif',
            ImageExtension.WEBP: 'image/webp'
        }[self]


class Intents(IntFlag):
    NONE = 0
    MEMBERS_READ = 1 << 0
    MEMBERS_WRITE = 1 << 1
    MEMBERS_EVENTS = 1 << 2
    GROUPS_READ = 1 << 3
    GROUPS_WRITE = 1 << 4
    GROUPS_EVENTS = 1 << 5
    LATCH_READ = 1 << 6
    LATCH_WRITE = 1 << 7
    LATCH_EVENTS = 1 << 8
    MESSAGES_READ = 1 << 9
    MESSAGES_WRITE = 1 << 10
    MESSAGES_EVENTS = 1 << 11
    MEMBERS_USERPROXY_TOKEN_READ = 1 << 12
    MEMBERS_USERPROXY_TOKEN_WRITE = 1 << 13
    GROUPS_SHARE = 1 << 14
