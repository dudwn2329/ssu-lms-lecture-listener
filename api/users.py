from dataclasses import dataclass
from typing import Union
from api.base import api, ApiResponse


@dataclass
class Course:
    course_format: Union['online', 'offline', 'none']
    id: int
    term_id: int
    name: str
    professors: str
    total_students: int
    is_observer: bool
    use_purecanvas: bool
    enrolled_status: str
    ended: bool


def learnActivities(token: str, term_id: int) -> ApiResponse:
    try:
        return api(f"/learn_activities/courses?term_ids[]={term_id}", token, response_class=Course)
    except Exception as e:
        print(f"An error occurred: {e}")
