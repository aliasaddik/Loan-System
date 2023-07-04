from django.urls import path
from Loan.myapp.views.loan import(
    LoanAdminAPIView,
    LoanByIdAPIView,
    LoanCreateAPIView,
    LoanCustomerAPIView,
    LoanRejectAPIView,
    LoanCSVDownloadAPIView,
    LoanStatsAPIView,
    

)
urlpatterns = [
    path('create/', LoanCreateAPIView.as_view(), name='create a loan'),
    path('get_all/', LoanCustomerAPIView.as_view(), name='get loans of a customer'),
    path('view_all_data/', LoanAdminAPIView.as_view(), name='loan_admin'),
    path('<str:id>/', LoanByIdAPIView.as_view(), name='loan_by_id'),
    path('reject/<str:id>/', LoanRejectAPIView.as_view(), name='loan_reject'),
    path('view_all_data/csv/', LoanCSVDownloadAPIView.as_view(), name='loan_csv'),
    path('loan_stats/get_stats/', LoanStatsAPIView.as_view(), name='loan_stats'),]