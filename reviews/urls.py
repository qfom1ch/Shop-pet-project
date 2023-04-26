from django.urls import path

from .views import AddReview, DeleteReview

app_name = 'review'

urlpatterns = [
    path("review/<int:pk>/", AddReview.as_view(), name='add_review'),
    path("review_del/<int:pk>/", DeleteReview.as_view(), name='del_review'),
]
