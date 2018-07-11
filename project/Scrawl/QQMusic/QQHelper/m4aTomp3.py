# __fileName__ : m4aTomp3.py
# __date__ : 2018/07/05
# __author__ : Yaxuan

import os

def m4aTomp3(m4afile, mp3file, rmsrc = False):
	'''
	m4a转换为mp3
	m4afile : m4a文件路径
	mp3file : mp3文件路径
	rmsrc : 是否删除m4a文件
	返回值 : 删除成功与否
	'''
	try:
		assert(m4afile.endswith('.m4a'))
		tmpfile = m4afile
		tmpfile = tmpfile.replace('.m4a', '.wav')
		os.system('ffmpeg -y -i ' + m4afile + ' ' + tmpfile + '>file 2>&1')	
		os.system('ffmpeg -y -i ' + tmpfile + ' ' + mp3file + '>file 2>&1')
		os.remove(tmpfile)
		if rmsrc: os.remove(m4afile)
		return True
	except:
		return False

if __name__ == '__main__':
	m4aTomp3('/QQCache/000HJ60D3ATlw5.m4a', '/QQCache/000HJ60D3ATlw5.mp3')