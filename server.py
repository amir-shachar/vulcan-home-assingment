import psycopg2
from flask import Flask, jsonify
from flask_restful import Resource, Api

from home_assingment.my_api.connectNessus import LoadFromVulners
from home_assingment.my_api.DbCommunication import PopulateIntoDb

db_connect = psycopg2.connect(user="postgres",
                              password="Aa123456",
                              host="localhost",
                              port="5432",
                              database="vulcandb")
app = Flask(__name__)
api = Api(app)


class AllPlugins(Resource):
    def get(self, parameter):
        if parameter.lower() in {"pluginid", "published", "score"}:
            conn = db_connect  # connect to database
            cursor = conn.cursor()
            cursor.execute("select * from plugins order by {0};".format(parameter))
            return {'plugin': ['{0}'.format((i,)) for i in cursor.fetchall()]}
        else:
            return "Cannot evaluate param: " + str(parameter)


class PluginByCve(Resource):
    def get(self, parameters):
        params = parameters.split(',')
        cursor = db_connect.cursor()
        query = "select p.* from plugins p where p.cvelist like %s;"
        if len(params) > 1:
            query = "select p.* from plugins p where p.cvelist like %s order by {0};".format(params[1])
        params = ("%{0}%".format(params[0]),)
        cursor.execute(query, params)
        result = dict(data=["{0}".format((i,)) for i in cursor.fetchall()])
        return jsonify(result)


class SpecificPlugin(Resource):
    def get(self, pluginid):
        conn = db_connect  # connect to database
        cursor = conn.cursor()
        query = "select * from plugins p where p.pluginID like %s;"
        params = ("%{0}%".format(pluginid),)
        cursor.execute(query, params)
        result = {'data': cursor.fetchone()}
        return jsonify(result)


populator = PopulateIntoDb()
vulner_loader = LoadFromVulners()
populator.populate(vulner_loader.load())

api.add_resource(AllPlugins, '/plugins/<parameter>')  # Route_1
api.add_resource(PluginByCve, '/plugin_by_cve/<parameters>')  # Route_2
api.add_resource(SpecificPlugin, '/get_plugin/<pluginid>')  # Route_3

if __name__ == '__main__':
    app.run(port='5002')
