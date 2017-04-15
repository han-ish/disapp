from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
import datetime

# take a look at the urls.py file for more information about how pages as handled

# signup page
def signup(request):
	"""This function will take care of rendering the signup page"""

	return render(request, 'qa/signup.html')

# login page
def signin(request):
	"""This function will take care of rendering the signin page"""

	#return render(request, 'qa/signin.html')
	return render(request, 'qa/new__signin.html')

def signout(request):
	"""This function will take care of rendering the signout page and uploading the feedback to backend"""


	token = request.session["token"]

	f_id = request.session["feed_id"]

	feedback_answer_url = "http://139.59.13.7/questionnaire/answers/"

	header_field = {'Content-Type' : 'application/json', 'X-Authorization-Token' : token}

	answer_list = []

	for i in range(1,4):    # use dynamic indexing when adding more feedback questions
		answer = request.POST.get("choice" + str(i), "")
		qid = request.POST.get("id" + str(i), "")
		answer_list.append({qid : [answer]})

	qid = request.POST.get("id4", "")
	answer = request.POST.get("text", "")

	answer_list.append({qid : [answer]})


	answer_data = {"language" : "en", "questionnaire_id" : f_id, "answer_list" : answer_list}

	form_answer = requests.post(feedback_answer_url, headers=header_field, data=json.dumps(answer_data))

	return render(request, 'qa/signout.html', {'message' : form_answer.content, 'answer_data' : answer_data})


#disclaimer
import requests, json

#import logging
# should enable logging
def signin_check(request):
	"""This function will take care of rendering the disclaimer page and also checking for authentication"""


	email = request.POST.get("email", "invalid")
	pswd = request.POST.get("pswd", "pass")
	location = request.POST.get("location", "0.0")
	request.session["loc"] = location.replace(" ", ",")	# trying a replace
	validate_url = "http://139.59.13.7/userservice/uservalidation/"
	data = {'email' : email, 'pswd' : pswd, 'remember_me' : 1}

	#f = open("locations.txt", "w")
	#f.write("hello world")
	#f.close()

	try:
		validate_res = requests.post(validate_url, json=data)
		validate_data = json.loads(validate_res.content)
		token_validated = validate_data['responseData']['content']['X-Authorization-Token']

		# saving token

		request.session["token"] = token_validated
	except Exception as e:

		error = "Invalid email id  or password"

		return render(request, 'qa/signin.html', {'error' : error })

	#question_url = "http://139.59.13.7/questionnaire/qlists/"
        #header_field = {'Content-Type' : 'application/json', 'X-Authorization-Token' : token_validated}
        #question_res = requests.get(question_url, headers=header_field)
        #question_data = json.loads(question_res.content)
        #question_id = question_data['responseData']['questionnaire'][0]['id']

        # fetching question list using question_id

        #question_list_url = "http://139.59.13.7/questionnaire/%s/?language=en&location=%s/" %(question_id, location)
        #data = {'language' : 'en'}
        #question_list_res = requests.get(question_list_url, data, headers=header_field)
        #question_list_data = json.loads(question_list_res.content)
	#questions = question_list_data['responseData']['questionnaire'][0]

	return render(request, 'qa/disclaimer.html')

def claim(request):
	"""This function will return the question list"""

	return question_now(request, 0)

def prevent(request):
	"""This function will take care of rendering the prevention page"""

	return render(request, 'qa/prevent.html')

#sign-up
def signupp(request):
	"""This function will take care of authenticating the user after a signup and also handles rendering the disclaimer page"""

	email = request.POST.get("email", "invalid")
	pswd = request.POST.get("pswd", "unknown")
	first_name = request.POST.get("first_name", "")

	location = request.POST.get("location", "0.0")

	mob_no = request.POST.get("mobile", "")

	org = request.POST.get("org", "NA")

	request.session["loc"] = location.replace(" ", ",")

	pin = request.POST.get("pin", "")


	# creating the user and accepting token

	create_url = "http://139.59.13.7/userservice/create/"
	data = {'email' : email, 'pswd' :pswd, 'details' : {'first_name' : first_name, 'location' : location, 'pincode' : pin, 'mobile_no' : mob_no, 'organization' : org}}

	header_field = {'Content-Type' : 'application/json'}
	try:
		create_res = requests.post(create_url, json=data, headers=header_field)
		create_json = json.loads(create_res.content)

		token =  create_json['responseData']['content']['X-Authorization-Token']
		
		validate_url = "http://139.59.13.7/userservice/uservalidation/"
        	data = {'email' : email, 'pswd' : pswd, 'remember_me' : 1}
        	validate_res = requests.post(validate_url, json=data)
        	validate_data = json.loads(validate_res.content)
        	token_validated = validate_data['responseData']['content']['X-Authorization-Token']

		# saving token

		request.session["token"] = token_validated




	except Exception as e:


		error = "email id  already exist"
		return render(request, 'qa/signup.html', {'error' : error})

	return render(request, 'qa/disclaimer.html')

		
