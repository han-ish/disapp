from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from .models import Question, Choice, UserData
import datetime

#this function takes care of pages

#to-do
#------
#add the choice
#make it somewhat pretty


def login(request):
	""" This will handle the login page. """
	form = LoginForm()
	return render(request, 'qa/newlogin.html', {'form' : form})

def disclaimer(request):
	""" This will take care of the disclaimer. """
	if request.method == "POST":
		#form = LoginForm(request.POST)
		#form.full_clean()
		#if form.is_valid():
		#	return HttpResponse("the form is valid")
		request.session["usergroup"] = request.POST.get("usergroup", "")
		request.session["email"] = request.POST.get("email", "")
		request.session["gps_data"] = request.POST.get("gpslocation", "")
	#print(request.POST.get("email", ""))
	return render(request, 'qa/disclaimer.html')


def page(request, pg_no):
	""" This will handle the pages """

	# page_no is variable used to pass to the template
	
	#question = Question.objects.get(id=pg_no)
	#count = len(Question.objects.all())
	page_no = int(pg_no) + 1
	#
	#if page_no - 1 > count:
	#	return HttpResponse("This will be final submit page")

	pre_choice = ""
	if request.method == "POST":
		pre_choice = request.POST.get("choice", "")
		key = "q" + str(page_no - 2)
		print(key)
		request.session[key] = pre_choice


	try:
		#question = get_object_or_404(Question, pk=pg_no)
		question = Question.objects.get(pos=pg_no)
	except Question.DoesNotExist:
		#return HttpResponse("This will be the submit page.")
		#test_val = request.session["test"]
		username = request.session["usergroup"]
		email_id = request.session["email"]
		que1 = request.session["q1"]
		que2 = request.session["q2"]
		que3 = request.session["q3"]
		que4 = request.session["q4"]
		que5 = request.session["q5"]
		gps = request.session["gps_data"]
		# adding user data to the database

		user_data = UserData(gps_data=gps, usergroup=username, email=email_id, q1=Question.objects.get(pos=1), q2=Question.objects.get(pos=2), q3=Question.objects.get(pos=3), q4 = Question.objects.get(pos=4), q5 = Question.objects.get(pos=5), c1=que1, c2=que2, c3=que3, c4=que4, c5=que5, submit_date=datetime.datetime.now())
		user_data.save()
		
		data_dict = {'username': username, 'email' : email_id, 'q1' : que1,
				'q2' : que2, 'q3' : que3, 'q4' : que4, 'q5' : que5 }
		context = {'username' : username, 'email' : email_id, 'q1' : que1, 'q2' : que2, 'q3' : que3, 'q4' : que4, 'q5' : que5}
		#context = { 'data_dict' : data_dict }
		return render(request, 'qa/last.html', context)
	
	choices = question.choice_set.all()
	context = {'question' : question, 'pg_no' : pg_no, 'choices' : choices, 'page_no' : page_no, 'error_msg' : "", 'pre_choice' : pre_choice}

	
	#try:
	#	selected_choice = question.choice_set.get(pk=request.POST['choice'])
	#except (KeyError, Choice.DoesNotExist):
	#	context['error_msg'] = "error message"
	#	return render(request, 'qa/pages.html', context)
	return render(request, 'qa/pages.html', context)

from qa.forms import LoginForm
def better(request):
	form = LoginForm()
	return render(request, 'qa/newlogin.html', {'form' : form})

def signup(request):
	return render(request, 'qa/signup.html')
def signin(request):
	return render(request, 'qa/signin.html')
def signout(request):
	return render(request, 'qa/signout.html')


#disclaimer

def disclaimer(request):
	pass
import requests, json
import pprint


