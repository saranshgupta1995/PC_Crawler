import pyHook, pythoncom, sys, logging,os, httplib, urllib, getpass, shutil, pickle
from datetime import datetime

grph = pickle.load(open("datadict.p","rb"))

file_log = datetime.now().strftime('%y%m%w%d')+".txt"

line_buff=""
window_buff=""
filecheck=False
filename=""
conf=False
sub=[]

def OnKeyboardEvent(event):
    global line_buff
    global window_buff
    global filecheck
    global filename
    global conf
    global sub
    
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    ky=event.Ascii
    
    if(not event.WindowName == window_buff and not event.WindowName==None):
        window_buff=event.WindowName
        line_buff+="\n"
        line_buff+=datetime.now().strftime('%X')+"\t"
        line_buff+=event.WindowName
        line_buff+="\n"
        logging.log(10,line_buff)
        line_buff=""

        
#### Check if user needs file/folder opened
        
    if(len(line_buff)>3):
        if((line_buff[-1]+line_buff[-2]+line_buff[-3]+line_buff[-4])==">>>>"):
            filecheck=True


#### Deal with limited conflicts in filename
            
    if(conf):
        os.system("taskkill /im notepad.exe")
        if(ky>47 and ky<58):
            os.startfile(sub[int(chr(ky))]+"\\"+filename)
        filename=""
        conf=False
            

        
#### Check if file/folder name exists and open
            
    if(filecheck):
        if(ky > 31 and ky < 127):
            if(not chr(ky)=="<"):
                filename += chr(ky)
            else:
                try:
                    sub=grph[filename]
                except:
                    sub=[]
                if(len(sub)==1):
                    os.startfile(sub[0]+"\\"+filename)
                    filename=""
                elif(len(sub)<=10 and len(sub)>1):
                    txt="Enter Numbered FilePath to Open\n\n"
                    f=open("Conflicts.txt","w")
                    for i in range(len(sub)):
                        txt+=str(i)+"- "+sub[i]+"\\"+filename+"\n"
                    f.write(txt)
                    f.close()
                    os.startfile("Conflicts.txt")
                    os.startfile("Conflicts.txt")
                    conf=True
                else:
                    filename=""
                filecheck=False

#### Update linebuff with event
        
    if(ky > 31 and ky < 127):
        line_buff += chr(ky)
        return True
    
    if(ky == 13):
        line_buff+="\n"
        return True
    
    
    if(event.Ascii == 8):
        line_buff = line_buff[:-1]
        return True

    return True



hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
