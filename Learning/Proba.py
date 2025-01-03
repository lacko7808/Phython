import array as arr

a = arr.array('i', [1, 2, 3, 5])

print("Tömb: ", end="")

for i in a:
    print(i, ", ", end="")

employee = {
    "name": 'Laci',
    "role": "Fejlesztő",
    "FTE": 1,
}

print()

for key in employee:
    print(key, employee[key])

for key, value in employee.items():
    print(f"{key}: {value}")
