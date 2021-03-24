import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import  pyautogui


class Alexa:
    def __init__(self):
        self.isquit = True
        self.listener = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty('voice', self.voices[1].id)
    def talk(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
    def take_command(self):
        command=None
        try:
            with sr.Microphone(device_index=0) as source:
                self.talk("What can I Do For You...")
                print('listening...')
                voice= self.listener.listen(source)
                command=self.listener.recognize_google(voice)
                command=self.command.lower()
                if 'alexa' in command:
                    command=command.replace('alexa','')
        except: pass

        return command

    def run_alexa(self):
        command=self.take_command()
        if (not(command==None)):
            if 'play' in command:
                song=command.replace('play','')
                self.talk('playing'+song)
                pywhatkit.playonyt(song)
            elif 'time' in command:
                current_time=datetime.datetime.now().strftime('%H:%M %p')
                print(current_time)
                self.talk('Current Time is '+current_time)
            elif 'who is' in command:
                command=command.replace('who is','')
                info=wikipedia.summary(command,1)
                if info is not None:
                    print(info)
                    self.talk(info)
                else:
                    self.talk("Person Not Found in Wikipedia")
            elif 'joke' in command:
                self.talk(pyjokes.get_joke())
            elif 'scroll' in command:
                if 'up' in command:
                    pyautogui.scroll(500)
                elif 'down' in command:
                    pyautogui.scroll(-500)


            elif 'move' in command:
                if 'left' in command:
                   pyautogui.moveTo(30, 0, 1.5)
                elif 'right' in command:
                    pyautogui.moveTo(1152, 137, 1.5)
            elif 'quit' in command or 'by' in command:
                self.talk("By Have A Good Day")
                self.isquit = False
                print("closed")
                pyautogui.hotkey("alt", "f4")



            elif 'click' in command:
                if 'left' in command:
                    pyautogui.click(button="left")
                elif 'right' in command:
                    pyautogui.click(button="right")
        else:
            self.talk("I dont Understand .What You Say..")


    def start_assistant(self):
        self.run_alexa()


