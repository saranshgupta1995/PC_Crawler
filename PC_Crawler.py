import os,pickle

grph={}

drives=["F"]


bsname=os.path.basename
orig_path=os.getcwd()

def addtogrph(branch,node):
    grph.update({node:branch})

def readfoldersin(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def readfilesin(path):
    return [d for d in os.listdir(path) if not os.path.isdir(os.path.join(path, d))]

def iterthrough(path):
    os.chdir(path)
    if(len(readfilesin(path))<1000):
        a=[addtogrph(path,filee) for filee in readfilesin(path) if not filee.startswith('.')]

    for folder in readfoldersin(path):
        addtogrph(path,folder)
        newpath=path+"\\"+folder
        if(os.path.isdir(newpath)):
            if not folder.startswith('.'):
                try:
                    os.chdir(newpath)
                    iterthrough(newpath)
                except:
                    pass

def findpath(dest):
    poss=[]
    for value in grph.values():
        try:
            value.index(dest)
            poss.append(list(grph.keys())[list(grph.values()).index(value)])
        except :
            pass
    return poss

if(not os.path.exists("datadict1.p")):
    print("run")
    for drive in drives:
        drivepath=drive+":\\"
        iterthrough(drivepath)
        os.chdir(orig_path)
    pickle.dump(grph,open("datadict.p","wb"))

        

