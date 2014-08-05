def translate(punctuation):
    i = 0
    if punctuation == 'PERIOD':
        i = 0
    elif punctuation == 'COMMA':
        i = 1
    elif punctuation == 'SEMICOLON':
        i = 2
    elif punctuation == 'COLON':
        i = 3
    elif punctuation == 'EXCLAM':
        i = 4
    elif punctuation == 'QMARK':
        i = 5
    else:
        i = 6
    return i


f = open('result','r')
data = f.read()
f.close

l = data.split('\n')
l = filter(None,l)
#punction=[".",",",";",":","!","?",u"\u2026"]
punction = ['PERIOD', 'COMMA', 'SEMICOLON', 'COLON', 'EXCLAM', 'QMARK', 'ELLIPSIS']
num_class = len(punction)
cfm = [ [0 for i in range(7)] for j in range(num_class)]
correct = 0.0
#create confusion matrix
for s in l:
    s_temp = s.split('\t')
    true_idx = translate(s_temp[1])
    predict_idx = translate(s_temp[2])
    cfm[true_idx][predict_idx] += 1
    #accuracy:
    if true_idx == predict_idx:
        correct+= 1

recall = []
precision = []
f_1 = []


for i in range(num_class):
    tpI = float(cfm[i][i]) + 1
    denum_precision = sum(cfm[i])
    denum_recall = i
    for j in range(num_class):
        denum_recall += cfm[j][i]

    r = float(tpI / denum_recall)
    p = float(tpI / denum_precision)
    recall.append(r)
    precision.append(p)

    f_score = 2*(r*p)/(r + p)
    
    f_1.append(f_score)

avr_p= sum(precision)/len(precision)
avr_r = sum(recall)/len(recall)
avr_f1 = 2* (avr_p * avr_r) / (avr_p + avr_r)

average = 'AVERAGE:\n\t Recall: ' + str(100*avr_r) + ' %\n\t Precision: ' + str(100*avr_p) + ' %\n\t F_1 score: '  + str(100*avr_f1) + ' %\n'   


accuracy = correct / len(l)
line_break = '#'*50 + '\n'
f = open('statistic','wb')
f.write('OVERALL ACCURACY: ' +str(100*accuracy) + ' %\n')
f.write(line_break)
for i in range(num_class):
    f.write(punction[i] + ':\n')
    f.write('\t Recall: ' + str(100*recall[i]) + ' %\n')
    f.write('\t Precision: ' + str(100*precision[i]) + ' %\n')
    f.write('\t F_1 score: ' + str(100*f_1[i]) + ' %\n')
    f.write(line_break)

f.write(average)    
f.close()
