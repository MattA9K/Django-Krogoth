from rest_framework import serializers
from kapp_notes.models import AKNote
from django.contrib.auth.models import User
from datetime import datetime



class AKNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AKNote
        fields = ('title','author','body','date_created','date_modified')
        read_only_fields = ('author',)

    def create(self, validated_data):
        validated_data['date_created'] = datetime.now()
        validated_data['date_modified'] = datetime.now()
        validated_data['author'] = User.objects.get(id=self.context['request'].user.id)
        return AKNote.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.body = validated_data.get('body', instance.body)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.date_modified = datetime.now()
        instance.save()
        return instance

