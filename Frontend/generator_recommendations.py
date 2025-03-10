import requests
import json

class RecipeGenerator:
    def __init__(self, nutritional_data: list, ingredient_list: list = [], query_params: dict = {'n_neighbors': 5, 'return_distance': False}):
        self.nutritional_data = nutritional_data
        self.ingredient_list = ingredient_list
        self.query_params = query_params

    def update_request(self, nutritional_data: list, ingredient_list: list, query_params: dict):
        self.nutritional_data = nutritional_data
        self.ingredient_list = ingredient_list
        self.query_params = query_params

    def create_request(self):
        request_data = {
            'nutritional_data': self.nutritional_data,
            'ingredient_list': self.ingredient_list,
            'query_params': self.query_params
        }
        response = requests.post(url='http://backend:8080/predict/', data=json.dumps(request_data))
        return response
