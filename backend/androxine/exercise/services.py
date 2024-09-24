import logging

from typing import Optional

from elasticsearch_dsl import Q

logger = logging.getLogger(__name__)


def get_exercise_elasticsearch_query(name: Optional[str] = None, category: list[str] = []):
    bool_query = {}

    if category:
        bool_query['filter'] = {'terms': {"category": category}}

    if name:
        bool_query['must'] = {"match": {"name": name}}

    if bool_query:
        query = {'bool': bool_query}
    else:
        query = {'match_all': {}}

    elasticsearch_query = Q(query)

    logger.info(
        'A query was received from elasticsearch with input data: name - {}, category - {}, query - {}'.format(
            name, category, query
        ))

    return elasticsearch_query
