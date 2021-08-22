

import matplotlib.pyplot as plt
import pandas as pd

def expRes():
	df = pd.read_csv('isface.csv')
	s = df['Expression'].value_counts().rename('Total_Exp')
	s.to_csv('test_exp.csv')
	df1 = pd.read_csv('test_exp.csv')
	df1.columns.values[0] = 'index'
	df1.to_csv('test_exp.csv',index=False)
	df2 =  pd.read_csv('test_exp.csv')
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

	country_data = df2["Total_Exp"]
	medal_data = df2["index"]  
	plt.pie(country_data, labels=medal_data, explode=None, colors=None,autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title("Expressions")
	plt.savefig('pie_exp.png')
	plt.show()
	return num
