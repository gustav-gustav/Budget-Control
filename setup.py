import os

current_path = os.getcwd()
pasta = 'data'
subpasta1 = 'spend'
subpasta2 = 'limit'
subpasta3 = 'data'
path1 = os.path.join(current_path, pasta, subpasta1)
path2 = os.path.join(current_path, pasta, subpasta2)
path3 = os.path.join(current_path, pasta, subpasta3)

try:
    os.mkdir(os.path.join(current_path, pasta))
    os.mkdir(path1)
    os.mkdir(path2)
    os.mkdir(path3)
    with open(os.path.join(path1, 'default_spend.txt'), 'w') as f:
        f.write('0')
    with open(os.path.join(path2, 'default_limit.txt'), 'w') as f:
        f.write('0')
    with open(os.path.join(path3, 'categorias.txt'), 'w') as f:
        f.write('')
    with open(os.path.join(path3, 'budget.txt'), 'w') as f:
        f.write('0')

except:
    print('Your program is already setup!')
