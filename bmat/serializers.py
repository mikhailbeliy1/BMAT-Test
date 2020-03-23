from .models import MusicalWork

from rest_framework import serializers


class MusicalWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = MusicalWork
        fields = ('id', 'title', 'contributors', 'iswc')