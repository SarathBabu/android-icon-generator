#!/usr/bin/env python
import glob
import sys, getopt, subprocess
import os.path
import os
import glob


def main(argv):

	size_ratios= {'ldpi':0.75, 'mdpi':1, 'hdpi':1.5, 'xhdpi':2, 'xxhdpi':3, 'xxxhdpi':4}
	
	color = None
	dest = '.'
	dp = 24
	padding = 0
	file_name = None
	try:
		opts, args = getopt.getopt(argv,"h",['size=','color=','padding=','name=','dest='])
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
		if opt == '--size':
			dp = int(arg)
		if opt == '--padding':
			padding = int(arg)
		if opt == '--name':
			file_name = arg
	if len(args)>0:
		image_path = args[0]
	if file_name == None:
		file_name = os.path.basename(image_path)

	temp_dir = '.temp_res'
	subprocess.call('rm -rf '+temp_dir, shell=True)		
	subprocess.call('mkdir '+temp_dir, shell=True)

	for suffix,ratio in size_ratios.iteritems():
		px = int(dp*ratio)
		sub_dir  = 'drawable-'+suffix
		subprocess.call(['mkdir', sub_dir], cwd=temp_dir)
		subprocess.call(['convert', image_path, '-resize', str(px)+'x'+str(px), file_name], cwd=temp_dir+'/'+sub_dir)
		if padding>0:
			new_padding = int(padding*ratio)
			subprocess.call(['convert',file_name,'-background','transparent','-gravity', 'center', '-extent', str(px+new_padding)+'x'+str(px+new_padding),file_name], cwd=temp_dir+'/'+sub_dir)
		if color<>None:
			subprocess.call(['convert',file_name,'-alpha','extract','-background',color,'-alpha','shape',file_name], cwd=temp_dir+'/'+sub_dir)


	if len(glob.glob(dest+'/res')) == 0 :
		subprocess.call('rsync -a '+temp_dir+'/ '+dest+'/res', shell=True)
	else:
		subprocess.call('rsync -a '+temp_dir+'/ '+dest+'/res\('+str(len(glob.glob(dest+'/res(*)'))+1)+'\)', shell=True)


			
if __name__ == "__main__":
	main(sys.argv[1:])
