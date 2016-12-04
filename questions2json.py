import json
import argparse
import sys
import copy
import re
import collections

alphanumeric = re.compile(r'[^\da-zA-z]+')
debug = False

def get_data(line):
    global alphanumeric
    data = map(str.strip, line.split(' '))  # strip each element in list after splitting
    data = filter(bool, data)  # Removes empty lines from list
    data[0] = alphanumeric.sub('', data[0])  # remove non-alphanumeric from identifier

    return data
# Will convert actualtest.com PDFs after using pdf2text.py provided PDFMiner
def questions2json(**kwargs):
    global debug
    test = {}
    test['name'] = kwargs['test_name']
    test['questions'] = [] # question number as key
    question_obj = {'question': '', 'answers': [], 'explanation': '', 'answer_bank': collections.OrderedDict()}
    current_question= question_obj.copy()
    in_question_bank=False
    in_answer_bank=False
    line=''
    with open(kwargs['file_name'], 'r') as f:
        while True:
            line=f.readline().strip()
            if not line: break

            if line.startswith(';questions'):
                in_question_bank = True
                continue # pass on, next line will be data we need
            if line.startswith(';answers'):
                in_question_bank=False
                in_answer_bank=True
                continue # pass on, next line will be data we need

            if in_question_bank:
                data=get_data(line)

                # If it's a digit, then we are in a question
                if data[0].isdigit():
                    if debug: print data[0] # question #
                    if debug: print data[1:] # the question itself
                    current_question=copy.deepcopy(question_obj) # deep copy the question_obj to replace old question\
                    if kwargs['chapter']: current_question['chapter']=kwargs['chapter']
                    current_question['question']=' '.join(data[1:])
                    test['questions'].append(current_question)
                    continue # skip further processing
                else:
                    if debug: print data[0] # the answer
                    if debug: print data[1:]  # the answer itself

                    test['questions'][-1]['answer_bank'][data[0]]=' '.join(data[1:])
                    if debug: print test['questions'][-1]['answer_bank']
                    continue # skip further processing
            if in_answer_bank:
                data = get_data(line) # splits, removes alphanumeric from data[0] and all empty elements
                if data[0].isdigit(): # identifies the index of question we should modify
                    data[1]=alphanumeric.sub('', data[1])
                    idx=int(data[0])-1
                    test['questions'][idx]['answers']=list(data[1]) #splits multiple answers into a list
                    test['questions'][idx]['explanation']=' '.join(data[2:])
                pass


    print json.dumps(test, indent=4, separators=(',',':',))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    parser.add_argument('-t', '--testname')
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    parser.add_argument('-c', '--chapter')
    args=parser.parse_args()
    debug=args.debug

    if args.file and args.testname:
        questions2json(file_name=args.file, test_name=args.testname, chapter=args.chapter)
    else:
        print "Filename must be provided."
        sys.exit(1)