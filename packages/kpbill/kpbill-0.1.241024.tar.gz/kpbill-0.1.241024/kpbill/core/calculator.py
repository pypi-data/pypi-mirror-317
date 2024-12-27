from datetime import datetime, date, timedelta

from kpbill.core.usage_parser import parse_list

from .data_models import Policy, EnergyCharge, SeasonCharge
from .policy_parser import load_policy, find_latest_policy_id
import logging

logger = logging.getLogger(__name__)


def get_season(timestamp: datetime) -> str:
    """
    - 여름철(summer): 6~8월
    - 겨울철(winter): 11~2월
    - 봄, 가을철(spring_fall): 3~5월, 9~10월
    """
    month = timestamp.month
    if month in (6, 7, 8):
        return "summer"
    elif month in (11, 12, 1, 2):
        return "winter"
    else:
        return "spring_fall"


def get_time_of_use(timestamp: datetime) -> tuple[str, str]:
    """timestamp가 어느 시간대(off-peak, mid, peak) 인지 판별한다."""
    season = get_season(timestamp)

    if season == "spring_fall":
        if timestamp.hour <= 8 or 22 < timestamp.hour:
            return season, "off_peak_load"
        elif 8 < timestamp.hour <= 11 or 12 < timestamp.hour <= 13 or 18 < timestamp.hour <= 22:
            return season, "mid_load"
        elif 11 < timestamp.hour <= 12 or 13 < timestamp.hour <= 18:
            return season, "peak_load"

    if season == "summer":
        if timestamp.hour <= 8 or 22 < timestamp.hour:
            return season, "off_peak_load"
        elif 8 < timestamp.hour <= 11 or 12 < timestamp.hour <= 13 or 18 < timestamp.hour <= 22:
            return season, "mid_load"
        elif 11 < timestamp.hour <= 12 or 13 < timestamp.hour <= 18:
            return season, "peak_load"

    if season == "winter":
        if timestamp.hour <= 8 or 22 < timestamp.hour:
            return season, "off_peak_load"
        elif 8 < timestamp.hour <= 9 or 12 < timestamp.hour <= 16 or 19 < timestamp.hour <= 22:
            return season, "mid_load"
        elif 9 < timestamp.hour <= 12 or 16 < timestamp.hour <= 19:
            return season, "peak_load"

    raise ValueError("경/중/최대부하 구간을 판별할 수 없는 시간대입니다")


class BillCalculator:
    def __init__(self, contract_type: str, rate_option: str | int):
        """
        Args:
            contract_type (str): 계약종별. 예) "일반용전력(을)고압A"
            rate_option (str|int): 선택요금. 예) "1", "2" ...
        """

        self.usage_dict: dict[datetime, float] = {}

        policy_id = find_latest_policy_id()
        if not policy_id:
            raise ValueError("최신 정책을 찾을 수 없습니다")
        self.policy: Policy = load_policy(policy_id)

        self.contract_type: str = contract_type

        if isinstance(rate_option, int):
            rate_option = str(rate_option)
        self.rate_option: str = rate_option

        # policy에서 해당 contract_type, rate_option 찾기
        ctype_item = next((ct for ct in self.policy.contract_types if ct.contract_type == contract_type), None)
        if not ctype_item:
            raise ValueError(f"계약종별 '{contract_type}'을 정책 '{policy_id}'에서 찾을 수 없습니다")

        if rate_option not in ctype_item.rate_options:
            raise ValueError(f"선택요금'{rate_option}'을 계약종별 '{contract_type}'에서 찾을 수 없습니다")

        self.rate_option_obj = ctype_item.rate_options[rate_option]

    # ------------------------------------------------
    # 사용량 데이터 등록 파트
    # ------------------------------------------------

    def add_usage_record(self, timestamp: datetime, usage: float):
        """단일 데이터를 삽입합니다."""
        self._store_usage({timestamp: usage})

    def add_usage_dict(self, usage_dict):
        self._store_usage(usage_dict)

    def add_usage_list(self, usage_list: list[dict[str, datetime | float]]):
        parsed_dict = parse_list(usage_list)
        self._store_usage(parsed_dict)

    def add_usage_df(self, df):
        ...
        # usage_list = parse_dataframe(df)
        # self._store_usage(usage_list)

    def add_usage_csv(self, csv_path: str): ...

    def _store_usage(self, usage_dict: dict[datetime, float]):
        overwrite_count = 0  # 덮어쓴 데이터 개수
        for key, value in usage_dict.items():
            if key in self.usage_dict:
                overwrite_count += 1
            self.usage_dict[key] = value

        logger.info(f"{overwrite_count}개의 데이터를 덮어썼습니다")

    # ------------------------------------------------
    # 전력량 요금 계산
    # ------------------------------------------------
    def calculate_energy_charge(self, start_dt: datetime | date, end_dt: datetime | date) -> float:
        """
        전력량 요금을 계산합니다.
        지정된 기간(start_dt, end_dt] 내의 15분 데이터만 골라서
        - (계절, 시간대)에 따라 부하 구간을 판별
        - 각 구간에 맞는 단가 곱
        - 전력량 요금 합계를 반환
        """

        if isinstance(start_dt, date):
            start_dt = datetime.combine(start_dt, datetime.min.time())

        if isinstance(end_dt, date):
            end_dt = datetime.combine(end_dt, datetime.min.time()) + timedelta(days=1)

        # 기간 내 15분 데이터 필터링
        filtered_dict = {k: v for k, v in self.usage_dict.items() if start_dt <= k < end_dt}

        # 2) (계절, 시간대)별 usage를 합산
        #    구조 예: seasonal_usage[season][time_of_use] = 총 kWh
        seasonal_usage = {
            "spring_fall": {"off_peak_load": 0.0, "mid_load": 0.0, "peak_load": 0.0},
            "summer": {"off_peak_load": 0.0, "mid_load": 0.0, "peak_load": 0.0},
            "winter": {"off_peak_load": 0.0, "mid_load": 0.0, "peak_load": 0.0},
        }

        for key, value in filtered_dict.items():
            season, tou = get_time_of_use(key)
            seasonal_usage[season][tou] += value

        # 3) 요금 단가 읽기
        season_charge: SeasonCharge = self.rate_option_obj.energy_charge

        # 4) 전력량요금 계산
        energy_charge_total = 0.0
        for season in seasonal_usage.keys():
            energy_charge: EnergyCharge = getattr(season_charge, season)

            for tou in seasonal_usage[season].keys():
                usage_kwh = seasonal_usage[season][tou]
                # 단가
                rate = getattr(energy_charge, tou)
                energy_charge_total += usage_kwh * rate

        return energy_charge_total

    # ------------------------------------------------
    # 기본 요금
    # ------------------------------------------------

    def get_demand_charge(self) -> int:
        return self.rate_option_obj.demand_charge
