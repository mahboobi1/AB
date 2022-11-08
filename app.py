import csv
import random
import datetime
import ast
import pandas as pd


''' 3 classes (appointment, category, location) '''


class AppClass:
    def __init__(self, app_name=None, app_time=None, app_duration=None,
                 app_cat_list=None, app_loc_id=None, app_loc_name=None):

        self.file_path = 'app_file.csv'
        self.app_id = int(random.uniform(1000000, 9999999))
        self.app_name = app_name
        self.app_time = app_time
        self.app_duration = app_duration
        self.app_cat_list = app_cat_list
        self.app_loc_id = app_loc_id
        self.app_loc_name = app_loc_name

    def get_info(self):
        self.app_name = input('app title: ')
        self.app_time = get_valid_date_func()
        self.app_duration = get_int_input_func('App duration')

        self.app_cat_list = multy_select_func(CatClass)

        loc_data = one_select_func(LocClass)
        self.app_loc_id = loc_data[0]
        self.app_loc_name = loc_data[1]

    def give_info(self):
        return self.app_id, self.app_name, self.app_time, self.app_duration, \
               self.app_cat_list, self.app_loc_id, self.app_loc_name


class CatClass:
    def __init__(self, cat_name=None, cat_priority=None):
        self.file_path = 'cat_file.csv'
        self.cat_id = int(random.uniform(1000000, 9999999))
        self.cat_name = cat_name
        self.cat_priority = cat_priority

    def get_info(self):
        self.cat_name = input('cat name')
        self.cat_priority = get_int_input_func('cat priority:')

    def give_info(self):
        return self.cat_id, self.cat_name, self.cat_priority


class LocClass:
    def __init__(self, loc_name=None, loc_address=None):
        self.file_path = 'loc_file.csv'
        self.loc_id = int(random.uniform(1000000, 9999999))
        self.loc_name = loc_name
        self.loc_address = loc_address

    def get_info(self):
        self.loc_name = input('loc name')
        self.loc_address = input('loc address')

    def give_info(self):
        return self.loc_id, self.loc_name, self.loc_address


''' 7 main functions (new, read, search1, search2, edit, delete, sort)'''


def new_func(class_name):
    new_object = class_name()
    new_object.get_info()
    with open(new_object.file_path, 'a') as f:
        csv.writer(f, delimiter=';').writerow(new_object.give_info())
    f.close()


def read_func(class_name):
    with open(class_name().file_path, 'r') as f:
        for i, row in enumerate(csv.reader(f, delimiter=';')):
            print(i+1, row)
    f.close()


def search_func(class_name):
    result_list = []
    search_key = input('what are you looking for')
    with open(class_name().file_path, 'r') as f:
        for i in csv.reader(f, delimiter=';'):
            for j in i:
                if j == search_key:
                    result_list += [i]
    if result_list:
        for i in range(len(result_list)):
            print(result_list[i])
    else:
        print('not exist')
    f.close()


def search_in_app_func(class_name):
    result_list = []
    search_field = get_int_input_func('where? title = 1, date = 2, category = 4, location = 6')
    search_key = input('what are you looking for?')

    if search_field == 1 or search_field == 6:
        with open(class_name().file_path, 'r') as f:
            for i in csv.reader(f, delimiter=';'):
                if i[search_field] == search_key:
                    result_list += [i]
        if result_list:
            for i in range(len(result_list)):
                print(result_list[i])
        else:
            print('not exist')
        f.close()

    elif search_field == 4:
        with open(class_name().file_path, 'r') as f:
            for i in csv.reader(f, delimiter=';'):
                cat_ls = ast.literal_eval(i[search_field])
                for j in range(len(cat_ls)):
                    if cat_ls[j][1] == search_key:
                        result_list += [i]
            if result_list:
                for i in range(len(result_list)):
                    print(result_list[i])
            else:
                print('not exist')
            f.close()

    elif search_field == 2:
        date_value = ''
        with open(class_name().file_path, 'r') as f:
            for i in csv.reader(f, delimiter=';'):
                for j in range(10):
                    date_value = date_value + i[search_field][j]
                if date_value == search_key:
                    result_list += [i]
                date_value = ''
            if result_list:
                for i in range(len(result_list)):
                    print(result_list[i])
            else:
                print('not exist')
            f.close()


def edit_func(class_name):
    delete_func(class_name)
    new_func(class_name)


def delete_func(class_name):
    line_index = get_int_input_func('line number')
    temp_list = []
    with open(class_name().file_path, 'r') as f:
        for i, row in enumerate(csv.reader(f, delimiter=';')):
            if i == line_index - 1:
                continue
            temp_list.append(row)
    f.close()

    with open(class_name().file_path, 'w') as f:
        for i in range(len(temp_list)):
            csv.writer(f, delimiter=';').writerow(temp_list[i])
    f.close()


def sort_fuc(class_name):
    csv_data = pd.read_csv(class_name().file_path, delimiter=';', header=None)
    print(csv_data.sort_values(1))


''' 6 helpful functions to handle routines '''


def one_select_func(class_name):
    read_func(class_name)
    user_select = int(input('line number to select'))
    with open(class_name().file_path, 'r') as f:
        for i, row in enumerate(csv.reader(f, delimiter=';')):
            if i == user_select - 1:
                return row


def multy_select_func(class_name):
    read_func(class_name)
    cat_list = []
    while True:
        user_select = get_int_input_func('line number to select')
        with open(class_name().file_path, 'r') as f:
            for i, row in enumerate(csv.reader(f, delimiter=';')):
                if i == user_select - 1:
                    cat_list += [row]
                    x = input('want to add more? (y, n)')
                    if x != 'y':
                        return cat_list


def get_valid_date_func():
    while True:
        try:
            date_text = input('Enter date and time in this format: YYY-MM-DD 00:00')
            x = datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M')
            return x
        except ValueError:
            print("Incorrect data format, should be YYY-MM-DD 00:00")


def get_int_input_func(message):
    print(message)
    while True:
        try:
            int_value = int(input('Type a number: '))
            return int_value
        except ValueError:
            print('Just a number')


def action_user_input():
    while True:
        try:
            action_choice = int(input('(Create = 1, Read = 2, Search = 3, Edit = 4, Delete = 5, Sort = 6, Exit = 0 )'))
            if action_choice > 6 or action_choice < 0:
                print('Please choose a number according to the menu!')
                continue
            break
        except ValueError:
            print('Please choose a number according to the menu!')
    return action_choice


def area_user_input():
    while True:
        try:
            area_choice = int(input('(Appointment = 1, Category = 2, Location = 3, Exit = 0 )'))
            if area_choice > 3 or area_choice < 0:
                print('Please choose a number according to the menu!')
                continue
            break
        except ValueError:
            print('Please choose a number according to the menu!')
    if area_choice == 1:
        return AppClass
    elif area_choice == 2:
        return CatClass
    elif area_choice == 3:
        return LocClass
    else:
        exit()


''' 1 navigation menu '''


def menu():
    x = action_user_input()
    y = area_user_input()
    if x == 0:
        exit()
    if x == 1:
        new_func(y)
    if x == 2:
        read_func(y)
    if x == 3:
        if y == AppClass:
            search_in_app_func(y)
        else:
            search_func(y)
    if x == 4:
        read_func(y)
        edit_func(y)
        read_func(y)
    if x == 5:
        read_func(y)
        delete_func(y)
        read_func(y)
    if x == 6:
        sort_fuc(y)


while True:
    menu()







