from pathlib import Path
from requests import get
from shutil import copyfile

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
    
#start from the next image
for i in range(start,total):
    try:
        if i%10==0:
            print(i)
        line = lines[i]
        temp = line.split(',')
        crnt = temp[0]
        dwnld = temp[1][:-1]
        
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
        with open("img_errors.txt", 'w') as f: # write errors
            f.write(str(i+1))

