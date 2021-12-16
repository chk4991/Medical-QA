import re
import os
from py2neo import Graph

root_path = os.path.dirname(os.path.dirname(__file__))
dict_path = os.path.join(root_path, "jieba_userdict", "Diseases_dic.txt")
disease_names = [i.split()[0].strip() for i in open(dict_path, 'r', encoding='UTF-8').readlines()]
graph = Graph(uri="http://localhost:7474/", user="neo4j", password="neo4j")


def retrieve_disease_name(name):
    names = []
    name = '.*' + '.*'.join(list(name)) + '.*'
    pattern = re.compile(name)
    for i in disease_names:
        candidate = pattern.search(i)
        if candidate:
            names.append(candidate.group())
    return names


def make_button(title, payload):
    return {'title': title, 'payload': payload}


if __name__ == '__main__':
    disease = "老年肺炎"
    res = graph.run("MATCH (:Disease{name: {disease}})-[:has_symptom]->\
                                                    (symptom:Symptom) RETURN symptom", disease=disease)
    for x in res:
        print(x['symptom']['name'])
    res = retrieve_disease_name("慢性肺炎")
    print(res)