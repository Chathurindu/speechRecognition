import librosa
import numpy as np
import os
import pickle
import soundfile

from django.conf import settings
from django.http import JsonResponse

from rest_framework import status
from rest_framework import views
from django.views.decorators.csrf import csrf_exempt
from .phoneme import ASR

class AgePredict(views.APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_name = 'age_mlp_classifier.model'
        self.loaded_model = pickle.load(
            open(os.path.join(settings.MODEL_ROOT, model_name), "rb"))  # load trained model
        self.prediction = None

    def extract_feature(self, file_name, **kwargs):
        mfcc = kwargs.get("mfcc")
        chroma = kwargs.get("chroma")
        mel = kwargs.get("mel")
        contrast = kwargs.get("contrast")
        tonnetz = kwargs.get("tonnetz")
        with soundfile.SoundFile(file_name) as sound_file:
            X = sound_file.read(dtype="float32")
            sample_rate = sound_file.samplerate
            if chroma or contrast:
                stft = np.abs(librosa.stft(X))
            result = np.array([])
            if mfcc:
                mfccs = np.mean(librosa.feature.mfcc(
                    y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
                result = np.hstack((result, mfccs))
            if chroma:
                chroma = np.mean(librosa.feature.chroma_stft(
                    S=stft, sr=sample_rate).T, axis=0)
                result = np.hstack((result, chroma))
            if mel:
                mel = np.mean(librosa.feature.melspectrogram(
                    X, sr=sample_rate).T, axis=0)
                result = np.hstack((result, mel))
            if contrast:
                contrast = np.mean(librosa.feature.spectral_contrast(
                    S=stft, sr=sample_rate).T, axis=0)
                result = np.hstack((result, contrast))
            if tonnetz:
                tonnetz = np.mean(librosa.feature.tonnetz(
                    y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
                result = np.hstack((result, tonnetz))
        return result

    def post(self, request):

        path = request.POST.get("path")

        try:
            features = self.extract_feature(path, mfcc=True, chroma=True, mel=True).reshape(
                1, -1)  # extract features and reshape it
            prediction = self.loaded_model.predict(features)[0]
            print("result:", prediction)
            return JsonResponse({'age_prediction': prediction}, status=status.HTTP_200_OK)
        except ValueError as err:
            return JsonResponse(str(err), status=status.HTTP_400_BAD_REQUEST)


class IntoPredict(views.APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_name = 'into_mlp_classifier.model'
        self.loaded_model = pickle.load(open(os.path.join(settings.MODEL_ROOT, model_name), "rb"))# load trained model
        self.prediction = None

    def extract_feature(self, file_name, **kwargs):
        # MFCC takes into account human perception for sensitivity at appropriate frequencies by converting the conventional frequency to Mel-Scale
        mfcc = kwargs.get("mfcc")
        chroma = kwargs.get("chroma")
        mel = kwargs.get("mel")
        contrast = kwargs.get("contrast")
        tonnetz = kwargs.get("tonnetz")
        zcr = kwargs.get("zcr") # Zero-crossing rate
        with soundfile.SoundFile(file_name) as sound_file:
            X = sound_file.read(dtype="float32")
            sample_rate = sound_file.samplerate
            if chroma or contrast:
                stft = np.abs(librosa.stft(X))
            result = np.array([])
            if mfcc:
                mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
                result = np.hstack((result, mfccs))
                # print("-----mfcc---")
                # print(result)
            if chroma:
                chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
                # print("-----chroma---")
                # print(result)
                result = np.hstack((result, chroma))
            if mel:
                mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
                # print("-----mel---")
                # print(result)
                result = np.hstack((result, mel))
            if contrast:
                contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
                # print("-----contrast---")
                # print(result)           
                result = np.hstack((result, contrast))
            if tonnetz:
                tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
                # print("-----tonnetz---")
                # print(result)
                result = np.hstack((result, tonnetz))
            # if zcr:
            #     zcr = np.mean(librosa.feature.zero_crossing_rate(y=librosa.load(soundfile)))
            #     result = np.hstack((result, zcr))
            #     print(result)
            #     print("---------------------")
        return result

    def post(self, request):
        path = request.POST.get("path")
        try:
            features = self.extract_feature(path, mfcc=True, chroma=True, mel=True).reshape(1, -1) # extract features and reshape it
            prediction = self.loaded_model.predict(features)[0]
            print("result:", prediction)
            return JsonResponse({'into_prediction': prediction}, status=status.HTTP_200_OK)
        except ValueError as err:
            return JsonResponse(str(err), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def phone_predict(request):
    path = request.POST.get("path")

    model_name = "phoneme_model.hdf5"
    model = ASR(model=os.path.join(settings.MODEL_ROOT, model_name))

    phone_list =  model.make_prediction(path)

    return JsonResponse({'phone_prediction': phone_list},status=status.HTTP_200_OK)

