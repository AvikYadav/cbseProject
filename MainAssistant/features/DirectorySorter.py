# get path done
# check for files if directory return error done
# get files extension done
# add them to set done
# create folder according to data in set
# copy files with same type to their respective folder
import os
from pathlib import Path
import shutil
import MainAssistant.main as main
def Main():
    main.speak("Enter directory path : ")
    path = input("enter path: ")
    original = r""
    target = r""
    direCreates = []
    def isEmpty(directoryPath):
        try:
            if os.path.exists(directoryPath):
                if len(os.listdir(directoryPath)) == 0:
                    print("no file")
                    return False
                else:
                    print("some file")
                    return True
            else:
                print("path invalid")
                return False
        except NotADirectoryError:
            print("no directory")
            return False

    check  = isEmpty(path)


    extension = set()
    if check:
        isDirec = os.listdir(path)
        for i in isDirec:
            string = str(i)
            string = string.lower()
            spli = string.split(".")
            print(spli[-1])
            extension.add(spli[-1])
        print(extension)
        print(isDirec)
        for singleExtention in extension:
            directoryFileName = os.path.join(path,singleExtention)
            os.mkdir(directoryFileName)
            print(directoryFileName)
            name = Path(r""+directoryFileName).parts[-1]
            direCreates.append(name)
            for fileadd in isDirec:
                string = str(fileadd)
                spli = string.lower().split(".")
                print("fileAdd is working")
                print(direCreates[-1])
                if spli[-1] == direCreates[-1]:
                    print("dirCreate is working")
                    if spli[-1] in fileadd:
                        print("spli is working")
                        original = r""+os.path.join(path,fileadd)
                        target = r"" + os.path.join(directoryFileName,fileadd)
                        print(original)
                        print(target)
                        shutil.copyfile(original,target)
                        os.remove(original)

if __name__ == '__main__':
    Main()