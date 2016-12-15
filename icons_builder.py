#!/usr/bin/env python
import glob
import sys, getopt, subprocess
import os.path
import os



def main(argv):

	size_ratios= {'ldpi':0.75, 'mdpi':1, 'hdpi':1.5, 'xhdpi':2, 'xxhdpi':3, 'xxxhdpi':4}
	
	color = None
	dest = '.'
	dp = 24
	try:
		opts, args = getopt.getopt(argv,"h",['dp=','color=','dest='])
	except getopt.GetoptError:
		print './change.py [-h] [--dp dp-value] [--color color] [--dest dest_dir] <image_path>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print './change.py [-h] [--color color] [--dest dest_dir] <image_path>'
			sys.exit()
		if opt == '--color':
			color = arg
		if opt == '--dest':
			dest = arg
		if opt == '--dp':
			dp = float(arg)
	if len(args)>0:
		image_path = args[0]
		file_name = os.path.basename(image_path)

	temp_dir = '.temp_res'
	subprocess.call('rm -rf '+temp_dir, shell=True)		
	subprocess.call('mkdir '+temp_dir, shell=True)

	for suffix,ratio in size_ratios.iteritems():
		px = int(dp*ratio)
		sub_dir  = 'drawable-'+suffix
		subprocess.call(['mkdir', sub_dir], cwd=temp_dir)
		subprocess.call(['convert', image_path, '-resize', str(px)+'x'+str(px), file_name], cwd=temp_dir+'/'+sub_dir)
		if color<>None:
			subprocess.call(['convert',file_name,'-alpha','extract','-background',color,'-alpha','shape',file_name], cwd=temp_dir+'/'+sub_dir)
	subprocess.call('mv '+temp_dir+' '+dest+'/res', shell=True)


			
if __name__ == "__main__":
	main(sys.argv[1:])
