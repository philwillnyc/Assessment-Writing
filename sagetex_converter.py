import os
import shutil
import subprocess
import random
import numpy
import numpy as np
import array_builder as AB
import row_reduction as RR
from numpy.linalg import matrix_power
from numpy import matrix
from array_builder import tex_matrix
import webbrowser
from random import randint
from random import choice
from random import choices
from sympy import latex

#defining the replacement function which will be used to insert python output into tex.
def indices(open,string):
    i = string.find(open)
    k = len(open)
    n = 0
    L = []
    s = string
    while i != -1:
        i = s.find(open)
        if i != -1:
            n+=i+k
            L.append(n-k)
        s = string[n:]
    return L

#extract the string between the first instance of the opening characters and the close characters;
# return a list of the inside and also with the opening and closing characters included.
def read(string, open, close):
    o = string.find(open)+len(open)
    c = string[o:].find(close)+o
    return [string[o:c], string[o-len(open):c+len(close)]]

#make a list of outputs
def outputs(string, open, close, variables):
    L = []
    for i in indices(open,string):
        L.append(eval(read(string[i:], open, close)[0], globals(), variables))
    return L

def replacement(string, open, close, variables):
    new_string = string
    ops = outputs(string, open, close, variables)
    if ops == []:
        return new_string
    for o in ops:
        r = read(new_string, open, close)
        new_string = new_string.replace(r[1], str(o),1)
    return new_string

#An assessment object contains a list of question objects and a title.


class Assessment():

    def __init__(self, prelude, title, questions_per_page, grade_table, name, instructions, header):
        self.list_of_questions = []
        self.prelude = prelude
        self.title = title
        self.questions_per_page = questions_per_page
        self.grade_table = grade_table
        self.name = name #set to false to omit the name in the header
        self.instructions = instructions
        self.header = header
        self.points_list = None #not yet implemented 

    #The following functions build a latex document out of an assessment object:
    #Creates a text file with a latex prelude using the exam format and various packages:        
    def tex_prelude(self):
        file = open(self.title + "TEMP" + ".txt", "w+")
        prelude = open(self.prelude, 'r')
        file.write(prelude.read() + "\n")
        file.close()
        prelude.close()
        
    #begins the document section of the tex document:
    def tex_begin(self, solutions = False):
        file = open(self.title + "TEMP" + ".txt", "a")
        file.write("\\begin{document}" + "\n")
        if solutions == True:
            file.write("\\printanswers"+"\n") 
        file.close()

    #appends to the file created by prelude tex code for a header and instructions for the assessment:
    def tex_header(self):
        file = open(self.title + "TEMP"+".txt", "a")
        file.write("\\makebox[\\textwidth]{" + self.header + "} \n")
        if self.name == True:
            file.write("\\begin{center}\n\\fbox{\\fbox{\\parbox{5.5in}{\\centering \n" + self.instructions +
                   "}}} \n\\end{center} \n \n\\vspace{5mm} \n \n\\makebox[\\textwidth]{Name:\\enspace\\hrulefill} \n \n\\vspace{5mm}\n")
        else:
            file.write("\\begin{center}\n\\fbox{\\fbox{\\parbox{5.5in}{\\centering \n" + self.instructions +
                   "}}} \n\\end{center} \n \n\\vspace{5mm} \n")
        file.close()

    #creates a {questions} environmment in latex and adds latexed versions of questions (with variables computed):
    def tex_question_list(self):
        file = open(self.title + "TEMP" + ".txt", "a")
        file.write("\n"+"\\begin{questions}"+"\n")
        i=1
        for question in self.list_of_questions:
            file.write(question.tex_question())
            if i % self.questions_per_page == 0:
                file.write("\\clearpage" + "\n")
            i+=1
        file.write("\n"+"\\end{questions}"+"\n")
        file.close()
        
    #finishes the latex document.
    def tex_finish(self):
        file = open(self.title + "TEMP"+ ".txt", "a")
        if self.grade_table == True:
            file.write("\\begin{center}\n\\gradetable[h][questions]\n\\end{center}")
        file.write("\n"+"\\end{document}")
        file.close()
        
    #Creates the latex source for an assessment object:
    def tex_assessment(self):
        self.tex_prelude()
        self.tex_begin()
        self.tex_header()
        self.tex_question_list()
        self.tex_finish()
                    
    #Writes a texable latex file from an assessment object and extra info (header, instructions):
            
    def write_assessment(self): 
        self.tex_assessment()
        if os.path.exists(self.title + ".tex"):
            os.remove(self.title + ".tex")
            os.rename(self.title + "TEMP" + ".txt" , self.title + ".tex")
        else:
            os.rename(self.title + "TEMP" + ".txt" , self.title + ".tex")
        os.system('pdflatex ' + '"' + self.title + '.tex' + '"') #these commands(at least the second) are windows only.
        #os.startfile(self.title + ".pdf", 'open')
        webbrowser.open_new(self.title + '.pdf')
    #given an assessment object, this reduces the question list to a random subset; the order is maintained.
        
    def questions_subset(self, number): 
        if number < len(self.list_of_questions):
            self.list_of_questions = [self.list_of_questions[i] for i in sorted(random.sample(range(len(self.list_of_questions)), number))]
    
#A question object contains a question body of latex code, a body of python code, 
# and a list of variables that can be used for formatting.

