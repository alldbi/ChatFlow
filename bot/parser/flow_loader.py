import json

from ..models.node import node_factory
"""
code for loading json file of the bot and initiate flow of the chatbot
"""

def read_json(flow_file_path: str):
    with open(flow_file_path) as file:
        data = json.load(file)

    return data

def json_data_parser(flow_file_path: str):
    data = read_json(flow_file_path)

    node_list = []
    for node in data['nodes']:
        node_list.append(node_factory(node))

    # TODO return other objects that are extracted from the file
    return node_list
