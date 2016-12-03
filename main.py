import json, argparse, sys, random, os, re
from threading import Thread
from time import sleep
from collections import Iterator

# See example.json for example
class Exam(Iterator):
    def __init__(self, file_name= None, shuffle=False, shuffle_answers=False, limit=-1, test_mode=False, **kwargs):
        self.file_name = file_name
        self.exam = self.load_test()
        self.questions = self.exam['questions']
        if shuffle: random.shuffle(self.questions)
        self.shuffle_answers = shuffle_answers
        self.limit = limit
        if self.limit == -1: self.limit = len(self.questions)
        self.test_mode = test_mode
        self.correct = 0
        self.i = -1
        self.count_questions = None
        if kwargs:
            self.count_questions = kwargs['count_questions']

    def load_test(self):
        exam_data = None
        with open(self.file_name) as f:
            exam_data = f.readlines()
            exam_data = ''.join(map(str,exam_data))
        if json is not None:
            exam_data = json.loads(exam_data)

        return exam_data

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self.questions) - 1 and (self.limit <= 0 or self.i < self.limit - 1):
            self.i += 1
            return self.questions[self.i]
        else:
            raise StopIteration

def countdown():
    for i in range(60):
        sys.stdout.write("Timer: %d\r" % (i))
        sys.stdout.flush()
        sleep(1)

def main(exam):
    input = None
    current_question=0
    incorrect_questions=[]
    if not exam.count_questions:
        for i, question in enumerate(exam):
            current_question+=1
            print "" # necessary for countdown??
            print "Question(%s of %s): %s" % (current_question, exam.limit, question['question'])
            answer_keys = question['answer_bank'].keys()
            answers = map(str, question['answers'])
            required_correct_answers = len(answers)
            correct_answers = 0
            #print required_correct_answers

            # Shuffle if enabled, else sort by key
            if exam.shuffle_answers: random.shuffle(answer_keys)
            else: answer_keys = sorted(answer_keys)

            print ""
            for k in answer_keys:
                print k + ': ' + question['answer_bank'][k]

            while True:
                did_not_know_answer = False
                print ""
                input = raw_input("Your answer [" + str(required_correct_answers) + "]: ").strip().upper()
                if len(input):

                    if "P" in input:
                        print "Passed."
                        break

                    if "X" in input and not exam.test_mode:
                        print answers
                        print ""
                        print "Explanation: %s" % question['explanation']
                        break

                    # Sort then uniquefy the input
                    if sorted(input) == sorted(answers):
                        if exam.test_mode:
                            exam.correct += 1
                        else:
                            print "Correct!"
                            if len(question['explanation']):
                                print "Explanation: %s" % question['explanation']
                        break
                    else:
                        if not exam.test_mode:
                            print "Try again!"
                        else:
                            incorrect_questions.append(question)
                            break


                else:
                    print "An answer must be provided."
                    continue

            print ""
            print raw_input("Next?")
            os.system('clear')

        if exam.test_mode:
            print "Test score: %s / %s" % (exam.correct, exam.limit)
            while True:
                show_incorrect = raw_input("Do you wish to view the questions that were answered incorrectly (y/n)? ").lower()
                if show_incorrect == "n": break
                elif show_incorrect == "y":
                    for j, inc_question in enumerate(incorrect_questions):
                        print "Question %s: %s" % (j, inc_question['question'])
                        print ""
                        answer_keys = inc_question['answer_bank'].keys()
                        for k in sorted(answer_keys):
                            print k + ': ' + inc_question['answer_bank'][k]

                        print ""
                        print "Answer(s): %s" % (map(str,inc_question['answers']))
                        print ""
                        print "Explanation: %s" % inc_question['explanation']
                        raw_input("Next?")
                        os.system('clear')
                break
    else:
        os.system('clear')
        print "Total questions in exam: %s" % len(exam.questions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default=None)
    parser.add_argument('-r', '--random_questions', default=False, action='store_true')
    parser.add_argument('-s', '--shuffle_answers', default=False, action='store_true')
    parser.add_argument('-t', '--test_mode', default=False, action='store_true')
    parser.add_argument('-l', '--question_limit', type=int, default=-1)
    parser.add_argument('--count_questions', default=False, action='store_true')
    pargs = parser.parse_args()

    if pargs.file:
        os.system('clear')
        exam=Exam(file_name=pargs.file, shuffle=pargs.random_questions, shuffle_answers=pargs.shuffle_answers, limit=pargs.question_limit, test_mode=pargs.test_mode, count_questions=pargs.count_questions)
        #t1=Thread(target=countdown)
        t2=Thread(target=main, args=(exam,))
        #t1.start()
        t2.start()
    else:
        print "Exam file name must be provided."
        sys.exit(1)