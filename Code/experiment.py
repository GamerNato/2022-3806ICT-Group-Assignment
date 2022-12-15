from T import process
from replan import run

folder = 'mazes/'
mazes = []

size = '10x10'
side = int(size.split('x')[0])
for x in range(10):
	mazes.append((folder+size+'_'+str(x),side))
	process(folder+size+'_'+str(x),side,side,[],0,False,True)

size = '50x50'
side = int(size.split('x')[0])
for x in range(10):
	mazes.append((folder+size+'_'+str(x),side))
	process(folder+size+'_'+str(x),side,side,[],0,False,True)

size = '100x100'
side = int(size.split('x')[0])
for x in range(10):
	mazes.append((folder+size+'_'+str(x),side))
	process(folder+size+'_'+str(x),side,side,[],0,False,True)
	
print(mazes)

results = []
for x in mazes:
	results.append(run(x))

f = open('table.txt','w')
for x in results:
	f.write(str(x[0]))
	f.write(',')
	f.write(str(x[1]))
	f.write('\n')
f.close()