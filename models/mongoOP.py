# -*- coding: utf-8 -*-
# Importa mongocliente para realizar a conexão com bd do mongo criado
from pymongo import MongoClient
from flask import jsonify, request
import json
import sys
from bson.json_util import dumps
from bson.objectid import ObjectId
from routes import routers
# from controllers import cupgames

# Classe definida para disponibilizar operações com o mongodb
# define e cria conexão e inserção, remoção, atualização e re-
# cuperação de dados
class OpMongoDB():

    # client = MongoClient('localhost', 27017)
    client = MongoClient("mongodb://user:123@ds135619.mlab.com:35619/worldcup2018")

    # Construtor db = banco de dados, collection
    def __init__(self, db, collection):
        self.db = self.client.get_database(db)
        self.collection = self.db.get_collection(collection)

    # Metodo para atualizar ou inserir novos dados
    def saveIW(self, dados):
        response = {}

        try:
            response = self.collection.insert(response)
            # self.collection.insert_one({"dados":1})

        except:
            response = {
                "Error": True,
                "Menssage": "FAIL",
            }

        return dados

    def getSimulation(self, id):

        dados = {}
        response = {}

        try:
            res = self.collection.find_one({"id": id})
            response = {
                "user": id,
                "name": res['name'],
                "simulacao": res['simulacao']
            }
        except:
            response = {}

        return response

    def saveSimulation(self,id,dados):

        response = {"simulacao":dados}

        try:

            res = self.collection.update({'id': id }, {"$set": response}, upsert=True)

            response = {
                "Error": False,
                "Message": "Arquivo atualizado com sucesso",
            }

        except:
            response = {
                "Error": True,
                "Message": "Error ao processar serviço",
            }

        return response

    def save(self, dados):

        # Criando variável que armazena a resposta
        response = {}
        # ----------------------------------------
        # Caso exista um id apenas faz o update
        # se não, adiciona um novo
        # ----------------------------------------
        try:
            a= dados['_id']
        except:
            a = None

        if not a:
            # Faz um try catch para garantir inserção dos dados
            try:

                inserted_id = self.collection.insert_one(dados)
                response = {
                    "Error": False,
                    "Menssage": "Objeto adicionado com sucesso!",
                    "_id": (str(inserted_id.inserted_id))
                }
            except:
                response = {
                    "Error": True,
                    "Menssage": "Error no processamento do serviço!",
                    "Dica" : "Possivelmente esse email já existe"
                }

            #--------------------------
            # Resposta do servidor
            return response
            #--------------------------
            #--------------------------
        else:
            # Caso não exista id é feito uma atualização com base
            # no id recebido e mais uma vez com segurança que os dados
            # sejam atualizados
            try:
                print ("tem id")
                inserted = self.collection.update(dados)
                response = {
                    "Error": False,
                    "Menssage": "Arquivo atualizado com sucesso"
                }
            except:
                response = {
                    "Error": True,
                    "Menssage": "Error ao processar servicço"
            	}

    def upload(self, id, dados):
        # Caso não exista id é feixo uma atualização com base
        # no id recebido e mais uma vez com segurança que os dados
        # sejam atualizados

        # try:
        #     del dados['key']
        # except:
        #     pass

        try:
            # self.collection.replace_one({'_id': ObjectId(id)}, {"$set": dados}, upsert=False)
            res = self.collection.replace_one({'_id': ObjectId(id)}, dados, upsert=False).raw_result
            response = {
                "Error": False,
                "Menssage": "Arquivo atualizado com sucesso",
                "data" : res
            }
        except:
            response = {
                "Error": True,
                "Menssage": "Error ao processar serviço"
            }

        # --------------------------
        # Resposta do servidor
        # --------------------------
        return response
        # --------------------------


    def patch(self, id, dados):
        # Caso não exista id é feixo uma atualização com base
        # no id recebido e mais uma vez com segurança que os dados
        # sejam atualizados

        try:

            res = self.collection.update({'_id': ObjectId(id)}, {"$set": dados}, upsert=True)

            response = {
                "Error": False,
                "Message": "Arquivo atualizado com sucesso",
                "data" : res
            }
        except:
            response = {
                "Error": True,
                "Message": "Error ao processar serviço",
            }

        # --------------------------
        # Resposta do servidor
        # --------------------------
        return response
        # --------------------------



    def remove(self, id):
        try:
            res = self.collection.delete_one({"_id": ObjectId(id)})
            # print()
            response = {
                "Error": False,
                "QuatDelete": res.deleted_count,
            }
        except:
            response = {
                "Error": True,
                "Data": "Não foi possivel remover"
            }
        return response

    def list(self):
        response = {}
        try:
            data = self.collection.find()
            data = [x for x in data]
            for x in data:
                x['_id'] = str(x['_id'])

            if (data):
                # print (data)
                response = {
                    "Error": False,
                    "Data": data
                }
            else:
                response = {
                    "Error": True,
                    "Menssage": "Erro ao acessar serviço"
                }
        except Exception as e:
            print(e)
            response = {
                "Error": True,
                "Menssage": "Error no serviço "
            }

        return response


    def findById(self, id):
        try:
            res = self.collection.find_one({"_id": ObjectId(id)})
            res["_id"] = str(res['_id'])

            response = {
                "Error": False,
                "data": res
            }
        except:
            response = {
                "Error": True,
                "Menssage": "Error no serviço "
            }

        return response

    def findUser(self, id):

        try:
            res = self.collection.find_one({"id": id})
            # res["_id"] = str(res['_id'])

            if res==None:
                return False
            else:
                return True

        except:
            pass

    def findTeam(self, id):
        try:
            res = self.collection.find_one({"id_selecao": int(id)})
            res["_id"] = str(res['_id'])

            response = {
                "Error": False,
                "data": res
            }
        except:
            response = {
                "Error": True,
                "Menssage": "Error no serviço "
            }

        return response


    def findMatchById(self, id):
        try:
            res = self.collection.find_one({"id_partida": int(id)})
            res["_id"] = str(res['_id'])

            response = {
                "Error": False,
                "data": res
            }
        except:
            response = {
                "Error": True,
                "Menssage": "Error no serviço "
            }

        return response


    def listMatchbyRodada(self, id):
        try:
            res = self.collection.find_one({"rodada": int(id)})
            res["_id"] = str(res['_id'])

            response = {
                "Error": False,
                "data": res
            }
        except:
            response = {
                "Error": True,
                "Menssage": "Error no serviço "
            }

        return response



    def listarSelecoes(self):
        response = {}
        try:
            data = self.collection.find()
            data = [x for x in data]
            for x in data:
                x['_id'] = str(x['_id'])
                numidselecaoa = int(x['selecao_a'])
                numidselecaob = int(x['selecao_b'])
                x['selecao_a'] = routers.getIdSelecao2(numidselecaoa)
                x['selecao_b'] = routers.getIdSelecao2(numidselecaob)
                # x['selecao_a'] = cupgames.getTeam(num, request.json)

            if (data):
                # print (data)
                response = {
                    "Error": False,
                    "Data": data
                }
            else:
                response = {
                    "Error": True,
                    "Menssage": "Erro ao acessar serviço"
                }
        except Exception as e:
            print(e)
            response = {
                "Error": True,
                "Menssage": "Error no serviço "
            }

        return response


    def findSimulationByIdUser(self, id):
        try:
            data = self.collection.find({"id_usuario": id})
            data = [x for x in data]
            for x in data:
                x['_id'] = str(x['_id'])


            # res["_id"] = str(res['_id'])
            if (data):
                # print (data)
                response = {
                    "Error": False,
                    "Data": data
                }
            else:
                response = {
                    "Error": True,
                    "Menssage": "Erro ao acessar serviço"
                }
        except Exception as e:
            print(e)
            response = {
                "Error": True,
                "Menssage": "Error no serviço "
            }

        return response


    def listSort(self):
        response = {}
        try:
            data = self.collection.find().sort("id_selecao")
            data = [x for x in data]
            for x in data:
                x['_id'] = str(x['_id'])

            if (data):
                # print (data)
                response = {
                    "Error": False,
                    "Data": data
                }
            else:
                response = {
                    "Error": True,
                    "Menssage": "Erro ao acessar serviço"
                }
        except Exception as e:
            print(e)
            response = {
                "Error": True,
                "Menssage": "Error no serviço "
            }

        return response


    def findGroup(self, id):
        try:
            data = self.collection.find({"grupo": id}).sort("id_selecao")
            data = [x for x in data]
            for x in data:
                x["_id"] = str(x['_id'])

            if (data):
                # print (data)
                response = {
                    "Error": False,
                    "Data": data
                }
            else:
                response = {
                    "Error": True,
                    "Menssage": "Erro ao acessar serviço"
                }
        except:
            response = {
                "Error": True,
                "Menssage": "Error no serviço "
            }

        return response


    # def makeSimulation(self, iduser, rodada):
    #     response = {}
    #     try:
    #         data = self.collection.find({"id_usuario": iduser})
    #         data = [x for x in data]
    #         for x in data:
    #             x['_id'] = str(x['_id'])
    #             rodada = int(x['rodada'])
    #             x['rodada'] = routers.getIdPartida3(rodada)
    #             # x['selecao_a'] = cupgames.getTeam(num, request.json)
    #
    #         if (data):
    #             # print (data)
    #             response = {
    #                 "Error": False,
    #                 "Data": data
    #             }
    #         else:
    #             response = {
    #                 "Error": True,
    #                 "Menssage": "Erro ao acessar serviço"
    #             }
    #     except Exception as e:
    #         print(e)
    #         response = {
    #             "Error": True,
    #             "Menssage": "Error no serviço "
    #         }
    #
    #     return response
