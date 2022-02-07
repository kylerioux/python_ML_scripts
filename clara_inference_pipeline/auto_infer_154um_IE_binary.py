"""
This script monitors a directory for updated model files and begins inference to test the new model.
file structire:
auto_infer_.py
argmax3_.py
./commands/infer.sh
./commands/export.sh
"""

import datetime
import pathlib
import time
from subprocess import call
import os

path = pathlib.Path()
path_res = path.resolve()
path_res_gp = path_res.parent.parent

fname = pathlib.Path(str(path_res_gp)+"/tmp-data-fake/inference_current_best/model.ckpt.data-00000-of-00001")

sleep_time = 20.0

from argmax3label import postprocess #change depending on postprocessing to apply

starttime = time.time()

if os.path.exists('../../tmp-data-fake/inference_current_best/model.ckpt.data-00000-of-00001'):
	mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
else:
	mtime = 0

while True:

	print("tick") #indicate auto inference is checking for updated checkpoint file

	if os.path.exists('../../tmp-data-fake/inference_current_best/model.ckpt.data-00000-of-00001'):
		newmtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
	else:
		newmtime = 0

	#if the new modified time doesn't match previous
	if newmtime != mtime:
		print("File's changed!")
		execution_start_time = time.time()
		rc = call("./export.sh",cwd='../commands/')

		#ensure the previous command has run to completion before this executes.
		rc = call("./infer_154um_IE_binary.sh",cwd='../commands/')

		time.sleep(10)	

		#turns probabilities to segmentation
		postprocess()
		print("--- %s seconds ---" % (time.time() - execution_start_time))

				
	if os.path.exists('../../tmp-data-fake/inference_current_best/model.ckpt.data-00000-of-00001'):
		mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
	else:
		mtime = 0
	
	print(sleep_time - ((time.time() - starttime) % sleep_time))
	time.sleep(sleep_time - ((time.time() - starttime) % sleep_time))
