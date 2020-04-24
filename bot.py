

import telebot
import json
import requests
from time import time
import datetime
import time
import re 
import logging
 #
bot = telebot.TeleBot('1115488703:AAFc_53Pk5iqDKAmT5k52GXk-j6lVUNED5U')
chat_id='@mktest123'


DictMatchN ={} #словарь (ИДматча, длинна словаря с ходом боя)
DictMatchHead ={} # словарь (ИДматча, Персы+кефы)
DictSendMes={} # словарь (номер матча, ИДсообщения)
DictTime = {} # словарь (номер матча, время меньше , среднее , больше)
#*******************************ФУНКЦИИ************************************
def printaster(dataZ): #выводим данные в виде таблицы
    kef4a=dataZ['Value']['GE']
    FWtext =""
    for lika in kef4a:   #кефы 
        if lika['G'] == 563:
            WinP1 = 0
            WinP2 = 0
        #print(lika['E'])
            for li in lika['E']:
                #print(li)
                if li[0]["T"] == 2140:
                    WinP1 = li[0]["C"]
                elif li[0]["T"] == 2141:
                    WinP2 = li[0]["C"]
            print(WinP1, WinP2)
        
        #print(str(WinP1)+"/"+str(WinP2))
        if lika['G'] == 572: # добивания
            print("Добивания")
            print(lika['E'][0])
            Fat = 0
            Bru = 0
            Ruka = 0
            for li in lika['E'][0]:
                if li["T"] == 4057:
                    Fat = li["C"]
                elif li["T"] == 4058:
                    Bru = li["C"]
                elif li["T"] == 4059:
                    Ruka = li["C"]

            print(Fat, Bru , Ruka)

        if lika['G'] == 576: # время
            #print("Время в раунде")
            m = int(str(lika['E'][0][0]['P'])[-3:-1])+0.5
            cp = int(str(lika['E'][0][1]['P'])[-3:-1])+0.5
            b = int(str(lika['E'][0][2]['P'])[-3:-1])+0.5
            tmm = lika['E'][1][0]['C']
            tbm = lika['E'][0][0]['C']
            tmcp = lika['E'][1][1]['C']
            tbcp = lika['E'][0][1]['C']
            tmb = lika['E'][1][2]['C']
            tbb = lika['E'][0][2]['C']
            cp2 = round(float(cp)/1.5,2)
        if lika['G'] == 1442: #фат да нет
            print(lika['E'][0])
            FatYes = 0
            FatNo = 0
            for li in lika['E'][0]:
                if li["T"] == 4929:
                    FatYes = li['C']
                if li["T"] == 4930:
                    FatNo = li['C']
        if lika['G'] == 1092:
            FW = lika['E'][0][0]['C']
            FWtext = '\n'+"#FW - "+ str(FW)
    
    x1text= '_P1/P2_ - '+str(WinP1)+"/"+str(WinP2)+'\n'+'_FBR_'+' -  '+str(Fat)+" | *"+str(Bru)+"* | "+str(Ruka)+FWtext+'\n'+'TIME(M-B)'+'\n'+str(m)+" ("+str(tmm)+" - "+str(tbm)+ ")"+'\n'+str(cp)+" ("+str(tmcp)+" - "+str(tbcp)+")"+ '\n'+str(b)+" ("+str(tmb)+" - "+str(tbb)+")"+ '\n'+ "_FYes_ -" +str(FatYes)+ " "*4 + "_FNo_ -"+str(FatNo)+'\n'    #'\n'    
    return x1text
    
    #x1text= '_P1/P2_ - '+str(WinP1)+"/"+str(WinP2)+'\n'+'_FBR_'+' -  '+str(Fat)+" | *"+str(Bru)+"* | "+str(Ruka)+'\n'+'TIME(M-B)'+'\n'+str(m)+".5"+" ("+str(tmm)+" - "+str(tbm)+ ")"+'\n'+str(cp)+".5"+" ("+str(tmcp)+" - "+str(tbcp)+")"+ '\n'+str(b)+".5"+" ("+str(tmb)+" - "+str(tbb)+")"+ '\n'+ "_FYes_ -" +str(FatYes)+ " "*4 + "_FNo_ -"+str(FatNo)+'\n'    #'\n'    
    #return x1text   

def dobiv(x): #выводим данные лайва в виде букв
    if x == "Fatality" or x == "Faction Kill":
        return "_F_"
    elif x == "Regular":
        return "R"
    elif x == "Brutality":
        return "*B*"
        
