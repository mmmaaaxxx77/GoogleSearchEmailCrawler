from rest_framework import serializers
from .models import Job


class KeypoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id',
                  'title',
                  'query_url',
                  'skip_url',
                  'total_count',
                  'skip_count',
                  'status',
                  'created_at',
                  'updated_at',
                  'filename')
