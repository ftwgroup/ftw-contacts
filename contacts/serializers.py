from rest_framework import serializers
from contacts.models import Tag, Contact


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

class ContactSerializer(serializers.ModelSerializer):

    tags = TagSerializer()

    class Meta:
        model = Contact
        exclude = ('account',)