import keras
import librosa
import numpy as np
import os
# import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def get_adjacent_classes(predictions, predict_probabilities):
    #print("fun1", predict_probabilities)
    predicted_class_probability = (predict_probabilities[0][predictions][0])
    new_predict_probabilities = (predict_probabilities[0]).copy()
    new_predict_probabilities.sort()

    lower_class_probability = new_predict_probabilities[6]
    # print("sorted", new_predict_probabilities)
    # print("fun2", predict_probabilities)
    # print(lower_class_probability)
    return predicted_class_probability, lower_class_probability


def analyze_adjacent_classes(predicted_class_probability, lower_class_probability):
    lower_gap = (predicted_class_probability * 100) - (lower_class_probability * 100)

    if lower_gap <= 10:
        return lower_class_probability, lower_gap
    else:
        return -99, -99


def find_class_from_probability(probabilities, lower_class_probability):
    label = 0
    for probability in probabilities[0]:

        if probability == lower_class_probability:
            return label
        label = label+1

class LivePredictions:
    """
    Main class of the application.
    """

    def __init__(self,model= None):
        """
        Init method is used to initialize the main parameters.
        """
        if model:
            self.loaded_model = keras.models.load_model(model)
        else:
            self.loaded_model = keras.models.load_model("Emotion_Voice_Detection_Model.h5")

    def load_audio_file(self,file):
        self.file = file


    def make_predictions(self):
        """
        Method to process the files and create your features.
        """
        data, sampling_rate = librosa.load(self.file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=2)
        x = np.expand_dims(x, axis=0)
        predictions = self.loaded_model.predict_classes(x)
        predict_probabilities = self.loaded_model.predict_proba(x)
        #print("main1",predict_probabilities)

        print(" ")
        print("Prediction is", " ", self.convert_class_to_emotion(predictions))
        print("Percentage of the Prediction is", " ", round(((predict_probabilities[0][predictions][0]) * 100), 3), "%")

        predicted_class_probability, lower_class_probability = get_adjacent_classes(predictions, predict_probabilities)
        lower_class_probability, probability_gap = analyze_adjacent_classes(predicted_class_probability, lower_class_probability)

        #print("main2",predict_probabilities)
        lower_prediction = None
        if (lower_class_probability != (-99)):
            is_lower = True

            lower_class = find_class_from_probability(predict_probabilities, lower_class_probability)
            print("There is a", round(probability_gap, 3), "% probability gap for this speech to be classified as ", self.convert_class_to_emotion(lower_class), "(",round(lower_class_probability*100 ,3),"% )")
            lower_prediction = {
                "gap": round(probability_gap, 3),
                "emotion": self.convert_class_to_emotion(lower_class),
                "percentage":round(lower_class_probability*100 ,3)
            }
        print("For file ", " ", self.file)
        prediction_dict = {
            "emotion": self.convert_class_to_emotion(predictions),
            "percentage": round(((predict_probabilities[0][predictions][0]) * 100), 3),
            "low_level": lower_prediction,
        }
        return prediction_dict

    @staticmethod
    def convert_class_to_emotion(pred):
        """
        Method to convert the predictions (int) into human readable strings.
        """

        label_conversion = {'0': 'neutral',
                            '1': 'calm',
                            '2': 'happy',
                            '3': 'sad',
                            '4': 'angry',
                            '5': 'fearful',
                            '6': 'disgust',
                            '7': 'surprised'}

        for key, value in label_conversion.items():
            if int(key) == pred:
                label = value
        return label
