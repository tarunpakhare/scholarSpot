import re
from django.core.cache import cache
import joblib
import pandas as pd
import pickle
import os
import numpy as np

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))

pathname = PROJECT_ROOT + '/colleges'
files = os.listdir(pathname)

col_names=['Gre','Cgpa','Got_in']
for datasheet in files:
	if(datasheet=='Richmond Scholars Program.csv'):
		break
	df = pd.read_csv(pathname + '/' + datasheet, sep=','  ,names=col_names)
	#x=df[['Gre','Cgpa']]
	#y=df[['Got_in']]
	x=df.iloc[1:,0:2].values
	y=df.iloc[1:,2:3].values

	filename = ''
	i = 0
	while datasheet[i] != '.':
		filename += datasheet[i]
		i += 1

	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 0)
	#print(X_train,y_train)
	

	#X_train=re.findall('Gre',X_train)

	from sklearn.linear_model import LinearRegression
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)

	filename = filename  + '.sav'
	with open(filename, 'wb') as f:
		pickle.dump(regressor,f)
	
	#with open(filename,'rb') as f:
	#	model=pickle.load(f)
	#a = model.predict(X_test)
	#print(a)