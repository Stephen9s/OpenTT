import json, argparse, sys, random, os, re
from collections import Iterator

# See example.json for example
class Exam(Iterator):
    def __init__(self, file_name= None, shuffle=False, shuffle_answers=False, limit=-1):
        self.file_name = file_name
        self.exam = self.load_test()
        self.questions = self.exam['questions']

        if shuffle:
            random.shuffle(self.questions)

        self.shuffle_answers = shuffle_answers
        self.limit = limit
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
    for question in exam:
        print "Question: " + question['question']
        answer_keys = question['answer_bank'].keys()
        answers = question['answers']
        required_correct_answers = len(answers)
        correct_answers = 0

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

                for answer in input:
                    answer = answer.upper()
                    if answer == "X":
                        print answers
                        print ""
                        print "Explanation: %s" % question['explanation']
                        did_not_know_answer = True
                        break
                    if re.match("[A-Z]", answer):
                        if answer in answers:
                            correct_answers += 1

                if did_not_know_answer:
                    break

                if correct_answers == required_correct_answers:
                    print "Correct!"
                    break
                elif correct_answers == 0:
                    print "Try again!"
                else:
                    print "There are multiple answers. Try again."

            else:
                print "An answer must be provided."
                continue

        print ""
        print raw_input("Next?")
        os.system('clear')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default=None)
    parser.add_argument('-r', '--random_questions', default=False, action='store_true')
    parser.add_argument('-s', '--shuffle_answers', default=False, action='store_true')
    parser.add_argument('-l', '--question_limit', type=int, default=0)
    args = parser.parse_args()

    if args.file:
        main(Exam(file_name=args.file, shuffle=args.random_questions, shuffle_answers=args.shuffle_answers, limit=args.question_limit))
    else:
        print "Exam file name must be provided."
        sys.exit(1)