from dataclasses import dataclass
from typing import List, Optional
from api.base import api


@dataclass
class ItemContentData:
    _id: str
    content_id: str
    content_type: str
    view_url: str
    thumbnail_url: str
    progress_support: int
    duration: int
    updated_at: str
    created_at: str


@dataclass
class ContentData:
    item_id: int
    course_id: int
    original_item_id: int
    use_attendance: bool
    item_content_type: str
    item_content_id: str
    week_position: int
    lesson_position: int
    title: str
    description: int
    created_at: str
    updated_at: str
    published: bool
    lecture_period_status: str
    unlock_at: str
    late_at: str
    due_at: str
    lock_at: str
    item_content_data: Optional[ItemContentData]
    opened: bool


@dataclass
class ModuleItem:
    module_item_id: int
    title: str
    content_type: str
    content_id: int
    content_data: ContentData
    position: int
    published: Optional[bool]
    indent: int
    url: str
    is_child_content: bool


@dataclass
class Module:
    module_id: int
    title: str
    position: int
    published: Optional[bool]
    unlock_at: Optional[str]
    is_child_content: bool
    module_items: List[ModuleItem]


@dataclass
class ContentData:
    _id: str
    content_id: str
    content_type: str
    view_url: str
    thumbnail_url: str
    progress_support: bool
    duration: float
    updated_at: str
    created_at: str


@dataclass
class AttendanceData:
    completed: bool
    attendance_status: str
    progress: float
    last_at: float


@dataclass
class AttendanceItem:
    item_id: int
    course_id: int
    original_item_id: int
    use_attendance: bool
    item_content_type: str
    item_content_id: str
    week_position: int
    lesson_position: int
    title: str
    description: str
    created_at: str
    updated_at: str
    published: bool
    lecture_period_status: str
    unlock_at: str
    late_at: str
    due_at: str
    lock_at: Optional[str]
    item_content_data: ContentData
    opened: bool
    viewer_url: str
    attendance_data: AttendanceData


def modules(courseId: int, token: str):
    try:
        return api(f"/courses/{courseId}/modules", response_class=Module, token=token)
    except Exception as e:
        print(f"an error occurred: {e}")


def attendanceItems(courseId: str, itemId: str, token: str):
    try:
        return api(f"/courses/{courseId}/attendance_items/{itemId}", token, response_class=AttendanceItem)
    except Exception as e:
        print(f"An error occurred: {e}")
