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
    omit_progress: bool
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
    use_week_and_lesson: str


@dataclass
class Activities:
    total_unread_announcements: int
    total_announcements: int
    total_unread_resources: int
    total_resources: int
    total_incompleted_video_conferences: int
    total_incompleted_metaverse_conferences: int
    total_incompleted_commons_resources: int
    total_incompleted_smart_attendances: int
    total_incompleted_movies: int
    total_unsubmitted_assignments: int
    total_unsubmitted_quizzes: int
    total_unsubmitted_discussion_topics: int


@dataclass
class TodoItem:
    section_id: int
    unit_id: int
    component_id: int
    generated_from_lecture_content: bool
    component_type: str
    title: str
    due_date: str
    commons_type: str


@dataclass
class Todo:
    course_id: int
    activities: Activities
    todo_list: Optional[List[TodoItem]]


@dataclass
class Todos:
    to_dos: List[Todo]
    total_unread_messages: int
    total_count: int


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


def to_dos(termId: int, token: str):
    try:
        return api(f"/learn_activities/to_dos?term_ids[]={termId}", token, response_class=Todos)
    except Exception as e:
        print(f"An error occurred: {e}")
