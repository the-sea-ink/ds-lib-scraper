import os

#os.system('(head -n 1 spiders/items.csv && tail -n+2 spiders/items.csv | sort) > spiders/pandas_kb.csv')

with open('spiders/items.csv') as infile, open('spiders/pandas_kb.csv', 'w') as outfile:
    for idx, line in enumerate(infile):
        if idx == 0:
            outfile.write(f'index,{line}')
        else:
            outfile.write(f'{idx},{line}')