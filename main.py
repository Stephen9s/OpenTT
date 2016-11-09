import json, argparse, sys, random, os, re
from collections import Iterator

# See example.json for example
class Exam(Iterator):
    def __init__(self, file_name= None, shuffle=False, shuffle_answers=False, limit=-1, test_mode=False):
        self.file_name = file_name
        self.exam = self.load_test()
        self.questions = self.exam['questions']

        if shuffle:
            random.shuffle(self.questions)

        self.shuffle_answers = shuffle_answers
        self.limit = limit
        if self.limit == -1: self.limit = len(self.questions)
        self.test_mode = test_mode
        self.correct = 0
        self.i = -1

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

def main(exam):
    input = None
    current_question=0
    for question in exam:
        current_question+=1
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
            input = raw_input("Your answer [" + str(required_correct_answers) + "]: ")
            if len(input):
                correct_answers = 0
                for answer in input:
                    answer = answer.upper().strip()
                    if answer == "P":
                        print "Passed."
                        did_not_know_answer = True
                        break
                    if answer == "X" and not exam.test_mode:
                        print answers
                        print ""
                        print "Explanation: %s" % question['explanation']
                        did_not_know_answer = True
                        break
                    if re.match("[A-Z]", answer):
                        #print answers
                        if answer in answers:
                            correct_answers += 1

                #print correct_answers

                if did_not_know_answer:
                    break

                if correct_answers == required_correct_answers:
                    if exam.test_mode:
                        exam.correct += 1
                    else:
                        print "Correct!"
                        if len(question['explanation']):
                            print "Explanation: %s" % question['explanation']

                    break
                elif correct_answers == 0 and not exam.test_mode:
                    print "Try again!"
                elif correct_answers == 0 and exam.test_mode:
                    break


            else:
                print "An answer must be provided."
                continue

        print ""
        print raw_input("Next?")
        os.system('clear')

    if exam.test_mode:
        print "Test score: %s / %s" % (exam.correct, exam.limit)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default=None)
    parser.add_argument('-r', '--random_questions', default=False, action='store_true')
    parser.add_argument('-s', '--shuffle_answers', default=False, action='store_true')
    parser.add_argument('-t', '--test_mode', default=False, action='store_true')
    parser.add_argument('-l', '--question_limit', type=int, default=-1)
    args = parser.parse_args()

    if args.file:
        os.system('clear')
        main(Exam(file_name=args.file, shuffle=args.random_questions, shuffle_answers=args.shuffle_answers, limit=args.question_limit, test_mode=args.test_mode))
    else:
        print "Exam file name must be provided."
        sys.exit(1)