class Question(): 
    def __init__(self):
        self.body = ""
        self.variables = None
        self.variables_code = ""

    def print_question(self):
        print(self.body %self.variables)

    #This will take a question, execute it's python code (which can set self.variables and also set variables for replacement),
    #and replace \py{stuff} with the output of 'stuff.'
    def tex_question(self, points = '', stand_alone = False): #stand_alone = True for question_editor.py
        Int = random.randint
        exec(self.variables_code)
        if self.variables != None:
            text_body = self.body %self.variables
        else:
            text_body = self.body
        text_body = replacement(text_body, r'\py{', '}', locals())
        if stand_alone == False:
            return "\n" + "\\question " + points + text_body + "\n" + "\\vspace{\\stretch{1}}" + "\n" + "\n"
        return text_body

        #takes a question and adds it to a csv file:
    def csv_question(self, csv_file):
        pass

    #Makes a list of question objects from a given bank.
def listify_bank(bank):
    L = []
    if isinstance(bank, str):  #can use either the file path or the open file object
        file = open(bank, 'r')
    else:
        file = bank
    ql = file.readlines()
    b_indices = [i for i, x in enumerate(ql) if x[0] == "&"] #extracts the indices of marker lines for when each question body begins
    v_indices = [i for i, x in enumerate(ql) if x[0] == "@"] #extracts the indices of marker lines for when each question variables begin
    i=0
    while i < len(b_indices):
        L.append(Question()) #creates a new question on the list
        for line in ql[b_indices[i]+1:v_indices[i]]: #puts the body of the question in the body variable
            L[-1].body += line
                
        if i + 1 < len(b_indices):
            for line in ql[v_indices[i]+1:b_indices[i+1]]: 
                L[-1].variables_code += line 
        else:
            for line in ql[v_indices[i]+1:len(ql)]:
                L[-1].variables_code += line
                    #puts the variable code in the variable code variable
        i+=1
    file.close
    return L
def py_to_sage(question):
    """replace all instances of \py with \sage"""
    question.body = question.body.replace(r'\py{', r'\sage{')

def variables_code_fix(question):
    """change self.variables into a tuple with an unlikely name"""
    question.variables_code = question.variables_code.replace('self.variables','vvv')

def old_string_replace(question):
    """replaces instances of old string formatting with appropriate references to the tuple defined in
    variables_code_fix"""
    flag = True
    i = 0
    while flag is True:
        old_body = question.body
        question.body = question.body.replace(r'%s',r'\sage{vvv['+str(i)+']}',1)
        if question.body == old_body:
            flag = False
        i += 1

def sageify_question(question, command = r'\question'):
    """Converts a question object into a sagetex question"""
    variables_code_fix(question)
    old_string_replace(question)
    py_to_sage(question)
    tex = r'\begin{sagesilent}'+ '\n' + question.variables_code + r'\end{sagesilent}'
    tex += '\n'+ command + '\n' + question.body
    return tex


def sageify_bank(bank, command = r'\question'):
    """Converts a question bank into sagetex format. Input question text file name. """
    L = listify_bank(bank)
    filename, file_extension = os.path.splitext(bank)
    filename = filename + '.tex'
    with open(filename, 'x') as output:
        for question in L:
            tex = sageify_question(question, command=command)
            output.write(tex+ '\n\n')

#The main function for writing assessments.   
def write(question_banks, 
          #prelude = r'C:\Users\philw\Dropbox\Teaching\Assessment Writing\support\preludes\default_prelude',
          prelude = os.path.join(os.path.dirname(__file__), 'support', 'preludes','default'),
          subsets = None, 
          repeats = None, 
          points_list = None,
          title = "questions",
          questions_per_page = 1, 
          grade_table = False,
          name = True, 
          instructions = "", 
          header = "", 
          scramble_each_bank = False, 
          scramble_whole_list = False,
          ):
    
    if repeats == None:
        repeats = [1 for bank in question_banks]
    elif not(len(repeats)==len(question_banks)):
        raise Exception('Subsets list is the wrong size.')
    if subsets == None:
        subsets = [len(listify_bank(bank)) for bank in question_banks]
    elif not(len(repeats)==len(question_banks)):
        raise Exception('Repeats list is the wrong size.')
    
    A = Assessment(prelude, title, questions_per_page, grade_table, name, instructions, header)
    A.questions_per_page = questions_per_page
    A.grade_table = grade_table
    A.name = name
    A.instructions = instructions
    A.header = header
    A.points_list = points_list

    for i in range(0,len(question_banks)):
        L = listify_bank(question_banks[i])
        if scramble_each_bank == True:
            random.shuffle(L)
        for j in range(0, repeats[i]):
            B = [L[j] for j in sorted(random.sample(range(len(L)), subsets[i]))]
            A.list_of_questions = A.list_of_questions + B
    if scramble_whole_list == True:
        random.shuffle(A.list_of_questions)
    A.write_assessment()
    
#legacy functions:

def write_exam(textfile, title, header, instructions, number_of_questions, grade_table, questions_per_page):
    write([textfile], subsets = [number_of_questions],
          title = title, header = header, instructions = instructions, grade_table = grade_table,
          questions_per_page = questions_per_page)

def write_worksheet(question_banks, title, header, instructions, number_of_each, questions_per_page,
                    scramble_each_bank, scramble_whole_list):
    write(question_banks, title = title, header = header,
          instructions = instructions, repeats = [number_of_each for i in range(0, len(question_banks))],
          scramble_each_bank = scramble_each_bank, scramble_whole_list = scramble_whole_list,
          questions_per_page = questions_per_page)


if __name__ == '__main__':
    try:
        os.mkdir('tex_files')
    except:
        pass
    for filename in os.listdir():
        if os.path.splitext(filename)[1] == '.txt':
            new_name = os.path.splitext(filename)[0] + '.tex'
            sageify_bank(filename)
            shutil.move(new_name, 'tex_files')

