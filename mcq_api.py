import json
from fastapi import FastAPI, Depends, Query, HTTPException
from pydantic import BaseModel
from typing import List
from mcq_utils import get_user, get_admin, get_uses, get_subjects, get_random_mcq


# INIT

api = FastAPI(title="MCQ API",
              description="MCQ API return Multiple Choice Questions from a database based on a subject and a type of question",
              version="1.0.0")


class MCQ(BaseModel):
    """
    a multiple choice question in the database
    """
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: str | None = None
    remark: str | None = None


# ENDPOINTS

@api.get('/mcq', tags={'mcq'})
async def get_mcq(username: str = Depends(get_user), 
                  subjects: List[str] = Query(default='BDD', description="Choose a subject : " + ','.join(get_subjects())), 
                  use : str = Query(default='Test de positionnement', description="Choose a use : " + ','.join(get_uses())), 
                  nb : int = Query(default=5, description="Choose number of questions :  5, 10 or 20")):
    """
    Returns a list of questions given a subject, use and number of questions in unordered fashion
    """

    if set(subjects).issubset(set(get_subjects())) and \
        use in get_uses() and \
            nb in [5,10,20]:
            
            questions = get_random_mcq(subjects,use,nb)
            return {'username': username,
                    'authorization': 'Basic',
                    'Number of questions': len(questions),
                    'Use': use,
                    'Subjects': subjects,
                    'Questions': json.loads(questions.to_json(orient='index'))}
    else:
        raise HTTPException(
                status_code=400,
                detail='Bad Request : One or more parameter not valid'
            )



@api.post('/add_mcq', tags={'admin'})
async def post_mcq(mcq: MCQ, username: str = Depends(get_admin)):
    """
    Write a multiple choice question in the database and returns acknowledgment 
    """

    mcq_values = [str(i[1]) for i in mcq]
    try:
        with open('questions.csv','a') as f:
            f.write(','.join(mcq_values)+'\n')
            #f.write('\n')
                
        return {'username': username,
                'authorization': 'Basic',
                'Question inserted': True,
                'Question': mcq}
    except FileNotFoundError:
        return {'Error':'File not found'}


@api.get('/api_status', tags={'admin'})
async def get_api_status(username: str = Depends(get_admin)):
    """
    Returns API status
    """

    return {'status':'API working'}

