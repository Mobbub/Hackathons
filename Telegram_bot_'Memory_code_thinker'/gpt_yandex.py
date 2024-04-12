import requests, re

def get_yandexgpt_response(person_info: dict, request_subject: dict) -> str:
    ai_role = ''
    if request_subject['deys'] == 'биография':
        ai_role = 'биограф'
    elif request_subject['deys'] == 'эпитафия':
        ai_role = 'писатель эпитафий'
    prompt = {
        'modelUri': 'gpt://token_catalog/yandexgpt-lite',
        'completionOptions': {
            'stream': False,
            'temperature': 0.8,
            'maxTokens': '2000'
        },
        'messages': [
            {
                'role': 'system',
                'text': f'Ты {ai_role}, который составляет {request_subject["deys"]} о человеке.'
            },
            {
                'role': 'user',
                'text': f'Привет! Я бы хотел, чтобы ты составил {request_subject["deys"]} о человеке, сможешь сделать?'
            },
            {
                'role': 'assistant',
                'text': 'Привет! Хорошо, расскажи мне что-нибудь о нём.'
            },
            {
                'role': 'user',
                'text': f'Этого человека зовут {person_info["fio"]}, он родился {person_info["dr"]} в {person_info["mr"]} и умер {person_info["ds"]} в {person_info["ms"]}. Его супругом(супругой) был(была) {person_info["supr"]}. Этот человек окончил {person_info["obr"]}. Его родом деятельности было {person_info["rd"]}. Его гражданство - {person_info["graj"]}. Из детей у него(неё) были {person_info["deti"]}, а из внуков - {person_info["vnuki"]}. Его достижения - {person_info["dost"]}'
            }
        ]
    }
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Api-Key token_key_gpt'
    }
    response = requests.post(url, headers=headers, json=prompt)
    start_point = '\\\\n\\\\n'
    end_point = '"},"status"'
    result = re.search(f'{start_point}(.*?){end_point}', response.text)
    result = result.replace('`', '')
    if result:
        return result.group(1).replace('\\n', '\n')
    else:
        return ''
