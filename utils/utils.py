import csv

with open('input_data/death_rate_age.csv', newline='') as csvfile:
    data_age = dict()
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        data_age[row[0]] = row[1]

with open('input_data/death_rate_gender.csv', newline='') as csvfile:
    data_gender = dict()
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        data_gender[row[0]] = row[1]
