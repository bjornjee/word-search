#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import shutil
import sys
from datetime import datetime
from multiprocessing import Pool, Queue, Value, Lock, Process
import time
import uuid

from config import *

PUZZLES_FOLDER = os.path.join('/'.join(os.getcwd().split('/')[:-1]),"puzzles")
LETTERS = "letters"
NUMBERS = "numbers"
CHINESE = "chinese"


random.seed(datetime.now().timestamp())

# Directions are:
# +. left to right
# -. right to left
# .+ top to bottom
# .- bottom to top

all_directions = ('+-', '+.', '++', '.+', '.-', '--', '-.', '-+')

styles = {
    'easy': ('10x10', ('+.', '.+')),
    'standard': ('10x10', ('+-', '+.', '++', '.+', '.-', '-.')),
    'hard': ('12x12', all_directions),
    'ying ying': ('10x10', ('+.','++','.+, +-'))
}

confi = {
    '10x10': 1.8,
    '12x12': 1.5,
    '15x15': (1.3,22,16)
}

dirconv = {
    '-': -1,
    '.': 0,
    '+': 1,
}

letters = u"abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
shapes = "◊●♠♣♥▲▼*%#@"


class Grid(object):
    def __init__(self, wid, hgt):
        self.wid = wid
        self.hgt = hgt
        self.data = ['.'] * (wid * hgt)
        self.used = [' '] * (wid * hgt)
        self.words = []

    def to_text(self):
        result = []
        for row in range(self.hgt):
            result.append(''.join(self.data[row * self.wid:
                                            (row + 1) * self.wid]))
        return '\n'.join(result)

    def used_to_text(self):
        result = []
        for row in range(self.hgt):
            result.append(''.join(self.used[row * self.wid:
                                            (row + 1) * self.wid]))
        return '\n'.join(result)

    def to_pdf(self, filename, words, type):
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.platypus.paragraph import Paragraph
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus.flowables import Spacer
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.units import inch
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont

        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        #pdfmetrics.registerFont(TTFont('Wingding', './winding.ttf'))
        font_chinese = 'STSong-Light'  # from Adobe's Asian Language Packs
        font_shape = 'Courier'
        pdfmetrics.registerFont(UnicodeCIDFont(font_chinese))
        doc = SimpleDocTemplate(filename, pagesize=A4, topMargin = 28, creator = 'Bjorn')
        data = [self.data[x: x + self.wid] for x in range(0, len(self.data), self.wid)]
        l = cm * 1.5
        t = Table(data, len(data[0]) * [l], len(data) * [l])
        t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('BOX', (0, 0), (-1, -1), 1, colors.black),
                               ('FONTSIZE', (0, 0), (-1, -1), 22),
                               ]))
        if (type == 'chinese'):
            t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                   ('BOX', (0, 0), (-1, -1), 1, colors.black),
                                   ('FONTSIZE', (0, 0), (-1, -1), 22),
                                   ('FONTNAME', (0, 0), (-1, -1), font_chinese)
                                   ]))
        style = ParagraphStyle(
            'default',
            fontName='Vera',
            fontSize=24,
            leading=18,
            spaceBefore=10,
            spaceAfter=10,
            bulletFontName='Vera',
            bulletFontSize=18,
            bulletIndent=4,
        )
        style_heading = ParagraphStyle(
            'default',
            alignment=1,
            fontName='Vera',
            fontSize=32
        )
        if (type == 'letters'):
            elements = [Paragraph('WORD SEARCH', style_heading, None)]
        elif(type == 'numbers'):
            elements = [Paragraph('NUMBER SEARCH', style_heading, None)]
        elif (type == 'chinese'):
            elements = [Paragraph('CHINESE SEARCH', style_heading, None)]
            style.fontName = font_chinese
            style_heading.fontName = font_chinese
        elif (type == 'shapes'):
            elements = [Paragraph('SHAPE SEARCH', style_heading, None)]
            style.fontName = font_shape
            style_heading.fontName = font_shape
        elements.append(Spacer(1, 2 * cm))
        elements.append(t)
        elements.append(Spacer(1, 0.5 * cm))
        style.fontSize = 18
        if (type == 'letters' or type == 'chinese'):
            elements.append(Paragraph('Find the words :',style))
        elif (type == 'numbers'):
            elements.append(Paragraph('Find the numbers: ',style))
        elif (type == 'shapes'):
            elements.append(Paragraph('Find the shapes: ',style))
        style.leading = 30
        style.fontSize = 18
        #add words
        #first half
        length = len(words)
        #second half
        elements.append(Paragraph(', '.join(words[:length//2]),style))
        elements.append(Paragraph(', '.join(words[length // 2:]), style))

        '''
        if(type == 'chinese'):
            out = ""
            for i in range(len(words)):
                if (i==2):
                    out = out + words[i] + ',&nbsp'
                else:
                    out = out + words[i] + ',&nbsp&nbsp&nbsp'
            elements.append(Paragraph(out,style))
        else :
            for n , word in enumerate(words):
                if (n % 2 == 0):
                    s = word
                elif(n % 2 == 1):
                    elements.append(Paragraph(fill_spaces(s,word),style))
        '''
        doc.build(elements)

    def pick_word_pos(self, wordlen, directions):
        xd, yd = random.choice(directions)
        minx = (wordlen - 1, 0, 0)[xd + 1]
        maxx = (self.wid - 1, self.wid - 1, self.wid - wordlen)[xd + 1]
        miny = (wordlen - 1, 0, 0)[yd + 1]
        maxy = (self.hgt - 1, self.hgt - 1, self.hgt - wordlen)[yd + 1]
        x = random.randint(minx, maxx)
        y = random.randint(miny, maxy)
        return x, y, xd, yd

    def write_word(self, word, ox, oy, xd, yd):
        x, y = ox, oy
        for c in word:
            p = x + self.wid * y
            e = self.data[p]
            if e != '.' and e != c:
                return False
            x += xd
            y += yd

        x, y = ox, oy
        for c in word:
            p = x + self.wid * y
            self.data[p] = c
            self.used[p] = '.'
            x += xd
            y += yd

        return True

    def place_words(self, words, directions, tries=100):
        # Sort words into descending order of length
        words = list(words)
        words.sort(key=lambda x: len(x), reverse=True)

        for word in words:
            wordlen = len(word)
            while True:
                x, y, xd, yd = self.pick_word_pos(wordlen, directions)
                if self.write_word(word, x, y, xd, yd):
                    self.words.append((word, x, y, xd, yd))
                    break
                tries -= 1
                if tries <= 0:
                    return False
        return True

    def fill_in_letters(self, words):
        # 90% time hard, 10% not hard
        should_be_hard = random.randint(0,9) != 0
        pool = letters
        if should_be_hard:
            pool = ''.join([w[:3] for w in words])
        for p in range(self.wid * self.hgt):
            if self.data[p] == '.':
                self.data[p] = random.choice(pool)

    def fill_in_numbers(self):
        for p in range(self.wid * self.hgt):
            if self.data[p] == '.':
                self.data[p] = random.choice(numbers)

    def fill_in_shapes(self):
        for p in range(self.wid * self.hgt):
            if self.data[p] == '.':
                self.data[p] = random.choice(shapes)

    def fill_in_chinese(self,words):
        chinese_pool = ''.join([w[:3] for w in words])
        for p in range(self.wid * self.hgt):
            if self.data[p] == '.':
                self.data[p] = random.choice(chinese_pool)


def make_grid(stylep="standard", words=[], type = 'letters',tries=100):
    # Parse and validate the style parameter.
    size, directions = styles.get(stylep, (stylep, all_directions))
    size = size.split('x')
    if len(size) != 2:
        raise ValueError("Invalid style parameter: %s" % stylep)
    try:
        wid, hgt = map(int, size)
    except ValueError:
        raise ValueError("Invalid style parameter: %s" % stylep)

    directions = [(dirconv[direction[0]], dirconv[direction[1]])
                  for direction in directions]

    while True:
        grid = Grid(wid, hgt)
        if grid.place_words(words, directions):
            break
        tries -= 1
        if tries <= 0:
            return None
    if (type == 'letters'):
        grid.fill_in_letters(words)
    elif (type == 'numbers'):
        grid.fill_in_numbers()
    elif(type == 'chinese'):
        grid.fill_in_chinese(words)
    elif(type == 'shapes'):
        grid.fill_in_shapes()
    return grid

def fill_spaces(old_string, new_string):
    for i in range (40- len(new_string)-len(old_string)):
        old_string += '&nbsp;'
    old_string += new_string
    return old_string

#TODO: Generate words max length 10


def retrieve_words(num_of_words,title='animals'):
    import numpy as np
    PATH = '../data/{}.txt'.format(title)
    from numpy.random import choice as ch
    out = []
    with open(PATH,'r') as file:
        words = [line.rstrip().lower() for line in file]
        length = len(words)
        positions = ch(length,num_of_words,replace=False)
        for i in positions:
            out.append(words[i])
        #print("OUT: {}".format(out))
        file.close()
    return out

def retrieve_chinese_words(num_of_words):
    import numpy as np
    PATH = '../data/chinese_idioms.txt'
    from numpy.random import choice as ch
    out = []
    with open(PATH,'r') as file:
        words = [line.rstrip().lower() for line in file]
        length = len(words)
        positions = ch(length,num_of_words,replace=False)
        for i in positions:
            out.append(words[i])
        #print("OUT: {}".format(out))
        file.close()
    return out

def worker(in_queue: Queue,out_queue:Queue):
    while True:
        try:
            task = in_queue.get(timeout=3)
            func,args = task
            try:
                # this assumes func is lock safe
                result = func(**args)
                out_queue.put(result)
            except:
                in_queue.put((func,args))

        except Exception as e:
            time.sleep(1)


def generate(title,type, length, difficulty, dir, random = False, num_choices = 8):
    if (type == 'letters'):
        words = retrieve_words(num_choices, title)
        input_l = ["".join(w.lower().split()) for w in words]
    elif (type == 'numbers' and not random):
        input_l = generate_numbers_fixed(num_choices,length)
    elif (type == 'numbers' and random):
        input_l = generate_numbers_random(num_choices)
    elif (type == 'chinese'):
        words = retrieve_chinese_words(num_choices)
        input_l = ["".join(w.lower().split()) for w in words]
    elif (type == 'shapes'):
        input_l = generate_shapes(num_choices, length)
    grid = make_grid(difficulty, input_l,type)
    if grid is None:
        print(
            "Can't make a grid")
        return type,0
    else:
        pass
    filename= str(uuid.uuid4())[:6]
    grid.to_pdf(os.path.join(dir, filename + ".pdf"), input_l,type)
    return type,1


def generate_numbers_random(num,length = 4):
    out = []
    c= [4,5,6,7]
    random.seed()
    for i in range(num):
        q = random.choice(c)
        a = random.randrange(10**(q-1),10**(q),1)
        out.append(str(a))
    return out

def generate_numbers_fixed(num, length=4):
    out = []
    random.seed()
    for i in range(num):
        a = random.randrange(10 ** (length - 1), 10 ** (length), 1)
        out.append(str(a))
    return out

def generate_shapes(num, length = 4):
    out = []
    c = [4,5,6,7]
    random.seed()
    for i in range(num):
        q = random.choice(c)
        random_chars = [random.randint(0,len(shapes)-1) for _ in range(q)]
        a = ''.join([shapes[r] for r in random_chars])
        out.append(a)
    return out


#TODO: Format words to find at the bottom of PDF

def create_all(number_of_files):
    NUM_WORKERS=4
    print(f'running with {NUM_WORKERS} subprocesses')
    # spin up workers
    worker_queue = Queue()
    done_queue = Queue()
    write_lock = Lock()
    worker_pool = Pool(NUM_WORKERS, worker, (worker_queue, done_queue,))

    l = os.path.join(PUZZLES_FOLDER,LETTERS)
    c = os.path.join(PUZZLES_FOLDER,CHINESE)
    n = os.path.join(PUZZLES_FOLDER,NUMBERS)

    dir_list = [l,c,n]

    #clean folder
    for dir in dir_list:
        if not os.path.isdir(dir):
            os.mkdir(dir)
        else:
            if os.listdir(dir):
                shutil.rmtree(dir)
                os.mkdir(dir)
        curr_type = str(dir.split('/')[-1])
        titles = ['meat', 'plants', 'sports', 'travel']
        l = len(titles)
        random.seed()
        print(f'processing for {curr_type}')
        for i in range(number_of_files):
            r = random.randint(0, l - 1)
            title = titles[r]
            length=7
            difficulty='hard'
            isRandom=True
            worker_queue.put((generate, {
                'title':title,
                'type':curr_type,
                'length':length,
                'difficulty':difficulty,
                'dir':dir,
                'random':isRandom,
                "num_choices":10}))
        # await queues
        while not worker_queue.empty():
            pass
        counter=0
        while counter < number_of_files:
            try:
                _,c = done_queue.get()
                counter+=c
            except Exception:
                pass
        print(f'completed for {curr_type}, counter: {counter}')
        while len(os.listdir(dir)) < number_of_files:
            print(f' num files in {dir}: {len(os.listdir(dir))}')
            pass
        #merge all files to one pdf
        merge_pdf(dir)
        print(f'completed merge for {curr_type}')
    worker_queue.close()
    worker_pool.close()

def merge_pdf(dir):
    from PyPDF2 import PdfMerger, PdfReader
    mergedObject = PdfMerger()
    for file in os.listdir(dir):
        file_full_path = os.path.join(dir, file)
        mergedObject.append(PdfReader(file_full_path, 'rb'))
        os.remove(file_full_path)
    mergedObject.write(os.path.join(dir, "yy-{}.pdf".format(dir.split('/')[-1])))


if __name__ == '__main__':
    s = time.perf_counter()
    create_all(200)
    print(time.perf_counter()-s)

