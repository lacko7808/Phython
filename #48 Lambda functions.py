#48 Lambda functions

#same as the lambda function below:
#def divide(x, y):
#  return x/y

# function name | lambda keyword | parameter list (x,y) | content
divide = lambda x,y: x/y

print (divide(15,3))

#Alternatively you can use this - crap code:
print((lambda x,y: x / y)(15,3))

#Example for avarage calculating
#Original way
#def average(sequence):
#    return sum(sequence) / len(sequence)
#Lambda way - hier is not really good idea.
average = lambda sequence: sum(sequence) / len(sequence)

students = [
    {"name": "Rolf", "grades": (67, 90, 95, 100)},
    {"name": "Bob", "grades": (56, 78, 80, 90)},
    {"name": "Jen", "grades": (98, 90, 95, 99)},
    {"name": "Anne", "grades": (100, 100, 95, 100)},
]

for student in students:
    print(average(student["grades"]))