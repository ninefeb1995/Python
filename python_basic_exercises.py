# 1. Given a list of integer, find the sum of all values in that list 

list_integer = [1, 2, 3, 4, 5]
sum_of_list = reduce(lambda x, y: x + y, list_integer)
#or
result = 0
for each in list_integer:
	result += each
return result

# 2. Write a function which takes a list of integer as an argument and returns a list with ordered values.

def ordered_list(list_integer_input):
	list_result = sorted(list_integer_input)
	return list_result

#or we can define a function ourselves to sort the list

# 3. Write a function which takes a list of values in different data type (String, Integer and Float) and returns a list of Integer and Float values.

def get_number_in_list(list_of_item_input):
	list_result = []
	for each in list_of_item_input
		if type(each) in (float, int):
			list_result.append(each)
	return list_result


# 4. Write a function to convert the data of the following data structures
	# List -> Tuple
	# Tuple -> List

def  convert_list_and_tuple(list_or_tuple_input):
	if type(list_or_tuple_input) is tuple:
		return list(list_or_tuple_input)
	if type(list_or_tuple_input) is list:
		return tuple(list_or_tuple_input)

# 5. Write a function which takes a Tuple of n integer as an argument and returns a tuple of these integer with no duplicates.

def tuple_with_no_duplicated_item(tuple_input):
	result_temp = [ a for a in tuple_input if a not in result_temp]
	for each in tuple_input:
		if each not in result_temp:
			result_temp.append(each)
	return tuple(result_temp)

#or 

def tuple_with_no_duplicated_item(tuple_input):
	return tuple(set(tuple_input))

# 6. Given an dictionary, find the list of key and list of values of that dictionary.

dictionary_a = {
    'a': 1,
    'b': 2,
    'c': 3
}

dictionary_a.keys()
dictionary_a.values()

# 7. Given a list of n integer, find all prime numbers.

list_integer = [1, 2, 3, 4, 5]

prime_number = []

for item in list_integer:
	if item not in prime_number:
		if item > 1:
			for i in range(2, item):
				if item % i == 0:
					break
			# if (i + 1) == item:
			# 	prime_number.append(item)	
			else: # this of for loop
				prime_number.append(item)	

# 8. Given two lists of integers. Find the list of integer which contains all values of two given lists.

list_a = [2, 1, -1, 10, 15, 10.5]
list_b = [12, -12, -1, 10, 10.5]
list_result = []
for item in list_a:
	if item in list_b:
		list_result.append(item)

#or we use 'set'

set_a = set(list_a)
set_b = set(list_b)
result = list(set_a.intersection(set_b))

# 9. Given two tuple of integers. Find the tuple of integers which contains all values of two given tuples

tuple_a = (2, 1, -1, 10, 15, 10.5)
tuple_b = (12, -12, -1, 10, 10.5)
list_temp = list(tuple_a)

for item in tuple_b:
	if item not in list_temp:
		list_temp.append(item)

tuple_result = tuple(list_temp)

#or we use 'set'

set_a = set(tuple_a)
set_b = set(tuple_b)
result = list(set_a.union(set_b))

# 10. Given a list of n integer. Find the negative sum and positive sum.

list_of_integer = [1, 2, -10, -1, 5, 8, -10.4, 50]

sum_of_negative_int = sum(i for i in list_of_integer if i < 0)
sum_of_positive_int = sum(i for i in list_of_integer if i > 0)

# 11. Given GPA, find the student classification based on the following table.

dict_gpa = {
    range(85, 101): "Excellent",
    range(75, 85): "Very Good",
	range(65, 75): "Good",
	range(60, 65): "Fairly Good",
	range(55, 60): "Fair",
	range(50, 55): "Average",
	range(30, 50): "Weak",
	range(10, 30): "Rather Weak",
	range(0, 10): "Too Weak",
}

i = int(input("Input gpa of the student:"))

for item in dict_gpa:
    if i in item:
        print(dict_gpa[item])

# 12. Write a function which accepts datetime data in string (yyyy/mm/dd hh:mm:ss) and return a datetime data in string (yyyy/mm/dd) of 7 days before that date
from datetime import datetime, timedelta

def date_time(datetime_in_string):
    try:
        datetime_in_datetime = datetime.strptime(datetime_in_string, '%Y/%m/%d %I:%M:%S')
    except ValueError:
        print("Input must be formatted: yyyy/mm/dd hh:mm:ss.")
    else:
        return datetime.strftime(datetime_in_datetime - timedelta(7), '%d/%m/%Y')

# 13. Find 3 maximum values of a list of n integers (Note: only use “max” function)

list_a = []
max_result = []

for i in range(0, 3):
	max_result.append(list_a.pop(list_a.index(max(list_a))))

# 14. Given a float number. Find the float number which has been rounded to 2 decimal places

float_given = 2. 020304

float_result = float("{0:.2f}".format(float_given))

# 15. Given a list of integer, use list comprehension to get the list of positive integer.

given_list = [1, 2, 3, 4, 5, -6, -7, -8, -9]

positive_list = [item for item in given_list if item > 0]

# 16. Define a variable which can holds the following data
	  # - A list of students
	  # - Each student has student ID, name, gender, age, list of contacts
	  # - Each contact contains contact name, phone, address

class Contact:
	
	def __init__(self, name, phone, address):
		self.name = name
		self.phone = phone
		self.address  =address


class Student:

	def __init__(self, id, name, gender, age, contact):
		self.id = id 
		self.name = name
		self.gender = gender
		self.age = age
		self.contact = contact
