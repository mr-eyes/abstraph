import json

class JsonParser:

    __json_data = dict()

    def __init__(self, filename):
        json_file = open(filename, 'r')
        json_file_content = json_file.read()
        json_file.close()
        self.__json_data = json.loads(json_file_content)
        
    def get_data(self, feature):
        return self.__json_data[feature]
        