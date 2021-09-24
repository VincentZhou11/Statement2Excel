from django.http import HttpResponse
from shunting_yard_utils.shunting_yard import Tree, remove_unknown_characters, contains_unknown_characters
from urllib.parse import unquote

import json

from django.views.decorators.csrf import csrf_exempt


def process_query(string: str) -> dict:
    queries = string.split("&")
    ret_dict = {}
    for query in queries:
        if "=" in query:
            key_value = query.split("=")
            key = key_value[0]
            value = key_value[1]
            ret_dict[key] = value
    return ret_dict


def index(request):
    string = unquote(request.META["QUERY_STRING"])
    print(string)
    query_dict: dict = process_query(string)
    response_dict: dict = {}
    if "statements" in query_dict and "mapping" in query_dict and "row" in query_dict:
        statements = query_dict["statements"].strip('][').split(',')
        results = []
        for statement in statements:
            statement = statement.replace('"', '').strip()
            response_dict["unknown_chars"] = {statement: contains_unknown_characters(statement)}
            statement = remove_unknown_characters(statement)

            try:
                tree = Tree.build(statement)
                result = tree.evaluate()
                results.append(result)
            except:
                response_dict["error"] = True
                response_dict["error_code"] = 2
                return HttpResponse(json.dumps(response_dict))

        mapping = {}

        try:
            mapping = json.loads(query_dict["mapping"])
        except:
            response_dict["error"] = True
            response_dict["error_code"] = 3
            return HttpResponse(json.dumps(response_dict))

        mapped_results = []
        for result in results:
            for key in mapping.keys():
                result = result.replace(key, mapping[key] + str(query_dict["row"]))
            mapped_results.append(result)

        response_dict["error"] = False
        response_dict["result"] = mapped_results
    else:
        response_dict["error"] = True
        response_dict["error_code"] = 1
    return HttpResponse(json.dumps(response_dict))
