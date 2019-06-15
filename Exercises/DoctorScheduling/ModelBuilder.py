import ModelContainer
import Constants

class ModelBuilder:
    def __init__(self, doctors, hospitals, shifts, shift_days, placements, nightshifts, total_work_time):
        self.doctors = doctors
        self.hospitals = hospitals
        self.shifts = shifts
        self.shift_days = shift_days
        self.placements = placements
        self.nightshifts = nightshifts
        self.total_work_time = total_work_time

        # Create model object
        self.model = ModelContainer.ModelContainer()

    def solve(self):
        self.create_model()
        self.model.solve()
        return self.model.get_placement_list()

    def create_model(self):
        self.create_variables()
        self.add_constraints()
        self.add_objective_function()

    def create_variables(self):
        self.model.define_placement_variables(self.placements)
        self.model.define_nightshift_change(self.nightshifts)
        self.model.define_auxiliary_variables_for_doctors(self.doctors)

    def add_constraints(self):
        for shift in self.shifts:
            for hospital in self.hospitals:
                self.model.force_shift_fulfillment(shift, hospital)

        for doctor in self.doctors:
            for day in self.shift_days:
                self.model.one_shift_limit(doctor, day)
                self.model.max_time_working(doctor, day, Constants.limit_for_working_days_in_a_row)

            self.model.enforce_hospital_limit(doctor)
            self.model.force_auxiliary_variables_1(doctor, self.total_work_time)
            self.model.force_auxiliary_variables_2(doctor, self.total_work_time)

        for nightshift in self.nightshifts:
            self.model.force_nightshift_work(nightshift, Constants.number_of_days_working_nightshift)
            self.model.force_rest(nightshift, Constants.number_of_days_working_nightshift, Constants.number_of_days_rest_after_nightshift)

    def add_objective_function(self):
        self.model.set_objective_function()






