import os
import gc
import psutil
import codecs
punction=[";",":","!","?",u"\u2026"]
end_punc = ['.','?','!']

f = open('test.txt','r')
data = f.readlines()
f.close()
count = 0

mistakes = ''
sentences = 0

for i in range(0,len(data)):
    line = data[i].decode('utf-8')
    if line == '\n':
        continue
    arr = line.split(' ')
    word = arr[0]
    p = arr[1]
    
    if any(punc in word for punc in punction) and (len(word) < 1 or len(p) < 1) :
        count += 1
        mistakes += str(i+1)
        mistakes += '\n'
        mistakes += line
        mistakes += '\n'

    if any(punc in word for punc in end_punc):
        sentences += 1

f = codecs.open('bug','w',encoding = 'utf-8')
f.write(str(sentences))
f.write('\n#########################\n')
f.write(mistakes)
f.close()

proc = psutil.Process(os.getpid())
gc.collect()
mem0 = proc.get_memory_info().rss
