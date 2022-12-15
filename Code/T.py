##### needed libraries #####
import string
import random
import copy as cp

##### functions #####
def protect(maze,path,x,y):
	for i in range(y):
		for j in range(x):
			if maze[i][j] == 'S':
				break;
		if maze[i][j] == 'S':
			break;

	safe = maze
	start = (i,j)
	#print(start)

	for i in range(y):
		for j in range(x):
			#print(i,j,maze[i][j],maze[i][j]=='G')
			if maze[i][j] == 'G':
				#print('here')
				oend = (i,j)
				break
		if maze[i][j] == 'G':
			#print('and here')
			break
	maze[oend[0]][oend[1]] = 'O'
	
	i = start[0]
	j = start[1]
	if safe[i][j] == 'S':
		safe[i][j]='P'
		for k in path:
			if k == 'right':
				j+=1
			elif k == 'left':
				j-=1
			elif k == 'down':
				i+=1
			else:
				i-=1
			#print(i,j)
			safe[i][j]='P'
	end = (i,j)
	#print(start,end)
	return safe,start,end,oend

def find(maze,path,x,y):
	safe,start,end,oend = protect(maze,path,x,y)
	#print(safe)
	#u,d,l,r
	junctions = []
	for i in range(y):
		for j in range(x):
			options = [False,False,False,False]
			directions = 0
			if i>1 and safe[i-2][j] in ['O','P','S','G']:
				directions+=1
				if safe[i-1][j] in ['H','O']:
					options[0] = True
			if (y-(i+1))>1 and safe[i+2][j] in ['O','P','S','G']:
				directions+=1
				if safe[i+1][j] in ['H','O']:
					options[1] = True
			if j>1 and safe[i][j-2] in ['O','P','S','G']:
				directions+=1
				if safe[i][j-1] in ['H','O']:
					options[2] = True
			if (x-(j+1))>1 and safe[i][j+2] in ['O','P','S','G']:
				directions+=1
				if safe[i][j+1] in ['H','O']:
					options[3] = True
			if directions>2:
				junctions.append([(i,j),tuple(options)])
	#print(junctions)
	return junctions,start,end,oend

def mutate(maze,path,x,y,m=1,re=False,goal=False):
	junctions,start,end,oend = find(maze,path,x,y)
	if len(junctions) == 0:
		print('maze has no possible T junctions')
		return maze
	if m > len(junctions):
		print('maze is too small for that many mutations, it has been automatically limited')
		m = len(junctions)
	swap = dict()
	swap['O'] = 'H'
	swap['H'] = 'O'
	for k in range(m):
		#visual(maze)
		chosen = random.choice(junctions)
		junctions.pop(junctions.index(chosen))
		i = chosen[0][0]
		j = chosen[0][1]
		direction = []
		for e,l in enumerate(chosen[1]):
			if l:
				direction.append(e)
		direction = random.choice(direction)
		if direction == 0:
			#print(i,j,'up')
			maze[i-1][j] = swap[maze[i-1][j]]
		elif direction == 1:
			#print(i,j,'down')
			maze[i+1][j] = swap[maze[i+1][j]]
		elif direction == 2:
			#print(i,j,'left')
			maze[i][j-1] = swap[maze[i][j-1]]
		else:
			#print(i,j,'right')
			maze[i][j+1] = swap[maze[i][j+1]]
		if re:
			junctions,start,end = find(maze,path,x,y)
	for i in range(y):
		for j in range(x):
			if maze[i][j] == 'P':
				maze[i][j] = 'O'
	nend = end
	maze[start[0]][start[1]] = 'S'
	#print(goal)
	if goal:
		#print('goal')
		end = walk(maze,x,y,path,end,start)
		maze[end[0]][end[1]] = 'G'
	else:
		maze[oend[0]][oend[1]] = 'G'
	return maze,nend,start==end

