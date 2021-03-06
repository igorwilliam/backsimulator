# -*- coding: utf-8 -*-

# Este modulo carrega todas as funções do flask

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.routing import BaseConverter, ValidationError
from itsdangerous import base64_encode, base64_decode
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.errors import InvalidId
from flask import jsonify


class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(base64_decode(value))
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()
    def to_url(self, value):
        return base64_encode(value.binary)


# Importando controllers
from controllers import user
from controllers import team
from controllers import simulation
from controllers import match
from controllers import group


import json

# Flask app
application = Flask(__name__)
application.url_map.converters['objectid'] = ObjectIDConverter
CORS(application)
# Rota index para teste


@application.route("/", methods=['GET'])
def ctrlRoot():
    return "<h1>World Cup Simulator 2018</h1> <p>Web Service</p><a href='http://chutedegenio.herokuapp.com/'>Front</a>"




"""
----------------------------------------------------
                    USER
----------------------------------------------------
"""

@application.route("/user", methods=['POST','GET'])
# Função da rota indextree
def ctrlUser():

    if (request.method == 'POST'):
        res = user.createUser(request.json)
        return dumps(request.json)

    elif (request.method == 'GET'):
        res = user.listUser()
        return dumps(res)

@application.route('/user/<iduser>',  methods=['GET', 'DELETE', 'PUT', 'PATCH'])
def getIdUser(iduser):

    if (request.method == "GET"):
        res = user.getUser(iduser,request.json)
        return dumps(res)

    elif (request.method == 'DELETE'):
        res = user.deleteUser(iduser,request.json)
        return dumps(res)

    elif (request.method == 'PUT'):
        res = user.uploadUser(iduser,request.json)
        return dumps(res)

    elif (request.method == 'PATCH'):
        res = user.patchUser(iduser,request.json)
        return dumps(res)

"""
----------------------------------------------------
                    SIMULATION
----------------------------------------------------
"""

@application.route('/simulargrupo/<idgrupo>',  methods=['POST','GET'])
def postSimulationGroup(idgrupo):

    if (request.method == 'POST'):
        res = simulation.simulateGroup(request.json, idgrupo)
        return dumps(res)

@application.route('/fase/1',  methods=['POST','GET'])
def postSimulation1():

    if (request.method == 'POST'):
        res = simulation.simulate1(request.json)
        return dumps(res)

@application.route('/fase/2',  methods=['POST','GET'])
def postSimulation2():

    if (request.method == 'POST'):
        res = simulation.simulate2(request.json)
        return dumps(res)


@application.route('/fase/3',  methods=['POST','GET'])
def postSimulation3():

    if (request.method == 'POST'):
        res = simulation.simulate3(request.json)
        return dumps(res)

@application.route('/fase/4',  methods=['POST','GET'])
def postSimulation4():

    if (request.method == 'POST'):
        res = simulation.simulate4(request.json)
        return dumps(res)

@application.route('/simulacao/<iduser>',  methods=['GET', 'DELETE', 'PUT', 'PATCH'])
def getIdSimulation(iduser):

    if (request.method == "GET"):
        res = simulation.getSimulations(iduser,request.json)
        return dumps(res)

"""
----------------------------------------------------
                    TEAM
----------------------------------------------------
"""
@application.route("/selecao", methods=['POST','GET'])
# Função da rota indextree
def ctrlSelecao():

    if (request.method == 'POST'):
        res['id_selecao']=1;
        res = team.createTeam(request.json)
        return dumps(request.json)

    elif (request.method == 'GET'):
        res = team.listTeam()
        print (res)
        return dumps(res)


def getIdSelecao2(idselecao):

    if (request.method == "GET"):
        res = team.getTeam(idselecao,request.json)
        return res

def getIdPartida2(idpartida):

    res = match.listMatchbyId(idpartida,request.json)
    return res


def getIdPartida3(rodada):

    if (request.method == "GET"):
        res = match.listMatchbyRodada(rodada,request.json)
        return res

@application.route('/selecao/<idselecao>',  methods=['GET', 'DELETE', 'PUT', 'PATCH'])
def getIdSelecao(idselecao):

    if (request.method == "GET"):
        res = team.getTeam(idselecao,request.json)
        return dumps(res)

    elif (request.method == 'DELETE'):
        res = team.deleteTeam(idselecao,request.json)
        return dumps(res)

    elif (request.method == 'PUT'):
        res = team.uploadTeams(idselecao,request.json)
        return dumps(res)

"""
----------------------------------------------------
                    MATCH
----------------------------------------------------
"""

@application.route("/partida", methods=['POST','GET'])
# Função da rota indextree
def ctrlPartida():

    if (request.method == 'POST'):
        res = match.createMatch(request.json)
        return dumps(request.json)

    elif (request.method == 'GET'):
        res = match.listMatch()
        return dumps(res)

@application.route('/partida/<idpartida>',  methods=['GET', 'DELETE', 'PUT', 'PATCH'])
def getIdPartida(idpartida):

    if (request.method == "GET"):
        res = match.listMatchbyId(idpartida,request.json)
        return dumps(res)

"""
----------------------------------------------------
                    SAVE
----------------------------------------------------
"""

@application.route('/user/<idUser>/simulacao',  methods=['POST','GET'])
def saveSimulation(idUser):

    if (request.method == "POST"):
        res = user.saveSimulation(idUser,request.json)
        return dumps(res)

    if (request.method == "GET"):
        res = user.getSimulation(idUser)
        return dumps(res)

############################################
################## grupos ##################
############################################

@application.route('/grupo/<idgrupo>',  methods=['GET', 'DELETE', 'PUT', 'PATCH'])
def getIdGrupo(idgrupo):

    if (request.method == "GET"):
        res = group.getGroup(idgrupo, request.json)
        return dumps(res)

def getIdGrupo2(idgrupo):

    res = team.getGroup(idgrupo,request.json)
    return res
