# Conflict-Detection-Chatbot




1-Chatbot Setup: 

The chatbot, developed using the Rasa platform (https://rasa.com/docs/rasa/), enables real-time detection of conflicts.
The project folder includes the different types of training data (data folder) that go into a Rasa assistant and how this training data is structured.
After each user message, the model will predict an action that the assistant should perform next (Action folder).
To set up the chatbot :
* Download and configure the Docker compose. It represents a valuable tool for defining and executing multi-container applications. The tool is used to handle two containers:
a PostgreSQL database container and an Adminer container. To set up the PostgreSQL container, configure it with environment variables for username, password, and database name. The Adminer container, on the other hand, provided a web-based management tool. Together, these containers allowed the Rasa chatbot to interact with
the PostgreSQL database, while the Adminer interface provided an efficient way to manage and administer the database. 
* Configure this line of code as follows in app.py file:
import psycopg2
engine = create_engine("postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres")

* Configure the API for open ai in the file config.py

2-Example of the ChatGPT prompt: 
You can change or update the prompt in the messages variable in file app.py as described

![image](https://github.com/Geokiss/Conflict-Detection-Chatbot/assets/134546067/5d5126f5-7e52-454f-9a09-e1ac0837231f)




3- Rasa Commands:
After installing rasa in your local computer here are some important terminal commands:


Activating the Environment:
•	Navigate to the folder where env folder is present, then type:
env\Scripts\activate

Rasa Commands:
To interact with chatbot using terminal:
•	First navigate to the folder where the all the rasa files are present, activate the environment, then type:
rasa shell --debug

To interact with chatbot using the interface:
•	First navigate to the folder where the all the rasa files are present, activate the environment, then type:
rasa run -m models --enable-api --cors "*" --debug

To start Action Server:
•	Open a new Terminal, activate the environment, and then type:
rasa run actions


Docker Commands:
To run docker-compose.yml file:
•	First navigate to the folder where the file is present, then type:
docker-compose up -d

To stop docker-compose.yml file:
docker stop $(docker ps -a -q)

To remove docker-compose.yml file:
docker rm $(docker ps -a -q)



Database Queries:
•	Create a table in the Database:

CREATE TABLE documents (
id SERIAL PRIMARY KEY,
date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
doc_txt TEXT
);



* Insert a row in the Database:
INSERT INTO documents (doc_txt)
VALUES 
('The system should allow users to save their work')



4- Datasets for experiment
To work with the datasets that applied in the experiment please refer to this link:
https://github.com/Geokiss/Conflict-Detection-Chatbot/blob/main/datasets.zip
