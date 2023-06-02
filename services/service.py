from pathlib import Path
import tensorflow as tf
import matplotlib.pyplot as plt
import keras_ocr
from tensorflow.keras.layers import TextVectorization
import pickle



class TextClassification:
    
    def __init__(self) -> None:
        self.base_dir = Path(__file__).resolve().parent.parent
        self.h5_path = self.base_dir / 'files' / 'toxic_text_classification.h5'
        self.pickle_path = self.base_dir / 'files' / 'tv_layer.pkl'
        self.model = tf.keras.models.load_model(self.h5_path)
        
        self.from_disk = pickle.load(open(self.pickle_path, "rb"))
        self.vectorizer = TextVectorization(max_tokens=self.from_disk['config']['max_tokens'],
                                        output_mode=self.from_disk['config']['output_mode'],
                                        output_sequence_length=self.from_disk['config']['output_sequence_length'])
        self.vectorizer.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
        self.vectorizer.set_weights(self.from_disk['weights'])
        
    
    def toxic_values(self, comment):
        vectorized_comment = self.vectorizer([comment])
        results = self.model.predict(vectorized_comment)
        result = []
        toxic_level = ['Toxic','Severe_toxic','Obscene','Threat','Insult','Identity_hate']
        for idx,res in enumerate(results[0]):
            if res>0.5:
                result.append(toxic_level[idx])
        if not result:
            result.append('Non-toxic')
        return result