#importando o documento Tree
# -*- coding: utf-8 -*-
from bson.json_util import dumps
from models import mongoOP

dbSimulation = mongoOP.OpMongoDB('worldcup2018','simulacao')

def getSimulations(id, dados):
	return dbSimulation.findSimulationByIdUser(id)

def createSimulation(dados):
    return dbSimulation.saveIW(dados)