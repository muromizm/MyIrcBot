#-------Import modules---------------------

import socket
import sys
import time
import requests

from urllib.parse import unquote

#-------Functions---------------------------

# Function shortening of ic.send.  
def send(mes):
  return irc.send(bytes(mes,'utf-8'))

# Function of parcing of get TITLE from link.  
def link_title(n):
    if 'http://' in n or 'https://' in n:
        link_r = n.split('//',1)[1].split(' ',1)[0].rstrip()

    elif 'www.' in n:
        link_r = n.split('www.',1)[1].split(' ',1)[0].rstrip()
    link = 'http://'+link_r

    max_t_link = 5
    t_link = time.time()
    for i in requests.get(link, stream=True):
        t2_link = time.time()
        if t2_link > t_link + max_t_link:
            requests.get(link, stream=True).close()
            print('Title - Ошибка! Превышено время ожидания!')
            link_stat = False
            break
        else:
            link_stat = True

    if link_stat == True:
        unquoted_link = unquote(link)
        get_title = requests.get(link, timeout = 10)
        txt_title = get_title.text
        if '</TITLE>' in txt_title or '</title>' in txt_title or '</Title>' in txt_title:
            if '</TITLE>' in txt_title:
                title = '\x02Title\x02 of '+unquoted_link+': '+txt_title.split('</TITLE>',1)[0].split('>')[-1]
            elif '</title>' in txt_title:
                title = '\x02Title\x02 of '+unquoted_link+': '+txt_title.split('</title>',1)[0].split('>')[-1]
            elif '</Title>' in txt_title:
                title = '\x02Title\x02 of '+unquoted_link+': '+txt_title.split('</Title>',1)[0].split('>')[-1]

            return title.replace('\r','').replace('\n','').replace('www.','').replace('http://','').replace('https://','').strip()
        else:
            return 'Title is no'
          
#-------Global changes variables------------

# Install min & max timer vote.  
min_timer = 30
max_timer = 300

#-------Connect server----------------------

network = 'irc.tambov.ru'
port = 7770
irc = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
channel = '#botest'
botName = 'Govno_tik'
masterName = 'Кай'

#-------Conect to IRC-server----------------

irc.connect ((network, port))
print (irc.recv(2048).decode("UTF-8"))
send('NICK '+botName+'\r\n')
send('USER '+botName+' '+botName+' '+botName+' :Python IRC\r\n')
send('JOIN '+channel+' \r\n')
send('NickServ IDENTIFY xxxxxx\r\n')
send('MODE '+botName+' +x')

#-------Global_variables--------------------
   
name = ''
message = ''
message_voting = ''
voting_results = ''
time_vote_rest = 0

count_voting = 0
count_vote_plus = 0
count_vote_minus = 0
count_vote_all = 0
while_count = 0

btc_usd = 0
eth_usd = 0
usd_rub = 0
eur_rub = 0
btc_rub = 0
btc_usd_old = 0
eth_usd_old = 0
usd_rub_old = 0
eur_rub_old = 0
btc_rub_old = 0
btc_usd_su = str('')
eth_usd_su = str('')
usd_rub_su = str('')
eur_rub_su = str('')
time_vote = 0

whois_ip = ''
whois_ip_get_text = ''

timer_exc = 0
time_exc = 0

where_mes_exc = ''
t2 = 0

#-------Massives----------------------------

dict_users = {}
dict_count = {}
dict_voted = {}
dict_whois = {} 
list_vote_ip = []

# List who free from anti-flood function.
list_floodfree = ['Батый', 'Батый_', botName, masterName]

#-------Major_while-------------------------
  
