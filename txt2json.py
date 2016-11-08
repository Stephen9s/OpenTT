import json
import argparse
import sys
import copy
import re
import collections

debug = False

# Will convert actualtest.com PDFs after using pdf2text.py provided PDFMiner
def txt2json(file_name, test_name):
    global debug
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
                    if 'DRAG' in words or 'CORRECT' in words or'HOTSPOT' in words: continue
                    if debug: print 'Question: ' + words[2]
                    question = ''
                    while True:
                        line = f.readline().strip()
                        if not len(question) and not len(line):
                            continue
                        elif len(line) and ('actualtest' not in line and not re.match("^\d+$", line) and 'Exam' not in line):
                            question += " " + line
                        elif not len(line) and len(question):
                            break
                    if debug: print question
                    current_question['question'] = question.strip()
                    in_question = True

                if in_question:
                    accepted_answers = ['A','B','C','D','E','F','G','H']
                    if any(x in line for x in accepted_answers) and len(line) == 2:
                        answer_key = re.sub('[^A-Z]', '', line)
                        answer = ""
                        while True:
                            line = f.readline().strip()
                            if 'Answer:' in line: break
                            if not len(answer) and not len(line):
                                continue
                            elif len(line) and ('actualtest' not in line and not re.match("^\d+$", line) and 'Exam' not in line):
                                answer += line
                            elif not len(line) and len(answer):
                                break
                        current_question['answer_bank'][answer_key] = answer.strip()

                    if 'Answer' in line and not in_explanation:
                        answers = line.split(' ')
                        answers.pop(0)
                        if answers[0].find(','):
                            answers = answers[0].split(',')
                        if debug: print 'Answer: ' + str(answers)
                        current_question['answers'] = answers

                    if 'Explanation' in line:
                        explanation = ""
                        if debug: print 'Explanation: %s' % line
                        while True:
                            unstripped_line=f.readline()
                            line=unstripped_line.strip()
                            if 'QUESTION' in line or not len(unstripped_line): break
                            if len(line) and ('actualtest' not in line and not re.match("^\d+$", line) and 'Exam' not in line):
                                explanation += " " + line

                        current_question['explanation'] = explanation.strip()
                        in_explanation = False
                        in_question = False
                        push_results = True

                    if push_results:
                        #print str(current_question)
                        test['questions'].append(current_question)
                        current_question = copy.deepcopy(question_obj)
                        push_results = False

    print json.dumps(test, indent=4, separators=(',',':',))




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    parser.add_argument('-n', '--testname')
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    args=parser.parse_args()
    debug=args.debug

    if args.file and args.testname:
        txt2json(args.file, args.testname)
    else:
        print "Filename must be provided."
        sys.exit(1)