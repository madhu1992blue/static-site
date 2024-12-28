import os
import shutil
def removeRecurse(path: str):
    print("Removing: ",path)
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        os.remove(path)
        return
    for e in os.listdir(path):
        removeRecurse(path + "/" + e)
    shutil.rmtree(path)
    


def copy(src: str, dest: str):
    for sc in os.listdir(src):
        if os.path.isdir(src+"/"+sc):
            os.mkdir(dest+"/"+sc)
            print("Copying Dir: ",src+"/"+sc, dest + "/"+sc)
            copy(src+"/"+sc, dest + "/"+sc)
        else:
            print("Copying: ",src+"/"+sc, dest + "/"+sc)
            shutil.copy(src+"/"+sc, dest+"/"+sc)
                
        