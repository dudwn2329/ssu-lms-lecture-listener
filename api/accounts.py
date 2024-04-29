from dataclasses import dataclass
from typing import List, Union
from base import api, ApiResponse


@dataclass
class Term:
    default: bool
    end_at: Union[str, None]
    id: int
    name: str
    start_at: str
    workflow_state: str


@dataclass
class TermsResponse:
    enrollment_terms: List[Term]


def terms(userId: str, token: str) -> ApiResponse:
    try:
        return api(f"/users/{userId}/terms", token, response_class=TermsResponse)
    except Exception as e:
        print(f"An error occurred: {e}")
