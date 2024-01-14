# Задача №49.

# Создать телефонный справочник с возможностью импорта и экспорта данных в формате .txt. 
# Фамилия, имя, отчество, номер телефона - данные, которые должны находиться в файле. 
# 1. Программа должна выводить данные 
# 2. Программа должна сохранять данные в текстовом файле
# 3. Пользователь может ввести одну из характеристик для поиска определенной записи(Например имя или фамилию человека)
# 4. Использование функций. Ваша программа не должна быть линейной

from csv import DictReader, DictWriter
from os.path import exists

class LenNumberError:
    def __init__(self, txt):
        self.txt = txt
class LenFirstNameError:
    def __init__(self, txt):
        self.txt = txt

def get_info():
    second_name = "Ivanov"
    is_valid_number = False
    is_valid_first_name = False
    while not is_valid_number:
        try:
            phone_number = int(input('Введите номер: '))
            if len(str(phone_number)) != 11:
                raise LenNumberError('Невалидная длина')
            else:
                is_valid_number = True
        except ValueError:
            print('Невалидный номер')
            continue
        except LenNumberError as err:
            print(err)
            continue
    while not is_valid_first_name:
        try:
            first_name = str(input('Введите имя: '))
            if len(first_name) < 2:
                raise LenFirsNameError('Невалидное имя')
            else:
                is_valid_first_name = True
        except ValueError:
            print('Невалидное имя')
            continue
        except LenFirstNameError as err:
            print(err)
            continue

    return [first_name, second_name, phone_number]

def create_file(file_name):
    with open(file_name, 'w', encoding ='UTF-8') as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_writer.writeheader()

def read_file(file_name):
    with open(file_name, 'r', encoding ='UTF-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)
    
def write_file(file_name, user_data):
    res = read_file(file_name)
    if user_data == '':
        user_data = get_info()
        obj = {'Имя': user_data[0],'Фамилия': user_data[1], 'Телефон': user_data[2] }
    else:
        obj = user_data
    res.append(obj)
    if user_data == '':
        for el in res:
            if el['Телефон'] == str(user_data[2]):
                print('Пользователь уже существует')
                return

    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя','Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)

def define_new_file_name():
    new_file_name = input('Введите файл куда скопировать данные ')
    if exists(new_file_name) == True:
        return new_file_name
    else:
        request = str(input('Файл создать? y or n'))
        if request == 'y':
            create_file(new_file_name)
            return new_file_name
        else:
            return ''

def copy_line(file_name, new_file_name):
    res = False
    if file_name == '' or new_file_name == '':
        print('Имя файла пустое')
    else:
        data = read_file(file_name)
        while res == False:
            try:
                row = int(input('Введите строку для копирования'))
                if row < 1 or row >= len(data):
                    print('Введите значение от 1 до ' + str(len(data)) )
                else:
                    write_file(new_file_name, data[row-1])
                    res = True
            except ValueError:
                print('Невалидный номер')
                continue

    return res

file_name = 'phone.csv'

def main():
    while True:
        command = input('Введите команду: ').lower()
        if command == "q":
            break
        elif command == "w":
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, user_data='')
        elif command == "r":
            if not exists(file_name):
                print('Файл не создан. Создайте файл.')
                continue
            print(*read_file(file_name))
        elif command == 'c':
            if copy_line(file_name, define_new_file_name()) == True:
                print('Строка скопирована')
            else:
                print('Скопировать строку не удалось')

main()
        