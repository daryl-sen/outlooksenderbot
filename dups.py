original_list = """
"""

new_list = """
"""




new_list = new_list.split('\n')
original_list = original_list.split('\n')
list_difference = (item for item in new_list if item not in original_list)


print(list_difference)
for name in list_difference:
    # print(name)
    print(name.split(',')[1])
    # print(name)
