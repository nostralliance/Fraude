import numpy as np 
import pandas as pd 
import os 
import matplotlib.pyplot as plt 
import cv2
import sklearn
import seaborn as sns
from skimage.color import rgb2gray
from skimage.filters import laplace, sobel, roberts
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, classification_report
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import warnings
import pickle

warnings.filterwarnings("ignore")
warnings.warn("DelftStack")
warnings.warn("Do not show this message")
print("No Warning Shown")

path_img_blur = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture\blur'
path_img_sharp = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture\sharp'

img_blur = os.listdir(path_img_blur)
img_sharp = os.listdir(path_img_sharp)

def get_data(path, images):
    features = []
    for img in images:
        feature = []
        image_gray = cv2.imread(os.path.join(path, img), 0)
        if image_gray is not None:
            lap_feat = laplace(image_gray)
            sob_feat = sobel(image_gray)
            rob_feat = roberts(image_gray)
            if lap_feat is not None and sob_feat is not None and rob_feat is not None:
                feature.extend([img, lap_feat.mean(), lap_feat.var(), np.amax(lap_feat),
                                sob_feat.mean(), sob_feat.var(), np.max(sob_feat),
                                rob_feat.mean(), rob_feat.var(), np.max(rob_feat)])
                features.append(feature)

    return features

sharp_feature = get_data(path_img_sharp, img_sharp)
blur_feature = get_data(path_img_blur, img_blur)

sharp_df = pd.DataFrame(sharp_feature, columns=['Image', 'Laplace_Mean', 'Laplace_Var', 'Laplace_Max',
                                                'Sobel_Mean', 'Sobel_Var', 'Sobel_Max',
                                                'Roberts_Mean', 'Roberts_Var', 'Roberts_Max'])

blur_df = pd.DataFrame(blur_feature, columns=['Image', 'Laplace_Mean', 'Laplace_Var', 'Laplace_Max',
                                              'Sobel_Mean', 'Sobel_Var', 'Sobel_Max',
                                              'Roberts_Mean', 'Roberts_Var', 'Roberts_Max'])

sharp_df.drop('Image', axis=1, inplace=True)
blur_df.drop('Image', axis=1, inplace=True)

print(f"dataset sharp :\n {sharp_df.head()}\n dataset blur :\n{blur_df.head()}")

all_feature_sharp = np.array(sharp_df)
all_feature_blur = np.array(blur_df)

y_sharp = np.ones((sharp_df.shape[0],))
y_blur = np.zeros((blur_df.shape[0],))

x_train_sharp, x_valid_sharp, y_train_sharp, y_valid_sharp = train_test_split(all_feature_sharp, y_sharp, test_size=0.20, stratify=y_sharp)
x_train_blur, x_valid_blur, y_train_blur, y_valid_blur = train_test_split(all_feature_blur, y_blur, test_size=0.20, stratify=y_blur)

x_train = np.concatenate((x_train_sharp, x_train_blur), axis=0)
x_valid = np.concatenate((x_valid_sharp, x_valid_blur), axis=0)
y_train = np.concatenate((y_train_sharp, y_train_blur), axis=0)
y_valid = np.concatenate((y_valid_sharp, y_valid_blur), axis=0)

# Appliquer PCA
scaler = StandardScaler()
x_train_valid_scaled = scaler.fit_transform(np.concatenate((x_train, x_valid), axis=0))

n_components = 2
pca = PCA(n_components=n_components)
x_train_valid_pca = pca.fit_transform(x_train_valid_scaled)
var_pca_ratio = pca.explained_variance_ratio_.sum()
print(var_pca_ratio)

x_train_pca = x_train_valid_pca[:len(x_train)]
x_valid_pca = x_train_valid_pca[len(x_train):]


param_grid = {'C': [1,10,100,1000], 'kernel': ['linear', 'rbf', 'poly', 'sigmoid']}
svm_model = svm.SVC()
grid_search = GridSearchCV(svm_model, param_grid, scoring='accuracy', cv=5)
grid_search.fit(x_train_pca, y_train)

best_params = grid_search.best_params_
print("Best Parameters:", best_params)

final_svm_model = svm.SVC(**best_params)
final_svm_model.fit(x_train_pca, y_train)

file_save = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\model_vgg\final_svm.pkl'
with open(file_save, 'wb') as file:
    pickle.dump(final_svm_model, file)

pred = final_svm_model.predict(x_valid_pca)
print('Accuracy:', accuracy_score(y_valid, pred))
print('Confusion matrix:\n', confusion_matrix(y_valid, pred))
print(len(x_train_pca))
print(len(x_valid_pca))
print(len(y_train))
print(len(y_valid))
print('F1_score:', f1_score(y_valid, pred))
print('Classification_report:\n', classification_report(y_valid, pred))
