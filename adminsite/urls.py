from django.urls import path
from .views import *

urlpatterns = [
    # path("users", users_view, name="users-view"),
    path('users/', UsersView.as_view(), name="users"),
    path('users/<int:pk>/view/', UsersDetailsView.as_view(), name="view_user"),
    path('users/<int:pk>/update/', UpdateUpdateView.as_view(), name="update_user"),
    path('users/<int:pk>/delete/', UpdateDeleteView.as_view(), name="user_delete"),

    path("generate", generate_view, name="generate-view"),
    path("users/management", users_management, name="user-management"),
    path("journals", journal_view, name="journals-view"),
    path("journals/management", journals_management, name="journals_management"),
    path("reports", reports_view, name="reports-view"),
    path("report_results", reports_results, name="reports-results-view"),
    path("generate_researches", generate_researches_view,
         name="reports-results-view"),
]
