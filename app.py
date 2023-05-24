# Similarity Score imports
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

import re
import config
# DB imports
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
engine = create_engine("postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres")

# OpenAPI imports
import openai
# setting API_KEY
# Load API key from an environment variable or secret management service

openai.api_key = config.OPENAI_API_KEY


# Establish a connection to the database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mysecretpassword"
)


def listAllRequirements():
    query = "SELECT doc_txt FROM documents"
    # global df
    df  = pd.read_sql_query(query, con=engine)
    df = df.reset_index(drop=True)
    # print("lenth: ", type(df[['doc_txt']]))
    # print(df)
    if len(df) > 0 : 
        return df
    else: 
        return []


# Model Initialization for Similarity Score Calculation
model_name = "sentence-transformers/distilbert-base-nli-stsb-mean-tokens"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)



# sentence: str (argument)
def similarity_score(sentence: str):
    query = "SELECT doc_txt FROM documents"
    df  = pd.read_sql_query(query, con=engine)
    df = df.reset_index(drop=True)

    for i in range(len(df[['doc_txt']])):
        incoming_text = df[['doc_txt']].values.tolist()
        # print("First Element: ",incoming_text[i])
        print("Requirement: ", sentence)
        print("Statements from DB: ", incoming_text[i][0])
        # break
        sentences = [sentence, incoming_text[i][0]]
        encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors="pt")
        with torch.no_grad():
            model_output = model(**encoded_input).last_hidden_state
        
        similarity = cosine_similarity(model_output[0], model_output[1])[0][0]
        print("Similarity Score: ", similarity)
        # score.append(similarity)

        if similarity > 0.75:
            return [True,False,"","",""]

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',            
            messages=[
            {"role": "system", "content": "You are a helpful chatbot that detects and resolves conflicts in requirements engineering. The system will detect conflicts between two requirements according to these rules: 1) Incompatible requirements, where it is challenging to achieve these requirements at the same time due to conflicting objectives, restrictions, or assumptions. 2) Contradictory requirements can lead to another type of conflict when they state opposing or mutually exclusive conditions or outcomes. In this context, conflicts arise since it is impossible to implement both requirements simultaneously. Your answer should be True when one or both of these rules are satisfied otherwise the answer should be False"},
            {"role": "user", "content": "R1: The system should be able to store data indefinitely. VS R2: The system should automatically delete data after a set time period."},
            {"role": "assistant", "content": "True. These two requirements are contradictory. Possible Solution: A possible solution to this conflict could be to define a policy for data retention that specifies how long the data should be stored based on business or legal requirements. For example, the system could be configured to store data for a specific period, such as three years, after which the data is automatically deleted."},
            {"role": "user", "content": "R1: the system must play the selected movie automatically after it is selected from the list. VS R2: the system must start playing the movie within one second of the selection."},
            {"role": "assistant", "content": "True. These two requirements are incompatible. Possible Solution: Playing the movie automatically would violate the requirement to start playing it within one second, where the potential conflicts were between functionality and efficiency. To partially meet both requirements, the chatbot suggested delaying the automatic playing of the movie by one second. This solution allowed the system to start playing the movie within the specified time frame while still meeting the requirement for automatic playback."},
            {"role": "user", "content": "R1: The system should support multiple languages VS R2: The system should enable users to store their progress."},
            {"role": "assistant", "content": "False. These two requirements have no conflict with each other."},
            {"role": "user", "content": "R1: {} VS R2: {}".format(sentence, incoming_text[i][0])},
            ])
        message = response.choices[0]['message']
        msg = message['content']
        print(msg)
        val = re.search("false|true", message['content'], re.IGNORECASE)
        val = val.group()
        print("val: {}".format(val))
        if val == "True":
            return [False,True,msg,sentence,incoming_text[i][0]]  

    return [False, False, "","",""]


def insert_sentence(sentence: str):
    # Create a cursor object
    cur = conn.cursor()

    # query = "INSERT INTO documents (doc_txt) VALUES ('{}')".format(sentence)
    query = f"INSERT INTO documents (doc_txt) VALUES ('{sentence}')"
    # df  = pd.read_sql_query(query, con=engine)
    print("Value Inserted")

    # Execute the query
    cur.execute(query)

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    # cur.close()
    # conn.close()


# listAllRequirements()
# similarity_score("the system should be able to let the user have a authentication mechanism")

# CREATE TABLE documents (
#     id SERIAL PRIMARY KEY,
#     date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#     doc_txt TEXT
# );


# Insert Query

# INSERT INTO documents (doc_txt)
# VALUES ('This is an example text value');


# INSERT INTO documents (doc_txt)
# VALUES 
# ('The system should allow users to save their work'),
# ('The system should enable users to store their progress'),
# ('The system should enable users to collaborate'),
# ('The system should be reliable'),
# ('The system should allow users to organize their data'),
