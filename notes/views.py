import json

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Note


def to_dict(note):
    return {"id": note.id, "title": note.title, "content": note.content}


def health(request):
    """Used by Docker and Kubernetes health checks."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok"})
    except Exception:
        return JsonResponse({"status": "error", "detail": "database unavailable"}, status=503)


@csrf_exempt
def notes_collection(request):
    try:
        if request.method == "POST":  # Create
            data = json.loads(request.body or "{}")
            note = Note.objects.create(title=data.get("title"), content=data.get("content"))
            return JsonResponse(to_dict(note), status=201)
        if request.method == "GET":  # Read all
            notes = Note.objects.order_by("id")
            return JsonResponse([to_dict(n) for n in notes], safe=False)
        return JsonResponse({"error": "Method not allowed"}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def note_detail(request, note_id):
    try:
        if request.method == "GET":  # Read one
            note = Note.objects.filter(id=note_id).first()
            if not note:
                return JsonResponse({"error": "Not found"}, status=404)
            return JsonResponse(to_dict(note))

        if request.method == "PUT":  # Update
            data = json.loads(request.body or "{}")
            note = Note.objects.filter(id=note_id).first()
            if not note:
                return JsonResponse({"error": "Not found"}, status=404)
            note.title = data.get("title")
            note.content = data.get("content")
            note.save()
            return JsonResponse(to_dict(note))

        if request.method == "DELETE":  # Delete
            Note.objects.filter(id=note_id).delete()
            return JsonResponse({"message": "Deleted"})

        return JsonResponse({"error": "Method not allowed"}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)