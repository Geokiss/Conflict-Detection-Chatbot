# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk.events import Restarted
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from app import listAllRequirements, similarity_score, insert_sentence

class ActionListRequirements(Action):

    def name(self) -> Text:
        return "action_list_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        req = listAllRequirements()
        if req is None:
            dispatcher.utter_message(text="the list is empty")
        # req = req.to_html()
        dispatcher.utter_message(str(req['doc_txt']))
        # dispatcher.utter_message(req)


        return []


class ActionRestart(Action):

  def name(self) -> Text:
      return "action_restart"

  async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
  ) -> List[Dict[Text, Any]]:

      return [Restarted()]


class ActionAddRequirement(Action):


    def name(self) -> Text:
        return "action_add_requirement"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        requirement = tracker.latest_message['text']
        isSimilar, isConflict, msg, requirment1, requirment2 = similarity_score(requirement)
        print("Action Server Score: ", isSimilar)
        print("Action Server Values: ", isConflict)

        
        if isSimilar == True:
            print("ALready in DB")
            dispatcher.utter_message(text= "Your requirement is already in the database or has been written in another format.")
            dispatcher.utter_message(text="anything else can i help you with ?")
        else:
            if isConflict == True:
                print("Propose solution")
                dispatcher.utter_message(text="There is a conflict with the following requirements: \n\r{} \n\r{}".format(requirment1,requirment2))
                dispatcher.utter_message(text="Proposing Solution")
                dispatcher.utter_message(msg)
                dispatcher.utter_message(text="anything else can i help you with ?")
            else:
                print('Insert in DB')
                insert_sentence(requirement)
                dispatcher.utter_message(text="Your requirement has been added") 
                dispatcher.utter_message(text="anything else can i help you with ?")                    
        return []