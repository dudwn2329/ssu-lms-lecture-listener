import traceback
from datetime import datetime, timezone
from typing import List, Optional, Any

from service.auth import Authorization
from api.accounts import terms, Term
from api.users import learnActivities, Course
from api.courses import *


def get_uncompleted_course_components(me: Authorization, ignore_course_ids: Optional[List[int]] = None) -> List[Any]:
    try:
        response = terms(me.user_id, me.token)
    except Exception as e:
        print(e)

    if not response.ok:
        print(f"Failed to get terms: Status {response.status}")
        return []

    terms_data = response.result.enrollment_terms
    default_term = next((term for term in terms_data if term['default']), terms_data[-1])
    print(f"현재 학기: {default_term}")

    # response = learnActivities(me.token, default_term['id'])
    # courses = response.result
    # print(courses)
    # now = datetime.now(timezone.utc)
    #
    # online_courses = [course for course in courses]
    # print(f"online courses: {online_courses}")
    # components = []
    #
    # for course in online_courses:
    #     response = modules(course.id, me.token)
    #     moduleList = response.result
    #     for module in moduleList:
    #
    #         module_items = module.module_items
    #         filtered_module_items = [
    #             module_item for module_item in module_items
    #             if module_item.get('content_data', {}).get('item_content_data', {}).get('content_type') in ['movie', 'mp4', 'everlec']
    #         ]
    #         components.extend({**comp['content_data'], 'courseName': course.name} for comp in filtered_module_items)
    response = to_dos(default_term['id'], me.token)
    print(response)
    todos = response.result.to_dos
    todo_list = []

    for todo in todos:
        for _ in todo['todo_list']:
            todo_list.append({**_, 'course_id': todo['course_id']})

    active_components = []

    now = datetime.now(timezone.utc)
    try:
        for comp in todo_list:
            if comp:
                attendance = attendanceItems(comp['course_id'], comp['component_id'], me.token).result
                print(attendance)
                try:
                    if attendance.unlock_at is not None and attendance.due_at is not None:
                        if datetime.fromisoformat(attendance.unlock_at.replace("Z", "")).replace(
                                tzinfo=timezone.utc) < now < datetime.fromisoformat(attendance.due_at.replace("Z", "")).replace(
                                tzinfo=timezone.utc):
                            active_components.append(attendance)
                except AttributeError as e:
                    print(e)
                    continue

    except Exception as e:
        traceback.print_exc()
        print(e)

    finally:
        return [comp for comp in active_components if comp.attendance_data['attendance_status'] == 'none']
