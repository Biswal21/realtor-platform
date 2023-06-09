# from drf_instamojo.serializers import PaymentRequestSerializer
# from drf_instamojo.models import PaymentRequest
# from .models import *
# from .serializers import *
# from rest_framework import status

# import datetime


# class PaymentView(APIView):
#     serializer_class = PaymentReqSerializer

#     def post(self, request):
#         user = CustomUser.objects.get(email__exact=self.request.user.email)
#         serializer = self.serializer_class(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             try:
#                 user_plan = UserPlan.objects.filter(
#                     user__exact=user,
#                     start_datetime__lte=timezone.now(),
#                     end_datetime__gte=timezone.now(),
#                     is_paid=True,
#                     is_terminated=False,
#                 ).latest("created_at")
#                 todays_date = datetime.now().date()
#                 start_date = user_plan.start_datetime.date()
#                 end_date = user_plan.end_datetime.date()
#                 purchased_days = (end_date - start_date).days
#                 used_days = (todays_date - start_date).days + 1
#                 available_balance = round(
#                     user_plan.payment_request.amount
#                     - ((user_plan.payment_request.amount / purchased_days) * used_days),
#                     2,
#                 )

#                 plan = Plan.objects.get(id__exact=serializer.data["id"], is_active=True)
#                 amount = round(float(plan.cost) * 1.18, 2) - float(available_balance)
#                 prs = PaymentRequestSerializer(
#                     data={
#                         "amount": round(amount, 2),
#                         "purpose": "Upgrade ACE - "
#                         + user_plan.plan.name
#                         + " to "
#                         + plan.name,
#                         "send_sms": False,
#                         "redirect_url": str(os.getenv("FRONTEND_APP_URL"))
#                         + "/dashboard/billing",
#                         "allow_repeated_payments": False,
#                         "email": user.email,
#                         "buyer_name": user.first_name + " " + user.last_name,
#                     }
#                 )
#                 prs.is_valid(raise_exception=True)
#                 prs.save(created_by_id=user.id)
#                 payment_request = PaymentRequest(id=prs.data["id"])
#                 up = UserPlan(
#                     admin=user,
#                     user=user,
#                     cost=plan.cost,
#                     plan=plan,
#                     payment_request=payment_request,
#                 )
#                 up.save()
#                 return Response(
#                     {
#                         "plan_id": plan.id,
#                         "name": plan.name,
#                         "cost": plan.cost,
#                         "payable_amount": round(amount, 2),
#                         "payment_url": prs.data.get("longurl"),
#                     },
#                     status=status.HTTP_200_OK,
#                 )

#             except UserPlan.DoesNotExist:
#                 plan = Plan.objects.get(id__exact=serializer.data["id"], is_active=True)
#                 amount = round(float(plan.cost) * 1.18, 2)
#                 prs = PaymentRequestSerializer(
#                     data={
#                         "amount": amount,
#                         "purpose": "ACE - " + plan.name,
#                         "send_sms": False,
#                         "redirect_url": str(os.getenv("FRONTEND_APP_URL"))
#                         + "/dashboard/billing",
#                         "allow_repeated_payments": False,
#                         "email": user.email,
#                         "buyer_name": user.first_name + " " + user.last_name,
#                     }
#                 )
#                 prs.is_valid(raise_exception=True)
#                 prs.save(created_by_id=user.id)
#                 payment_request = PaymentRequest(id=prs.data["id"])
#                 up = UserPlan(
#                     admin=user,
#                     user=user,
#                     cost=plan.cost,
#                     plan=plan,
#                     payment_request=payment_request,
#                 )
#                 up.save()
#                 return Response(
#                     {
#                         "plan_id": plan.id,
#                         "name": plan.name,
#                         "cost": plan.cost,
#                         "payable_amount": amount,
#                         "payment_url": prs.data.get("longurl"),
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#         except Plan.DoesNotExist:
#             return Response(
#                 {"message": "Invalid plan", "status_code": 400},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


# class UpdatedPaymentView(APIView):
#     serializer_class = UpdatedPaymentSerializer

#     def post(self, request):
#         user = User.objects.get(email__exact=request.user.email)
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         ic = InstamojoConfiguration.objects.get(is_active=True)
#         imojo = Instamojo(
#             api_key=ic.api_key, auth_token=ic.auth_token, endpoint=ic.base_url
#         )
#         ps = PaymentSerializer(
#             data={
#                 "id": serializer.data["id"],
#                 "payment_request": serializer.data["payment_request"],
#             }
#         )
#         ps.is_valid(raise_exception=True)
#         ps.save()
#         payment = Payment.objects.get(id=ps.data["id"])
#         if payment.status == "Credit":
#             try:
#                 user_plan = UserPlan.objects.filter(
#                     user__exact=user,
#                     start_datetime__lte=timezone.now(),
#                     end_datetime__gte=timezone.now(),
#                     is_paid=True,
#                     is_terminated=False,
#                 ).latest("created_at")
#                 user_plan.is_terminated = True

#                 up = UserPlan.objects.get(
#                     payment_request__exact=payment.payment_request
#                 )
#                 up.is_paid = True
#                 up.start_datetime = timezone.now()
#                 up.end_datetime = timezone.now() + timedelta(up.plan.validity)
#                 up.admin.user_type = "EnterpriseAdmin"

#                 user_plan.save()
#                 up.admin.save()
#                 up.save()
#             except UserPlan.DoesNotExist:
#                 up = UserPlan.objects.get(
#                     payment_request__exact=payment.payment_request
#                 )
#                 up.is_paid = True
#                 up.start_datetime = timezone.now()
#                 up.end_datetime = timezone.now() + timedelta(up.plan.validity)
#                 up.admin.user_type = "EnterpriseAdmin"
#                 up.admin.save()
#                 up.save()
#         return Response(
#             {"message": "success", "status_code": 200}, status=status.HTTP_200_OK
#         )