#sign-up
def question(request):
	#print request.POST.get("passwd", "")
	email = request.POST.get("email", "")
	pswd = request.POST.get("pswd", "")
	first_name = request.POST.get("first_name", "")

	# creating the user and accepting token
	
	create_url = "http://139.59.13.7/userservice/create/"
        #email = sys.argv[1]
        #passwd = "foobar"
        data = {'email' : email, 'pswd' :pswd, 'details' : {'first_name' : first_name}}
        header_field = {'Content-Type' : 'application/json'}
        create_res = requests.post(create_url, json=data, headers=header_field)
        create_json = json.loads(create_res.content)
        token =  create_json['responseData']['content']['X-Authorization-Token']

	#question_now(request, 1)

	# validating the user token

	validate_url = "http://139.59.13.7/userservice/uservalidation/"
        data = {'email' : email, 'pswd' : pswd, 'remember_me' : 1}
        validate_res = requests.post(validate_url, json=data)
        validate_data = json.loads(validate_res.content)
        token_validated = validate_data['responseData']['content']['X-Authorization-Token']
        #question(token_validated)

	# fetching the questionnaire id

	question_url = "http://139.59.13.7/questionnaire/qlists/"
        header_field = {'Content-Type' : 'application/json', 'X-Authorization-Token' : token_validated}
        question_res = requests.get(question_url, headers=header_field)
        question_data = json.loads(question_res.content)
        print "hello world", question_data
        question_id = question_data['responseData']['questionnaire'][0]['id']

	# fetching question list using question_id

	question_list_url = "http://139.59.13.7/questionnaire/%s/" %(question_id)
        data = {'language' : 'en'}
        question_list_res = requests.get(question_list_url, data, headers=header_field)
        question_list_data = json.loads(question_list_res.content)
        #pprint.pprint(question_list_data)


	#return HttpResponse(question_list_data['responseData']['questionnaire'][0]['name'])

	questions = question_list_data['responseData']['questionnaire'][0]

	#return render(request, 'qa/questions.html', {'question' : questions})

	#return render(request, 'qa/questions.html', {'question' : questions, 'page_no' : 1})

	#question_now(request, 1)

	return render(request, 'qa/signin.html')


# sign-in

# enabled logging

import logging

def signin_now(request):

	#logging.basicConfig(filename='input_log.txt', level=logging.DEBUG)

	email = request.POST.get("email", "")
	pswd = request.POST.get("pswd", "")
	validate_url = "http://139.59.13.7/userservice/uservalidation/"
	data = {'email' : email, 'pswd' : pswd, 'remember_me' : 1}

	#logging.info("email :" + email + "pswd :" +  pswd )
	try:
		validate_res = requests.post(validate_url, json=data)
		validate_data = json.loads(validate_res.content)
		token_validated = validate_data['responseData']['content']['X-Authorization-Token']
	except Exception, e:
		return HttpResponse("something went wrong " + str(e))

	question_url = "http://139.59.13.7/questionnaire/qlists/"
        header_field = {'Content-Type' : 'application/json', 'X-Authorization-Token' : token_validated}
        question_res = requests.get(question_url, headers=header_field)
        question_data = json.loads(question_res.content)
        print "hello world", question_data
        question_id = question_data['responseData']['questionnaire'][0]['id']

        # fetching question list using question_id

        question_list_url = "http://139.59.13.7/questionnaire/%s/" %(question_id)
        data = {'language' : 'en'}
        question_list_res = requests.get(question_list_url, data, headers=header_field)
        question_list_data = json.loads(question_list_res.content)
	questions = question_list_data['responseData']['questionnaire'][0]

        #return render(request, 'qa/questions.html', {'question' : questions, 'page_no' : 1})

	return question_now(request, 0)


#sign-up
def signupp(request):
	email = request.POST.get("email", "")
	pswd = request.POST.get("pswd", "")
	first_name = request.POST.get("first_name", "")

	# creating the user and accepting token

	create_url = "http://139.59.13.7/userservice/create/"
	data = {'email' : email, 'pswd' :pswd, 'details' : {'first_name' : first_name}}

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

	except Exception, e:
		return HttpResponse("something went wrong " + str(e))

	#return render(request, 'qa/questions.html', {'page_no' : 1})

	return question_now(request, 0)

		
