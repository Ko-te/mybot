import requests, json


def get_random_coctail():
    data_json = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic')
    data = json.loads((data_json.text))
    name = data.get('strDrink')
    data_json_1 = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}')
    data_1 = json.loads((data_json_1.text))
    recipe = data_1.get('strInstructions')
    return name, recipe

def random_coctail_photo():
    data_json = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic')
    data = json.loads((data_json.text))
    photo = data.get('strDrinkThumb')
    return photo

