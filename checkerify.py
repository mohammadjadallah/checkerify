from tkinter import *
from tkinter.messagebox import showwarning
# from tkinter.tix import *
from textblob import *
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from pyttsx3 import *
import re
import random as rand
# threading
from threading import Thread

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
strLabel_wedgit2 = StringVar()
strMsg = StringVar()


# function to correct words with TextBlob

def correctWords():
    clear()
    get_text = textWidget1.get("1.0", 'end-1c')

    # clean text from things like [14][45]
    preCleanText = re.sub(r'\[\d+\]', ' ', get_text)
    afterCleanText = "".join(preCleanText)

    def reduce_lengthening(text):
        pattern = re.compile(r"(.)\1{2,}")
        return pattern.sub(r"\1\1", text)

    checkText = TextBlob(reduce_lengthening(afterCleanText))
    correct = checkText.correct()
    textWidget2.insert(1.0, str(correct))
    # Get the number of characters from the text box 2, this will help to see the difference between the text box 1 and the text box 2
    number_chars = textWidget2.get('1.0', 'end-1c')
    label2['text'] = "{} / infinite".format(str(len(number_chars)))

# function to clear words from text every press


def clear():
    textWidget2.delete(1.0, END)


# function to say what we write when press button with pyttsx3

# Initialize engine
engine = init()
# Get all voices
voices = engine.getProperty('voices')
# set the rate of the voice
engine.setProperty('rate', 120)
# set the voice
engine.setProperty('voice', voices[1].id)


# function for the first textbox
def pre_audio():
    get_text = textWidget1.get("1.0", 'end-1c')
    engine.say(get_text)
    engine.runAndWait()


# function for the second textbox
def after_audio():
    get_text = textWidget2.get("1.0", 'end-1c')
    engine.say(get_text)
    engine.runAndWait()


def number_chars1(event):
    get_text = textWidget1.get('1.0', 'end-1c')
    strLabel.set("{} / infinite".format(str(len(get_text))))


def number_chars2(event):
    get_text = textWidget2.get('1.0', 'end-1c')
    label2['text'] = "{} / infinite".format(str(len(get_text)))

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
                    activebackground="#C55FFC", cursor='hand2')

    entry = Entry(top, font=("Normal bold", 15), insertbackground="#C55FFC")

    msg = Message(top, textvariable=strMsg, font=('Normal bold', 14))

    button.place(width=100, height=60, x=340, y=50)
    entry.place(width=300, height=60, x=30, y=50)
    msg.place(x=30, y=150)

    def appear():
        # count = 1
        # if count == 1:
        #     wait = Label(top, text="I am going to get the definition...",
        #                 font=('Normal bold', 14))
        #     wait.place(x=20, y=150)
        #     count = 0

        getTextEntry = entry.get()
        word = Word(getTextEntry)
        defintions = word.definitions
        try:
            if len(defintions) >= 4:
                defintions = word.definitions[0:4]
                strMsg.set(f'''1. {defintions[0]}
        
2. {defintions[1]}

3. {defintions[2]}

4. {defintions[3]}''')
            elif len(defintions) == 3:
                defintions = word.definitions
                strMsg.set(f'''1. {defintions[0]}
            
2. {defintions[1]}

3. {defintions[2]}''')
            elif len(defintions) == 2:
                defintions = word.definitions
                strMsg.set(f'''1. {defintions[0]}
    
2. {defintions[1]}
''')
            else:
                defintions = word.definitions
                strMsg.set(f'''1. {defintions[0]}''')
        except IndexError:
            showwarning('Warning', "Sorry can't find a definition, you should put just one word")

    # Here, the term protocol refers to the interaction between the application and the window manager.
    # The most commonly used protocol is called WM_DELETE_WINDOW,
    # and is used to define what happens when the user explicitly closes a window using the window manager.
    def on_closing():
        # To remove the text on the top window if user close it
        strMsg.set('')
        top.destroy()

    top.protocol("WM_DELETE_WINDOW", on_closing)

    button.configure(command=lambda: Thread(target=appear).start())


def placeholder(event):
    if textWidget1.get('1.0', 'end-1c') == 'Start writing here':
        textWidget1.delete('1.0', END)

# Text box 1
textWidget1 = Text(root, bd=2, highlightthickness=4,
                   highlightbackground="#2a2f4d",
                   highlightcolor='#2a2f4d',
                   bg='#212324',
                   fg='#d3d1cf',
                   spacing1=10,
                   font=setFontText,
                   insertbackground="yellow",
                   undo=True, wrap='word')
textWidget1.place(width='400', height='300', x=30, y=80)
# Insert the starting text as a placeholder in the text box 1
textWidget1.insert(END, 'Start writing here')

# Text box 2
textWidget2 = Text(root, bd=2, highlightthickness=4,
                   highlightbackground="#2a2f4d",
                   highlightcolor='#2a2f4d',
                   bg='#212324',
                   fg='#d3d1cf',
                   spacing1=10,
                   font=setFontText,
                   insertbackground="yellow",
                   undo=True, wrap='word')
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
label2 = Label(root, bg='#2a2f4d',
               fg='#A7A5A5', font=setFontText)
label3 = Label(root,
               text='You can access the definition of any word you want to know its meaning by searching in the dictionary ⏩',
               fg='#A7A5A5', bg='#212324', font=('Normal bold', 13))

label1.place(width=150, height=30, x=40, y=390)
label2.place(width=150, height=30, x=680, y=390)
label3.place(width=800, height=30, x=30, y=500)

btn1 = Button(root, image=imgResizeBtn,
              bd=0,
              bg='#212324',
              activebackground='#212324',
              cursor="hand2",
              command=lambda: Thread(target=correctWords).start()
              )

btn2 = Button(root, image=imgAudio,
              bd=0,
              bg='#212324',
              activebackground='#212324',
              cursor="hand2",
              command=lambda: root.after(1, Thread(target=after_audio).start())
              )

btn3 = Button(root, image=imgAudio,
              bd=0,
              bg='#212324',
              activebackground='#212324',
              cursor="hand2",
              command=lambda: root.after(1, Thread(target=pre_audio).start())
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
