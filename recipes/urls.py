from django.urls import path
from . import views

# recipe
urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
   
    path('add-recipe/', views.add_recipe_view, name='add-recipe'),
    path('edit-recipe/<int:pk>/', views.edit_recipe_view, name='edit-recipe'),
    path('edit-recipe-step2/', views.recipe_edit_step2_view, name='edit-recipe-step2'),
    path('delete-recipe/<int:recipe_id>/', views.delete_recipe_view, name='delete-recipe'),

    path('search/', views.search_view, name="search-recipe"),

    path('clear/', views.clear_recipe_session, name='clear-recipe'),

    path('add-step/', views.add_step_view, name='step-add'),
    path('edit-step/', views.edit_step_view, name='step-edit'),
    path('delete-step/<str:pk>', views.delete_step_view, name='step-delete'),

    path('search-ingredient/', views.search_ingredient_view, name='recipe-search-ingredient'),
    path('add-ingredient/<str:ingredient_id>/', views.add_used_ingredient_view, name='recipe-add-ingredient'),
    path('edit-ingredient/', views.edit_used_ingredient_view, name='recipe-edit-ingredient'),
    path('delete-ingredient/<str:pk>/', views.delete_used_ingredient_view, name='recipe-delete-ingredient'),
]