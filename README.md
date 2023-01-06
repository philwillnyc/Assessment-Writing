# Assessment-Writing

The goal of this project was to automate and randomize exam/assessment content for my math classes. The basic idea is to take a latex template for an exam or quiz or whatever, along bits of python code, and randomize the numbers/expressions/etc in the exam content, as well as to randomize the content itself (for example selecting a random question from a list of stored questions). Content is stored as text files consisting of latex code for questions, followed by python code, with a latex style command \py{<content>} to place values of variables computed in the python code into the latex code. The main program takes as input a "test bank" consisting of questions, and outputs a latex file which is then rendered by pdflatex and a pdf is generated. In this way I was able to, for example, generate multiple versions of quizzes and exams. 

I went into this project not knowing much about python and I did everything basically from scratch. The code is not very well documented and has bad design aspects to it. I learned a lot in the process, and the final product was very useful to me for several semesters. It remained a work in progress but is essentially unfinisehd: eventually I discovered pythontex and sagetex which give most of the functionality of what I had created in a more user-friendly format, and so I wrote scripts to transfer the content I'd already created into a sagetex format, which I current use. If I were to redo this, it might be a good idea to use a jinja template--this would provide question level randomization that can't, as far as I can tell, easily be done using sagetex. 

The actual student assessment content itself, which is probably what took the most work, is omitted from the public repository as this content is still in use!