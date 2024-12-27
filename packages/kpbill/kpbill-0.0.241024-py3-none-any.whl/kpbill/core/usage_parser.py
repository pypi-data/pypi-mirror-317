from datetime import datetime


def parse_list(usage_list: list[dict[str, datetime | float]]) -> dict[datetime, float]:
    usage_dict = {}
    for item in usage_list:
        timestamp: datetime = item["timestamp"]
        usage: float = item["usage"]
        usage_dict[timestamp] = usage
    return usage_dict


def parse_dataframe(df, timestamp_col="timestamp", usage_col="usage_kwh") -> dict[datetime, float]:
    """
    pandas가 설치되어 있을 때만 작동
    """
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError("pandas 라이브러리가 설치되어 있지 않습니다") from e

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input data는 pandas DataFrame이어야 합니다")

    usage_dict = {}
    for _, row in df.iterrows():
        ts = pd.to_datetime(row[timestamp_col]).to_pydatetime()
        usage_kwh = float(row[usage_col])
        usage_dict[ts] = usage_kwh
    return usage_dict
