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


def msv(k):
    mf = '{:.2f}'.format(k)
    dec = mf[-2:]
    intf = '{:,}'.format(int(k))
    antes = str(intf).replace(',', '.')
    fn = '{}{}{}'.format(antes, ',', dec)
    return fn


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
                    x = list(map(float, x))
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
    try:
        if mode == 'w':
            with open(file, mode) as f:
                value = float(f.write(amount))
                return value

        elif mode == 'a':
            with open(file, mode) as f:
                value = f.write(amount)

        elif mode == 'r' and amount == 0:
            with open(file) as f:
                value = f.read()
                return value
    except IOError as err:
        print('Could not get file. Be sure it exists')
        # errno.ENOENT
        '''print(err.errno)
                                print(err.strerror)'''


def try_file(name, type_):
    x = action_file(get_file_name(name, type_))
    if x is None:
        return False
    else:
        return True


def file_not_found():
    print('The category does not exist.')


def try_cat(category):
    if ' ' in category:
        category = category.replace(' ', '_')
    else:
        pass
    return category


def get_budget():
    budget = float(action_file(get_file_name('budget', 'data')))
    return budget


def add_money(amount):
    action_file(get_file_name('budget', 'data'), mode='w', amount=str(amount))
    print('\nYour new balance is: {}\n'.format(msv(amount)))


def set_limit(category, amount):
    budget = get_budget()
    total_limits = sum_files('limit')
    soma = amount + total_limits
    category = try_cat(category)
    filepath_categorias = get_file_name('categorias', 'data')
    contents = action_file(filepath_categorias)

    if budget == 0:
        print('\nYou have to register an income first! \nFor that you can use the command "add money" and type in the amount.\n')

    elif soma > budget and category not in contents:
        sobra = budget - total_limits
        print('\nThe limit exceeded your budget. \nYou have ${} left on your budget\n'.format(msv(sobra)))

    else:

        if category not in contents:
            action_file(filepath_categorias, mode='a', amount=(category + ' '))

        filepath = get_file_name(try_cat(category), 'limit')
        action_file(filepath, mode='w', amount=str(amount))

        print('\nYour new limit on {} is: {} \n'.format(category, msv(amount)))

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
    contents_c = action_file(get_file_name('categorias', 'data'))

    if try_file(category, 'spend') is True:

        if budget == 0:
            print('\nYou have to register an income first! \nFor that you can use the command "add money" and type in the amount.\n')

        elif category not in contents_c:
            print('There are no records on that category. Did you typed in correctly?')

        else:
            action_file(filepath_spend, mode='a', amount=(str(amount) + '\n'))
            limit = float(action_file(filepath_limit))
            fs_contents = action_file(filepath_spend)
            number_list = fs_contents.split()
            number_list = list(map(float, number_list))
            number = sum(number_list)
            saldo = limit - number
            print('\nYou just spent ${} on {}. \nYour limit is ${} \nYou stil have ${} on that category\n'.format(str(amount), category, msv(limit), msv(saldo)))

            try:
                default_file = os.path.join(os.getcwd(), 'data', 'spend', 'default_spend.txt')
                os.remove(default_file)
            except:
                pass
    else:
        file_not_found()


def saldo():
    budget = get_budget()
    saldo = budget - sum_files('spend')
    return saldo


def clear_expense(category):
    if try_file(try_cat(category), 'spend') is True:
        filepath = get_file_name(try_cat(category), 'spend')
        action_file(filepath, mode='w', amount='')
    else:
        file_not_found()


def check_expenses(category, print_=False):
    if try_file(try_cat(category), 'spend') is True:
        budget = get_budget()
        filepath_limit = get_file_name(try_cat(category), 'limit')
        filepath_spend = get_file_name(try_cat(category), 'spend')
        limit = float(action_file(filepath_limit))
        fs_contents = action_file(filepath_spend)
        number_list = fs_contents.split()
        number_list = list(map(float, number_list))
        number = sum(number_list)
        saldo = limit - number
        contents_c = action_file(get_file_name('categorias', 'data'))
        if category not in contents_c:
            print('There are no records on that category. Did you typed in correctly?')

        elif print_ is True:
            print('Your limit in {} category is ${} \nYour total expenses on that category is ${}\nYou have ${} left on that category.\n'.format(category, msv(limit), msv(number), msv(saldo)))

        else:
            return number, saldo
    else:
        file_not_found()


def print_stats():
    path = os.path.join(os.getcwd(), 'data', 'limit', '*.txt')
    files = glob.glob(path)
    print('\n')
    for name in files:
        try:
            with open(name, 'r')as fl:
                limit = float(fl.read())
                name_list = name.split('\\', )
                file_name = (name_list[len(name_list) - 1])
                file_name = file_name.split('.')
                file_name = file_name[0]
                number, saldo = check_expenses(file_name)
                file_name = file_name.replace('_', ' ')

                if saldo == 0:
                    print('Your limit in {} category is ${} \nYou have used all your limit on that category'.format(file_name, msv(limit)))
                else:
                    print('Your limit in {} category is ${} \nYour total expenses on that category is ${}\nYou have ${} left on that category.'.format(file_name, msv(limit), msv(number), msv(saldo)))
            print('\n')

        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise

    print('Your total limit is {} \nYour total spent is {}\n'.format(msv(sum_files('limit')), msv(sum_files('spend'))))


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
            print('\nYour current balance is: {}\n'.format(msv(saldo())))

        elif prompt == 'check limits':
            print_stats()

        elif prompt == 'check expenses':
            category = input('What category would you like to check the expenses? \n')
            check_expenses(category, print_=True)

        elif prompt == 'quit':
            break

        else:
            print('\nType a valid command\n')


prompt()

# you can set the commands here too as a quick way to set limits and spend
# but you'll have to comment out "prompt()"
# I suggest you to do this in a python envoronment instead of just opening the file
# If you set a spend() command on the code, don't forget to comment it out or clear the expenses first as you
# run the program again, or it'll count as another expense.
# But if you prefer to use the "prompt()", just open the file
