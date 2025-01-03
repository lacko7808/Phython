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
print(employee)
