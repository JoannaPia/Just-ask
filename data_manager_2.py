import csv
def open_file(file_name):
    with open(file_name, "r") as f:
        reader = csv.DictReader(f)
        list_of_dict = list(reader)
        return list_of_dict

list_of_dict = open_file("question.csv")

#print(list_of_dict[0])
for key,value in list_of_dict[0].items():
    print(value)