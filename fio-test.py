__author__ = 'Jungsik Choi'

import subprocess
import re

def execute(_cmd):
	print '[execute] ' + _cmd
	fd = subprocess.Popen(_cmd, shell=True,
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE)
	stdout, stderr = fd.communicate()
	return stdout

def main():
	result_file = open("result-populate", 'w')
	ioengine_list = ['sync', 'mmap']
	rw_list = ['read', 'write']
	numjobs_list = ['1', '4', '8', '12', '16', '20', '24']
	size = '512m'
	directory = '/mnt/tmpfs'
	runtime = '60'
	expression = '\s*aggrb=(?P<number>\d+\.*\d*)MB/s'
	re_compile = re.compile(expression)

	for ioengine in ioengine_list:
		for rw in rw_list:
			for numjobs in numjobs_list:
				cmd = 'rm -rf /mnt/tmpfs/*'
				result = execute(cmd)
				cmd = 'fio --name=test'
				cmd += ' --ioengine=' + ioengine
				cmd += ' --rw=' + rw
				cmd += ' --numjobs=' + numjobs
				cmd += ' --size=' + size
				cmd += ' --directory=' + directory
				cmd += ' --runtime=' + runtime
				cmd += ' --time_based'
				result = execute(cmd)
				re_search = re_compile.search(result)
				aggrb = re_search.group('number')
				string = ioengine + '-' + rw + '-' + numjobs
				string += ', ' + aggrb + '\n'
				print '[result] ' + string
				result_file.write(string)

	result_file.close()

if __name__ == '__main__':
	main()
