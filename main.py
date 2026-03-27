from  pathlib import Path

def readfileandfolder():
    path =  Path('')
    items = list(path.rglob('*'))
    for i,item in enumerate(items):
        print(f"{i+1}  : {item}")


def createfile():
    try:
        readfileandfolder()
        name = input("Please tell the name of the file: ")
        p = Path(name)
        if not p.exists():
            with open(p, 'w') as r:
                text = input("Would you also like to add some text in the file? (Y/N) ")
                if text.upper() == "Y":
                    content = input("Please write the content: ")
                    r.write(content)
            print("File created successfully!")
        else:
            print("This file already exists")
    except Exception as err:
        print(f"An error occurred as {err}")

def readfile():
    try:
     readfileandfolder()

     name=input("Enter the name of the file you wanna read")
     p = Path(name)

     if p.exists():
        with open(p,'r') as f:
            content=f.read()
            print(content)
     else:
        print("File does not exist")
    except Exception as e:
        print(e)

def updatefile():
    try:
     readfileandfolder()
     name=input("Enter the name of the file you wanna read")
     p = Path(name)

     if p.exists():
         with  open(p,'a') as g:
             content=input("Please type in what do  you wanna update")
             g.write("\n" + content)
             print("Content has been successfully appended")
     else:
         print("File does not exist")        
    except Exception as e:
        print(e)

def deletefile():
    try:
     readfileandfolder()
     name=input("Enter the name of the file you wanna read")
     p = Path(name)

     if p.exists():
         p.unlink()
         print("File deleted")
     else:
         print("file  does not exist")
    except Exception as e:
        print(e)
        
print("press 1 for creating a file")
print("press 2 for reading a file")
print("press 3 for updating a file")
print("press 4 for deleting a file")

check=int(input("please tell your response"))
if  check == 1:
    createfile()
if check == 2:
    readfile()
if check == 3:
    updatefile()
if check == 4:
    deletefile()