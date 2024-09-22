from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from exercise.models import Exercise


@registry.register_document
class ExerciseDocument(Document):

    category = fields.TextField(attr='category.name')
    slug = fields.TextField(attr='slug')
    name = fields.TextField(attr='name', fielddata=True)

    class Index:
        name = 'exercise'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Exercise
        fields = [
            'id',
        ]
