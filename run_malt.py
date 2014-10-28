import os,sys

if len(sys.argv)<5:
	print 'python run_malt.py [malt_dir] [train|parse] [model_file] [input_file] [output_file(for parsing)]'
	sys.exit(0)
malt_dir=os.path.abspath(sys.argv[1])
process='parse'
if sys.argv[2]=='train':
	process='train'
else:
	process='parse'

model=sys.argv[3]
f=os.path.abspath(sys.argv[4])
of=''
if process=='parse':
	of=os.path.abspath(sys.argv[5])

os.chdir(malt_dir)

print process
print model
print f
print of

if process=='train':
	print '/home/rasooli/jre/jre1.8.0_25/bin/java -jar maltparser-1.8.jar -c '+model+' -i '+f+' -m learn'
	os.system('/home/rasooli/jre/jre1.8.0_25/bin/java -jar maltparser-1.8.jar -c '+model+' -i '+f+' -m learn')
else:
	os.system('/home/rasooli/jre/jre1.8.0_25/bin/java -jar maltparser-1.8.jar -c '+model+' -i '+f+' -o '+of+' -m parse')
