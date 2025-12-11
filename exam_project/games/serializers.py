from rest_framework import serializers
from .models import GameModel
from exam_project.common.models import BoughtGame


class GameSerializer(serializers.ModelSerializer):
    seller_display = serializers.CharField(source='user.display_name', read_only=True)

    class Meta:
        model = GameModel
        fields = [
            'id', 'title', 'summary', 'price', 'category',
            'game_picture', 'user', 'seller_display',
        ]
        read_only_fields = ['id', 'user', 'seller_display']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameModel
        fields = ['title', 'summary', 'price', 'category', 'game_picture']


class BoughtGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoughtGame
        fields = ['id', 'user', 'game', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
