import requests

database = {
    1: 'alice',
    2: 'bob',
    3: 'charlie'
}

def getUserFromDB(id):
    return database[id]


def getUsers():
    response = requests.get('https://jsonplaceholder.typicode.com/users/')
    if response.status_code == 200:
        return response.json()

    raise requests.HTTPError