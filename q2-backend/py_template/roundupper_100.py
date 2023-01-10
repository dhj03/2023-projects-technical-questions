from dataclasses import dataclass
from enum import Enum
from json import dumps
from math import sqrt
from typing import Union, NamedTuple, List
from flask import Flask, request

# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location

# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    data = request.get_json()
    try:
        entities = data['entities']

        for entity in entities:
            metadata = entity['metadata']
            location = entity['location']

            if entity['type'] == "space_cowboy":
                space_database.append(SpaceEntity(
                    SpaceCowboy(metadata['name'], metadata['lassoLength']),
                    SpaceEntity.Location(location['x'], location['y'])
                ))
            elif entity['type'] == "space_animal":
                space_database.append(SpaceEntity(
                    SpaceAnimal(metadata['type']),
                    SpaceEntity.Location(location['x'], location['y'])
                ))
            else:
                raise ValueError

    except:
        return "", 400

    return "", 200

# lassoable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    data = request.get_json()
    try:
        name = data['cowboy_name']
        cowboy_location = None

        for entity in space_database:
            if isinstance(entity.metadata, SpaceCowboy) and entity.metadata.name == name:
                cowboy_location = entity.location
                lassoLength = entity.metadata.lassoLength
                break

        if cowboy_location is None:
            raise ValueError

        space_animals = []

        for entity in space_database:
            if isinstance(entity.metadata, SpaceAnimal):
                animal_location = entity.location
                x_dist = cowboy_location.x - animal_location.x
                y_dist = cowboy_location.y - animal_location.y
                dist = sqrt(pow(x_dist, 2) + pow(y_dist, 2))

                if dist <= lassoLength:
                    space_animals.append({
                        "type": entity.metadata.type,
                        "location": {
                            "x": animal_location.x,
                            "y": animal_location.y
                        }
                    })

    except:
        return "", 400

    return dumps({"space_animals": space_animals}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
