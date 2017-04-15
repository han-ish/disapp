import requests
import json
import pprint
import datetime
import sys


def create():
	create_url = "http://139.59.13.7/userservice/create/"
	email = sys.argv[1]
	passwd = "foobar"
	data = {'email' : email, 'pswd' : passwd, 'details' : {'first_name' : 'foo'}}
	header_field = {'Content-Type' : 'application/json'}
	create_res = requests.post(create_url, json=data, headers=header_field)
	create_json = json.loads(create_res.content)
	token =  create_json['responseData']['content']['X-Authorization-Token']
	#question(token)
	validate(email, passwd)
	#question(token)


def validate(email, passwd):
	validate_url = "http://139.59.13.7/userservice/uservalidation/"
	data = {'email' : email, 'pswd' : 'foobar', 'remember_me' : 1}
	validate_res = requests.post(validate_url, json=data)
	validate_data = json.loads(validate_res.content)
	token_validated = validate_data['responseData']['content']['X-Authorization-Token']	
	question(token_validated)

def question(token_validated):
	question_url = "http://139.59.13.7/questionnaire/qlists/"
	header_field = {'Content-Type' : 'application/json', 'X-Authorization-Token' : token_validated}
	question_res = requests.get(question_url, headers=header_field)
	question_data = json.loads(question_res.content)
	print "hello world", question_data
	question_id = question_data['responseData']['questionnaire'][0]['id']

	#question_id = 'Q1'
	
	question_list_url = "http://139.59.13.7/questionnaire/%s/" %(question_id)
	data = {'language' : 'en'}
	question_list_res = requests.get(question_list_url, data, headers=header_field)
	question_list_data = json.loads(question_list_res.content)

	answer_url = "http://139.59.13.7/questionnaire/answers/"

	answers = {"language" : "en", "questionnaire_id" : "Q1", "answer_list" : [{"1" : ["very little"]}, {"2" : ["no"]}, {"3" : ["don't know"]}]}


	pprint.pprint(question_list_data)

	response = requests.post(answer_url, headers=header_field, data=json.dumps(answers))

	print response.text

if __name__ == '__main__':
	create()