def logErr(logStr):
    name = "error" + str(datetime.datetime.now().strftime("%d-%m-%H")) + ".log"# функция для записи лога
    with open(name, 'a', encoding='utf-8') as f_obj:
        string = str(datetime.datetime.now().strftime("%H:%M:%S"))+"\n"+str(tima)+ '\n' + ': ' + logStr+ '\n' + "*"*50+ '\n'
        f_obj.write(string)
        
def logInst(logStr):
    name = "logInst" + str(datetime.datetime.now().strftime("%d-%m-%H")) + ".log"
# функция для записи лога
    with open(name, 'a', encoding='utf-8') as f_obj:
        string = str(datetime.datetime.now().strftime("%H:%M:%S"))+"\n"+str(tima)+ '\n' + ': ' + logStr+ '\n' + "*"*50+ '\n'
        f_obj.write(string)

def logPars(logStr):
    name = "logPars" + str(datetime.datetime.now().strftime("%d-%m-%H")) + ".log"
# функция для записи лога
    with open(name, 'a', encoding='utf-8') as f_obj:
        string = str(datetime.datetime.now().strftime("%H:%M:%S"))+"\n"+str(tima)+ '\n' + ': ' + logStr+ '\n' + "*"*50+ '\n'
        f_obj.write(string)
        
def logXOD(logStr):
    name = "logXOD" + str(datetime.datetime.now().strftime("%d-%m-%H")) + ".log"
# функция для записи лога
    with open(name, 'a', encoding='utf-8') as f_obj:
        string = str(tima)+ '\n' + ': ' + logStr + "*"*50+ '\n'
        f_obj.write(string)
        
def ClearDict(Dicta):
    if len(Dicta)>11:
        #print(Dicta)
        soga  = list(Dicta.keys())
        r=0
        while r<5 :
            #print(soga[r])
            del Dicta[int(soga[r])]
            r+=1
    return Dicta
def cleanPers(Perk):
    zwd = Perk.replace(' ', '').replace("'", "").replace("-", "")
    #print(zwd)
    return zwd
#*************************КОНЕЦ ФУНКЦИЯМ**************************************************


