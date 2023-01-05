import assessment_writing as aw
import os
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pylatex import Document, Package
from pylatex.utils import italic, NoEscape
from pylatex.base_classes import Options, Command

#input is a bank file, output is latex for a specified question in the bank
def make_question(bank, number = -1):
    try:
        question_list = aw.listify_bank(bank)
        return question_list[number].tex_question(stand_alone = True)
    except:
        return 'Error in question code.'
    

def print_question_latex(bank, number = -1):
    question_text = make_question(bank,number = number)
    print(question_text)
    df=pd.DataFrame([question_text]) 
    df.to_clipboard(index=False,header=False) #copies the latex output to the clipboard
    return question_text

#Makes the question into a pdf and opens it in the web browser. 
def pdf_question(bank, save_path, number = -1):
    question_text = print_question_latex(bank, number = number)
    doc = Document('question_preview', 
                    documentclass = Command('documentclass', 
                                            options = Options('12pt', 'preview'), 
                                            arguments = 'standalone',
                                            ),
                    )
    doc.append(NoEscape(question_text))
    doc.packages.append(Package('amsmath'))
    cwd = os.getcwd() #save cwd
    os.chdir(save_path)
    try:
        doc.generate_pdf()
        os.startfile('question_preview.pdf')
    #if the standalone class doesn't compile, we try the exam class. 
    except:
        print('Trying exam class...')
        doc = Document('question_preview', 
                    documentclass = Command('documentclass', 
                                            options = Options('12pt', 'preview', 'answers'), 
                                            arguments = 'exam',
                                            ),
                    )
        doc.append(NoEscape(question_text))
        doc.packages.append(Package('amsmath'))
        doc.packages.append(Package('enumitem'))
        doc.packages.append(Package('dashrule'))
        try:
            doc.generate_pdf()
            os.startfile('question_preview.pdf')
        except: 
            print('Latex error.')
    
    os.chdir(cwd) #restore cwd
    

if __name__ == '__main__':
    Tk().withdraw()
    #auxi_file should begin with a path to the bank as the first line; the second line is the question number. It should end with a new line. 
    with open('question_editor.auxi','r') as auxi_file:
        settings = auxi_file.readlines()
        try:
            bank = settings[0][:-1] #handles the newline
            os.chdir(os.path.dirname(bank))
        except:
            bank = askopenfilename()
            settings[0] = bank + '\n'
            os.chdir(os.path.dirname(bank))
        finally: 
            number = int(settings[1][:-1])
            pdf_question(bank, 
                        save_path = os.path.join(os.path.dirname(__file__), 'support', 'generated'), 
                        number = number)
            os.chdir(os.path.dirname(__file__))

    with open('question_editor.auxi','w') as auxi_file:
        auxi_file.writelines(settings)