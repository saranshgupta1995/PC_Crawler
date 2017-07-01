import os,pickle
from difflib import SequenceMatcher

filenum=0
allpaths=[None]*(10**7)
alldests=[None]*(10**7)

grph={}

drives=["F"]

orig_path=os.getcwd()

def addtogrph(node, branch):
    if node in list(grph.keys()):
        grph[node]=grph[node]+[branch]
    else:
        grph[node]=[branch]

def addtolist(filename,filepath):
    global filenum
    allpaths[filenum]=filepath
    alldests[filenum]=filename
    filenum+=1

def readfoldersin(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def readfilesin(path):
    return [d for d in os.listdir(path) if not os.path.isdir(os.path.join(path, d))]

def iterthrough(path):
    os.chdir(path)
    if(len(readfilesin(path))<1000):
        for filee in readfilesin(path):
            if not filee.startswith('.'):
                addtolist(filee,path)
                addtogrph(path[-(path[-1::-1].find("\\")):],filee)
    for folder in readfoldersin(path):
        addtogrph(path[-(path[-1::-1].find("\\")):],folder)
        addtolist(folder,path)
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

if(not os.path.exists("datalist.p")):
    print("run")
    for drive in drives:
        drivepath=drive+":\\"
        iterthrough(drivepath)
        for i in range(len(allpaths)):
            if (allpaths[i]==None):
                allpaths=allpaths[:i]
                alldests=alldests[:i]
                break
        os.chdir(orig_path)
    pickle.dump(allpaths,open("pathlist.p","wb"))
    pickle.dump(grph,open("datadict.p","wb"))
    pickle.dump(alldests,open("filelist.p","wb"))
else:
    grph = pickle.load(open("datadict.p","rb"))
    allpaths = pickle.load(open("pathlist.p","rb"))
    alldests= pickle.load(open("filelist.p","rb"))

        

