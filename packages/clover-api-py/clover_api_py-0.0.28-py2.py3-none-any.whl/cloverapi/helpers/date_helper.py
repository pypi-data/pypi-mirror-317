from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from typing import List, Dict, Union
from zoneinfo import ZoneInfo


class DateHelper:
    def __init__(self, timezone: str = "UTC"):
        """
        Initialize DateHelper with a default timezone.

        :param timezone: Timezone string (e.g., "America/New_York", "UTC").
        """
        self.timezone = timezone
        self.zoneinfo = ZoneInfo(timezone)

    def ms_to_date(self, ms: int, override_timezone: str = None) -> datetime:
        """
        Convert milliseconds since epoch to a specified timezone datetime.

        :param ms: Milliseconds since epoch (Unix time).
        :param override_timezone: Optional timezone string to override the default.
        :return: Datetime object localized to the specified timezone.
        """
        # Convert milliseconds to UTC datetime
        utc_datetime = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
        # Use the default or override timezone
        target_timezone = ZoneInfo(override_timezone) if override_timezone else self.zoneinfo
        return utc_datetime.astimezone(target_timezone)

    def filters_period(self, period: Union[str, int]) -> (int, int):
        """
        Get the start and end timestamps for a specified period.

        :param period: Reporting period (e.g., 'daily', 'weekly', 'monthly', etc.) or an integer for last n days.
        :return: Tuple of start and end timestamps in milliseconds.
        """
        now = datetime.now(self.zoneinfo)  # Use the initialized timezone

        time_ranges = {
            "day": self.today,
            "today": self.today,
            "yesterday": self.yesterday,
            "week": self.current_week,
            "month": self.current_month,
            "quarter": self.current_quarter,
            "year": self.current_year,
        }

        period = period.lower()
        if isinstance(period, str):
            method = time_ranges.get(period)
            if not method:
                raise ValueError(f"Unsupported period: {period}. Use one of {list(time_ranges.keys())}.")
            return method()
        elif isinstance(period, int):
            return self.last_n_days(period)
        else:
            raise ValueError("Period must be a recognized string or an integer for last n days.")

    def today(self) -> (int, int):
        now = datetime.now(self.zoneinfo)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1) - timedelta(microseconds=1)
        return self._to_milliseconds(start), self._to_milliseconds(end)

    def yesterday(self) -> (int, int):
        now = datetime.now(self.zoneinfo)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        end = start + timedelta(days=1) - timedelta(microseconds=1)
        return self._to_milliseconds(start), self._to_milliseconds(end)

    def current_week(self) -> (int, int):
        now = datetime.now(self.zoneinfo)
        start = now - timedelta(days=now.weekday())  # Start of the week (Monday)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7) - timedelta(microseconds=1)
        return self._to_milliseconds(start), self._to_milliseconds(end)

    def current_month(self) -> (int, int):
        now = datetime.now(self.zoneinfo)
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = (start + relativedelta(months=1)) - timedelta(microseconds=1)
        return self._to_milliseconds(start), self._to_milliseconds(end)

    def current_quarter(self) -> (int, int):
        now = datetime.now(self.zoneinfo)
        quarter_start_month = (now.month - 1) // 3 * 3 + 1
        start = now.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = (start + relativedelta(months=3)) - timedelta(microseconds=1)
        return self._to_milliseconds(start), self._to_milliseconds(end)

    def current_year(self) -> (int, int):
        now = datetime.now(self.zoneinfo)
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        return self._to_milliseconds(start), self._to_milliseconds(end)

    def last_n_days(self, n: int) -> (int, int):
        now = datetime.now(self.zoneinfo)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=n)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return self._to_milliseconds(start), self._to_milliseconds(end)

    @staticmethod
    def _to_milliseconds(dt: datetime) -> int:
        return int(dt.timestamp() * 1000)

    def group_by_period(
        self, data: List[Dict], group_by: str, date_key: str = "createdTime", value_key: str = "total", override_timezone: str = None
    ) -> Dict:
        """
        Group data by a specified period (day, week, quarter, or year).

        :param data: List of dictionaries to group (e.g., orders or inventory items).
        :param group_by: Grouping period ('day', 'week', 'quarter', or 'year').
        :param date_key: Key in the dictionary containing the date in milliseconds.
        :param value_key: Key in the dictionary containing the value to aggregate (e.g., 'total').
        :param override_timezone: Optional timezone to override the default.
        :return: Dictionary grouped by the specified period with aggregated totals.
        """
        grouped_data = {}
        target_timezone = ZoneInfo(override_timezone) if override_timezone else self.zoneinfo

        for item in data:
            try:
                created_time = self.ms_to_date(item[date_key], override_timezone=override_timezone)
                localized_time = created_time.astimezone(target_timezone)

                if group_by == "day":
                    key = localized_time.strftime("%Y-%m-%d")
                elif group_by == "week":
                    key = localized_time.strftime("%Y-W%U")
                elif group_by == "quarter":
                    quarter = (localized_time.month - 1) // 3 + 1
                    key = f"{localized_time.year}-Q{quarter}"
                elif group_by == "year":
                    key = localized_time.year
                else:
                    raise ValueError(f"Unsupported group_by: {group_by}. Use 'day', 'week', 'quarter', or 'year'.")

                if key not in grouped_data:
                    grouped_data[key] = {"total_count": 0, "total_amount": 0}

                grouped_data[key]["total_count"] += 1
                grouped_data[key]["total_amount"] += item.get(value_key, 0)

            except Exception as e:
                print(f"Error processing item {item}: {e}")

        return grouped_data