from T import process, load
import subprocess as sp
import random

def step(maze):
	command = f"mono PAT3.Console.exe -csp -engine 1 {maze}.csp result.txt".split(" ")
	print(command)
	sp.run(command)
	return read("result.txt")

def read(name):
	file = open(name,'r')
	# read and find first step in results
	valid = False
	for line in file:
		#print(line)
		if line[48:-2] == "VALID":
			valid = True
		if line[0] == '<':
			break
	#line = line[:-1]
	#line = line[1:-1]
	line = line[1:-2].split(" -> ")[1:]
	#print(line,valid)
	file.close()
	return line[0],valid

def check(filepath,path,side):
	maze = load(filepath)
	for i in range(side):
		for j in range(side):
			if maze[i][j] == 'S':
				break;
		if maze[i][j] == 'S':
			break;
	#print(path)
	for k in path:
		if k == 'right':
			j+=1
		elif k == 'left':
			j-=1
		elif k == 'down':
			i+=1
		else:
			i-=1
	#print('ij=',i,j)
	return maze[i][j] == 'G'

def run(maze):
	path = []
	while not check(maze[0],path,maze[1]):
		pass
		tick = step(maze[0])
		path.append(tick[0])
		if random.choice(range(10)):
			process(maze[0],maze[1],maze[1],path,0,False,False)
		else:
			process(maze[0],maze[1],maze[1],path,1,False,True)
		if not tick[1]:
			break
	print("done")
	print(path,len(path))
	return path,tick[1]

#print(read("result.txt"))

#print(read('result.txt'))
#step('maze/20x20')
#process('20x20',20,20,[],0,False)
#run(('20x20',20))