import json
import os
from dacite import from_dict, Config

from .data_models import Policy, TimelineItem


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_timeline() -> list[TimelineItem]:
    """
    timeline.json 파일을 읽고, 각 항목을 TimelineItem(dataclass)으로 변환하여 반환.
    """
    timeline_path = os.path.join(DATA_DIR, "timeline.json")
    with open(timeline_path, "r", encoding="utf-8") as f:
        data = json.load(f)  # data: list[dict]

    items = []
    for policy in data["policies"]:
        # policy: { "start_date": "...", "end_date": "...", "policy_id": "...", "file_path": "..." }
        item = from_dict(
            data_class=TimelineItem, data=policy, config=Config(strict=True)  # 정의되지 않은 필드가 있으면 오류
        )
        items.append(item)

    return items


def load_policy(policy_id: str) -> Policy:
    """
    주어진 policy_id에 해당하는 JSON(예: 20241024.json)을 읽어
    Policy(dataclass) 인스턴스로 변환해 반환.
    """
    policy_file = os.path.join(DATA_DIR, f"{policy_id}.json")
    with open(policy_file, "r", encoding="utf-8") as f:
        data = json.load(f)  # dict 구조

    policy_obj = from_dict(data_class=Policy, data=data, config=Config(strict=True))
    return policy_obj


def find_latest_policy_id() -> str | None:
    """
    최신 정책을 찾아 policy_id 반환.
    """
    items = load_timeline()
    if not items:
        return None

    # start_date 기준으로 최신 정책 하나
    items.sort(key=lambda x: x.start_date, reverse=True)
    return items[0].policy_id
