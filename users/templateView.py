from django.views.generic import TemplateView

# Bu sadəcə HTML səhifəni göstərmək üçündür
class FaceStreamView(TemplateView):
    template_name = 'face_stream.html'
