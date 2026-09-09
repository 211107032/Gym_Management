import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from gym_settings.models import GymSetting
from members.models import Member
from memberships.models import MembershipPlan, MemberSubscription
from attendance.models import Attendance
from payments.models import Payment
from trainers.models import Trainer, TrainerAssignment
from workouts.models import WorkoutPlan, WorkoutExercise, MemberProgress
from notifications.models import Notification

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds realistic sample data for the Gym Management System'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting data seeding process..."))

        # 1. Gym Settings
        gym_setting = GymSetting.get_settings()
        gym_setting.name = "Apex Gym & Fitness Center"
        gym_setting.phone = "+1 (555) 019-2834"
        gym_setting.email = "contact@apexgym.com"
        gym_setting.save()

        # 2. Admin User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@apexgym.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write("Created Admin user: admin / admin123")

        # 3. Staff User
        staff_user, created = User.objects.get_or_create(
            username='staff1',
            defaults={
                'email': 'staff1@apexgym.com',
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'role': User.Role.STAFF,
                'is_staff': True
            }
        )
        if created:
            staff_user.set_password('staff123')
            staff_user.save()
            self.stdout.write("Created Staff user: staff1 / staff123")

        # 4. Membership Plans
        plans_data = [
            {'name': 'Monthly Standard', 'days': 30, 'price': 1500.00, 'desc': 'Full access to cardio & weight area', 'feat': 'Cardio Access\nWeight Floor\nLocker Room'},
            {'name': 'Quarterly Pro', 'days': 90, 'price': 3999.00, 'desc': '3 Months access with sauna & group classes', 'feat': 'All Gym Access\nSauna & Steam\n2 Group Classes/Week'},
            {'name': 'Half-Yearly Elite', 'days': 180, 'price': 6999.00, 'desc': '6 Months all-inclusive access', 'feat': 'Unlimited Gym Access\nSauna & Steam\nUnlimited Group Classes\nDiet Consultation'},
            {'name': 'Yearly VIP', 'days': 365, 'price': 11999.00, 'desc': '1 Year complete VIP membership', 'feat': '24/7 Access\nPersonal Trainer Consultation\nFree Locker\nUnlimited Amenities'},
            {'name': 'Personal Training Package', 'days': 30, 'price': 5000.00, 'desc': '1-on-1 Dedicated Trainer Assistance', 'feat': 'Dedicated Trainer\nCustomized Workout Plan\nWeekly Body Analysis'},
        ]
        created_plans = []
        for p in plans_data:
            plan_obj, _ = MembershipPlan.objects.get_or_create(
                name=p['name'],
                defaults={
                    'duration_days': p['days'],
                    'price': p['price'],
                    'description': p['desc'],
                    'features': p['feat'],
                    'is_active': True
                }
            )
            created_plans.append(plan_obj)
        self.stdout.write(f"Seeded {len(created_plans)} membership plans.")

        # 5. Trainers
        trainers_info = [
            ('trainer1', 'Alex', 'Rider', 'Crossfit & Strength', 6, 'ACE Certified Master Trainer', 45000.00),
            ('trainer2', 'Marcus', 'Vance', 'Bodybuilding & Powerlifting', 8, 'IFBB Pro Coach', 50000.00),
            ('trainer3', 'Elena', 'Rostova', 'Yoga & Pilates', 4, 'Certified Yoga Alliance 500hr', 40000.00),
            ('trainer4', 'David', 'Beckett', 'Cardio & Fat Loss', 5, 'NASM CPT Certified', 42000.00),
            ('trainer5', 'Samantha', 'Reed', 'Rehabilitation & Conditioning', 7, 'B.Sc. Sports Medicine', 48000.00),
        ]
        created_trainers = []
        for uname, fname, lname, spec, exp, qual, sal in trainers_info:
            u, c = User.objects.get_or_create(
                username=uname,
                defaults={
                    'email': f'{uname}@apexgym.com',
                    'first_name': fname,
                    'last_name': lname,
                    'role': User.Role.TRAINER
                }
            )
            if c:
                u.set_password('trainer123')
                u.save()
            t_obj, _ = Trainer.objects.get_or_create(
                user=u,
                defaults={
                    'specialization': spec,
                    'experience': exp,
                    'qualification': qual,
                    'salary': sal,
                    'phone': f'+1 555-010{random.randint(10, 99)}',
                    'email': f'{uname}@apexgym.com'
                }
            )
            created_trainers.append(t_obj)
        self.stdout.write(f"Seeded {len(created_trainers)} trainers.")

        # 6. Members & Subscriptions
        member_names = [
            ("member1", "John", "Doe"), ("member2", "Jane", "Smith"),
            ("member3", "Robert", "Johnson"), ("member4", "Emily", "Davis"),
            ("member5", "Michael", "Brown"), ("member6", "Jessica", "Wilson"),
            ("member7", "Daniel", "Taylor"), ("member8", "Amanda", "Anderson"),
            ("member9", "James", "Thomas"), ("member10", "Sophia", "Martinez"),
            ("member11", "Benjamin", "White"), ("member12", "Olivia", "Harris"),
            ("member13", "William", "Martin"), ("member14", "Isabella", "Thompson"),
            ("member15", "Ethan", "Garcia"), ("member16", "Mia", "Martinez"),
            ("member17", "Alexander", "Robinson"), ("member18", "Charlotte", "Clark"),
            ("member19", "Henry", "Rodriguez"), ("member20", "Amelia", "Lewis"),
            ("member21", "Lucas", "Lee"), ("member22", "Harper", "Walker")
        ]

        created_members = []
        today = timezone.now().date()

        for idx, (uname, fname, lname) in enumerate(member_names):
            u, c = User.objects.get_or_create(
                username=uname,
                defaults={
                    'email': f'{uname}@gmail.com',
                    'first_name': fname,
                    'last_name': lname,
                    'role': User.Role.MEMBER
                }
            )
            if c:
                u.set_password('member123')
                u.save()

            join_days_ago = random.randint(10, 180)
            joining_dt = today - timedelta(days=join_days_ago)

            mem_obj, _ = Member.objects.get_or_create(
                user=u,
                defaults={
                    'phone': f'+1 555-01{idx+10:02d}',
                    'email': f'{uname}@gmail.com',
                    'gender': random.choice(['MALE', 'FEMALE']),
                    'joining_date': joining_dt,
                    'status': 'ACTIVE',
                    'height': random.randint(160, 190),
                    'weight': random.randint(55, 95),
                    'emergency_contact_name': f'{fname} Emergency',
                    'emergency_contact_phone': '+1 555-999-0000'
                }
            )
            created_members.append(mem_obj)

            # Create Subscriptions
            selected_plan = random.choice(created_plans)
            sub_start = joining_dt
            sub_end = sub_start + timedelta(days=selected_plan.duration_days)
            sub_status = 'ACTIVE' if sub_end >= today else 'EXPIRED'

            sub_obj, _ = MemberSubscription.objects.get_or_create(
                member=mem_obj,
                membership_plan=selected_plan,
                defaults={
                    'start_date': sub_start,
                    'end_date': sub_end,
                    'price': selected_plan.price,
                    'discount': 0.00,
                    'final_amount': selected_plan.price,
                    'status': sub_status
                }
            )

            # Create Payments for Subscriptions
            Payment.objects.get_or_create(
                member=mem_obj,
                subscription=sub_obj,
                defaults={
                    'amount': sub_obj.final_amount,
                    'payment_method': random.choice(['CASH', 'UPI', 'CARD', 'ONLINE']),
                    'payment_date': sub_start,
                    'transaction_id': f'TXN-{random.randint(100000, 999999)}',
                    'status': 'PAID'
                }
            )

        self.stdout.write(f"Seeded {len(created_members)} members with subscriptions & payment records.")

        # 7. Assign Trainers & Workouts
        for idx, m in enumerate(created_members[:10]):
            t = created_trainers[idx % len(created_trainers)]
            TrainerAssignment.objects.get_or_create(trainer=t, member=m)

            wp, created_wp = WorkoutPlan.objects.get_or_create(
                member=m,
                defaults={
                    'trainer': t,
                    'name': f"{m.user.first_name}'s Fitness Routine",
                    'goal': random.choice(['Weight Loss', 'Muscle Building', 'Strength Conditioning'])
                }
            )
            if created_wp:
                WorkoutExercise.objects.create(workout_plan=wp, exercise_name='Barbell Bench Press', muscle_group='Chest', sets=4, repetitions=10, weight=60.0)
                WorkoutExercise.objects.create(workout_plan=wp, exercise_name='Barbell Squats', muscle_group='Legs', sets=4, repetitions=12, weight=80.0)
                WorkoutExercise.objects.create(workout_plan=wp, exercise_name='Lat Pulldown', muscle_group='Back', sets=3, repetitions=12, weight=50.0)

            # Progress logs over past 3 months
            for month_idx in range(3, -1, -1):
                p_date = today - timedelta(days=month_idx*30)
                w_val = float(m.weight) + (month_idx * 1.5)
                MemberProgress.objects.get_or_create(
                    member=m,
                    date=p_date,
                    defaults={'weight': w_val, 'height': m.height}
                )

        # 8. Attendance Records
        for day_offset in range(14, -1, -1):
            att_date = today - timedelta(days=day_offset)
            for m in random.sample(created_members, k=15):
                Attendance.objects.get_or_create(
                    member=m,
                    date=att_date,
                    defaults={
                        'check_in_time': timezone.now().time(),
                        'status': random.choice(['PRESENT', 'PRESENT', 'LATE'])
                    }
                )

        # 9. Initial Notification
        Notification.objects.create(
            user=admin_user,
            title="System Ready & Seeded",
            message="Gym Management System seeded successfully with demo members, trainers, payments, and workouts.",
            notification_type="SYSTEM"
        )

        self.stdout.write(self.style.SUCCESS("All seed data successfully generated! Ready for local testing & production deployment."))
