from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Sum, Count

from members.models import Member
from memberships.models import MembershipPlan, MemberSubscription
from attendance.models import Attendance
from payments.models import Payment
from trainers.models import Trainer
from workouts.models import WorkoutPlan

from .serializers import (
    MemberSerializer, MembershipPlanSerializer, MemberSubscriptionSerializer,
    AttendanceSerializer, PaymentSerializer, TrainerSerializer, WorkoutPlanSerializer,
    RegisterSerializer, UserSerializer
)

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.role == user.Role.MEMBER:
                Member.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone': user.phone or '',
                        'email': user.email or '',
                        'joining_date': timezone.now().date(),
                        'status': 'ACTIVE',
                    }
                )
            elif user.role == user.Role.TRAINER:
                Trainer.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone': user.phone or '',
                        'email': user.email or '',
                        'specialization': 'Fitness & Conditioning',
                        'experience': 1,
                        'qualification': 'Certified Trainer',
                        'salary': 0.00,
                        'joining_date': timezone.now().date(),
                    }
                )
            return Response({'message': 'User registered successfully', 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IsAdminOrStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_staff_user)

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related('user').all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = MemberSubscription.objects.select_related('member', 'membership_plan').all()
    serializer_class = MemberSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('member').all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='check-in')
    def check_in(self, request):
        member_id = request.data.get('member_id')
        if not member_id:
            return Response({'error': 'member_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.now().date()
        att, created = Attendance.objects.get_or_create(
            member=member,
            date=today,
            defaults={'check_in_time': timezone.now().time(), 'status': 'PRESENT'}
        )
        if not created:
            return Response({'message': 'Already checked in today', 'attendance': AttendanceSerializer(att).data})
        
        return Response(AttendanceSerializer(att).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='check-out')
    def check_out(self, request):
        attendance_id = request.data.get('attendance_id')
        if not attendance_id:
            return Response({'error': 'attendance_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            att = Attendance.objects.get(id=attendance_id)
            att.check_out_time = timezone.now().time()
            att.save()
            return Response(AttendanceSerializer(att).data)
        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance record not found'}, status=status.HTTP_404_NOT_FOUND)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('member', 'subscription').all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.select_related('user').all()
    serializer_class = TrainerSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.select_related('member', 'trainer').all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

class DashboardStatsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        month_start = today.replace(day=1)

        return Response({
            'total_members': Member.objects.count(),
            'active_members': Member.objects.filter(status='ACTIVE').count(),
            'expired_members': Member.objects.filter(status='EXPIRED').count(),
            'total_trainers': Trainer.objects.count(),
            'today_attendance': Attendance.objects.filter(date=today).count(),
            'monthly_revenue': Payment.objects.filter(status='PAID', payment_date__gte=month_start).aggregate(Sum('amount'))['amount__sum'] or 0.00,
        })
