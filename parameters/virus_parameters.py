from utils.utils import data_age, data_gender

incubation_time = [5, 14]
disease_time = [10, 14]
min_recovery_time = incubation_time[0] + disease_time[0]
max_recovery_time = incubation_time[1] + disease_time[1]


lifetime = 50


p_get_infected = .99
p_get_recovered = .005
p_dies = 0.1

