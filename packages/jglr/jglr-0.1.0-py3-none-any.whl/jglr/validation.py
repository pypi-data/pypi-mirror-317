from dataclasses import dataclass
import re


@dataclass
class vc():
    key: str
    items: list
    combstring: list


# (till_hour=None, till_minute=None, till_time=None, quadrant=4, duration_hour=0, duration_minute=10, duration_time=None)
class argValidator():
    def __init__(self, args):
        self.till_hour = args.till_hour
        self.till_minute = args.till_minute
        self.till_time = args.till_time
        self.quadrant = args.quadrant
        self.duration_hour = args.duration_hour
        self.duration_minute = args.duration_minute
        self.duration_time = args.duration_time
        self._Combs = {
            "th": vc("th",
                     [self.till_time, self.duration_hour,
                         self.duration_minute, self.duration_time],
                     ["tt", "dh", "dm", "dt"]),

            "tm": vc("tm",
                     [self.till_time, self.duration_hour,
                         self.duration_minute, self.duration_time],
                     ["tt", "dh", "dm", "dt"]),

            "tt": vc("tt",
                     [self.till_hour, self.till_minute, self.duration_hour,
                         self.duration_minute, self.duration_time],
                     ["th", "tm", "dh", "dm", "dt"]),

            "dh": vc("dh",
                     [self.duration_time, self.till_hour,
                         self.till_minute, self.till_time],
                     ["dt", "th", "tm", "tt"]),

            "dm": vc("dm",
                     [self.duration_time, self.till_hour,
                         self.till_minute, self.till_time],
                     ["dt", "th", "tm", "tt"]),

            "dt": vc("dt",
                     [self.duration_hour, self.duration_minute,
                         self.till_hour, self.till_minute, self.till_time],
                     ["dh", "dm", "th", "tm", "tt"])
        }

    def getString(self):
        if self.till_time and any(self._Combs["tt"].items):
            return f"{self._Combs["tt"].key} cannot be used with {self._Combs["tt"].combstring}"

        if self.till_hour and any(self._Combs["th"].items):
            return f"{self._Combs['th'].key} cannot be used with {self._Combs['th'].combstring}"

        if self.till_minute and any(self._Combs["tm"].items):
            return f"{self._Combs['tm'].key} cannot be used with {self._Combs['tm'].combstring}"

        if self.duration_time and any(self._Combs["dt"].items):
            return f"{self._Combs['dt'].key} cannot be used with {self._Combs['dt'].combstring}"

        if self.duration_hour and any(self._Combs["dh"].items):
            return f"{self._Combs['dh'].key} cannot be used with {self._Combs['dh'].combstring}"

        if self.duration_minute and any(self._Combs["dm"].items):
            return f"{self._Combs['dm'].key} cannot be used with {self._Combs['dm'].combstring}"

        return self.dataValidity()

    def dataValidity(self):
        if self.till_time:
            return "please provide tt in valid HH:MM format" if not re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", self.till_time) else None

        if self.till_hour:
            return "hours must be within 0-23" if self.till_hour > 23 or self.till_hour < 0 else None

        if self.till_minute:
            return "minutes must be within 0-59" if self.till_minute > 59 or self.till_minute < 0 else None

        if self.duration_time:
            return "please provide tt in valid HH:MM format" if not re.match(r"^(0[0-5]):[0-5][0-9]$", self.duration_time) else None

        if self.duration_hour:
            return "hours must be within 0-23" if self.duration_hour > 5 or self.duration_hour < 0 else None

        if self.duration_minute:
            return "minutes must be within 0-59" if self.duration_minute > 59 or self.duration_minute < 0 else None
