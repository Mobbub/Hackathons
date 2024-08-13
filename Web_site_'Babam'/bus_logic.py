# Функция для вычисления общей статистики и вывода всех пользователь на фронт
def general_Statistics(data: dict) -> dict:
    list_prodects_popular = list()
    result = {}

    for key, value in data.items():
        fio = f"{value['client_surname']} {value['client_name']} {value['client_middle_name']}"
        result[key] = {
            'id': value['id'],
            'FIO': fio
        }

    data_users = {
        'users': result
    }
    for key, value in data.items():
        record = data[key]
        num_users = key
        for key, value in record['client_take_products'].items():
            list_prodects_popular.append(value)
    
    count_dict = {}
    
    for item in list_prodects_popular:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1

    sorted_dict = dict(sorted(count_dict.items(), key=lambda x: x[1], reverse=True))

    items = list(count_dict.items())
    items.sort(key=lambda x: x[1], reverse=True)
    result_dict = {i+1: item[0] for i, item in enumerate(items)}
    
    if len(result_dict) < 10:
        for i in range(len(result_dict)+1, 11):
            result_dict[i] = ""
        
    data_stat = {
        'status_result': 200,
        'stat': {
            'num_users': num_users,
            'popular_product': {
                'name': result_dict[1],
                'num_sales': sorted_dict[result_dict[1]],
                'percentage_take_product': sorted_dict[result_dict[1]]/sum(count_dict.values())*100
            },
            'top_10_product': {
                1: result_dict[1],
                2: result_dict[2],
                3: result_dict[3],
                4: result_dict[4],
                5: result_dict[5],
                6: result_dict[6],
                7: result_dict[7],
                8: result_dict[8],
                9: result_dict[9],
                10: result_dict[10]
            }
        }
    }
    
    data_otput = {**data_stat, **data_users}
    print(data_otput)
    return data_otput

def user_Statistics(data: dict, id_user: str) -> dict:
    list_user = list()
    list_info = list()
    for key, value in data.items():
        if data[key]['id'] == id_user:
            if data[key]['client_birthplace'] not in list_info:
                list_info.append(data[key]['client_birthplace'])
            if data[key]['tariff'] not in list_info:
                list_info.append(data[key]['tariff'])
            if data[key]['client_education'] not in list_info:
                list_info.append(data[key]['client_education'])
            if data[key]['credit_sum'] not in list_info:
                list_info.append(data[key]['credit_sum'])
            if data[key]['client_family_status'] not in list_info:
                list_info.append(data[key]['client_family_status'])
            if data[key]['client_client_children_dependents'] not in list_info:
                list_info.append(data[key]['client_client_children_dependents'])
            if data[key]['client_registration_own_type'] not in list_info:
                list_info.append(data[key]['client_registration_own_type'])
            if data[key]['job_type'] not in list_info:
                list_info.append(data[key]['job_type'])
            if data[key]['workplace_client_position'] not in list_info:
                list_info.append(data[key]['workplace_client_position'])
            if data[key]['workplace_additional_income_type'] not in list_info:
                list_info.append(data[key]['workplace_additional_income_type'])
            if data[key]['car_brand'] not in list_info:
                list_info.append(data[key]['car_brand'])
            if data[key]['car_type'] not in list_info:
                list_info.append(data[key]['car_type'])
    return list_info