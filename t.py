import json

test_json_string = '{"names": ["jd", "jc", "je"]}'
test_object = {"titles": ["blacksmith", "woodsmith"]}

print("test_json_string:")
print(test_json_string)

print("test_object:")
print(test_object)

print("type(test_json_string):")
print(type(test_json_string))  # str

print("type(test_object):")
print(type(test_object))  # dict

# Corrected way to print dictionary items
print("test_object items:")
for key, value in test_object.items():
    print(key, ":", value)

# Alternatively, if you want to use list comprehension:
print(list(test_object.items()))

json_string_converted_into_object = json.loads(test_json_string)
print("json_string_converted_into_object")
print(json_string_converted_into_object)
print(type(json_string_converted_into_object))