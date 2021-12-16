# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import os.path
import sys
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from markdownify import markdownify as md
sys.path.append(os.path.dirname(__file__))

from utils import retrieve_disease_name, graph, make_button


class ActionFirst(Action):
    def name(self) -> Text:
        return "action_first"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=md("您可以这样向我提问: "
                                    "<br/>头痛怎么办<br/>\
                              什么人容易头痛<br/>\
                              头痛吃什么药<br/>\
                              头痛能治吗<br/>\
                              头痛属于什么科<br/>\
                              头孢地尼分散片用途<br/>\
                              如何防止头痛<br/>\
                              头痛要治多久<br/>\
                              糖尿病有什么并发症<br/>\
                              糖尿病有什么症状"))
        return []


class ActionDonKnow(Action):
    def name(self) -> Text:
        return "action_donknow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=md("您可以这样向我提问: "
                                    "<br/>头痛怎么办<br/>\
                              什么人容易头痛<br/>\
                              头痛吃什么药<br/>\
                              头痛能治吗<br/>\
                              头痛属于什么科<br/>\
                              头孢地尼分散片用途<br/>\
                              如何防止头痛<br/>\
                              头痛要治多久<br/>\
                              糖尿病有什么并发症<br/>\
                              糖尿病有什么症状"))
        return []


class ActionSearchFood(Action):
    def name(self) -> Text:
        return "action_search_food"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)  # 搜索的疾病名称是否在疾病名称词表中
        """ 进行neo4j搜索 """
        food = dict()
        if disease == pre_disease or len(possible_diseases) == 1:
        # if len(possible_diseases) == 1:
            can_eat_food = [x["food"]["name"] for x in graph.run("match (:Disease{name: {disease}})-[:can_eat]->(food:Food) return food",
                                                                 disease=disease).data()]
            food['can_eat'] = "、".join(can_eat_food) if can_eat_food else "抱歉，助手还在努力进步中！！！"
            can_not_eat_food = [x["food"]["name"] for x in graph.run("match (:Disease{name: {disease}})-[:not_eat]->(food:Food) return food",
                                                                 disease=disease).data()]
            food['not_eat'] = "、".join(can_not_eat_food) if can_not_eat_food else "抱歉，助手还在努力进步中！！！"

            message = "在 {0} 期间，推荐食用：{1}，\n但不推荐食用：{2} ". \
                format(disease, food['can_eat'], food['not_eat'])

            dispatcher.utter_message(message)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_food{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_message("请点击选择想查询的疾病  ", buttons=buttons)
        else:
            dispatcher.utter_message("抱歉，知识库中暂无与 {0} 相关的记录".format(disease))
        return []


class ActionSearchSymptom(Action):
    def name(self) -> Text:
        return "action_search_symptom"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
        # if len(possible_diseases) == 1:
            symptom_list = [x['symptom']['name'] for x in graph.run("MATCH (:Disease{name: {disease}})-[:has_symptom]->\
                                                (symptom:Symptom) RETURN symptom", disease=disease).data()]
            message = "{}可能的症状以下几种：{}".format(disease, "、".join(symptom_list))
            dispatcher.utter_message(message)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_symptom{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_message("请点击选择想查询的疾病  ", buttons=buttons)
        else:
            dispatcher.utter_message("抱歉，知识库中暂无与 {0} 相关的症状记录".format(disease))

        return []


class ActionSearchDrug(Action):
    def name(self) -> Text:
        return "action_search_drug"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
        # if len(possible_diseases) == 1:
            drug_list = [x['drug']['name'] for x in graph.run("MATCH (:Disease{name: {disease}})-[:can_use_drug]->\
                                                (drug:Drug) RETURN drug", disease=disease).data()]
            if drug_list:
                message = "在患 {} 时，已有的用药记录有：{}".format(disease, "、".join(drug_list))
            else:
                message = "无 %s 的用药记录" % disease
            dispatcher.utter_message(message)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_drug{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_message("请点击选择想查询的疾病  ", buttons=buttons)
        else:
            dispatcher.utter_message("抱歉，知识库中暂无与 {0} 相关的用药记录".format(disease))
        return []