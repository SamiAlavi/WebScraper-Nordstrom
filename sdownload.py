from pathlib import Path
from requests import get
from shutil import copyfile
from time import time
from os.path import isdir

# copy the img_url.txt file
copyfile('img_url.txt', 'img_url_Copy.txt')

# read the copied file
with open('img_url_Copy.txt','r') as r:
    lines = r.readlines()

#read how many imgs have been previously downloaded
with open('img_downloaded.txt','r') as r:
    start = int(r.read())

total = len(lines)
print('Total images to download:',total)
print('Downloaded images:',start)    
print('Remaining images:',total-start)

timee = time()
#start from the next image
for i in range(start,total):
    try:
        if i%100==0:
            print(f'{i}\t{(time()-timee)/60} minutes')
            timee = time()
        line = lines[i]
        temp = line.split(';')
        crnt = temp[1]
        dwnld = temp[2]
        detail = temp[3]
        price = temp[4][:-1]
        sep = '/'
        direct = crnt.split(sep)
        direct = sep.join(direct[:-1])

        if not isdir(direct):
            Path(f"{direct}").mkdir(parents=True,exist_ok=True)
            with open(f"{direct}/price.txt",'w') as f:
                f.write(price)
            with open(f"{direct}/detail.txt",'w') as f:
                f.write(detail)
        
        Path(f"{crnt}").mkdir(parents=True,exist_ok=True) # make directories
        r = get(dwnld, stream=True).content # download image bytes
        indx = dwnld.index('.jpeg')+5 # now gets the index of first occurence of .jpeg
        dwnld = dwnld[36:indx]        # and slices based on it
        path = f"{crnt}/{dwnld}"  

        with open(path, 'wb') as f: # write image bytes to path
            f.write(r)
        with open("img_downloaded.txt", 'w') as f: # write how many images have been downloaded
            f.write(str(i+1))
    except:
        with open("img_errors.txt", 'a+') as f: # write errors
            f.write(f'{i}\n')

