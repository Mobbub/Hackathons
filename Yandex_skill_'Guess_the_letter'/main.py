def hlp(text):
    if text.find("помощь") != -1:
        return True
    return False       
    
def rul(x):
    rules = ['что ты умеешь', 'что делать']
    if (x in rules) or x.find("правила") != -1:
        return True
    return False
    
def gam0(text):
    gam0 = ['алиса начинай', 'алиса давай играть', 'начать игру', 'поехали', 'запускай', 'начинай', 'запусти'] 
    if (text in gam0) or (text.find("начать") != -1) or (text.find("играть") != -1):
        return True
    return False
    
def exit(text):
    message_exit = ['выйти', 'закончить', 'прекратить','вернись','хватит', 'стоп', 'завершить']
    if (text in message_exit) or (text.find("хватит") != -1):
        return True
    return False
    
def popitki(tries_num):
    if tries_num ==0:
        return ('попыток')
    elif tries_num%100>=10 and tries_num%100<=20:
        return ('попыток')
    elif tries_num%10==1:
        return ('попытку')
    elif tries_num%10>=2 and tries_num%10<=4:
        return ('попытки')
    else:
        return ('попыток')
        
def kol_words(words):
    if words ==0:
        return ('слов')
    elif words%100>=10 and words%100<=20:
        return ('слов')
    elif words%10==1:
        return ('слово')
    elif words%10>=2 and words%10<=4:
        return ('слова')
    else:
        return ('слов')
        
def game(answer, l, tries_num, words, ready, session):
    message_exit = ['выйти', 'закончить', 'прекратить','хватит', 'стоп', 'завершить']
    if (answer.find('буква') != -1) or (len(answer) == 1):
        all_words = answer.split(' ')
        if (l in all_words) or (l == 'ь' and 'мягкий' in all_words) \
             or (l == 'ъ' and 'твердый' in all_words):
            ppp = popitki(tries_num)
            www = kol_words(words)
            return [f'''Ура! Вы победили, вы использовали {tries_num} {ppp} и назвали {words} {www}!
            Если хотите сыграть снова, скажите играть, если выйти из навыка, то скажите хватит''', 'false', '', 0, 0, 'false', 'false']
        else:
            return [f'Увы! Ваш ответ {answer} неверен, попробуйте еще раз.', 'true', l, tries_num + 1, words, 'false', 'false']
    for ext in message_exit:
        if answer.find(ext) != -1:
            return [f'''Вы завершили текущую игру. Чтоб начать новую скажите играть, чтоб выйти из навыка скажите хватит''', 'false', '', 0, 0, 'false', 'false']
    if hlp(answer):
        return ['''Возникли вопросы? Вы можете прослушать правила, сказав слово: "Правила" или написать сообщение 
        в Телеграм по адресу: @ioannkul''', 'true', l, tries_num, words, 'false', 'false'] 
    if rul(answer):
        return ['''Правила очень простые: я загадываю букву русского алфавита, а вы должны отгадать её. 
        Чтоб сделать это, вам необходимо подбирать слова. Я буду сообщать вам, имеется или нет моя загаданная буква в вашем слове ''', 'true', l, tries_num, words, 'false', 'false']
    if answer.find(' ') != -1:
        return [f'Скажите, пожалуйста, одно слово', 'true', l, tries_num, words, 'false', 'false']
    if l in answer:
        return [f'В слове {answer} есть эта буква', 'true', l, tries_num, words + 1, 'false', 'false']
    else:
        return [f'В слове {answer} нет этой буквы', 'true', l, tries_num, words + 1, 'false', 'false']

def usual(answer):
    if hlp(answer):
        return ['''Возникли вопросы? Вы можете прослушать правила, сказав слово: "Правила" 
        или написать сообщение в Телеграм по адресу: @ioannkul ''', 'false', '', 0, 0, 'false', 'false'] 
    if rul(answer):
        return ['''Правила очень простые: я загадываю букву русского алфавита, а вы должны отгадать её. 
        Чтоб сделать это, вам необходимо подбирать слова. 
        Я буду сообщать вам, имеется или нет моя загаданная буква в вашем слове''', 'false', '', 0, 0, 'false', 'false']
    if gam0(answer):
        from random import choice
        l = choice('абвгдежзиклмнопрстуфхцчшщыэюя') #буква загаданная Алисой
        return ['Начинаем, я загадала букву', 'true', l, 1, 0, 'false', 'false']
    if exit(answer):
        return ['''Приятно было поиграть с вами! 
        Чтобы вернуться в навык, скажите "Запусти навык Отгадай букву". 
        До свидания!''', 'false', '', 0, 0, 'false', 'true']
    return ['''Извините, я Вас не поняла. 
    Произнесите одно из слов: Правила, Помощь, Играть, Завершить''' , 'false', '', 0, 0, 'false', 'false']  

def handler(event, context):    
    text = ''
    answer = ''
    game_started = 'false'
    letter = ''
    tries_num = 0
    words = 0
    ready = 'false'
    session = 'false' 
    if 'state' in event and \
            'session' in event['state'] \
            and 'letter' in event['state']['session']:
        letter = event['state']['session']['letter']
    if 'state' in event and \
            'session' in event['state'] \
            and 'tries_num' in event['state']['session']:
        tries_num = event['state']['session']['tries_num']
    if 'state' in event and \
            'session' in event['state'] \
            and 'words' in event['state']['session']:
        words = event['state']['session']['words']
    if 'state' in event and \
            'session' in event['state'] \
            and 'ready' in event['state']['session']:
        ready = event['state']['session']['ready']
    if 'state' in event and \
            'session' in event['state'] \
            and 'game_started' in event['state']['session']:
        game_started = event['state']['session']['game_started']
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        answer = event['request']['original_utterance'].lower()
    new_state = []
    if game_started == 'false':
        new_state = usual(answer)       
    else:
        new_state = game(answer, letter, tries_num, words, ready, session)
    text = new_state[0]
    game_started = new_state[1]
    letter = new_state[2]
    tries_num = new_state[3]
    words = new_state[4]
    ready = new_state[5]
    session = new_state[6]
    if not ('state' in event and \
        'session' in event['state'] \
        and 'letter' in event['state']['session']):
        text = ''' Здравствуйте, вы запустили навык "отгадай букву". Чтобы начать игру, скажите играть. 
                   Для ознакомления с правилами, скажите правила. '''
    return {
        'version': event['version'],
        'session': event['session'],
        'response': { 
            'text': text,
            'end_session': session
        },
        'session_state': {
             'game_started': game_started,
             'letter': letter,
             'tries_num': tries_num,
             'words': words,
             'ready': ready,
        }
    }
