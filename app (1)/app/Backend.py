import time
import os
from Database import *
from config import initialize_config
import openai
import json
install()
client = openai.OpenAI(api_key='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')
config=initialize_config("C:\\Users\\Tobe\\Judah project\\app\\data")
def getID(info_txt_path):
    with open(info_txt_path, "r") as info_txt:
        info_content = info_txt.read()
    
    # Update records
    ID = int(info_content[:20])
    next_id = str(ID + 1) + (20 - len(str(ID))) * ' '
    info_content = next_id + info_content[20:]
    
    with open(info_txt_path, "w") as info_txt:
        info_txt.write(info_content)
        
    return ID

def Uploadfile(user, category,name, content):
    contentpath = config.content_path
    sourceinfo_txt_path = os.path.join(config.info_txt_path, "source_info.txt")
    ID = getID(sourceinfo_txt_path)
    # Save files
    with open(contentpath + str(ID) + '.txt', "w") as content_file:
        content_file.write(content)
    print(3)
    DBupload("Filesmanager", [ID,name, time.time(), user, "'" + contentpath + str(ID) + ".txt'", True])
    return ID

def Generatesum(ID, category,user):
    summarypath = config.summary_path
    suminfo_txt_path = os.path.join(config.info_txt_path, "sum_info.txt")
    sum_id = getID(suminfo_txt_path)
    
    sf = DBretrieve('Filesmanager', ["filepath"], ["id", ID])[0][0][:-1][1:]
    with open(sf, "r") as sf:
        print(sf)
        sf_content = sf.read()
    if category:
            prompt = f"""
        Instructions:

        Read the entire document carefully.
        Identify all the key points, arguments, and main ideas presented.
        For each key point or idea, create a concise bullet point.
        Ensure each bullet point is brief, clear, and captures the essence of the point without additional detail.
        Do not include extraneous information; focus only on the core elements.
        Organize the bullet points in the same order as they appear in the document for easy reference.:
        document:
        dont add any unnecessary sentence just return the summary dont even add a topic  
        {sf_content}
        """
    else:
        prompt = f"""
        Create a a full summary on the following content:
        {sf_content}

       """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates quizzes based on provided content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096  
    )
    summary = response.choices[0].message.content    
    # Save summary
    with open(summarypath + str(sum_id) + ".txt", "w") as summarycontent:
        summarycontent.write(summary)
    
    DBupload('summaries', [str(sum_id), str(ID), category, time.time(), "'" + summarypath + str(sum_id) + ".txt'", 'True',user])
    return sum_id

def Generatequiz(ID,userid, subtext=None):
    source_path = os.path.join(config.content_path, f"{ID}.txt")
    
    with open(source_path, "r") as sf:
        sf_content = sf.read()
    if subtext:
        types="sub"
        prompt = f"""
        Create a quiz based on{subtext}the following content:
        {sf_content}

        The quiz should contain:
        - A title
        - A brief introduction
        - Multiple-choice questions (at least 10)
        - Each question should have 4 options, with one correct answer clearly indicated
        -sturcture the response in a dictionary with this schemaj ["name":a,"num_questions":b,"questions":[[ "Questiontxt": "What is the capital of France?", "wrongoption": ["Berlin", "Madrid", "Rome"], "correctoption": "Paris"],...]]
        """
    else:
        types="full"
        prompt = f"""
        Create a quiz based on the following content:
        {sf_content}

        The quiz should contain:
        - A title
        - A brief introduction
        - Multiple-choice questions (at least 20)
        - Each question should have 4 options, with one correct answer clearly indicated
        -sturcture the response in a dictionary with this schemaj ["name":a,"num_questions":b,"questions":[[ "Questiontxt": "What is the capital of France?", "wrongoption": ["Berlin", "Madrid", "Rome"], "correctoption": "Paris"],...]]
        note the structure should always be this with no additional text so i can just parse the response in json
        """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates quizzes based on provided content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500  
    )
    quiz = response.choices[0].message.content  
    quiz_data=json.loads(quiz[quiz.index('{'):])

    # Upload the quiz to the database
    quizinfo_txt_path = os.path.join(config.info_txt_path, "quiz_info.txt")
    quiz_id = getID(quizinfo_txt_path)  
    
    DBupload('Quizlet', [quiz_id,int(ID), quiz_data['name'], time.time(), 0, quiz_data['num_questions'], types, True, userid])

    for question in quiz_data["questions"]:
        DBupload('Questions', [None, question['Questiontxt'], str(question['wrongoption']), question['correctoption'], quiz_id])

    return quiz_id

def questions(quizid):
    question = []
    quizdata = DBretrieve('Questions', [ "Questiontxt", "wrongoption", "correctoption"], ["Quizlet_id", quizid])
    
    for i in quizdata:
        quizpath = config.quiz_path + str(i[0]) + ".txt"
        with open(quizpath, "r") as quiz_file:
            quiz_content = quiz_file.read().split('__')
            question.append(quiz_content)
    return question

