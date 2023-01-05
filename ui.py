from assessment_writing import *
from tkinter import *
from tkinter import filedialog

assessment = Assessment(os.path.join(os.path.dirname(__file__), 'support','preludes','default'), 
'',
1,
False,
'Untitled Assessment',
'',
'')
root = Tk()
root.title('Assessment Writer')
root.geometry('640x480')
root.resizable(True,True)
root.mainloop()


#adding questions:
def add_questions(assessment):
    bank = filedialog.askopenfilename()
    assessment.list_of_questions.append(listify_bank(bank))




#inputs: collection of banks, header, instructions and prelude 