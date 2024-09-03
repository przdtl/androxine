import logging

from typing import Optional

from elasticsearch_dsl import Q

logger = logging.getLogger(__name__)


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

    logger.info(
        'A query was received from elasticsearch with input data: name - {}, category - {}'.format(
            name, category
        ))

    return elasticsearch_query
