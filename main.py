import json
import sqlite3
name_JSON = input('Укажите путь до json файла с которого хотите считать данные')# приглашение к вводу в командной строке
f = open(name_JSON,'r')# открываем JSON файл
data_dict = json.load(f) #выгружаем всю информацию из джсон файла и задаем для нее переменную
f.close() # закрываем файл
name_SQL = input('Укажите путь до sqlite файла в который хотите внести данные') #приглашение к вводу в командной строке
conn = sqlite3.connect(name_SQL)# объявляем переменную, которая отвечает за соединение с базой данных
list_title = list(data_dict[0].keys())# сделаем список из ключей первого словаря
create_cmd = f"""CREATE TABLE IF NOT EXISTS PERSONAL ( {list_title[0]} TEXT, {list_title[1]} INT, {list_title[2]} TEXT, {list_title[3]} TEXT, {list_title[4]} TEXT, {list_title[5]} TEXT, {list_title[6]} TEXT, {list_title[7]} TEXT)"""#создаем таблицу в базе данных используя ключи из первого словаря
conn.execute(create_cmd)# заставляем SQL запрос работать
conn.commit()# принимаем работу SQL запроса и регаем ее в базе
select_cmd = f"SELECT name FROM personal" #собираем значения всех имен из скл таблицы
cursor=conn.execute(select_cmd)# заставляем SQL запрос работать и объявляем его в переменную
names_JSON=[] #пустой список имен из джсон файла
for i in data_dict:# циклом проходимся по информации из джсон файла
    names_JSON.append(i[list_title[0]]) #добавляем все значения имен которые нам встретились во время выполнения цикла в пустой список имен из джсон файла
names_SQL = []# пустой список имен в скл
names_NOT=[]# пустой список имен которые есть в скл, но нет в джсон
for row in cursor:# проходим циклом по каждому имени в скл таблице
    names_SQL.append(row[0])# добавляем значение имени из скл таблицы в пустой список имен в скл
    if row[0] not in names_JSON:# если имя есть в скл, но нет в джсоне
        names_NOT.append(row[0])# добавляем значение имени которого нет в джсоне, но есть в скл в соответствующий список
cursor.close()# закрываем SQL запрос
for i in names_NOT:# проходим циклом по списку имен, которых нет в джсон, но есть в скл
    del_cmd = f"DELETE FROM PERSONAL WHERE {list_title[0]}='{i}'"# удаляем строчку с iм именем из списка
    conn.execute(del_cmd)# заставляем СКЛ запрос работать
conn.commit()# регаем запрос в базе данных
for i in data_dict:# проходим циклом по по всей информации из джсон файла
    list_dict = list(i.keys())# создаем список из ключей, которые есть в iм словаре в информации из джсон файла
    if i[list_dict[0]] in names_SQL:# если значение имени в iм словаре есть в списке имен, которые есть в скл
        update_cmd = f"UPDATE PERSONAL SET {list_dict[1]}={i[list_dict[1]]},{list_dict[2]}='{i[list_dict[2]]}', {list_dict[3]}='{i[list_dict[3]]}',{list_dict[4]}='{i[list_dict[4]]}',{list_dict[5]}='{i[list_dict[5]]}',{list_dict[6]}='{i[list_dict[6]]}',{list_dict[7]}='{i[list_dict[7]]}' WHERE name = '{i[list_dict[0]]}'"# обновляем информацию которая изменилась из джсон файла
        conn.execute(update_cmd)# заставляем СКЛ запрос работать
    else:# если значения имени в iм словаре нет в списке имен, которые есть в скл
        insert_cmd = f"INSERT INTO PERSONAL ({list_dict[0]}, {list_dict[1]}, {list_dict[2]},{list_dict[3]},{list_dict[4]},{list_dict[5]},{list_dict[6]},{list_dict[7]}) VALUES ('{i[list_dict[0]]}', {i[list_dict[1]]}, '{i[list_dict[2]]}','{i[list_dict[3]]}','{i[list_dict[4]]}','{i[list_dict[5]]}','{i[list_dict[6]]}','{i[list_dict[7]]}')"# добавляем всю известную информацию из джсон файла
        conn.execute(insert_cmd)# заставляем СКЛ запрос работать
conn.commit()# регаем запрос в базе данных
conn.close()# закрываем соединение с базой данный