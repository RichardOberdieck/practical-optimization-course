import numpy as np
import ssl
import xpress as xp
from datetime import timedelta

class ModelContainer:
    def __init__(self):
        self.model = xp.problem("Doctor scheduling")

    def define_placement_variables(self, placements):
        self.x = {p: xp.var(vartype=xp.binary, name=f'x_{p.doctor.name}, {p.shift}, {p.hospital}') for p in placements}
        self.model.addVariable(self.x)

    def define_nightshift_change(self, nightshifts):
        self.y = {n: xp.var(vartype=xp.integer, lb=-1, ub=1, name=f'y_{n.doctor.name},{n.day}') for n in nightshifts}
        self.model.addVariable(self.y)

    def define_auxiliary_variables_for_doctors(self, doctors):
        self.t = {d: xp.var(vartype=xp.continuous, lb=0, name=f'Auxiliary for doctor {d.name}') for d in doctors}
        self.model.addVariable(self.t)

    def force_shift_fulfillment(self, shift, hospital):
        shift_fulfillment = xp.constraint(xp.Sum(self.x[p] for p in self.x if
                                                p.shift == shift and p.hospital == hospital) == 1,
                                        name = f'Force shift fulfillment for shift {shift} and hospital {hospital}')
        self.model.addConstraint(shift_fulfillment)

    def one_shift_limit(self, doctor, shift_day):
        shift_limit = xp.constraint(xp.Sum(self.x[p] for p in self.x
                                        if p.doctor == doctor and
                                        p.shift.start_time.date() == shift_day.date()) <= 1,
                                name = f'One shift limit for {doctor.name} and day {shift_day}')
        self.model.addConstraint(shift_limit)

    def max_time_working(self, doctor, shift_day, day_limit):
        time_working = xp.constraint(xp.Sum(self.x[p] for p in self.x for j in range(day_limit + 1)
                                         if p.doctor == doctor and p.shift.start_time.date() ==
                                         (shift_day + timedelta(days=j)).date()) <= day_limit,
                                 name = f'Max working time for day {shift_day} and doctor {doctor.name}')
        self.model.addConstraint(time_working)

    def enforce_hospital_limit(self, doctor):
        hospital_limit = xp.constraint(xp.Sum(self.x[p] for p in self.x
                                       if p.doctor == doctor and p.hospital not in doctor.work_locations) == 0,
                               name = f'Enforce hospital limits for doctor {doctor.name}')
        self.model.addConstraint(hospital_limit)

    def force_nightshift_work(self, nightshift, n_days_working):
        nightshift_work = xp.constraint(xp.Sum(self.x[p] for p in self.x for k in range(n_days_working)
                                              if p.doctor == nightshift.doctor and p.shift.start_time.date() == (nightshift.day.date() + timedelta(days = k))) >= 3*self.y[nightshift],
                                      name = f'Force nightshift for doctor {nightshift.doctor} at day {nightshift.day}')
        self.model.addConstraint(nightshift_work)

    def force_rest(self, nightshift, n_days_working, n_days_rest):
        force_rest = xp.constraint(xp.Sum(self.x[p] for p in self.x for k in range(n_days_working,n_days_working + n_days_rest)
                                              if p.doctor == nightshift.doctor and p.shift.start_time.date() == (nightshift.day.date() + timedelta(days = k))) <= 3*(1-self.y[nightshift]),
                                      name = f'Force rest for doctor {nightshift.doctor} at day {nightshift.day}')
        self.model.addConstraint(force_rest)

    def force_auxiliary_variables_1(self, doctor, total_work_time):
        aux_definition1 = xp.constraint(xp.Sum(p.shift.duration_in_hours * self.x[p] for p in self.x if p.doctor == doctor) -
                                         doctor.allocation * total_work_time <= self.t[doctor], name=f'Auxiliary 1 for {doctor}')
        self.model.addConstraint(aux_definition1)

    def force_auxiliary_variables_2(self, doctor, total_work_time):
        aux_definition2 = xp.constraint(doctor.allocation * total_work_time -
                                         xp.Sum(p.shift.duration_in_hours * self.x[p] for p in self.x if p.doctor == doctor)
                                         <= self.t[doctor], name=f'Auxiliary 2 for {doctor}')
        self.model.addConstraint(aux_definition2)

    def set_objective_function(self):
        self.model.setObjective(xp.Sum(self.t[d] for d in self.t.keys()))

    def solve(self):
        self.model.solve()

    def get_placement_list(self):
        return [placement for placement in self.x if self.model.getSolution(self.x[placement]) > 0.5]