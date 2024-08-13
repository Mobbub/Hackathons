# data_otput = {
#     'stat': {
#         'num_users': 10,
#         'popular_product': {
#             'name': '',
#             'num_sales': 0,
#             'percentage_take_product': 0
#         },
#         'top_10_product': {
#             1: '',
#             2: '',
#             3: '',
#             4: '',
#             5: '',
#             6: '',
#             7: '',
#             8: '',
#             9: '',
#             10: ''
#         }
#     }
# }

# data2 = {
#     'users': {
#         1: {
#             'id': '112312323321',
#             'FIO': 'Иванов Иван Иванович'
#         },
#         2: {
#             'id': '123321333',
#             'FIO': 'Иванов Иван Иванович'
#         },
#         3: {
#             'id': '122222222223321',
#             'FIO': 'Иванов Иван Иванович'
#         },
#         4: {
#             'id': '123ааааааа321',
#             'FIO': 'Иванов Иван Иванович'
#         },
#         5: {
#             'id': '12332555555551',
#             'FIO': 'Иванов Иван Иванович'
#         }
#     }
# }

# combined_data = {**data_otput, **data2}

# print(combined_data)

# {
    
#     'stat': {
#         'num_users': 10, 
#         'popular_product': {
#             'name': '', 
#             'num_sales': 0, 
#             'percentage_take_product': 0
#         }, 
#         'top_10_product': {
#             1: '', 
#             2: '', 
#             3: '', 
#             4: '', 
#             5: '', 
#             6: '', 
#             7: '', 
#             8: '', 
#             9: '', 
#             10: ''
#         }
#     }, 
#     'users': {
#         1: {
#             'id': '112312323321', 
#             'FIO': 'Иванов Иван Иванович'
#         }, 
#         2: {
#             'id': '123321333', 
#             'FIO': 'Иванов Иван Иванович'
#         }, 
#         3: {
#             'id': '122222222223321', 
#             'FIO': 'Иванов Иван Иванович'
#         }, 
#         4: {
#             'id': '123ааааааа321', 
#             'FIO': 'Иванов Иван Иванович'
#         }, 
#         5: {
#             'id': '12332555555551', 
#             'FIO': 'Иванов Иван Иванович'
#         }
#     }
# }

# initial_dict = {}
# sorted_dict = dict(sorted(initial_dict.items(), key=lambda x: x[1], reverse=True))

# print(sorted_dict)

input_data = {
    1: {
        'id': '23', 
        'client_name': 'Иван', 
        'client_middle_name': 'Иванович', 
        'client_surname': 'Иванов'
    }, 
    2: {'id': '2', 'client_name': 'Александр', 'client_middle_name': 'Петрович', 'client_surname': 'Петров'}, 
    3: {'id': '232', 'client_name': 'Максим', 'client_middle_name': 'Андреевич', 'client_surname': 'Иванов'}
}


result = {}

for key, value in input_data.items():
    fio = f"{value['client_surname']} {value['client_name']} {value['client_middle_name']}"
    result[key] = {
        'id': value['id'],
        'FIO': fio
    }

print(result)