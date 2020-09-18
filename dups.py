original_list = """
"""

new_list = """
"""




new_list = new_list.split('\n')
original_list = original_list.split('\n')
set_difference = set(new_list) - set(original_list)
list_difference = list(set_difference)
print(list_difference)
for name in list_difference:
    print(name)
    # print(name.split(',')[1])
    # print(name)
