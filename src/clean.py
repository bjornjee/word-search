import os

def retrieve(title):
    PATH = '../data/{}.txt'.format(title)
    PATH_TEMP = '../data/{}_temp.txt'.format(title)
    PATH_OLD = '../data/{}_old.txt'.format(title)
    words = []
    with open(PATH,'r+') as file:
        for line in file:
            word = line.rstrip().lower()
            if (not word or len(word) > 10):
                continue
            else:
                words.append(word)

        print("before: {}".format(words))
        words = sorted(list(set(words)))
        print("after: {}".format(words))
        with open(PATH_TEMP,'w') as temp_file:
            temp_file.write('\n'.join(words))
            temp_file.close()
        file.close()
    os.rename(PATH,PATH_OLD)
    os.rename(PATH_TEMP,PATH)

def retrieve_comma():
    words = []
    with open('../data/toclean', 'r+') as file:
        for line in file:
            words.extend(line.rstrip().lower().split(','))
        print(words)
        words = sorted([word.lstrip() for word in list(set(words))])
        print("after: {}".format(words))
        file.truncate(0)
        file.writelines('\n'.join(words))
        file.close()

if __name__ == '__main__':
    l = ['plants','sports','travel','fruits','geography']
    for i in l:
        retrieve(i)