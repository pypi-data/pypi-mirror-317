# all necessary steps wrapped into a class

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
import pickle

class VaSrch:
    def __init__(self):
        # Initialize the VGG16 model for feature extraction
        base_model = VGG16(weights='imagenet', include_top=False)
        self.feature_extractor = Model(inputs=base_model.input, outputs=base_model.get_layer('block5_pool').output)

    def extract_features(self, img_folder, save_to):
        """
        Extracts features from images in a folder and saves them as .npy files.
        """
        if not os.path.exists(save_to):
            os.makedirs(save_to)

        for root, dirs, files in os.walk(img_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                    img_path = os.path.join(root, file)
                    file_name = os.path.splitext(file)[0]
                    img = image.load_img(img_path, target_size=(224, 224))
                    img_data = image.img_to_array(img)
                    img_data = np.expand_dims(img_data, axis=0)
                    img_data = preprocess_input(img_data)
                    features = self.feature_extractor.predict(img_data)
                    np.save(os.path.join(save_to, file_name + '.npy'), features)
        print("Feature extraction and saving completed.")

    def get_optimal_num_clusters(self, features_folder, max_clusters, n_components):
        """
        Determines the optimal number of clusters using the Elbow Method and Silhouette Score.
        """
        features = []
        for root, dirs, files in os.walk(features_folder):
            for file in files:
                if file.lower().endswith('.npy'):
                    feature = np.load(os.path.join(root, file))
                    if feature.ndim > 1:
                        feature = feature.flatten()
                    features.append(feature)
        
        feature_matrix = np.vstack(features)
        pca = PCA(n_components=n_components)
        feature_matrix_reduced = pca.fit_transform(feature_matrix)

        inertia_values = []
        silhouette_scores = []

        for num_clusters in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            kmeans.fit(feature_matrix_reduced)
            inertia_values.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(feature_matrix_reduced, kmeans.labels_))

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(range(2, max_clusters + 1), inertia_values, marker='o', linestyle='-', color='b')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.title('Elbow Method')

        plt.subplot(1, 2, 2)
        plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o', linestyle='-', color='g')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Score')

        plt.tight_layout()
        plt.savefig('optimal_clusters.png')
        plt.show()
        print("Elbow Method and Silhouette Score analysis completed.")

    def train_clusters(self, features_folder, model_filename, csv_filename, num_clusters):
        """
        Trains K-means clustering on image features and saves the model and cluster assignments.
        """
        features = []
        file_names = []
        for root, dirs, files in os.walk(features_folder):
            for file in files:
                if file.lower().endswith('.npy'):
                    feature = np.load(os.path.join(root, file))
                    if feature.ndim > 1:
                        feature = feature.flatten()
                    features.append(feature)
                    file_names.append(file.split('.')[0])

        feature_matrix = np.vstack(features)
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        cluster_assignments = kmeans.fit_predict(feature_matrix)

        with open(model_filename, 'wb') as file:
            pickle.dump(kmeans, file)

        df = pd.DataFrame({'Image_File': file_names, 'Cluster': cluster_assignments})
        df.to_csv(csv_filename, index=False)
        print(f"Model saved to {model_filename} and cluster assignments saved to {csv_filename}.")

    def search_similar_images(self, image_path, model_filename, csv_file, top_n):
        """
        Searches for similar images to a given image based on cluster assignments using a saved CSV file.
        """
        with open(model_filename, 'rb') as file:
            kmeans = pickle.load(file)

        img = image.load_img(image_path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        features = self.feature_extractor.predict(img_data).flatten()

        cluster_label = kmeans.predict([features])[0]

        df = pd.read_csv(csv_file)
        similar_images = df[df['Cluster'] == cluster_label]['Image_File'].tolist()

        print(f"Found {len(similar_images)} images in the same cluster.")
        return similar_images[:top_n]

