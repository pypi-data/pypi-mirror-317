from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import os

# List notes
def index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})

# View note details
def detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes/detail.html', {'note': note})

# Create a new note
def create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NoteForm()
    return render(request, 'notes/form.html', {'form': form, 'title': 'Create Note'})

# Update an existing note
def update(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/form.html', {'form': form, 'title': 'Update Note'})

# Delete a note
def delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('index')
    return render(request, 'notes/delete.html', {'note': note})

# Show current datetime
def show_datetime(request):
    """Route to display the current date and time."""
    now = datetime.now()
    return JsonResponse({"current_datetime": now.strftime("%Y-%m-%d %H:%M:%S")})




def show_directory_listing(request):
    """Route to display directory contents and render file content as text."""
    base_dir = os.getcwd()  # Base directory
    directory = request.GET.get('dir', base_dir)

    try:
        # Resolve and secure directory
        directory = os.path.abspath(directory)
        if not directory.startswith(base_dir):
            raise PermissionError("Access denied to this directory")

        # Check if it's a file
        if os.path.isfile(directory):
            # Read and return file content as plain text
            try:
                with open(directory, 'r', encoding='utf-8') as file:
                    content = file.read()
                return render(request, 'notes/file_view.html', {
                    'file_name': os.path.basename(directory),
                    'content': content,
                    'current_time': datetime.now(),  # Add server time
                })
            except Exception as e:
                # Return error message for unreadable files
                return render(request, 'notes/error.html', {'message': f"Unable to read file: {str(e)}"})

        # If it's a directory, list its contents
        items = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            items.append({
                'name': item,
                'is_dir': os.path.isdir(item_path),
                'path': item_path,
            })

        context = {
            'directory': directory,
            'items': items,
            'parent': os.path.dirname(directory) if directory != base_dir else None,
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format to 24-hour

        }
        return render(request, 'notes/directory_listing.html', context)

    except Exception as e:
        return render(request, 'notes/error.html', {'message': str(e)})
