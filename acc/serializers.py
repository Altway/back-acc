from django.contrib.auth.models import User, Group
from django.db.models.fields.related import ForeignKey
from strategy.models import HierarchicalRiskParity, HistoricalValue, RecordHypothesis
from personnal.models import UserMeta
from rest_framework import serializers


class HistoricalValueSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    #user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    class Meta:
        model = HistoricalValue
        fields = ['name', 'created_at', 'user', 'capital']

        def create(self, validated_data):
            print(validated_data)
            return HistoricalValue()

class UserSerializer(serializers.ModelSerializer):
    #hropt = serializers.PrimaryKeyRelatedField(many=True, queryset=HierarchicalRiskParity.objects.all())
    #historicalvalue = HistoricalValueSerializer(many=True, read_only=False)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']#, 'historicalvalue']
    
    #def create(self, request):
    #    print("ICICICI")
    #    pass

class UserMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMeta
        fields = ['preferred_hypothesis_id']
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class HierarchicalRiskParitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = HierarchicalRiskParity
        fields = ['name', 'created_at', 'user']


class RecordHypothesisSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = RecordHypothesis
        fields = ['created_at', 'name', 'allocation', 'user', 'id']

class PortfolioPerformanceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = RecordHypothesis
        fields = ['created_at', 'user']