from utils.data.file_reader import CSV_Reader as CSV_Reader
import ast
import pandas as pd
import os 
import uuid
import shutil

csv_file= '/Users/debraji/Downloads/faceLandmarks.csv'
#csv_file='/Users/debraji/Documents/faceLandmarks.csv'
csv_data = CSV_Reader(csv_file, excel=False)
data_dicts = []

'''
for row in csv_data:
	diction = ast.literal_eval(row['f_json'])
	if len(diction['faces']) > 0:
		for key in diction['faces'][0]['landmark']:
			row[key] = diction['faces'][0]['landmark'][key]

	print row.keys()
	data_dicts.append(row)

df = pd.DataFrame.from_dict(data_dicts)

df.to_csv("faceLandmarks_reformatted.csv")
'''
count = 0
for row in csv_data:
	for filename in os.listdir("/Users/debraji/Downloads/allPPB_original_renamed"):
		if filename == row['avg.path'].replace('allPPB/', ''):
			hash=str(uuid.uuid1())
			count+=1
			new_name='%04d'%count+'_'+row['fitz']+'_'+row['gender']+'_'+row['country']+'.jpg'
			
			src_file="/Users/debraji/Downloads/allPPB_original_renamed/"+filename
			dst_dir = "/Users/debraji/Downloads/PPB-2/"
			full_filename= dst_dir+filename
			full_new_name = dst_dir+new_name
			shutil.copy(src_file,dst_dir)
			os.rename(full_filename, full_new_name)
			print new_name

	



