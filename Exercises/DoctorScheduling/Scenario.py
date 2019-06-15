import ModelBuilder
from datetime import datetime
import DataProcessing

class Scenario:
    def __init__(self, doctors, hospitals, shifts, shift_days, placements, nightshifts, start_time, end_time):
        self.doctors = doctors
        self.hospitals = hospitals
        self.shifts = shifts
        self.shift_days = shift_days
        self.placements = placements
        self.nightshifts = nightshifts
        self.start_time = start_time
        self.end_time = end_time
        self.total_work_time = (end_time - start_time).days * (40/7)

    def solve(self):
        model_builder = ModelBuilder.ModelBuilder(self.doctors, self.hospitals, self.shifts, self.shift_days,
                                                  self.placements, self.nightshifts, self.total_work_time)
        return model_builder.solve()


doctors, hospitals, shifts, shift_days, placements, nightshifts = DataProcessing.get_data_from_excel("DoctorData.xlsx")
start_time = datetime(2019,7,1)
end_time = datetime(2019,8,30)
scenario = Scenario(doctors, hospitals, shifts, shift_days, placements, nightshifts, start_time, end_time)
scenario.solve()

