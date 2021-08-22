import matplotlib.pyplot as plt
import pandas as pd

def faceRes():
	df = pd.read_csv('isFace.csv')
	s = df['person'].value_counts().rename('Total_Face')
	s.to_csv('test_Face.csv')
	df1 = pd.read_csv('test_Face.csv')
	df1.columns.values[0] = 'index'
	df1.to_csv('test_Face.csv',index=False)
	df2 =  pd.read_csv('test_Face.csv')
	# df.to_frame()
	# df.rename(columns={'':'index'}, inplace=True)
	num = df2.shape[0]

	if(num==2):
		colors = ["#1f77b4", "#ff7f0e"]
		explode = (0, 0)
	elif(num==3):
		colors = ["#1f77b4", "#ff7f0e","#ffffff"]
		explode = (0, 0, 0)
	elif(num==4):
		colors = ["#1f77b4", "#ff7f0e","#ffffff", "#000000"]
		explode = (0, 0, 0, 0)
	elif(num==5):
		colors = ["#1f77b4", "#ff7f0e","#ffffff", "#000000","#ff7f01"]
		explode = (0, 0, 0, 0, 0)
	elif(num==6):
		colors = ["#1f77b4", "#ff7f0e","#ffffff", "#000000","#ff7f01","#ff7f02"]
		explode = (0, 0, 0, 0, 0, 0)
	country_data = df2["Total_Face"]
	medal_data = df2["index"]
	plt.pie(country_data, labels=medal_data, explode=None, colors=None,autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title("Faces:")
	plt.savefig('pose_trial.png')
	plt.show()
	return num
