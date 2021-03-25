from django.contrib.auth.models import User, Group
from strategy.models import HierarchicalRiskParity, HistoricalValue, RecordHypothesis
from personnal.models import UserMeta
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #hropt = serializers.PrimaryKeyRelatedField(many=True, queryset=HierarchicalRiskParity.objects.all())
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class UserMetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserMeta
        fields = ['preferred_hypothesis_id']
    
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class HierarchicalRiskParitySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = HierarchicalRiskParity
        fields = ['name', 'created_at', 'user']

class HistoricalValueSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = HistoricalValue
        fields = ['name', 'created_at', 'user']

class RecordHypothesisSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = RecordHypothesis
        fields = ['created_at', 'name', 'allocation', 'user', 'id']

class PortfolioPerformanceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = RecordHypothesis
        fields = ['created_at', 'user']