def fetch_question(request):
	"""This function will take care of fteching the questions"""

        email = request.POST.get("email", "")
        pswd = request.POST.get("pswd", "")
        first_name = request.POST.get("first_name", "")

        # creating the user and accepting token
	#validate_url = "http://139.59.13.7/userservice/uservalidation/"

	#data = {'email' : email, 'pswd' : pswd, 'remember_me' : 1}

	try:
		#validate_res = requests.post(validate_url, json=data)

        	#data = {'email' : email, 'pswd' :pswd, 'details' : {'first_name' : first_name}}
		#validate_data = json.loads(validate_res.content)
        	#token_validated = validate_data['responseData']['content']['X-Authorization-Token']
		
		token_validated = request.session["token"]
        	# fetching the questionnaire id

	except Exception as e:
		return HttpResponse("something went wrong " + str(e))

	location = request.session["loc"]

        question_url = "http://139.59.13.7/questionnaire/qlists/"
        header_field = {'Content-Type' : 'application/json', 'X-Authorization-Token' : token_validated}
        question_res = requests.get(question_url, headers=header_field)
        question_data = json.loads(question_res.content)
        question_id = question_data['responseData']['questionnaire'][0]['id']

	question_list_url = "http://139.59.13.7/questionnaire/%s/?language=en&location=%s" %(question_id, location)


	#print(location)	# testing for location send


	data = {'language' : 'en'}
	question_list_res = requests.get(question_list_url, data, headers=header_field)
	question_list_data = json.loads(question_list_res.content)

	questions = question_list_data['responseData']['questionnaire']

	return questions

def question_now(request, page_no):
	"""This function will take care of handling the question page and result page. And also is responsible for handling the answers and determining the result of the fuzzy logic"""

	pg_no = int(page_no) + 1

	sum_val = 0

	color = "blue"

 
	if pg_no - 1   == 0:
		questions = fetch_question(request)
		request.session["questions"] = questions

		request.session["sum_val"] = 0

		request.session["answers"] = {"language" : "en", "questionnaire_id" : "Q1", "answer_list" : []}

	try:
		questions = request.session["questions"][pg_no - 1]

		pre_answer = request.POST.get("choice", "")

		pre_id = request.POST.get("id", "")


		# collecting answers


		if pg_no - 1 != 0:
			request.session["answers"]["answer_list"].append({pre_id : [pre_answer]})
			sum_val = fuzzy(pre_answer)

			request.session["sum_val"] = int(request.session["sum_val"]) + int(sum_val)

	except Exception as e:

		pre_answer = request.POST.get("choice", "")

		pre_id = request.POST.get("id", "")

		request.session["answers"]["answer_list"].append({pre_id : [pre_answer]})


		# sending answers

		validated_token = request.session["token"]

		headers = {'Content-Type' : 'application/json', 'X-Authorization-Token' : validated_token}

		answer_url = "http://139.59.13.7/questionnaire/answers/"

		cooked_data = request.session["answers"]

		# testing location

		location = request.session["loc"]

		response = requests.post(answer_url, headers=headers, data=json.dumps(cooked_data))


		error = str(e)

		


		answers = request.session["answers"]


		total = request.session["sum_val"] + int(fuzzy(request.POST.get("choice", "")))

		# fuzzy interpretation

		if total <= 3 :
			message = "very low"
			color = "greentext"
		elif total <= 7:
			message = "low"
			color = "greentext"
		elif total <= 11:
			message = "medium"
			color = "redtext"
		elif total <= 15:
			message = "high"
			color = "redtext"
		elif total <= 19:
			message = "very high"
			color = "redtext"


		request.session["sum_val"] = 0


		return render(request, 'qa/result.html', {'message' : message, 'color' : color, 'location' : location})


	return render(request, 'qa/questions.html', {'question' : questions, 'page_no' : pg_no, 'pre_answer' : pre_answer, 'pre_id' : pre_id, 'sum_val' : sum_val})

def fuzzy(choice):
	"""This function is responsible for returning the pre-determined value of fuzzy logic"""

        fuzzy_dict = {"no" : 0, 'none' : 0,  'very' : 1, 'some' : 3, 'more' : 3,  'high' : 4, 'yes' : 4,  "don't" : 2, '1' : 1, '2' : 2}
        key = choice.split()[0].lower()
        return fuzzy_dict[key]


def fetch_form(request):
	"""This function will be responsible for fetching the form tags for the feedback form"""

	feedback_url = "http://139.59.13.7/questionnaire/flists/"

	token = request.session["token"]

	headers = {'Content-Type' : 'application/json', 'X-Authorization-Token' : token}

	feedback = requests.get(feedback_url, headers=headers)

	feedback_data = json.loads(feedback.content)


	f_id = feedback_data['responseData']['questionnaire'][0]['id']

	feed_form_url = "http://139.59.13.7/questionnaire/%s/" %(f_id)

	request.session["feed_id"] = f_id

	form_data = requests.get(feed_form_url, headers=headers)

	form = json.loads(form_data.content)

	form_list = form['responseData']['questionnaire']


	return render(request, 'qa/feedback.html', {'questions' : form_list})


