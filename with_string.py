#1. Write a Python program to calculate the length of a string.
def count_string(string_input):
	count = 0
	for item in string_input:
		count += 1
	return count

#2. Write a Python program to count the number of characters (character frequency) in a string. 
#Sample String : google.com'
#Expected Result : {'o': 3, 'g': 2, '.': 1, 'e': 1, 'l': 1, 'm': 1, 'c': 1}
def frequent_character(string_input):
  
  dictionary = {}
  
  for item in string_input:
    if item not in dictionary:
      dictionary[item] = 1
    else:
      dictionary[item] += 1
  return dictionary

"""3. Write a Python program to get a string made of the first 2 and the last 2 chars from a given a string. If the string length is less than 2, return instead of the empty string.
Sample String : 'w3resource'
Expected Result : 'w3ce'
Sample String : 'w3'
Expected Result : 'w3w3'
Sample String : ' w'
Expected Result : Empty String """
def first_last(string_input):
  if len(string_input) < 2:
    return None
  first = string_input[:2]
  last = string_input[-2:]
  return first + last

""" 4. Write a Python program to get a string from a given string where all occurrences of its first char have been changed to '$', except the first char itself.
Sample String : 'restart'
Expected Result : 'resta$t' """
def changing_dola(string_input):
  first_char = string_input[0]
  string_temp = string_input[1:]
  string_output = first_char + string_temp.replace(first_char, '$')
  return string_output
 	#or
def change_char(str1):
  char = str1[0]
  str1 = str1.replace(char, '$')
  str1 = char + str1[1:]
  return str1

""" 5. Write a Python program to get a single string from two given strings, separated by a space and swap the first two characters of each string.
Sample String : 'abc', 'xyz'
Expected Result : 'xyc abz' """
def join_string(string_a, string_b):
  string_c = string_b[:2] + string_a[2:]
  string_d = string_a[:2] + string_b[2:]
  return string_c + ' ' + string_d

"""6. Write a Python program to add 'ing' at the end of a given string (length should be at least 3). If the given string already ends with 'ing' then add 'ly' instead. If the string length of the given string is less than 3, leave it unchanged.
Sample String : 'abc'
Expected Result : 'abcing'
Sample String : 'string'
Expected Result : 'stringly'"""
def adj_adv(string_input):
  length_string = len(string_input)
  if length_string < 3:
    return string_input
  else:
    if string_input.endswith("ing"):
      return string_input + "ly"
    else:
      return string_input + "ing"
#or
def add_string(str1):
  length = len(str1)
  if length > 2:
    if str1[-3:] == 'ing':
      str1 += 'ly'
    else:
      str1 += 'ing'
  return str1


""" 9. Write a Python program to remove the nth index character from a nonempty string.  """
def remove_string(string_input, index):
  if not string_input:
    return "String must not be empty"
  length = len(string_input)
  if index >= length:
    return "Index is over"
  return string_input[:index] + string_input[index+1:]

""" 15. Write a Python function to create the HTML string with tags around the word(s).
Sample function and result :
add_tags('i', 'Python') -> '<i>Python</i>'
add_tags('b', 'Python Tutorial') -> '<b>Python Tutorial </b>' """
def html(tag, string):
  return "<{}>{}</{}>".format(tag, string, tag)
#or
def html(tag, string):
	return "<%s>%s</%s>" % (tag, string, tag)