from django.test import TestCase

from elasticsearch_dsl import Q

from exercise.services import get_exercise_elasticsearch_query


class ExerciseElasticsearchQueryTest(TestCase):
    empty_elasticsearch_query = Q({
        "match_all": {},
    })
    non_empty_elasticsearch_query = Q({
        "bool": {
            "must": []
        }
    })

    def test_get_query_without_parameters(self):
        query = get_exercise_elasticsearch_query()

        empty_elasticsearch_query = Q({
            "match_all": {},
        })

        self.assertEqual(query, empty_elasticsearch_query)

    def test_get_query_only_with_category(self):
        category = 'category'
        query = get_exercise_elasticsearch_query(
            name=None,
            category=[category]
        )

        elasticsearch_query = Q({
            "bool": {
                "filter": [
                    {'terms': {"category": [category]}}
                ]
            }
        })

        self.assertEqual(query, elasticsearch_query)

    def test_get_query_only_with_name(self):
        name = 'name'
        query = get_exercise_elasticsearch_query(
            name=name,
            category=None
        )

        elasticsearch_query = Q({
            "bool": {
                "must": [
                    {'match': {"name": name}}
                ]
            }
        })

        self.assertEqual(query, elasticsearch_query)
