import os,sys,codecs
convertor = os.path.dirname(os.path.abspath(sys.argv[0]))+'/conll2mst.py'

f = os.path.abspath(sys.argv[1])+'/'
lf1 = os.path.abspath(sys.argv[2])
lf2 = os.path.abspath(sys.argv[3])
l1 = sys.argv[4]
l2 = sys.argv[5]
jar_file = os.path.abspath(sys.argv[6])

r1 = f + 'corpus.tok.clean.'+l1
r2 = f + 'corpus.tok.clean.'+l2

print r1
print r2

c1 = f + 'corpus.tok.clean.'+l1+'.conll'
c2 = f + 'corpus.tok.clean.'+l2+'.conll'

m1 = f + 'corpus.tok.clean.'+l1+'.mst'
m2 = f + 'corpus.tok.clean.'+l2+'.mst'

command  = 'java -jar '+jar_file + ' '+ lf1 + ' '+r1 + ' '+ c1
print command
os.system(command)
command = 'python '+convertor+ ' '+ c1 +' > '+m1
print command
os.system(command)
command = 'rm -f ' + c1 
print command
os.system(command)

command  = 'java -jar '+jar_file + ' '+ lf2 + ' '+r2 + ' '+ c2
print command
os.system(command)
command = 'python '+convertor+ ' '+ c2 +' > '+m2
print command
os.system(command)
command = 'rm -f ' + c2 
print command
os.system(command)
