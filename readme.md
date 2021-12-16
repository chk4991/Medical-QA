# 基于医疗知识图谱的问答系统

###Introduction

实现一个基于rasa的问答系统， 支持的意图有：查询疾病相应的症状、
疾病对应的药物、疾病对应忌口的食物等3种意图；可以根据疾病名称做进一步筛选

###Usage

#####Knowledge storage
    cd graph_database
    python create_graph.py

#####Train
    rasa train

#####Deploy
    rasa run actions --actions actions
    rasa shell

### Example
![Image text](https://github.com/chk4991/Medical-QA/blob/master/pic/1.png)
![Image text](https://github.com/chk4991/Medical-QA/blob/master/pic/2.png)

### Warning：
1、需要启动neo4j服务

###Todo

1、美化候选疾病打印信息

2、加入更多intent和story，扩展功能
