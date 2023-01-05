import os
import sys
file = os.path.realpath(__file__)
path = os.path.dirname(file)
while ('assessment_writer' in os.listdir(path)) == False and len(path)>3:
    path = os.path.dirname(path)
path = os.path.join(path, 'assessment_writer')
sys.path.insert(0, path)
import assessment_writing
question_banks = []
for name in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    print(name)
    print(os.path.splitext(name)[1])
    if os.path.splitext(name)[1] == '.txt':
        question_banks.append(name)
print(question_banks)
if len(question_banks) > 0:
    assessment_writing.write(question_banks, name = False, questions_per_page = 100000)
