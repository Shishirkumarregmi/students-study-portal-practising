
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('notes/', views.notes,name='notes'),
    path('delete_notes/<int:pk>', views.delete_notes,name='delete_notes'),
    path('delete_notesall/', views.delete_notesall,name='delete_notesall'),
    path('notesdetail/<int:pk>', views.NotesDetailView.as_view(),name='notes_detail'),
    path('homework/', views.homework,name='homework'),
    path('delete_homeworks/<int:pk>', views.delete_homeworks,name='delete_homeworks'),
    path('update_homework/<int:pk>', views.update_homework,name='update_homework'),
    path('youtube/', views.youtube,name='youtube'),
    path('todo/', views.todo,name='todo'),
    path('delete_todo/<int:pk>', views.delete_todo,name='delete_todo'),
    path('update_todo/<int:pk>', views.update_todo,name='update_todo'),
    path('books/', views.books,name='books'),
    path('wiki/', views.wiki,name='wiki'),
    path('conversion/', views.conversion,name='conversion'),
]
