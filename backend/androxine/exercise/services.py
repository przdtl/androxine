from typing import Optional

from elasticsearch_dsl import Q


def get_exercise_elasticsearch_query(name: Optional[str] = None, category: Optional[str] = None):
    matches = []
    if category:
        matches.append({"match": {"category": category}})
    if name:
        matches.append({"match": {"name": name}})

    if matches:
        elasticsearch_query = Q({
            "bool": {
                "should": matches
            }
        })
    else:
        elasticsearch_query = Q({
            "match_all": {},
        })

    return elasticsearch_query
