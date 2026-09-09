from rest_framework import serializers
from django.contrib.auth import get_user_model
from members.models import Member
from memberships.models import MembershipPlan, MemberSubscription
from attendance.models import Attendance
from payments.models import Payment
from trainers.models import Trainer
from workouts.models import WorkoutPlan, WorkoutExercise, MemberProgress

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'profile_picture']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Member
        fields = [
            'id', 'member_id', 'user', 'full_name', 'date_of_birth', 'gender',
            'phone', 'email', 'address', 'emergency_contact_name', 'emergency_contact_phone',
            'joining_date', 'status', 'height', 'weight', 'medical_notes'
        ]

class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = '__all__'

class MemberSubscriptionSerializer(serializers.ModelSerializer):
    member_detail = MemberSerializer(source='member', read_only=True)
    plan_detail = MembershipPlanSerializer(source='membership_plan', read_only=True)
    remaining_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = MemberSubscription
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    member_code = serializers.CharField(source='member.member_id', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.full_name', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'

class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Trainer
        fields = '__all__'

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = '__all__'

class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    member_name = serializers.CharField(source='member.full_name', read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = '__all__'
