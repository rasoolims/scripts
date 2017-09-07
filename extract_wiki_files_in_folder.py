import os,sys

python_script = os.path.abspath(sys.argv[1])
input_folder =  os.path.abspath(sys.argv[2])+'/'
output_folder =  os.path.abspath(sys.argv[3])+'/'

if not os.path.isdir('/tmp/tmp'): os.mkdir('/tmp/tmp/')

for f in sorted(os.listdir(input_folder)):
	lang = f[:f.find('wiki')]
	adrs = input_folder+f
	command = 'python '+python_script + '  ' + adrs+ ' --no-templates -cb 250K -o  /tmp/tmp/'
	
	print command
	os.system(command)
	command = 'find /tmp/tmp/ -name "*bz2" -exec bunzip2 -c {} \; > '+output_folder+lang
	print command
	os.system(command)
	command = 'rm -rf /tmp/tmp/*'
	print command
	os.system(command)
