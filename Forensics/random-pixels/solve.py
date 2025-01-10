import random, time, numpy
from PIL import Image
#ironCTF{p53ud0_r4nd0m_f0r_4_r3450n}

def derandomize(img, seed):
	random.seed(seed)
	new_y = list(range(img.shape[0]))
	new_x = list(range(img.shape[1]))
	random.shuffle(new_y)
	random.shuffle(new_x)
	
	new = numpy.empty_like(img)
	for i, y in enumerate(new_y):
		for j, x in enumerate(new_x):
			new[y][x] = img[i][j]
	return numpy.array(new)
    

creation = "file creation time"

with Image.open("encrypted.png") as f:
	img = numpy.array(f)
	out = derandomize(img, creation)
	image = Image.fromarray(out)
	image.save("flag.png")
