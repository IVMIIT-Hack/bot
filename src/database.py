#!seperaokeq/bin/python
import os
import requests
import pandas as pd
import sqlite3
import threading
from bs4 import BeautifulSoup
from pathlib import Path
from parser_table import HTMLTableParser

global_inst = [0, 1, 5]
global_typeofstudy = [0, 1, 2, 3]
global_category = [1, 2]

file_path = r"C:/Users/seper/Documents/IVMIIT-Hack/bot"

class DataBaseAbiturents():
    """
        Этот класс отвечает за обработку и импорт данных с сайта и
        создание базы данных локально, чтобы можно было работать с ней.
        
        Реализована поддержка (частично) многопоточности при обращении к сайту и парсинг данных.
    """
    def __init__(self):
        self.global_inst = [0, 1, 5]
        self.global_typeofstudy = [0, 1, 2, 3]
        self.global_category = [1, 2]
        
    #def existesLocalDB(self):
        #    for inst in self.global_inst:
        #        soup = BeautifulSoup(self.importNormalHTML(("https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_inst=" + str(inst))), 'html.parser')
        #        p_faculty = soup.select('select[name=p_faculty] > option')
        #        for p_faculty_option in p_faculty:
        #            conn_user = sqlite3.connect(str("./db/" + str(inst) + "/" + str(p_faculty_option['value']) + ".db"));
    #
    
    """
        Исправление от битого тега <OPTION SELECTED value=> в HTML странице.
    """
    def fixhtmlbrokentags(self, url):
        r = requests.get(url)
        return r.text.replace("<OPTION SELECTED value=>", " ") #Fix shift code KPFU site.  
    
    #def importAllDataToDB():
        #    conn_user = sqlite3.connect("./db/users.db");
        #    global cursor;
        #    cursor = conn_user.cursor()
        #
        #    for inst in self.global_inst:
        #        soup = BeautifulSoup(self.importNormalHTML(("https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_inst=" + str(inst))), 'html.parser')
        #        print("\n Институты/Факультеты:")
        #        p_faculty = soup.select('select[name=p_faculty] > option')
        #        for p_faculty_option in p_faculty:
        #            conn_user = sqlite3.connect(str("./db/" + str(inst) + "/" + str(p_faculty_option['value']) + ".db"));
        #            cursor.execute('CREATE TABLE UNIVERSITY_' + p_inst_option['value'] + ' (id text uuid primary key,snilsc char(150),otv1 varchar(50),otv2 varchar(50),otv3 varchar(50),pravotv varchar(50))')
        #
        #    soup = BeautifulSoup(importNormalHTML("https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open="), 'html.parser')
        #    print("\n Вузы:")
        #    p_inst = soup.select('select[name=p_inst] > option')
        #    for p_inst_option in p_inst:
        #        print ('value: {}, text: {}'.format(p_inst_option['value'], p_inst_option.text))
        #        #cursor.execute('CREATE TABLE UNIVERSITY_' + p_inst_option['value'] + ' (id int uuid primary key,snilsc char(150),otv1 varchar(50),otv2 varchar(50),otv3 varchar(50),pravotv varchar(50))')
        #
        #    print("\n Институты/Факультеты:")
        #    p_faculty = soup.select('select[name=p_faculty] > option')
        #    for p_faculty_option in p_faculty:
        #        print ('value: {}, text: {}'.format(p_faculty_option['value'], p_faculty_option.text))
        #    
        #    print("\n Направления/Специальности:")
        #    p_speciality = soup.select('select[name=p_speciality] > option')
        #    for p_speciality_option in p_speciality:
        #        print ('value: {}, text: {}'.format(p_speciality_option['value'], p_speciality_option.text))
        #    
        #    print("\n Форма обучения:")
        #    p_typeofstudy = soup.select('select[name=p_typeofstudy] > option')
        #    for p_typeofstudy_option in p_typeofstudy:
        #        print ('value: {}, text: {}'.format(p_typeofstudy_option['value'], p_typeofstudy_option.text))
        #    
        #    print("\n Категория:")
        #    p_category = soup.select('select[name=p_category] > option')
        #    for p_category_option in p_category:
        #        print ('value: {}, text: {}'.format(p_category_option['value'], p_category_option.text))
    #    
    def importfulldata(self):
        soup = BeautifulSoup(str(self.fixhtmlbrokentags(("https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open="))), 'html.parser')
        p_inst = soup.select('select[name=p_inst] > option')
        for p_inst_option in p_inst:
            print("ВУЗ:" + p_inst_option.text)
            soup_inst = BeautifulSoup(str(self.fixhtmlbrokentags(("https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_inst=" + str(p_inst_option['value'])))), 'html.parser')
            p_faculty = soup_inst.select('select[name=p_faculty] > option')
            for p_faculty_option in p_faculty:
                print(" Институт: " + p_faculty_option.text)
                soup_faculty = BeautifulSoup(str(self.fixhtmlbrokentags(("https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_inst=" + str(p_inst_option['value']) + "&p_faculty=" + p_faculty_option['value']))), 'html.parser')
                p_speciality = soup_faculty.select('select[name=p_speciality] > option')
                for p_speciality_option in p_speciality:
                    print("     Факультет: " + p_speciality_option.text)
                    soup_speciality = BeautifulSoup(str(self.fixhtmlbrokentags(("https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_inst=" + str(p_inst_option['value']) + "&p_faculty=" + p_faculty_option['value'] + "&p_speciality=" + p_speciality_option['value']))), 'html.parser')
                    p_typeofstudy = soup_speciality.select('select[name=p_typeofstudy] > option')
                    for p_typeofstudy_option in p_typeofstudy:
                        print("         Форма поступления:" + p_typeofstudy_option.text)
                        p_category = [0, 1]
                        for p_category_option in p_category:
                            print("             Тип обучения:" + str(p_category_option))
                            soup_category = BeautifulSoup(str(self.fixhtmlbrokentags(("https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_inst=" + str(p_inst_option['value']) + "&p_faculty=" + p_faculty_option['value'] + "&p_speciality=" + p_speciality_option['value'] + "&p_typeofstudy=" + p_typeofstudy_option['value'] + "&p_category=" + str(p_category_option)))), 'html.parser')
                            table = soup_category.find( "table", {"id":"t_common"} )
                            p = HTMLTableParser()
                            p.feed(str(table))
                            s = p.tables
                            if(s!=[]): 
                                df = pd.DataFrame(s[0])
                                full_file_path = str(file_path + "/db/csv/" + str(p_inst_option['value']) + "/" + str(p_faculty_option['value']) + "/" + str(p_speciality_option['value']) + "/" + str(p_typeofstudy_option['value']) + "/")
                                if not os.path.exists(full_file_path): #Если пути не существует создаем его
                                    os.makedirs(full_file_path)
                                df.to_csv(full_file_path + "/" + str(p_category_option) + ".csv")

if __name__ == "__main__":
    dba = DataBaseAbiturents()
    dba.importfulldata()


class DataBaseAbiturentsExport():
    
    def __init__(self):
        self.search_request = []
    
    #def fullsearch_data(self):
    #    