def overwrite(filepath,maze,x,y,path,start):
	txt = open(filepath+'.txt','w')
	for i in maze:
		for j in i:
			txt.write(j)
		txt.write('\n')
	txt.close()

	numerify = dict()
	numerify['O'] = 0
	numerify['H'] = 1
	numerify['S'] = 2
	numerify['G'] = 3
	#numerify['X'] = 4

	csp = open(filepath+'.csp','w')
	csp.write(f"#define NoOfRows {y};\n")
	csp.write(f"#define NoOfCols {x};\n")
	csp.write(f"#define limit (2*NoOfRows);\n\n")
	csp.write(f"var maze[NoOfRows][NoOfCols]:{{0..4}} = [")
	for w,i in enumerate(maze):
		for z,j in enumerate(i):
			csp.write(str(numerify[j]))
			if not(w == len(maze)-1 and z == len(i)-1):
				csp.write(',')
		csp.write('\n	')
	csp.write('];\n\n')
	#print('start = ',start)
	csp.write(f"var pos[2]:{{0..{y}}} = [{start[0]},{start[1]}];\n\n")
	csp.write(f"var time = {len(path)};\n")
	csp.write("""
//Move the current position up 1
MoveUp() = up{pos[0] = pos[0] - 1; time = time+1;}-> Move();

//Move the current position down 1
MoveDown() = down{pos[0] = pos[0] + 1; time = time+1;}-> Move();

//Move the current position left 1
MoveLeft() = left{pos[1] = pos[1] - 1; time = time+1;}-> Move();

//Move the current position right 1
MoveRight() = right{pos[1] = pos[1] + 1; time = time+1;}-> Move();

//Define when goal is found
#define goalGoalFound (maze[pos[0]][pos[1]] == 3 && time<=limit);

//The task Move is the sequence of primitive tasks MoveUp, MoveDown, MoveLeft, MoveRight.
Move() = [pos[0] != 0 &&            maze[pos[0]-1][pos[1]] != 1]MoveUp()   []
         [pos[0] != NoOfCols - 1 && maze[pos[0]+1][pos[1]] != 1]MoveDown() []
         [pos[1] != 0  &&           maze[pos[0]][pos[1]-1] != 1]MoveLeft() []
         [pos[1] != NoOfRows - 1 && maze[pos[0]][pos[1]+1] != 1]MoveRight();

#assert Move() reaches goalGoalFound;
""")
	csp.close()

def visual(maze):
	for x in maze:
		for y in x:
			print(y,end='')
		print()
	print()

def compare(maze1,maze2,x,y):
	for i in range(y):
		for j in range(x):
			#print(maze1[i][j] != maze2[i][j])
			if maze1[i][j] != maze2[i][j]:
				print('X',end='')
			else:
				print('O',end='')
		print()

def walk(maze,x,y,path,location,start):
	copy = cp.deepcopy(maze)
	limit = x*2
	time = len(path)
	print(path)
	print(location,limit-time)
	for z in range(limit-time):
		print(z)
		copy[location[0]][location[1]] = 'P'
		newlocation = move(copy,x,y,location)
		#print(newlocation)
		if newlocation == location or newlocation == start:
			return location
			break
		#copy[location[0]][location[1]] = 'P'
		location = newlocation
		#print('copy:')
		#visual(copy)
	return location

def move(maze,x,y,location):
	options = [False,False,False,False]
	# u,d,l,r
	#print(location[0]>0,(y-(location[0]+1))>1,location[1]>0,(x-(location[1]+1))>1)
	#print(maze[location[0]-1][location[1]],maze[location[0]+1][location[1]],maze[location[0]][location[1]-1],maze[location[0]][location[1]+1])
	if location[0]>0 and maze[location[0]-1][location[1]] in ['O','S']:
		options[0] = (location[0]-1,location[1])
	if (y-location[0])>1 and maze[location[0]+1][location[1]] in ['O','S']:
		options[1] = (location[0]+1,location[1])
	if location[1]>0 and maze[location[0]][location[1]-1] in ['O','S']:
		options[2] = (location[0],location[1]-1)
	if (x-location[1])>1 and maze[location[0]][location[1]+1] in ['O','S']:
		options[3] = (location[0],location[1]+1)

	#print("move options",options)
	pops = []
	for e,z in enumerate(options):
		if not z:
			pops.append(e)

	for e in pops[::-1]:
		options.pop(e)

	#print("move options",options)
	if len(options):
		location = random.choice(options)
	return location

def load(filepath):
	file = open(filepath+'.txt','r')
	maze = []
	for z in file:
		z = z.strip()
		maze.append(list(z))
	file.close()
	return maze

def process(filepath,x,y,path=[],m=1,re=False,goal=False):
	# filepath must be the path and name of the file but NOT the filetype as there is both a .txt and .csp used
	# x and y are of course the x and y dimensions of the maze
	#  - the maze MUST NOT be a jagged array
	# path must be a list of strings 'left','right','up','down' of the steps taken so far
	# m is the number of mutations to perform
	# re is a boolean for whether or not the program should recheck for new possible T junctions between each mutation

	maze = load(filepath)
	print('Original:')
	print(path)
	#visual(maze)
	
	for i in range(y):
		for j in range(x):
			if maze[i][j] == 'S':
				break;
		if maze[i][j] == 'S':
			break;
	
	if maze[i][j] == 'S':
		for k in path:
			if k == 'right':
				j+=1
			elif k == 'left':
				j-=1
			elif k == 'down':
				i+=1
			else:
				i-=1
			#print(i,j)
	if maze[i][j] == 'G':
		return True
	
	result = mutate(cp.deepcopy(maze),path,x,y,m,False,goal)
	#if result[-1]:
	#	print("return to start")
	#	return True
	print('Result')
	#visual(result[0])
	overwrite(filepath,result[0],x,y,path,result[1])
	return False
	#return maze[result[1][0]][result[1][1]] == 'G'


###### example calls #####
#process("mazes/20x20",20,20,[],0,False,True) # run this one to get an initial CSP

#process("mazes/20x20",20,20,["up","up","up","up"],3,False,True)
