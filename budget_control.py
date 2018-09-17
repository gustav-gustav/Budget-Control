#!/usr/bin/env python3

__author__ = 'gustavo barros'

import os
import glob
import errno

abertura = 'For available commands, type "cmd". \nTo leave type "quit"'
lista_de_comandos = ['\nadd money', 'set limit', 'spend', 'check limits', 'clear', 'balance\n']


def print_lista(lista):
    for x in lista:
        print(x)


def ppv(x):
    nx = x.replace(',', '.')
    if nx.count('.') == 0:
        fx = int(nx)
    else:
        fx = float(nx)
    return fx


def formatação(m):
    while True:
        try:
            v = ppv(str(input(m)))
            return v
        except ValueError:
            print('\nVocê digitou um ou mais caracteres inválidos. '
                  'Digite apenas números, separando as casas decimais com ponto ou vírgula!\n')
            continue


def try_cat(category):
    if ' ' in category:
        category = category.replace(' ', '_')
    else:
        pass
    return category


def sum_files(_type):
    path = os.path.join(os.getcwd(), 'data', _type, '*.txt')
    files = glob.glob(path)
    number_list = []
    for name in files:
        try:
            if _type == 'spend':
                with open(name) as f:
                    contents = f.read()
                    x = contents.split()
                    x = list(map(int, x))
                    number = sum(x)
                    number_list.append(number)
                    sum_number_list = sum(number_list)

            else:
                with open(name) as f:
                    number = int(f.read())
                    number_list.append(number)
                    sum_number_list = sum(number_list)

        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return(sum_number_list)


def get_file_path(filename, dataDir):
    pasta = 'data'
    currenDirPath = os.getcwd()
    filepath = os.path.join(currenDirPath, pasta, dataDir, filename)
    return filepath


def get_file_name(category, _type):
    filename = try_cat(category) + '.txt'
    filepath = get_file_path(filename, _type)
    return filepath


def action_file(file, mode='r', amount=0):
    if mode == 'w':
        with open(file, mode) as f:
            value = int(f.write(amount))
            return value

    elif mode == 'a':
        with open(file, mode) as f:
            value = f.write(amount)

    elif mode == 'r' and amount == 0:
        with open(file) as f:
            value = f.read()
            return value


def get_budget():
    budget = int(action_file(get_file_name('budget', 'data')))
    return budget


def add_money(amount):
    action_file(get_file_name('budget', 'data'), mode='w', amount=str(amount))
    print('\nYour new balance is: {}\n'.format(amount))


def set_limit(category, amount):
    budget = get_budget()
    total_limits = sum_files('limit')
    soma = amount + total_limits
    if budget == 0:
        print('\nYou have to register an income first! \nFor that you can use the command "add money" and type in the amount.\n')

    elif soma > budget:
        sobra = budget - total_limits
        print('The limit exceeded your budget. \nYou have ${} left on your budget'.format(sobra))

    else:
        category = try_cat(category)

        filepath_categorias = get_file_name('categorias', 'data')
        contents = action_file(filepath_categorias)

        if category not in contents:
            action_file(filepath_categorias, mode='a', amount=(category + ' '))

        filepath = get_file_name(try_cat(category), 'limit')
        action_file(filepath, mode='w', amount=str(amount))

        print('\nYour new limit on {} is: {} \n'.format(category, amount))

        try:
            default_file = os.path.join(os.getcwd(), 'data', 'limit', 'default_limit.txt')
            os.remove(default_file)
        except:
            pass


def spend(category, amount):
    budget = get_budget()
    category = try_cat(category)
    filepath_limit = get_file_name(category, 'limit')
    filepath_spend = get_file_name(category, 'spend')

    if budget == 0:
        print('\nYou have to register an income first! \nFor that you can use the command "add money" and type in the amount.\n')

    action_file(filepath_spend, mode='a', amount=(str(amount) + '\n'))
    limit = int(action_file(filepath_limit))
    fs_contents = action_file(filepath_spend)
    number_list = fs_contents.split()
    number_list = list(map(int, number_list))
    number = sum(number_list)
    saldo = limit - number
    print('\nYou just spent ${} on {}. \nYour limit is ${} \nYou stil have ${} on that category\n'.format(str(amount), category, str(limit), str(saldo)))

    try:
        default_file = os.path.join(os.getcwd(), 'data', 'spend', 'default_spend.txt')
        os.remove(default_file)
    except:
        pass


def saldo():
    budget = get_budget()
    saldo = budget - sum_files('spend')
    return saldo


def clear_expense(category):
    filepath = get_file_name(try_cat(category), 'spend')
    action_file(filepath, mode='w', amount='')


def print_stats():
    path = os.path.join(os.getcwd(), 'data', 'limit', '*.txt')
    files = glob.glob(path)
    print('\n')
    for name in files:
        try:
            with open(name, 'r')as fl:
                limit = int(fl.read())
                name_list = name.split('\\', )
                file_name = (name_list[len(name_list) - 1])
                file_name = file_name.split('.')
                file_name = file_name[0]
                file_name = file_name.replace('_', ' ')
                print('Your limit in {} category is ${}'.format(file_name, limit))
            print('\n')

        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise

    print('Your total limit is {} \nYour total spent is {}\n'.format(sum_files('limit'), sum_files('spend')))


def prompt():

    while True:

        print(abertura)

        prompt = input('prompt:')

        if prompt == 'cmd':
            print_lista(lista_de_comandos)

        elif prompt == 'add money':
            amount = formatação('Type the value that you would like to register:\n')
            add_money(amount)

        elif prompt == 'set limit':
            category = input('\nWhat category would you  like to set a limit on?\n')
            amount = formatação('Type the value:\n')
            set_limit(category, amount)

        elif prompt == 'spend':
            category = input('What category would you  like to register an expense?\n')
            amount = formatação('Type the value:\n')
            spend(category, amount)

        elif prompt == 'clear':
            category = input('What category would you  like to clear the records of?\n')
            clear_expense(category)

        elif prompt == 'balance':
            print('\nYour current balance is: {}\n'.format(saldo()))

        elif prompt == 'check limits':
            print_stats()

        elif prompt == 'quit':
            break

        else:
            print('\nType a valid command\n')


# prompt()

# you can set the commands here too as a quick way to set limits and spend
# but you'll have to comment out "prompt()"
# I suggest you to do this in a python envoronment instead of just opening the file
# If you set a spend() command on the code, don't forget to comment it out or clear the expenses first as you
# run the program again, or it'll count as another expense.
# But if you prefer to use the "prompt()", just open the file
