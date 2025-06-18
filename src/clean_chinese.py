
def remove_punctuation(s):
    import re
    punc = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
    #punc = punc.decode("utf-8")
    return re.sub(r"[%s]+" %punc, "", s)


def clean(filename):
    out = []
    with open(filename) as file:
        for line in file:
            line = remove_punctuation(line).rstrip()
            out += line
    with open('../data/chinese_pool_clean.txt','w') as nfile:
        nfile.write("".join(out))

def get_idioms(filename):
    out = []
    with open(filename) as file:
        for line in file:
            out.append(line.split(',')[1].replace('"',''))
    file.close()
    with open('../data/chinese_idioms.txt','a+') as file:
        file.write('\n')
        file.write('\n'.join(out))
    file.close()



if __name__ == '__main__':
    #get_idioms('../data/chinese_kaggle.txt')
    #clean('../data/chinese_pool.txt')