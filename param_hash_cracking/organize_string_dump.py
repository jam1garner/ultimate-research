with open('string_dump.txt', 'r') as f:
    text = ''.join([line.split('\tC\t')[1] for line in f.readlines()])

with open('string_dump.txt', 'w') as f:
    f.write(text)
