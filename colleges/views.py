import re
from django.shortcuts import render, redirect
import os
from os import listdir
from os.path import isfile, join
import pickle
from sign_in.models import Profile
from django.http import HttpResponse
from .models import College
from .forms import CollegeForm



#def predictor(student):
#	to_test = student
#	settings_dir = os.path.dirname(__file__)
#	PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
#	mypath = PROJECT_ROOT + '/'
#	all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#	colleges = []
	##loaded_model = pickle.load(open(mypath + file, 'rb'))
	##result = loaded_model.predict(to_test)

	#pickled_model = pickle.load(open('model.pkl', 'rb'))

	#for file in all_files:
	#	with open(file,'rb') as f:
	#		model=pickle.load(f)
	#		result=model.predict(to_test)
	#		if (int)(0.5 * result[0] + 0.5) >= 0.6:
	#			name = ''
	#			i = 0
	#			while file[i] != '.':
	#				name += file[i]
	#				i += 1
	#			colleges.append(name)
	#return colleges

def predictor(student):
	to_test = student
	settings_dir = os.path.dirname(__file__)
	PROJECT_ROOT = os.path.abspath(os.path.join(settings_dir, os.pardir))
	mypath = PROJECT_ROOT + '/'

	colleges = []

	for file in os.listdir(mypath):
		if file.endswith('.sav'):
			print('found')
			with open(os.path.join(mypath, file), 'rb') as f:
				model = pickle.load(f)
				print(to_test)
				result = model.predict(to_test)
				print(result)
				if result >= 0.5:
					name = re.findall(r'(.*)(?=\.sav)', file)
					colleges.append(name[0])
	print(colleges)
	return colleges



def checker(user):	
	profile = Profile.objects.get(user = user)
	possible_colleges = predictor([[profile.gre, profile.cgpa]])

	college_list = []

	for college in possible_colleges:
		college_details = College.objects.get(name = college)
		college_list.append(college_details)

	return college_list


def add_college(request):
	if request.user.is_authenticated and request.user.is_superuser:
		if request.method == "POST":
			college_form = CollegeForm(request.POST)

			if college_form.is_valid():
				college_form.save()
				return redirect('colleges:add')
		else:
			college_form = CollegeForm()
		return render(request, 'colleges/add.html', {'college_form': college_form})

def search(request):
	print('in search')

	if request.user.is_authenticated:
		user = request.user
		colleges = checker(user)
		colleges_copy = []
		colleges_copy1 = []

		maxCost = location = None
		
		maxCost = request.POST.get('maxRange')
		location = request.POST.get('location')
		print(maxCost, location)
		if maxCost is None and location is None:
			colleges_copy = colleges

		elif maxCost is not None and location is None:
			maxCost = (int)(maxCost)
			for college in colleges:
				if college.average_cost >= maxCost:
					colleges_copy.append(college)

		elif maxCost is None or maxCost is '' and location is not None:
			for college in colleges:
				if location.lower() in college.location.lower():
					colleges_copy.append(college)

		elif maxCost is not None and location is not None:
			maxCost = (int)(maxCost)
			for college in colleges:
				if college.average_cost <= maxCost:
					colleges_copy1.append(college)

			for college in colleges_copy1:
				if location.lower() in college.location.lower():
					colleges_copy.append(college)
			#print(colleges_copy)
			if colleges_copy is None:
				print("colleges_copy is None")
			else:
				colleges_copy = College.objects.all()
				return render(request, 'colleges/college_list.html', {'colleges_copy': colleges_copy})
			print(colleges_copy)
	#else:
	#	colleges_copy = College.objects.all()
			
		

		return render(request, 'colleges/college_list.html', {'colleges_copy': colleges_copy})
	return redirect('login')



#def filter(request):
#	maxCost = request.POST.get('maxRange')
#	location = request.POST.get('location')
	
#	if maxCost==None and location==None:
#		display();