from PIL import Image
from concurrent.futures import ProcessPoolExecutor
import edge_promoting_thread
import os

print('start move src data')
# move src data
src_path = "./data/images"
src_files = [f for f in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, f))]
src_files.sort()
train_files = src_files[:5400]

train_path = './data/src/train'
if not os.path.isdir(train_path):
    os.makedirs(train_path)
    
for i in train_files:
    Path(os.path.join(src_path, i)).rename(os.path.join(train_files, i))
    
testfiles = src_files[5400:6150]
test_path = './data/src/test'
if not os.path.isdir(test_path):
    os.makedirs(test_path)
for i in testfiles:
    Path(os.path.join(path, i)).rename(os.path.join(test_path, i))

print('start move tgt data')
# move tgt data
jojo_path = './data/jojo/05'
jojo_filenames = []
for s in os.listdir(jojo_path):
    if os.path.isdir(os.path.join(jojo_path, s)):
        subdir = os.path.join(jojo_path, s)
        for f in os.listdir(subdir):
            filepath = os.path.join(subdir, f)
            if os.path.isfile(filepath):
                jojo_filenames.append(filepath)
        
jojo_filenames.sort()

tgt_path = './data/tgt/train'
for i in train_files:
    Path(os.path.join(src_path, i)).rename(os.path.join(train_files, i))
    
j = 0
for i in jojo_filenames[:5000]:
    Path(i).rename(os.path.join(tgt_path, str(j)+'.jpg'))
    j += 1

print('edge-promoting start!!')
# edge_promoting
root = './data/tgt/train'
save = './data/tgt/pair'
if not os.path.isdir(save):
    os.makedirs(save)
cores = os.cpu_count()

file_list = os.listdir(root)
num_data = len(file_list)
indics = int(num_data/cores)
with ProcessPoolExecutor(max_workers=cores) as executor:
    for i in range(cores):
        executor.submit(edge_promoting_thread.edge_promoting, root, file_list[i*indics:(i+1)*indics], save)

