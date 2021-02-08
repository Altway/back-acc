from django.contrib.auth.models import User, Group
from strategy.models import HierarchicalRiskParity, RecordHypothesis
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    hropt = serializers.PrimaryKeyRelatedField(many=True, queryset=HierarchicalRiskParity.objects.all())
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class HierarchicalRiskParitySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = HierarchicalRiskParity
        fields = ['name', 'created_at', 'user']

class RecordHypothesisSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = RecordHypothesis
        fields = ['name', 'created_at', 'user', 'allocation']

class PortfolioPerformanceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = RecordHypothesis
        fields = ['name', 'created_at', 'user', 'allocation']