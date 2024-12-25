from typing import Optional

from django.db.models import QuerySet

from aleksis.core.managers import AlekSISBaseManagerWithoutMigrations, DateRangeQuerySetMixin


class TeacherPropertiesMixin:
    """Mixin for common teacher properties.

    Necessary method: `get_teachers`
    """

    def get_teacher_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([teacher.full_name for teacher in self.get_teachers()])

    @property
    def teacher_names(self) -> str:
        return self.get_teacher_names()

    def get_teacher_short_names(self, sep: str = ", ") -> str:
        return sep.join([teacher.short_name for teacher in self.get_teachers()])

    @property
    def teacher_short_names(self) -> str:
        return self.get_teacher_short_names()


class RoomPropertiesMixin:
    """Mixin for common room properties.

    Necessary method: `get_rooms`
    """

    def get_room_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([room.name for room in self.get_rooms()])

    @property
    def room_names(self) -> str:
        return self.get_room_names()

    def get_room_short_names(self, sep: str = ", ") -> str:
        return sep.join([room.short_name for room in self.get_rooms()])

    @property
    def room_short_names(self) -> str:
        return self.get_room_short_names()


class ValidityRangeQuerySet(QuerySet, DateRangeQuerySetMixin):
    """Custom query set for validity ranges."""


class ValidityRangeManager(AlekSISBaseManagerWithoutMigrations):
    """Manager for validity ranges."""
