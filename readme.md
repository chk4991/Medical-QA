# 基于医疗知识图谱的问答系统

## Introduction

实现一个基于rasa的问答系统， 支持的意图有：查询疾病相应的症状、
疾病对应的药物、疾病对应忌口的食物等3种意图；可以根据疾病名称做进一步筛选

## Install
    pip install -r requirements.txt

## Usage

#### Knowledge storage

    cd graph_database
    python create_graph.py

#### Train

    rasa train

#### Demo

    rasa run actions --actions actions
    rasa shell

## Example

![Image text](https://s3.bmp.ovh/imgs/2021/12/5033b0db20e8dc9b.png)

![Image text](https://s3.bmp.ovh/imgs/2021/12/eecf7db34a4937cb.png)

## Warning：

1、需要启动neo4j服务

## Todo

1、美化打印信息

2、扩展story和intent类别，提升问答能力
