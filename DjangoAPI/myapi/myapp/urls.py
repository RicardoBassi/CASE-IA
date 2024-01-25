from django.urls import path
from myapp.views import FirstPage
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import LoginView, RenewView, LogoutView


urlpatterns = [ path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('myapp/first_page.html', FirstPage.as_view(), name='first_page'),
                path('autentication/login/', LoginView.as_view(), name='login'),
                path('autentication/renovate/', RenewView.as_view(), name='renew'),
                path('autentication/logout/', LogoutView.as_view(), name='logout')

            ]




