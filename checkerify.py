from tkinter import *
from tkinter.tix import *
from textblob import *
import nltk
nltk.download('wordnet')
from pyttsx3 import *
import re
import random as rand

root = Tk()
root.geometry('1100x600')
root.configure(bg='#212324')
root.title('                                                                                             '
           '                                                                               Checkerify')
setFontText = ('Normal bold', 15)
setFontButton = ('Normal', 13)
imgButton = PhotoImage(file='checkButton.png')
imgResizeBtn = imgButton.subsample(2, 2)
imgAudio = PhotoImage(file='audio.png')
imgDefinition = PhotoImage(file='definitions.png')
imgDefinitions = imgDefinition.subsample(2, 2)
strLabel = StringVar()
strMsg = StringVar()

# function to correct words with TextBlob

def correctWords():
    clear()
    get_text = textWidget1.get("1.0", 'end-1c')

    #clen text from things like [14][45]
    preCleanText = re.sub(r'\[\d+\]', ' ', get_text)
    afterCleanText = "".join(preCleanText)

    def reduce_lengthening(text):
            pattern = re.compile(r"(.)\1{2,}")
            return pattern.sub(r"\1\1", text)
    checkText = TextBlob(reduce_lengthening(afterCleanText))
    correct = checkText.correct()
    textWidget2.insert(1.0, str(correct))

# function to clear words from text every press


def clear():
    textWidget2.delete(1.0, END)


# function to say what we write when press button with pyttsx3

def pre_audio():
    get_text = textWidget1.get("1.0", 'end-1c')
    engine = init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 120)
    engine.setProperty('voice', voices[1].id)
    engine.say(get_text)
    engine.runAndWait()


def after_audio():
    get_text = textWidget2.get("1.0", 'end-1c')
    engine = init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 120)
    engine.setProperty('voice', voices[1].id)
    engine.say(get_text)
    engine.runAndWait()


def number_chars1(event):
    get_text = textWidget1.get('1.0', 'end-1c')
    strLabel.set("{} / infinite".format(str(len(get_text))))


def number_chars2(event):
    get_text = textWidget1.get('1.0', 'end-1c')
    strLabel.set("{} / infinite".format(str(len(get_text))))


def hover():
    top = Toplevel()
    top.geometry('460x600')
    top.title('                                                Definition')

    button = Button(top, text='search',
                    relief=SUNKEN,
                    bd=0,
                    bg='#C55FFC',
                    fg='white',
                    font=setFontButton,
                    activebackground="#C55FFC")

    entry = Entry(top, font=("Normal bold", 15), insertbackground="#C55FFC")

    msg = Message(top, textvariable=strMsg, font=('Normal bold', 14))

    button.place(width=100, height=60, x=340, y=50)
    entry.place(width=300, height=60, x=30, y=50)
    msg.place(x=30, y=150)

    def appear():
        getTextEntry = entry.get()
        word = Word(getTextEntry)
        strMsg.set('\n'.join(word.definitions[0:4]))
    button.configure(command=lambda: appear())


def placeholder(event):
    if textWidget1.get('1.0', 'end-1c') == 'Start writing here':
        textWidget1.delete('1.0', END)

textWidget1 = Text(root, bd=2, highlightthickness=4,
                   highlightbackground="#2a2f4d",
                   highlightcolor='#2a2f4d',
                   bg='#212324',
                   fg='#d3d1cf',
                   spacing1=10,
                   font=setFontText,
                   insertbackground="yellow")
textWidget1.place(width='400', height='300', x=30, y=80)
textWidget1.insert(END, 'Start writing here')


textWidget2 = Text(root, bd=2, highlightthickness=4,
                   highlightbackground="#2a2f4d",
                   highlightcolor='#2a2f4d',
                   bg='#212324',
                   fg='#d3d1cf',
                   spacing1=10,
                   font=setFontText,
                   insertbackground="yellow")
textWidget2.place(width='400', height='300', x=670, y=80)


frame1 = Frame(root, highlightthickness=4,
               highlightbackground="#2a2f4d",
               highlightcolor='#2a2f4d',
               bg='#212324')
frame2 = Frame(root, highlightthickness=4,
               highlightbackground="#2a2f4d",
               highlightcolor='#2a2f4d',
               bg='#212324')

frame1.place(width=400, height=50, x=30, y=380)
frame2.place(width=400, height=50, x=670, y=380)

label1 = Label(root, textvariable=strLabel, bg='#2a2f4d',
               fg='#A7A5A5', font=setFontText)
label2 = Label(root, textvariable=strLabel, bg='#2a2f4d',
               fg='#A7A5A5', font=setFontText)
label3 = Label(root, text='You can access the definition of any word you want to know its meaning by searching in the dictionary➡',
               fg='#A7A5A5', bg='#212324', font=('Normal bold', 13))

label1.place(width=150, height=30, x=680, y=390)
label2.place(width=150, height=30, x=40, y=390)
label3.place(width=800, height=30, x=30, y=500)

btn1 = Button(root, image=imgResizeBtn,
              bd=0,
              bg='#212324',
              activebackground='#212324',
              cursor="hand2",
              command=lambda: correctWords()
              )

btn2 = Button(root, image=imgAudio,
              bd=0,
              bg='#212324',
              activebackground='#212324',
              cursor="hand2",
              command=lambda: root.after(1000, after_audio)
              )

btn3 = Button(root, image=imgAudio,
              bd=0,
              bg='#212324',
              activebackground='#212324',
              cursor="hand2",
              command=lambda: root.after(1000, pre_audio)
              )

btn4 = Button(root, image=imgDefinitions,
              bd=0,
              bg='#212324',
              cursor="hand2",
              activebackground='#212324',
              command=lambda: hover()
              )


btn1.place(width=210, height=110, x=450, y=200)
btn2.place(width=60, height=30, x=1000, y=390)
btn3.place(width=60, height=30, x=360, y=390)
btn4.place(width=200, height=170, x=880, y=470)

textWidget1.bind('<Button>', placeholder)
textWidget1.bind('<KeyRelease>', number_chars1)
textWidget2.bind('<KeyRelease>', number_chars2)

root.mainloop()