while True:
    try:
        data = irc.recv(2048).decode("UTF-8")
    except:
        continue
    # Ping-pong.
    if data.find('PING') != -1:
        send('PONG'+data.split()[1]+'\r\n')
    
    # Make variables Name, Message, IP from user message.
    if data.find('PRIVMSG') != -1:
        name = data.split('!',1)[0][1:]
        message = data.split('PRIVMSG',1)[1].split(':',1)[1]
    try:
        ip_user=data.split('@',1)[1].split(' ',1)[0]
    except:
        print('no ip_user on 73 line')

    #-----------Bot_help---------------

    if 'PRIVMSG '+channel+' :!помощь' in data or 'PRIVMSG '+botName+' :!помощь' in data:
        send('NOTICE %s : Помощь по командам бота:\r\n' %(name))
        send('NOTICE %s : ***Функция опроса: [!опрос (число) сек (тема опрос)], например (пишем \
без кавычек: \"!опрос 60 сек Вы любите ониме?\", если не писать время, то время установится на 60 сек\r\n' %(name))
        send('NOTICE %s : ***Функция курса: просто пишите (без кавычек): \"!курс\". Писать можно и в приват боту\r\n' %(name))
        send('NOTICE %s : ***Функция айпи: что бы узнать расположение IP, просто пишите (без кавычек): \"!где айпи (IP)\", пример: \"!где айпи \
188.00.00.01\". Писать можно и в приват к боту\r\n' %(name))        

    #-----------Anti_flood-------------

    # Count of while.  
    while_count += 1
    if while_count == 50:
        while_count = 0
        dict_count = {}
            
    # Insert nick in dict: dic_count.  
    if data.find('PRIVMSG') != -1 and name not in dict_count and name not in list_floodfree:
        dict_count[name] = int(1)
        if 'PRIVMSG '+channel in data:
            where_message = channel
        elif 'PRIVMSG '+botName in data:
            where_message = botName
    
    # If new message as last message: count +1.  
    if data.find('PRIVMSG') != -1 and message == dict_users.get(name) and name not in list_floodfree:
        dict_count[name] += int(1)
    
    # Add key and value in massiv.  
    if data.find('PRIVMSG') != -1 and name not in list_floodfree:
        dict_users[name] = message
    
    # Message about flood and kick. 
    if data.find('PRIVMSG') != -1 and name not in list_floodfree:
        for key in dict_count: 
            if dict_count[key] == 3 and key != 'none':
                send('PRIVMSG '+where_message+' :'+key+', Прекрати флудить!\r\n')
                dict_count[key] += 1
            elif dict_count[key] > 5 and key != 'none':
                send('KICK '+channel+' '+key+' :Я же сказал не флуди!\r\n')
                dict_count[key] = 0
            
    #--------Request-answer in channel-------------
      
    # Out command.  
    if data.find('PRIVMSG '+channel+' :!бот выйди') != -1 and name == masterName:
        send('PRIVMSG '+channel+' :Хорошо, всем счастливо оставаться!\r\n')
        send('QUIT\r\n')
        sys.exit()

    # Message per bot.  
    if "PRIVMSG %s :!напиши "%(channel) in data or "PRIVMSG %s :!напиши "%(botName) in data and name == masterName:
        mes_per_bot = message.split('!напиши ',1)[1]
        send(mes_per_bot)
        
    #---------Whois servis--------------------------

    if 'PRIVMSG '+channel+' :!где айпи' in data or 'PRIVMSG '+botName+' :!где айпи' in data:

        if 'PRIVMSG '+channel+' :!где айпи' in data:
            where_message_whois = channel
            
        elif 'PRIVMSG '+botName+' :!где айпи' in data:
            where_message_whois = name
                      
        try:
            whois_ip = data.split('!где айпи',1)[1].split('\r',1)[0].strip()
            whois_list_split=whois_ip.split('.')
            list_whois = []
            for i in whois_list_split:
                list_whois.append(int(i))
            try:
                whois_ip_get = requests.get('https://api.2ip.ua/geo.xml?ip='+whois_ip, timeout = 5)
            except:
                send('PRIVMSG %s :Ошибка! Не удалось полчить IP через API!\r\n'%(where_message_whois))
                continue

            if whois_ip in dict_whois:
                send('PRIVMSG '+where_message_whois+' :IP взято из памяти:\r\n')
                send('PRIVMSG %s :%s\r\n'%(where_message_whois,dict_whois[whois_ip]))
                continue
              
            country_whois=whois_ip_get.text.split('<country_rus>',1)[1].split('</country_rus>',1)[0]
            city_whois=whois_ip_get.text.split('<city_rus>',1)[1].split('</city_rus>',1)[0]
            time_zone_whois=whois_ip_get.text.split('<time_zone>',1)[1].split('</time_zone>',1)[0]
                     
            whois_final_reply = ' \x02IP:\x02 '+whois_ip+' \x02Страна:\x02 '+country_whois+' \x02Город:\x02 '+city_whois+' \x02Часовой пояс \
:\x02 '+time_zone_whois+'\r\n'
            send('PRIVMSG '+where_message_whois+' :'+whois_final_reply)

            # Make a IP as kay and final relpy as value in a dict for future use for reply again.  
            dict_whois[whois_ip] = whois_final_reply

        except:
            print('get Value Error in whois servis!')
            send('PRIVMSG '+where_message_whois+' :Ошибка! Вводите только IP адрес из цифр, разделенных точками! Или существующий ник!\r\n')
                     
    #---------Info from link in channel-------------
    
    if 'PRIVMSG %s :'%(channel) in data:
        if 'http://' in data or 'https://' in data or 'www.' in data:
            try:
                send('PRIVMSG %s :%s\r\n'%(channel,link_title(data)))
            except:
                print('Ошибка получения Title')
            
    #---------Voting--------------------------------
                
    t = time.time()
    if '!стоп опрос' in data and 'PRIVMSG' in data and name == masterName:
        t2 = 0
        print('счетчик опроса сброшен хозяином!')
    if 'PRIVMSG '+channel+' :!опрос ' in data:
        if t2 == 0 or t > t2+time_vote:
            if ' сек ' not in data:
                time_vote = 60
                # Make variable - text-voting-title form massage.  
                message_voting = message.split('!опрос',1)[1].strip()
            if ' сек ' in data:
                try:
                    # Get time of timer from user message.  
                    time_vote = int(message.split('!опрос',1)[1].split('сек',1)[0].strip())
                    # Make variable - text-voting-title form massage.  
                    message_voting = message.split('!опрос',1)[1].split('сек',1)[1].strip()
                except:
                    time_vote = 60
                    # Make variable - text-voting-title form massage.  
                    message_voting = message.split('!опрос',1)[1].strip()

            if min_timer>time_vote or max_timer<time_vote:
                send('PRIVMSG %s :Ошибка ввода таймера голосования. Введите от %s до %s сек!\r\n'%(channel,min_timer,max_timer))
                continue
            
            t2 = time.time()
            count_vote_plus = 0
            count_vote_minus = 0
            vote_all = 0
            count_voting = 0
            list_vote_ip = []
            # Do null voting massiv.  
            dict_voted = {}
            send('PRIVMSG %s :Начинается опрос: \"%s\". Опрос будет идти %d секунд. Чтобы ответить "да", пишите: \"!да\" \
", чтобы ответить "нет", пишите: \"!нет\". Писать можно как открыто в канал, так и в приват боту, чтобы голосовать анонимно \r\n' % (channel,message_voting,time_vote))
            list_vote_ip = []
                
    # If find '!да' count +1.  
    if data.find('PRIVMSG '+channel+' :!да') != -1 or data.find('PRIVMSG '+botName+' :!да') != -1:
        if ip_user not in list_vote_ip and t2 != 0:
            count_vote_plus +=1
            dict_voted[name] = 'yes'
            list_vote_ip.append(ip_user)
            # Make notice massage to votes user.  
            send('NOTICE '+name+' :Ваш ответ \"да\" учтен!\r\n')

    # If find '!нет' count +1.  
    if data.find('PRIVMSG '+channel+' :!нет') != -1 or data.find('PRIVMSG '+botName+' :!нет') != -1:
        if ip_user not in list_vote_ip and t2 != 0:
            count_vote_minus +=1
            dict_voted[name] = 'no'
            list_vote_ip.append(ip_user)
            # Make notice massage to votes user.  
            send('NOTICE '+name+' :Ваш ответ \"нет\" учтен!\r\n')
   
    # If masterName send '!список голосования': send to him privat messag with dictonary Who How voted.  
    if data.find('PRIVMSG '+botName+' :!список опроса') !=-1 and name == masterName:
        for i in dict_voted:
            send('PRIVMSG '+masterName+' : '+i+': '+dict_voted[i]+'\r\n')

    # Count how much was message in channel '!голосование'.  
    if data.find('PRIVMSG '+channel+' :!опрос') != -1 and t2 != 0:
        count_voting += 1

    # If voting is not end, and users send '!голосование...': send message in channel.  
    t4 = time.time()
    if data.find('PRIVMSG '+channel+' :!опрос') != -1 and t4-t2 > 5:
        t3 = time.time()
        time_vote_rest_min = (time_vote-(t3-t2))//60
        time_vote_rest_sec = (time_vote-(t3-t2))%60
        if (time_vote-(t3-t2)) > 0:
            send('PRIVMSG %s : Предыдущий опрос: \"%s\" ещё не окончен, до окончания опроса осталось: %d мин %d сек\r\n \
' % (channel,message_voting,time_vote_rest_min,time_vote_rest_sec))

    # Make variable message rusults voting.  
    vote_all = count_vote_minus + count_vote_plus
    voting_results = 'PRIVMSG %s : результаты опроса: \"%s\", "Да" ответило: %d человек(а), "Нет" ответило: %d человек(а), Всего ответило: %d человек(а) \
\r\n' % (channel, message_voting, count_vote_plus, count_vote_minus, vote_all)

    # When voting End: send to channel ruselts and time count to zero.  
    if t-t2 > time_vote and t2 != 0:
        t2 = 0
        send('PRIVMSG '+channel+' : Опрос окончен!\r\n')
        send(voting_results)
    
    #---------Exchange-------------

    # Get exchange from internet API at regular time.     
    if 'PRIVMSG '+channel+' :!курс' in data or 'PRIVMSG '+botName+' :!курс' in data:
        if 'PRIVMSG '+channel+' :!курс' in data:
            where_mes_exc = channel
        if 'PRIVMSG '+botName+' :!курс' in data:
            where_mes_exc = name

        try:
            api_exc_get = requests.get('https://api.exmo.com/v1/ticker/', timeout = 5)
            api_exc = api_exc_get.text
        except:
            print('Проблемы с получением API exchange!')

        try:
            btc_usd = round(float(api_exc.split('"BTC_USDT":',1)[1].split('"avg":"',1)[1].split('","vol"',1)[0][0:]),2)
        except:
            print('Проблемы с получением курса btc_usd')
        try:
            eth_usd = round(float(api_exc.split('"ETH_USDT":',1)[1].split('"avg":"',1)[1].split('","vol"',1)[0][0:]),2)
        except:
            print('Проблемы с получением курса eth_usd')
        try:
            usd_rub = round(float(api_exc.split('"USDT_RUB":',1)[1].split('"avg":"',1)[1].split('","vol"',1)[0][0:]),2)
        except:
            print('Проблемы с получением курса usd_rub')    
        try:
            btc_eur = round(float(api_exc.split('"BTC_EUR":',1)[1].split('"avg":"',1)[1].split('","vol"',1)[0][0:]),2)
        except:
            print('Проблемы с получением курса btc_eur')

        eur_rub = round(float(usd_rub*(btc_usd / btc_eur)),2)
        btc_rub = round(float(btc_usd * usd_rub),2)

        # Make trends symbols from last request.  
        if btc_usd > btc_usd_old:
            btc_usd_tend = '▲'
        elif btc_usd < btc_usd_old:
            btc_usd_tend = '▼'
        else:
            btc_usd_tend = '■'

        if eth_usd > eth_usd_old:
            eth_usd_tend = '▲'
        elif eth_usd < eth_usd_old:
            eth_usd_tend = '▼'
        else:
            eth_usd_tend = '■'    

        if btc_rub > btc_rub_old:
            btc_rub_tend = '▲'
        elif btc_rub < btc_rub_old:
            btc_rub_tend = '▼'
        else:
            btc_rub_tend = '■'    

        if usd_rub > usd_rub_old:
            usd_rub_tend = '▲'
        elif usd_rub < usd_rub_old:
            usd_rub_tend = '▼'
        else:
            usd_rub_tend = '■'

        if eur_rub > eur_rub_old:
            eur_rub_tend = '▲'
        elif eur_rub < eur_rub_old:
            eur_rub_tend = '▼'
        else:
            eur_rub_tend = '■'    

        # Make variables from nubmers for make trends (see up).      
        btc_usd_old = btc_usd
        eth_usd_old = eth_usd
        usd_rub_old = usd_rub
        eur_rub_old = eur_rub
        btc_rub_old = btc_rub        

        btc_usd_str = str(btc_usd)
        eth_usd_str = str(eth_usd)
        usd_rub_str = str(usd_rub)
        eur_rub_str = str(eur_rub)
        btc_rub_str = str(btc_rub)            

        send_res_exc = '\x033Курсы: \x02BTC/USD:\x02 '+btc_usd_str+' '+btc_usd_tend+' \x02ETH/USD:\x02 '+eth_usd_str+' '+eth_usd_tend+' \x02USD/RUB:\x02 \
'+usd_rub_str+' '+usd_rub_tend+' \x02EUR/RUB:\x02 '+eur_rub_str+' '+eur_rub_tend+' \x02BTC/RUB:\x02 \
'+btc_rub_str+' '+btc_rub_tend+'\r\n'

        send('PRIVMSG %s :%s\r\n'%(where_mes_exc,send_res_exc))
    
    #------------Printing---------------

    print(data)
