from skimage.feature import hog
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from face_recognition import face_locations, load_image_file, face_landmarks
import cv2
import numpy as np
from imutils import paths
import os
from sklearn.preprocessing import LabelEncoder
import time
import sys
'''class tiền xử lý ảnh để chuẩn bị dự liệu cho việc train'''
class PreprocessingFaceImg:
    def __init__(self):
        self.SIZE = (64,128)
        self.SOCHIEU = 3780#7*15*2*2*9
        self.pixels_per_cell = (8,8)
        self.cells_per_block = (2,2)
    '''xử lý tất cả các ảnh trong thư mực chứa ảnh train hoặc test'''
    def ManyFaceFeatures(self,derectory):
        #faces = list()
        try:
            path = list(paths.list_images(derectory))
            print("Dataset: "+str(len(path))+" images")
            x = np.zeros((self.SOCHIEU, len(path))) #tạo một mảng 2 chiều với giá trị 0 với kích thước 3780 x length
            count = 0
            print(len(path))
            for i in range(len(path)):
                print(i)
                try:
                    img = cv2.imread(path[i])
                    box = face_locations(img) # tìm tất cả các khuôn mặt có trong ảnh
                    if len(box) == 0:
                       continue
                    else:
                        top, right, bottom, left = box[0]
                        face = img[top:bottom, left:right]
                        face_resize = cv2.resize(face, self.SIZE)
                        # Use HOG to extract features of face images
                        fd, hog_image = hog(face_resize, orientations=9, pixels_per_cell= self.pixels_per_cell,cells_per_block= self.cells_per_block,visualize=True,transform_sqrt=True, multichannel=True)
                        x[:, i] = fd
                        count +=1
                        print(str(count) + " images was trained ==> "+ path[i])
                except:
                    print("Error ==> " + path[i])

            labels = [p.split(os.path.sep)[-2] for p in path]
        except:
            print("Error ==> " + path[i])
        return np.asarray(x), np.asarray(labels)

    def FaceFeatures(self,img_test):
        box = face_locations(img_test)
        if len(box) == 0:  # nếu k detect được khuôn mặt hoặc k có khuôn mặt trong màn hình thì return ảnh gốc
            return img_test, box
        else:
            #phần này để lấy đặc trưng của tất cả các khuôn mặt trong ảnh
            face_arr = []
            for i in box:
                x1, y1, x2, y2 = i
                img_crop = img_test[x1:x2, y2:y1]
                img_resize = cv2.resize(img_crop, self.SIZE)
                fd, hog_image = hog(img_resize, orientations=9, pixels_per_cell=self.pixels_per_cell,
                                    cells_per_block=self.cells_per_block, visualize=True, multichannel=True)
                face_arr.append(fd.T) 
            np.set_printoptions(threshold=sys.maxsize)
            face_arr = np.asarray(face_arr)
            return face_arr, box
    def encoder_label(self,labels):
        label_encoder = LabelEncoder()
        label = label_encoder.fit_transform(labels)
        return label    # trả về một mảng lables có các phần tử là các số nguyên ([0,0,0,0,1,1,1...])
class ModelAndPrediction:
    def __init__(self):
        self.C = 100
        self.gamma = 'scale'
        self.kernel = 'poly'
        self.degree = 3
    def BuiltModel(self, XTrain,YTrain):  # xây dựng thuật toán SVM
        model = SVC(kernel=self.kernel, degree= self.degree, gamma=self.gamma, C=self.C)
        model.probability=True
        model.fit(XTrain, YTrain)
        return model

if __name__ == '__main__':
    '''tiền xử lý dữ liệu rồi lưu thành 1 file npz để thuận tiện cho việc train và update model'''
    pre = PreprocessingFaceImg()
    #load folder train,thay ten model muon train
    link = 'image_model_26122021'
    folderName = link.split('/')[-1]
    X_train, labels = pre.ManyFaceFeatures(link)
    X_train = X_train.T
    #update model
    x_train_new = []
    if os.path.isfile('image_train_success/image_train_success.npz'):
        print("Start Update model-->")
        data = np.load('image_train_success/image_train_success.npz')
        x_data, x_data_label = data['arr_0'], data['arr_1']
        np.concatenate((x_data, X_train))
        x_train_new = np.vstack((np.array(x_data), np.array(X_train)))
        x_label_new = np.append(x_data_label,labels)
        print("Update model success-->")
    else:
        x_train_new = X_train
        x_label_new = labels
    #luu model update
    np.savez_compressed('image_train_success/image_train_success.npz', x_train_new, x_label_new)
    print("----> Train image success")
