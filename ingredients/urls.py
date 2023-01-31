from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home_view, name='ingredient'),
    path('', views.IngredientListView.as_view(), name='ingredient'),

    path('<int:ingredient_id>/', views.ingredient_detail_view, name='ingredient-detail'),
    
    path('edit-ingredient/', views.edit_ingredient_view, name='edit-ingredient'),
    path('add-ingredient/', views.add_ingredient_view, name='add-ingredient'),
    path('delete-ingredient/<int:ingredient_id>/', views.delete_ingredient_view, name="delete-ingredient"),

    path('search/', views.search_view, name="search-ingredient"),
    path('upload-ingredients/', views.extract_and_load_ingredients_view, name="upload-ingredients"),
    
]