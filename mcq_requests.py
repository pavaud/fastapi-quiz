import requests
from pprint import pprint
import json

if __name__ == '__main__':
    

    #########################################################
    # GET /mcq
    #########################################################

    auth=('clementine', 'mandarine')

    print("# GET /mcq")

    # without parameters
    url = 'http://127.0.0.1:8000/mcq'
    response = requests.get(url=url,auth=auth)
    print('response without parameters :\n', response.json())

    # without credentials
    subjects_list=['BDD','Systèmes distribués','Docker']
    subjects = '&subjects='.join(subjects_list)
    url = 'http://localhost:8000/mcq?subjects='+ subjects + '&use=Test de positionnement&nb=5'
    response = requests.get(url=url)
    print('\nresponse without credentials :\n', response.json())

    # with wrong parameter
    subjects_list=['Systèmes']
    subjects = '&subjects='.join(subjects_list)
    url = 'http://localhost:8000/mcq?subjects='+ subjects + '&use=Test de positionnement&nb=5'
    response = requests.get(url=url,auth=auth)
    print('\nresponse with wrong parameter :\n', response.json())

    # with all needed
    subjects_list=['BDD','Systèmes distribués','Docker']
    subjects = '&subjects='.join(subjects_list)
    url = 'http://localhost:8000/mcq?subjects='+ subjects + '&use=Test de positionnement&nb=5'
    response = requests.get(url=url,auth=auth)
    print('\nresponse with all needed :\n')
    pprint(response.json(), sort_dicts=False)


    #########################################################
    # POST /add_mcq
    #########################################################

    auth=('admin', '4dm1N')
    auth_wrong=('alice', 'wonderland')

    data_full = {
        "question": "Quelle est la couleur du cheval blanc d Henri IV ?",
        "subject": "Classification",
        "use": "Test de positionnement",
        "correct": "B",
        "responseA": "jaune",
        "responseB": "blanc",
        "responseC": "noir",
        "responseD": "la reponse D",
        "remark": ""
    }

    data_missing = {
        "question": "Quelle est la couleur du cheval blanc d Henri IV ?",
        "subject": "Classification",
        "use": "Test de positionnement",
        "responseB": "blanc",
        "responseC": "noir",
        "responseD": "la reponse D",
        "remark": ""}

    print("\n# POST /add_mcq")

    # with data missing required fields
    url = 'http://localhost:8000/add_mcq'
    response = requests.post(url=url,auth=auth,json=data_missing)
    print('\nresponse with data missing required fields :\n')
    pprint(response.json(), sort_dicts=False)

    # without credentials
    url = 'http://localhost:8000/add_mcq'
    response = requests.post(url=url,json=data_full)
    print('\nresponse without credentials :\n', response.json())
    
    # without wrong credentials
    url = 'http://localhost:8000/add_mcq'
    response = requests.post(url=url,auth=auth_wrong, json=data_full)
    print('\nresponse with wrong credentials :\n', response.json())

    # with all needed
    url = 'http://localhost:8000/add_mcq'
    response = requests.post(url=url,auth=auth,json=data_full)
    print('\nresponse with all needed :\n')
    pprint(response.json(), sort_dicts=False)
    with open('questions.csv','r') as f:
        lines = f.readlines()
        print("\nla dernière ligne de questions.csv est maintenant:")
        print(lines[-1])


    #########################################################
    # GET /api_status
    #########################################################

    auth=('admin', '4dm1N')
    auth_wrong=('alice', 'wonderland')

    print("\n# GET /api_status")

    # with wrong credentials
    url = 'http://localhost:8000/api_status'
    response = requests.get(url=url,auth=auth_wrong)
    print('\nresponse with wrong credentials :\n', response.json())
    
    # with all needed credentials
    url = 'http://localhost:8000/api_status'
    response = requests.get(url=url,auth=auth)
    print('\nresponse with all needed :\n', response.json())
    