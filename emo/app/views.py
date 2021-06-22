import librosa
import numpy as np
import os
import pickle
import soundfile

from django.conf import settings
from django.http import JsonResponse

from rest_framework import status
from rest_framework import views
from .emotions import LivePredictions

class EmotionPredict(views.APIView):
    # template_name = 'home.html'
    # renderer_classes = [TemplateHTMLRenderer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_name = 'Emotion_Voice_Detection_Model.h5'
        # self.loaded_model = pickle.load(open(os.path.join(settings.MODEL_ROOT, model_name), "rb"))# load trained model
        self.model = LivePredictions(model=os.path.join(settings.MODEL_ROOT, model_name))
        self.prediction = None

    def post(self, request):
        # filename = request.POST.getlist('file_name').pop()
        # filepath = str(os.path.join(settings.MEDIA_ROOT, filename))
        # _random = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        # path = default_storage.save(f'tmp2\\{_random}.wav', ContentFile(request.FILES.get("file_name").read()))
        # tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        path = request.POST.get("path")
        try:
            self.model.load_audio_file(path)
            prediction = self.model.make_predictions()
            print("result:", prediction)
            # os.remove(tmp_file)
            return JsonResponse({'emotion_prediction': prediction.get("emotion"), "prediction": prediction}, status=status.HTTP_200_OK)

        except ValueError as err:
            # os.remove(tmp_file)
            return JsonResponse(str(err), status=status.HTTP_400_BAD_REQUEST)
        # except Exception:
        #     os.remove(tmp_file)
