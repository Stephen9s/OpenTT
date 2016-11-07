import json
import argparse
import sys
import copy
import re
import collections

# Will convert actualtest.com PDFs after using pdf2text.py provided PDFMiner
def txt2json(file_name, test_name):
    test = {}
    test['name'] = test_name
    test['questions'] = []
    in_question = False
    in_explanation = False
    push_results = False
    question_obj = {'question': '', 'answers': [], 'explanation': '', 'answer_bank': collections.OrderedDict()}
    current_question = question_obj.copy()
    with open(file_name, 'r') as f:
        while True:
            line = f.readline()
            if not line: break

            line = line.strip()
            if not len(line): continue
            else:
                if 'QUESTION' in line:
                    in_explanation = False
                    words = line.split(' ')
                    if 'DRAG' in words or 'CORRECT' in words: continue
                    #print 'Question: ' + words[2]
                    question = ''
                    while True:
                        line = f.readline().strip()
                        if not len(question) and not len(line):
                            continue
                        elif len(line) and 'actualtest' not in line:
                            question += line
                        elif not len(line) and len(question):
                            break
                    #print question
                    current_question['question'] = question
                    in_question = True

                if in_question:
                    accepted_answers = ['A','B','C','D','E','F','G','H']
                    if any(x in line for x in accepted_answers) and len(line) == 2:
                        answer_key = re.sub('[^A-Z]', '', line)
                        answer = ""
                        while True:
                            line = f.readline().strip()
                            if not len(answer) and not len(line):
                                continue
                            elif len(line) and ('actualtest' not in line and not re.match("^\d", line) and '(ISC)2 CSSLP' not in line):
                                answer += line
                            elif not len(line) and len(answer):
                                break
                        current_question['answer_bank'][answer_key] = answer

                    if 'Answer' in line and not in_explanation:
                        answers = line.split(' ')
                        answers.pop(0)
                        if answers[0].find(','):
                            answers = answers[0].split(',')
                        #print 'Answer: ' + str(answers)
                        current_question['answers'] = answers

                    if 'Explanation' in line:
                        line = f.readline().strip()
                        explanation = ''
                        #print 'Explanation: %s' % line
                        while True:
                            line = f.readline().strip()
                            if len(line):
                                explanation += line
                                #print line
                            else: break
                        current_question['explanation'] = explanation
                        in_explanation = False
                        in_question = False
                        push_results = True

                    if push_results:
                        #print str(current_question)
                        test['questions'].append(current_question)
                        current_question = copy.deepcopy(question_obj)
                        push_results = False

    print json.dumps(test, indent=2, separators=(',',':',))




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    parser.add_argument('-n', '--testname')
    args = parser.parse_args()

    if args.file and args.testname:
        txt2json(args.file, args.testname)
    else:
        print "Filename must be provided."
        sys.exit(1)