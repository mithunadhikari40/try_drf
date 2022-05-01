from .models import Singer, Song
from rest_framework import serializers


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'singer', 'duration']


class SingerSerializer(serializers.ModelSerializer):
    # to get the list of songs that are referenced to this row
    # in song model, singer key is used to reference this record
    # one singer can have more than one song

    # songs = serializers.StringRelatedField(many=True, read_only=True)
    # songs = serializers.ManyRelatedField(read_only=True)

    # songs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # songs = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='song-detail')
    # songs = serializers.SlugRelatedField(many=True, read_only=True,slug_field='title')
    # songs = serializers.HyperlinkedIdentityField(view_name='song-detail',many=True)

    # returns the whole object rather than one field
    songs = SongSerializer(many=True, )

    class Meta:
        model = Singer
        # this singer is defined in model class as related_name in
        # singer = models.ForeignKey(Singer, on_delete=models.CASCADE, related_name='singer')
        fields = ['id', 'name', 'gender', 'songs']


"""Gives an extra param of url, which gives the url of this particular item"""


class SingerSerializerHyperLinked(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Singer
        fields = ['id', 'url', 'name', 'gender']


"""Nested serializer example"""


class SongSerializerRelated(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'singer', 'duration']


class SingerSerializerRelated(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Singer
        fields = ['id', 'name', 'gender', 'songs']
