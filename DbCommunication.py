import json
import psycopg2


class PopulateIntoDb:

    def __init__(self):
        self.connection = psycopg2.connect(user="postgres",
                                           password="Aa123456",
                                           host="localhost",
                                           port="5432",
                                           database="vulcandb")
        self.cursor = self.connection.cursor()
        self.cursor.execute('create table if not exists plugins(' /
                            'pluginID varchar(30) primary key, published text, title text, score text, cvelist text);')

    def insert_new_plugin(self, entry):
        insert_query = "INSERT INTO plugins(pluginID, published, title, score, cvelist) VALUES(%s,%s,%s,%s,%s)"
        params = ("pluginID :" + entry["_source"]["pluginID"], "published :" + entry["_source"]["published"],
                  "title :" + entry["_source"]["title"],
                  "score :" + json.dumps(entry["_source"]["enchantments"]["score"]["value"]),
                  "cvelist :" + json.dumps(entry["_source"]["cvelist"]))
        self.cursor.execute(insert_query, params)
        self.connection.commit()

    def get_plugin_count(self, entry):
        does_plugin_exist_query = "select count(*) from plugins where pluginId like %s;"
        does_exist_params = ("%{0}%".format(entry["_source"]["pluginID"]),)
        self.cursor.execute(does_plugin_exist_query, does_exist_params)
        return self.cursor.fetchone()[0]

    def populate(self, collection):
        for entry in collection:
            plugin_count = self.get_plugin_count(entry)
            if plugin_count == 0:
                self.insert_new_plugin(entry)

        self.cursor.close()
        self.connection.close()
