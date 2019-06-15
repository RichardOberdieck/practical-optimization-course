from dataclasses import dataclass
from datetime import datetime
import Constants


class Doctor:
    """
    Describes an instance of a doctor
    """
    def __init__(self, name, is_pregnant, allocation, work_locations):
        self.name = name
        self.is_pregnant = is_pregnant
        self.allocation = allocation
        self.work_locations = work_locations


class Shift:
    """
    A shift with a given start and end time
    """
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.duration_in_hours = (end_time - start_time).total_seconds() / Constants.seconds_in_one_hour
        self.is_nightshift = start_time.time() >= Constants.earliest_start_time_for_nightshift or start_time.time() <= Constants.latest_start_time_for_nightshift
        self.can_work_pregnant = self.duration_in_hours < Constants.work_time_limit_for_pregnant_in_hours and not self.is_nightshift


@dataclass(frozen=True)
class Placement:
    """
    Assigns a doctor to a given shift at a given hospital
    """
    doctor: Doctor
    shift: Shift
    hospital: str


@dataclass(frozen=True)
class Nightshift:
    """
    A night shift for a specific doctor at a given day
    """
    doctor: Doctor
    day: datetime