def fetch_question(request):
        #print request.POST.get("passwd", "")
        email = request.POST.get("email", "")
        pswd = request.POST.get("pswd", "")
        first_name = request.POST.get("first_name", "")

        # creating the user and accepting token

        #create_url = "http://139.59.13.7/userservice/create/"
        #email = sys.argv[1]
        #passwd = "foobar"
	validate_url = "http://139.59.13.7/userservice/uservalidation/"

	data = {'email' : email, 'pswd' : pswd, 'remember_me' : 1}

	try:
		validate_res = requests.post(validate_url, json=data)

        	data = {'email' : email, 'pswd' :pswd, 'details' : {'first_name' : first_name}}
		validate_data = json.loads(validate_res.content)
        	token_validated = validate_data['responseData']['content']['X-Authorization-Token']
        	#question(token_validated)

        	# fetching the questionnaire id

	except Exception, e:
		return HttpResponse("something went wrong " + str(e))
        question_url = "http://139.59.13.7/questionnaire/qlists/"
        header_field = {'Content-Type' : 'application/json', 'X-Authorization-Token' : token_validated}
        question_res = requests.get(question_url, headers=header_field)
        question_data = json.loads(question_res.content)
        print "hello world", question_data
        question_id = question_data['responseData']['questionnaire'][0]['id']

	question_list_url = "http://139.59.13.7/questionnaire/%s/" %(question_id)
	data = {'language' : 'en'}
	question_list_res = requests.get(question_list_url, data, headers=header_field)
	question_list_data = json.loads(question_list_res.content)

	questions = question_list_data['responseData']['questionnaire']

	#request.session["questions"] = question_list_data['responseData']['questionnaire']

        #return render(request, 'qa/questions.html', {'question' : questions})

	return questions

def question_now(request, page_no):
	pg_no = int(page_no) + 1


	print "hello from question now"

	#question = open("questions.txt", "a+")

	pre_id = 1

	sum_val = 0

	color = "blue"

	#request.session["sum_val"] = 0

 
	if pg_no - 1   == 0:
		questions = fetch_question(request)
		request.session["questions"] = questions
		#request.session["question_count"] = len(questions)

		#print "questions : ", questions[0]

		request.session["sum_val"] = 0


	try:
	#if pg_no - 1 < int(request.session["question_count"]):
		questions = request.session["questions"][pg_no - 1]

		#print "try : ", request.session["questions"]

		#print "question 1", questions

		pre_answer = request.POST.get("choice", "")

		pre_id = request.POST.get("id", "")

		if pg_no - 1 != 0:
			sum_val = fuzzy(pre_answer)

			request.session["sum_val"] = int(request.session["sum_val"]) + int(sum_val)

		#sess_val = request.session["sum_val"]
		#request.session["sum_val"] = sess_val + int(sum_val)

		print "request val : ",request.session["sum_val"]

		#sum_val = fuzzy(pre_answer)

		#sum_val = 0 
		#question.write(questions)
	except Exception, e:
		#question.close()
	#else:
		#return HttpResponse("No more questions" + str(e))

		error = str(e)

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


		return render(request, 'qa/result.html', {'message' : message, 'color' : color})
	print questions


	return render(request, 'qa/questions.html', {'question' : questions, 'page_no' : pg_no, 'pre_answer' : pre_answer, 'pre_id' : pre_id, 'sum_val' : sum_val})

def fuzzy(choice):
        fuzzy_dict = {"no" : 0, 'none' : 0,  'very' : 1, 'some' : 3, 'more' : 3,  'high' : 4, 'yes' : 4,  "don't" : 2, '1' : 1, '2' : 2}
        key = choice.split()[0].lower()
        print key
        return fuzzy_dict[key]