bot.send_message(chat_id= chat_id, text="START", parse_mode= 'Markdown')
i=1
while i<500:
    
    try:
        #logname = "mylog"+str(datetime.datetime.now().strftime("%d_%H"))+".log"
        #logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = logname) #
        
      #time.sleep(2) # in seconds
        tic = time.time()
        response = requests.get("https://1xbet.com/LiveFeed/Get1x2_Zip?champs=1252965&sports=103&count=10&mode=4&cyberFlag=1&country=1")
        Para = json.loads(response.text)
        Para
        for listik in Para["Value"]:
            tim = listik["S"]
            tima = datetime.datetime.fromtimestamp(tim).strftime('%M')
            #print(tima)
            if listik["L"]=="Mortal Kombat X":

                print(tima)
                response2 = requests.get('https://1xbet.com/LiveFeed/GetGameZip?id='+str(listik['I'])+'&lng=ru&cfview=0&isSubGames=true&GroupEvents=true&countevents=250&grMode=2')
                Para2 = json.loads(response2.text)
                #print(Para2)
                numberMatch = int(Para2['Value']["DI"])

                tima = datetime.datetime.fromtimestamp(tim).strftime('%H:%M %Y-%m-%d')
                dics = Para2["Value"]["SC"] #словарь в котором проверяем начало боя
                #PersLeft = str(listik["O1"].replace(' ', ''))
                #.replace("'", "") +'\n' +"#" +listik["O1"].replace(' ', '').replace("'", "")+"_"+ listik["O2"].replace(' ', '').replace("'", "")
                #PersRight = str(listik["O2"].replace(' ', ''))
                PersLeft = cleanPers(listik["O1"])
                PersRight = cleanPers(listik["O2"])
                Bouti = str(PersLeft + "" + PersRight)
                print ("KUKU")
                
                if DictMatchHead.get(numberMatch,0)==0:
                    TimeList = []
                    m = int(str(Para2['Value']['GE'][1]['E'][0][0]['P'])[-3:-1])+0.5
                    cp = int(str(Para2['Value']['GE'][1]['E'][0][1]['P'])[-3:-1])+0.5
                    b = int(str(Para2['Value']['GE'][1]['E'][0][2]['P'])[-3:-1])+0.5
                    TimeList.append(m)
                    TimeList.append(cp)
                    TimeList.append(b)
                    DictTime[numberMatch]= TimeList
                    #HEADstr= tima   + '\n'+"#" +PersLeft + " - "+"#" + PersRight + " - "+listik["DI"]+'\n' + printaster(Para2)
                    HEADstr= tima+ "  #N"+listik["DI"]  + '\n'+"#" +Bouti+ '\n'+"#" +PersLeft + " - "+"#" + PersRight +'\n' + printaster(Para2)
                    DictMatchHead.setdefault(numberMatch,HEADstr)
                    print("NEW game ", tima )
                    mes=bot.send_message(chat_id= chat_id, text=HEADstr, parse_mode= 'Markdown')
                    DictSendMes.setdefault(int(Para2['Value']['I']),int(mes.message_id))

                    # если матч уже есть в словаре , то редактируем ссобщение по АЙДИ
                else:
                    HEADstr=DictMatchHead.get(numberMatch)
                if 'TD' in dics:
                    #xtext = str(datetime.datetime.now().strftime("%d %H:%M:%S"))+ '\n' +  Para2["Value"]["L"]+'\n'+tima  +'\n'+"#" +listik["O1"].replace(' ', '') + " - "+"#" + listik["O2"].replace(' ', '')+ " - "+listik["DI"] + str(listik["SC"]['TS'])+'\n'+'До боя осталось ' + str(listik["SC"]['TS']) + ' секунд'+'\n'
                    #mesaga = HEADstr +'\n'+'До боя осталось ' + str(listik["SC"]['TS']) + ' секунд'+'\n'
                    print("Start Match", tima)
                    continue

                else:
                    xok = Para2['Value']['SC']['S'][1]['Value'] #ПОЛУЧАЕМ ход боя
                    xru = DictMatchN.setdefault(int(numberMatch),len(xok)) #проверяем словарь для отслеживания изменений
                    #logPars(str(xok))
                    if xru == len(xok): # если длинна не изменилась , то ничего не делаем
                        print('XOd Boya Ne IZmenilsya', tima)
                        continue
                    elif xru < len(xok):
                        
                        logXOD("="*25+str(datetime.datetime.now().strftime("%H:%M:%S"))+ "="*25+ "\n"+str(numberMatch)+"\n"+str(xru) + "<" + str(len(xok))+"\n")
                        #print(len(xok))
                        #x2text = str(datetime.datetime.now().strftime("%d %H:%M:%S"))+ '\n' + Para2["Value"]["L"]+'\n'+tima +'\n' + "#" +listik["O1"].replace(' ', '') + " - "+"#" + listik["O2"].replace(' ', '')+ " - "+listik["DI"]
                        s4e1 = dics["FS"].setdefault('S1', 0) # счет П1 , если нет значения , то 0
                        s4e2 = dics["FS"].setdefault('S2', 0)
                        s4 = str(s4e1)+str(s4e2)
                        print("Change XOD boya", tima)
                        DictMatchN[int(numberMatch)]=len(xok)
                        try:
                            Shapk =HEADstr  +'\n' +"*"+str(s4e1)+"*"+":"+"*"+str(s4e2)+"*" # выводим кефыs4e2 =="4":
                            logKef = str(datetime.datetime.now().strftime("%d %H:%M:%S")) +  str(Para2["Value"]["L"])+ '\n'+str(s4e1)+str(s4e2) + "\n"+ str(Shapk) + "\n"+ str(Para2["Value"]["SC"]) + "\n"+ str(Para2['Value']['GE'])  
                            logInst(logKef)
                        except Exception as e:
                            logStr = "ошибка ХОДА БОЯ" +"\n" + str(datetime.datetime.now().strftime("%d %H:%M:%S"))+"\n"+str(e)+"\n"+ str(Para2['Value']['GE'])
                            logErr(logStr)                            #print(str(e)) 
                        logPars("\n"+"XOD "+"\n"+str(xok)+"\n"+str(TimeList))
                        try:
                            sim =json.loads(Para2['Value']['SC']['S'][1]['Value'])
                            logXOD("\n"+"Вход в конструктор БоЯ "+"\n"+str(sim)+"\n")
                                                       
                            for a in sim:
                                persHead = (Para2['Value']['O1E']).lower() # имя перса из заголовка
                                persLive = (a["W"]).lower() # имя перса из хода боя
                                if ("takeda" in persHead and persLive.startswith("tak")): #проверяем на такеду
                                    per = "P1"
                                elif str(persHead) == str(persLive): #сравниваем П1 с победителем в раунде
                                    per = "P1"
                                else:
                                    per = "P2"
                                if int(a["T"])<=int(DictTime[numberMatch][0]):
                                    timR = "TMM"
                                elif int(a["T"])<=int(DictTime[numberMatch][1]):
                                    timR = "TM"
                                elif int(a["T"])<=int(DictTime[numberMatch][2]):
                                    timR = "TB"
                                else:
                                    timR = "TBB"
                                if a["WT"]=="1":
                                    Shapk = Shapk+ "\n" + str(a["R"])+"."+" "+per+"--"+dobiv(a["DI"])+"--"+str(a["T"])+"  "+ str(timR)+" "+"#ЧП"
                                else:
                                    Shapk = Shapk+ "\n" + str(a["R"])+"."+" "+per+"--"+dobiv(a["DI"])+"--"+str(a["T"])+"  "+ str(timR)
                                logXOD("\n" + str(a["R"])+"."+" "+per+"--"+dobiv(a["DI"])+"--"+str(a["T"])+"  "+ str(timR)+"\n")
                            logXOD(Shapk+"\n"+str(datetime.datetime.now().strftime("%H:%M:%S"))+"\n"+"*"*20)
                            #Shapk = Shapk +"\n" + str(a["R"])+"."+" "+per+"-"+dobiv(a["DI"])+"-"+str(a["T"])
                            #DictMatchHead[numberMatch]=HEADstr
                            #print(HEADstr)
                            #Shapk =HEADstr  +'\n' +"*"+str(s4e1)+"*"+":"+"*"+str(s4e2)+"*"
                            logInst(persHead+ "\n" + persLive + "\n" + "*<<***"+ Shapk + "*****>>*******")
                        except Exception as e:
                            logStr = str(datetime.datetime.now().strftime("%d %H:%M:%S"))+ "XOD Boya ERROR: "+"\n"+ str(e)+"\n"+ str(sim)+"\n"+str(a)
                            logErr(logStr)

                        logSter = str(Para2['Value']['I'])+"\n" + str(Para2['Value']['O1E'])+"****" + str(a["W"]) +"\n" + str(Shapk)+"\n" + str(DictMatchN) + "\n" + str(DictSendMes)
                        logInst(logSter)
                    else:
                        #logInst("\n" +"Fcuk YOU"+ "\n")
                        continue
                    print("SEND MESSSSSSSANGE"*3)
                    mesaga = Shapk
                # проверяем через словарь был матч у нас раньше или нет 
                # если не было - публикуем, запоминаем АЙДИ и заносим в словарь
                try:
                    if DictSendMes.get(Para2['Value']['I'],0)==0:
                        mes=bot.send_message(chat_id= chat_id, text=mesaga, parse_mode= 'Markdown')
                        DictSendMes.setdefault(int(Para2['Value']['I']),int(mes.message_id))
                        #print(listik)
                        #print(Para2)
                    # если матч уже есть в словаре , то редактируем ссобщение по АЙДИ
                    else:
                        bot.edit_message_text(chat_id= chat_id, message_id=DictSendMes.get(int(Para2['Value']['I'])), text=mesaga, parse_mode= 'Markdown')
                except Exception as e:
                    logStr = str(datetime.datetime.now().strftime("%d %H:%M:%S"))+ "TELEGRAM ERROR: "+"\n"+ str(e)+"\n"+ str(mesaga)+"\n"+str(DictSendMes)
                    logErr(logStr)
                
            
            else:
                continue

    except Exception as e:
        logStr = str(datetime.datetime.now().strftime("%d %H:%M:%S"))+ "ОБЩАЯ ОШИБКА: "+"\n"+ str(e)+"\n"+ str(listik)+"\n"+str(Para2)
        logErr(logStr)
        #print(str(e))
    try:        
        ClearDict(DictMatchN)
        ClearDict(DictSendMes)
        ClearDict(DictMatchHead)
        ClearDict(DictTime)
    except Exception as e:
        logStr = "ошибка ОЧИСТКИ СЛОВАРЕЙ" +"\n" + str(datetime.datetime.now().strftime("%d %H:%M:%S"))+"\n"+str(e)+"\n"+ str(DictMatchN) + "\n"+ str(DictSendMes)+"\n"+ str(DictMatchHead)+"\n"+"\n"
        logErr(logStr)
    #print(str(DictMatchN) + "\n" + str(DictSendMes))
    #i+=1
    toc = time.time()
    
    logPars("*-"*25+"\n"+"*"+str(toc - tic)+"*"+"*-"*25+"\n")


