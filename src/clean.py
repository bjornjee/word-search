import os

def find_repo_root(current_path):
    while True:
        # Check if a .git directory exists in the current path
        if os.path.exists(os.path.join(current_path, '.git')):
            return current_path
        
        # Move up one directory
        parent_path = os.path.dirname(current_path)
        
        # If we reach the root of the filesystem and haven't found .git, stop
        if parent_path == current_path:
            return None  # Or raise an error

        current_path = parent_path

def retrieve(title):
    root_path = find_repo_root(os.getcwd())
    PATH = '{}/data/{}.txt'.format(root_path,title)
    PATH_TEMP = '{}/data/{}_temp.txt'.format(root_path,title)
    PATH_OLD = '{}/data/{}_old.txt'.format(root_path,title)
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
    l = ['meat', 'plants', 'sports', 'travel','fruits','animals']
    for i in l:
        retrieve(i)