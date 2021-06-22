import scipy.io.wavfile as sciwav
import numpy as np
import numpy
import scipy.io.wavfile
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.activations import relu, sigmoid, softmax
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import BatchNormalization
from tensorflow.python.keras.layers import Input
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import AveragePooling2D
from tensorflow.python.keras.layers import Bidirectional
from tensorflow.python.keras.layers import Lambda
from tensorflow.python.keras.layers import Reshape

PHONEME = ['h#', 'sh', 'ix', 'hv', 'eh', 'dcl', 'jh', 'ih', 'd', 'ah',
                'kcl', 'k', 's', 'ux', 'q', 'en', 'gcl', 'g', 'r', 'w',
                'ao', 'epi', 'dx', 'axr', 'l', 'y', 'uh', 'n', 'ae', 'm',
                'oy', 'ax', 'dh', 'tcl', 'iy', 'v', 'f', 't', 'pcl', 'ow',
                'hh', 'ch', 'bcl', 'b', 'aa', 'em', 'ng', 'ay', 'th', 'ax-h',
                'ey', 'p', 'aw', 'er', 'nx', 'z', 'el', 'uw', 'pau', 'zh',
                'eng', 'BLANK']


def filter_banks(signal, sample_rate):
    """
    This method will filter all acoustic features into numarry
    TODO: mfcc
    """
    pre_emphasis = 0.97
    frame_size = 0.025
    frame_stride = 0.01
    NFFT = 512
    nfilt = 40
    num_cep = 500
    emphasized_signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
    frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate  # Convert from seconds to samples
    signal_length = len(emphasized_signal)
    frame_length = int(round(frame_length))
    frame_step = int(round(frame_step))
    num_frames = int(numpy.ceil(float(numpy.abs(signal_length - frame_length)) / frame_step))

    pad_signal_length = num_frames * frame_step + frame_length
    z = numpy.zeros((pad_signal_length - signal_length))
    pad_signal = numpy.append(emphasized_signal, z)  # Pad Signal

    indices = numpy.tile(numpy.arange(0, frame_length), (num_frames, 1)) + numpy.tile(
        numpy.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_signal[indices.astype(numpy.int32, copy=False)]
    frames *= numpy.hamming(frame_length)
    mag_frames = numpy.absolute(numpy.fft.rfft(frames, NFFT))  # Magnitude of the FFT
    pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))  # Power Spectrum
    low_freq_mel = 0
    high_freq_mel = (2595 * numpy.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
    mel_points = numpy.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10 ** (mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = numpy.floor((NFFT + 1) * hz_points / sample_rate)

    fbank = numpy.zeros((nfilt, int(numpy.floor(NFFT / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])  # left
        f_m = int(bin[m])  # center
        f_m_plus = int(bin[m + 1])  # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = numpy.dot(pow_frames, fbank.T)
    filter_banks = numpy.where(filter_banks == 0, numpy.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * numpy.log10(filter_banks)  # dB
    filter_banks -= (numpy.mean(filter_banks, axis=0) + 1e-8)
    padding = np.zeros((num_cep, nfilt))
    padding[:filter_banks.shape[0], :filter_banks.shape[1]] = filter_banks[:num_cep, :]
    return padding


class ASR():
    def __init__(self,model):
        """
        Create the model
        """
        self.model_path = model
        # self.data_set = DataSet()
        inputs = Input(shape=(500, 40, 1))
        # inputs = Input(shape=(60, 500, 40))
        conv_1 = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
        pool_1 = AveragePooling2D(pool_size=(2, 2))(conv_1)
        conv_2 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool_1)
        pool_2 = AveragePooling2D(pool_size=(2, 2))(conv_2)
        conv_3 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool_2)
        batch_norm_3 = BatchNormalization()(conv_3)
        pool_3 = AveragePooling2D(pool_size=(1, 2))(batch_norm_3)
        conv_4 = Conv2D(256, (2, 2), activation='relu', padding='same')(pool_3)
        batch_norm_4 = BatchNormalization()(conv_4)
        pool_4 = AveragePooling2D(pool_size=(1, 5))(batch_norm_4)
        lamb = Lambda(lambda x: K.squeeze(x, 2))(pool_4)
        blstm_1 = Bidirectional(LSTM(128, return_sequences=True, dropout=0.5))(lamb)
        blstm_2 = Bidirectional(LSTM(128, return_sequences=True, dropout=0.5))(blstm_1)
        outputs = Dense(62, activation='softmax')(blstm_2)

        # model to be used at test time
        self.act_model = Model(inputs, outputs)
        self.act_model.summary()

        labels = Input(name='the_labels', shape=[0], dtype='float32')
        input_length = Input(name='input_length', shape=[1], dtype='int64')
        label_length = Input(name='label_length', shape=[1], dtype='int64')

        loss_out = Lambda(self.ctc_lambda_func, output_shape=(1,), name='ctc')(
            [outputs, labels, input_length, label_length])

        # model to be used at training time
        self.model = Model(inputs=[inputs, labels, input_length, label_length], outputs=loss_out)

    def ctc_lambda_func(args, x):
        """
        Create cost function (CTC)
        """
        y_pred, labels, input_length, label_length = x

        return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


    def make_prediction(self,path):
        sample_rate, wav = sciwav.read(path)
        _au_data = filter_banks(wav, sample_rate)
        _au_data = _au_data.reshape((1,) + _au_data.shape + (1,))
        self.act_model.load_weights(self.model_path)
        prediction = self.act_model.predict(_au_data)
        out = K.get_value(K.ctc_decode(prediction, input_length=np.ones(prediction.shape[0]) * prediction.shape[1],
                                       greedy=True)[0][0])

        predic_phone = [PHONEME[i] for i in out[0]]

        return predic_phone