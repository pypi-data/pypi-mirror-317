from dataclasses import dataclass


@dataclass
class PolicyBase:
    value_added_tax_rate: float
    fuel_cost_pass_through_adjustment_rate: float


@dataclass
class EnergyCharge:
    off_peak_load: float
    mid_load: float
    peak_load: float


@dataclass
class SeasonCharge:
    spring_fall: EnergyCharge
    summer: EnergyCharge
    winter: EnergyCharge


@dataclass
class RateOptions:
    demand_charge: int
    energy_charge: SeasonCharge


@dataclass
class ContractTypeItem:
    contract_type: str
    rate_options: dict[str, RateOptions]


@dataclass
class Policy:
    policy_id: str
    base: PolicyBase
    contract_types: list[ContractTypeItem]


@dataclass
class TimelineItem:
    policy_id: str
    start_date: str  # YYYY-MM-DD
    end_date: str | None  # YYYY-MM-DD or null
    file_path: str
