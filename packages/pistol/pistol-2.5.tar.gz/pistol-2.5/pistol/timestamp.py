from typing import Literal

class Timestamp:
    def __init__(self, date: dict, time: dict, time_format: Literal["eu", "us"] = "eu"):
        self.date: dict = date
        self.time: dict = time
        self.repr_date_eu: str = f"{date['name']} {date['day']}.{date['month']}.{date['year']}"
        self.repr_date_us: str = f"{date['name']} {date['month']}/{date['day']}/{date['year']}"
        self.repr_date: str = self.repr_date_us if time_format == "us" else self.repr_date_eu
        self.repr_time: str = f"{time['hours']}:{time['minutes']}:{time['seconds']}"
        self.repr_full: str = f"{self.repr_date} {self.repr_time}"
        self.time_format: str = time_format
    def __repr__(self):
        return self.repr_full
    def __str__(self):
        return repr(self)
    @classmethod
    def from_now(cls, time_format: Literal["eu", "us"] = "eu"):
        from datetime import datetime

        now = datetime.now()
        return cls(
            date={
                "name": now.strftime("%A").lower(),
                "day": now.strftime("%d"),
                "month": now.strftime("%m"),
                "year": now.strftime("%Y")
            },
            time={
                "hours": now.strftime("%H"),
                "minutes": now.strftime("%M"),
                "seconds": now.strftime("%S")
            },
            time_format=time_format
        )
    @classmethod
    def from_dict(cls, obj):
        return cls(
            date={
                "name": obj["name"],
                "day": obj["day"],
                "month": obj["month"],
                "year": obj["year"]
            },
            time={
                "hours": obj["hours"],
                "minutes": obj["minutes"],
                "seconds": obj["seconds"]
            },
            time_format=obj["time_format"]
        )
    def to_dict(self):
        return {
            "name": self.date["name"],
            "day": self.date["day"],
            "month": self.date["month"],
            "year": self.date["year"],
            "hours": self.time["hours"],
            "minutes": self.time["minutes"],
            "seconds": self.time["seconds"],
            "time_format": self.time_format
        }