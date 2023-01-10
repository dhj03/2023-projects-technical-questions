import requests

URL = "http://localhost:8080"

# NOTE: The server must have no entities stored before running the test

# Invalid /entity request - Empty
response = requests.post(f"{URL}/entity", json = {})

assert response.status_code == 400

# Invalid /entity request - Invalid type
response = requests.post(f"{URL}/entity", json = {
    "entities": [
        {
            "type": "space_monster",
            "metadata": {
                "type": "hydra"
            },
            "location": {
                "x": 6,
                "y": 9
            }
        }
    ]
})

assert response.status_code == 400

# Valid /entity request
response = requests.post(f"{URL}/entity", json = {
    "entities": [
        {
            "type": "space_cowboy",
            "metadata": {
                "name": "Jim",
                "lassoLength": 1
            },
            "location": {
                "x": 3,
                "y": 2
            }
        },
        {
            "type": "space_animal",
            "metadata": {
                "type": "pig"
            },
            "location": {
                "x": 3,
                "y": 3
            }
        },
        {
            "type": "space_cowboy",
            "metadata": {
                "name": "Bob",
                "lassoLength": 2
            },
            "location": {
                "x": 7,
                "y": 3
            }
        },
        {
            "type": "space_animal",
            "metadata": {
                "type": "flying_burger"
            },
            "location": {
                "x": 6,
                "y": 3
            }
        },
        {
            "type": "space_cowboy",
            "metadata": {
                "name": "Loner",
                "lassoLength": 32
            },
            "location": {
                "x": -843,
                "y": -492
            }
        }
    ]
})

assert response.status_code == 200
assert response.text == ""

# Invalid /lassoable request - Empty
response = requests.get(f"{URL}/lassoable", json = {})

assert response.status_code == 400

# Invalid /lassoable request - No such cowboy
response = requests.get(f"{URL}/lassoable", json = {
    "cowboy_name": "rick"
})

assert response.status_code == 400

# Valid /lassoable request - No animals
response = requests.get(f"{URL}/lassoable", json = {
    "cowboy_name": "Loner"
})

assert response.status_code == 200
assert response.json() == {
    "space_animals": []
}

# Valid /lassoable request - Jim
response = requests.get(f"{URL}/lassoable", json = {
    "cowboy_name": "Jim"
})

assert response.status_code == 200
assert response.json() == {
    "space_animals": [
        {
            "type": "pig",
            "location": {
                "x": 3,
                "y": 3
            } 
        }
    ]
}

# Valid /lassoable request - Bob
response = requests.get(f"{URL}/lassoable", json = {
    "cowboy_name": "Bob"
})

assert response.status_code == 200
assert response.json() == {
    "space_animals": [
        {
            "type": "flying_burger",
            "location": {
                "x": 6,
                "y": 3
            } 
        }
    ]
}
