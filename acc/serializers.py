from django.contrib.auth.models import User, Group
from django.db.models.fields.related import ForeignKey
from strategy.models import HierarchicalRiskParity, HistoricalValue, RecordHypothesis
from personnal.models import UserMeta
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer


class RecordHypothesisSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = RecordHypothesis
        exclude = []
        #fields = ['created_at', 'name', 'allocation', 'user', 'id']

class HierarchicalRiskParitySerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    #hypothesisvalue = RecordHypothesisSerializer(many=True, read_only=False)
    class Meta:
        model = HierarchicalRiskParity
        exclude = []
        #fields = ['name', 'created_at', 'user']

class HistoricalValueSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.id')
    #expected_return_id = serializers.ReadOnlyField(source='expected_return.name')
    #capital = serializers.FloatField()
    #user = serializers.ReadOnlyField(source='user.username')
    #user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    #hypothesisvalue = RecordHypothesisSerializer(many=True, read_only=False)
    class Meta:
        model = HistoricalValue
        exclude = []
        #fields = ['name', 'created_at', 'user', 'capital', 'risk_free_rate', 'broker_fees', 'gamma', '']


class UserMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMeta
        exclude = []
        #fields = []

class UserSerializer(UserDetailsSerializer):
    #profile = UserProfileSerializer(source="userprofile")
    usermeta = UserMetaSerializer(many=False, read_only=False)

    #hropt = serializers.PrimaryKeyRelatedField(many=True, queryset=HierarchicalRiskParity.objects.all())
    historicalvalue = HistoricalValueSerializer(many=True, read_only=False)
    hropt = HierarchicalRiskParitySerializer(many=True, read_only=False)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        #exclude = []
        #fields = ['url', 'username', 'email', 'groups', 'historicalvalue', 'hropt']
        fields = UserDetailsSerializer.Meta.fields + ('usermeta','historicalvalue','hropt',)
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']




class PortfolioPerformanceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = RecordHypothesis
        fields = ['created_at', 'user']