import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import time
import DomainModels as dm


def get_data_from_excel(filename : str):
    # Import of the data using pandas
    df = pd.read_excel(filename, sheet_name=["Doctors", "Hospitals"])
    start_time = datetime(2019,7,1)
    end_time = datetime(2019,8,30)
    day_limit = 12 # Number of days a doctor can work in a row
    total_work_time = (end_time - start_time).days * (40/7) # How many hours a 100% allocated person would work

    # Create a list of hospitals
    hospitals = df["Hospitals"]["ID"].tolist()

    # Get the list of doctors
    doctors = list()
    for index, row in df["Doctors"].iterrows():
        is_pregnant = row["Pregnant"] == "Yes"
        work_list = list()
        for hospital in hospitals:
            if row[f'Work in {hospital}?'] == "Yes":
                work_list.append(hospital)
        doctors.append(dm.Doctor(row["Name"], is_pregnant, row["Allocation [%]"] / 100, work_list))

    # Create a list of shifts
    shifts = list()
    shift_days = list()
    current = start_time
    weekday_times = [(6, 14), (14, 22), (22, 30)]
    weekend_times = [(6, 18), (18, 30)]
    while current <= end_time:
        shift_days.append(current)
        if current.weekday() < 5:
            shifts += [dm.Shift(current + timedelta(hours=start), current + timedelta(hours=end))
                       for start, end in weekday_times]
        else:
            shifts += [dm.Shift(current + timedelta(hours=start), current + timedelta(hours=end))
                       for start, end in weekend_times]

        current += timedelta(days=1)

    placements = [dm.Placement(doctor, shift, hospital) for doctor in doctors for shift in shifts for hospital in hospitals]

    nightshifts = [dm.Nightshift(doctor, shift_day) for doctor in doctors for shift_day in shift_days]

    return doctors, hospitals, shifts, shift_days, placements, nightshifts