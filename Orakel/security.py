import numpy as np
from PIL import Image
import random
from matplotlib import pyplot as plt

egypt = Image.open('test_picture.jpg')
ocean = Image.open('test_picture_2.jpg')
movies = {'egypt': egypt, 'ocean': ocean}

def create_pattern(image,points):
	"""
	Function to create the pattern. Will have seperate function to apply the values to the picture. 
	"""
	random.seed					# Initializing random procedure. 
	data = np.array(image)    # Converting the picture into an array.
	key = [2, random.randint(2,10)]   # The key to the picture. 
	x = random.choices(np.arange(2,data.shape[0]-2), k=points)   # X-values of pattern.
	y = random.choices(np.arange(2,data.shape[0]-2), k=points)   # Y-values of pattern.
	pattern = np.zeros((1+points, 2)) # Creating a empty pattern array. 
	pattern[0][0] = key[0]; pattern[0][1] = key[1]   # Including the key. 
	pattern[1:,0] = x[:]; pattern[1:,1] = y[:]   # Finishing the pattern.
	return pattern

def use_pattern(image, pattern):
	"""
	Function to implement the pattern. The change of the pixels can vary here, it doesn't have to be this one.

	"""
	data = np.array(image)  # Converting the picture into an array.
	opposite = [0,0,0]

	for pix in pattern:   # Changing points.
		"""
		Opposite is used to find the color which is most opposite the current RGB-value. This is to ensure
		that the color stays when quality gets worse. 
		"""

		opposite += data[int(pix[0])+1][int(pix[1])+1] # down and + in x direction
		opposite += data[int(pix[0])+1][int(pix[1])-1] # down and + in x direction
		opposite += data[int(pix[0])-1][int(pix[1])+1] # up and + in x direction
		opposite += data[int(pix[0])-1][int(pix[1])-1] # up and + in x direction
		
		for i in range(3):

			if int(opposite[i])/(255*4) < 0.5:
				opposite[i] = 255

			if int(opposite[i])/(255*4) > 0.5:
				opposite[i] = 0

		print(opposite)


		if int(pix[0]) != 0:
			data[int(pix[0]-1)][int(pix[1])] = opposite # - 1 in y direction 

		data[int(pix[0])][int(pix[1]-1)] = opposite # - 1 in x direction
		data[int(pix[0])][int(pix[1]+1)] = opposite # + 1 in x direction
		data[int(pix[0]+1)][int(pix[1])] = opposite # + 1 in y direction 
		data[int(pix[0])][int(pix[1])] = opposite # data[int(pix[0])][int(pix[1])]+1  # Changing the values by 1. Temporary 

		data[int(pix[0]-1)][int(pix[1])] = opposite # - 1 in y direction 
		data[int(pix[0]-2)][int(pix[1])] = opposite # - 2 in y direction 
		data[int(pix[0]+2)][int(pix[1])] = opposite # - 2 in y direction 
		data[int(pix[0])][int(pix[1]-2)] = opposite # - 2 in x direction
		data[int(pix[0])][int(pix[1]+2)] = opposite # + 2 in x direction

		opposite = [0,0,0]
	return data



def watch(movie, user):
	"""
	Watch function. Creates a picture/screenshot specified to the user who watches it. 

	"""
	f = open(f'{movie}.txt', 'a+')          # Opening the movie text file containing the keys. 
	pattern = create_pattern(movies[movie], 5)  # Creating a pattern for 'user'.
	new = use_pattern(movies[movie], pattern)  # Implementing pattern on their stream.
	plt.imsave(f'{user}_{movie}.png', new)  # Saving the new picture. 

	f.write(user);f.write(' ')  # Writing into the text file what pattern it is. 
	for pix in pattern: f.write(str(int(pix[0])));f.write(' ');f.write(str(int(pix[1])));f.write(' ')
	f.write('\n')
	f.close()

def unlock(movie, stream):
	"""
	Check which user posted. 

	"""
	
	streamer = Image.open(stream).convert('RGB')    # Image/movie.version that has been streamed. 
	movie_arr = np.array(movies[movie])  # The real picture in an array. 
	stream_arr = np.array(streamer)   # The stream in an array. 
	differ_points = np.array(np.where(movie_arr!=stream_arr))  # Points where their differ. Will give for all rgb, 
													           #just take every third element in the first two arrays.
	key = np.matrix.transpose(differ_points[:-1, :-1:3]).flatten()

	with open(f"{movie}.txt") as file:
		for line in file:
			check_key = np.array((line.rstrip().split(" ")[1:-1])).astype(int)    # Splitting the line up into all the elments of the key that is to be checked. 
			if all(item in key for item in check_key):        # Deciding if it is the key. 
				print(line.rstrip().split(" ")[0])            # Returning the dirty thief. 

def unlock_worse_res(stream, error):

	streamer = Image.open(stream).convert('RGB')
	ser = np.array(streamer)
	flagged = []
	summer = np.array([0, 0, 0])
	
	print(ser.shape)


	for j in range(1, ser.shape[0] - 1 ):
		for k in range(1, ser.shape[1]  - 1 ):
			print(j,k)

			summer += ser[j+1][k+1] # down and + in x direction
			summer += ser[j+1][k-1] # down and + in x direction
			summer += ser[j-1][k+1] # up and + in x direction
			summer += ser[j-1][k-1] # up and + in x direction

			if error < np.linalg.norm((summer/4) - ser[j][k]):
				flagged.append([j, k])

			summer = np.array([0, 0, 0])

	print(flagged)
			


#watch('ocean','Felix')
#unlock('ocean', '/Users/Felix/Desktop/Orakel/Felix_ocean.png')
unlock_worse_res('/Users/Felix/Desktop/Orakel/felix_egypt_shit.png', 150)




