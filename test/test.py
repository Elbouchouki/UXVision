import cv2
from traitement import Database, Person
import json
import sqlite3
import numpy as np
from face_detection import Detection
from app_functions import *
import json
import face_recognition
# c = sqlite3.connect('test.db')
# # from face_detection import Detection
# # import app_functions
# faces = Database().get_encoded_faces()
# # imgdiractory = openfilename()
# # print(unknown_image_encoded(imgdiractory))
# # print(classify_face(imgdiractory, faces))
cap = cv2.VideoCapture(0)
while True:
    imgResult = Detection().detect_object(cap)
    # print("s")
    # print(imgResult.shape[1])
    # print("z")
    # print(imgResult.shape[0])
    # scale_percent = int(self.ui.detection_Object_label.height() /
    #                     imgResult.shape[0])
    scale = 1.5
    # print(scale_percent)
    width = int(imgResult.shape[1] * scale)
    height = int(imgResult.shape[0] * scale)
    dim = (width, height)
    imgResult = cv2.resize(
        imgResult, dim, interpolation=cv2.INTER_AREA)
    # frame = cv2.cvtColor(imgResult, cv2.COLOR_BGRA2RGB)
    # image = QtGui.QImage(
    #     frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
    # self.ui.detection_Object_label.setPixmap(
    #     QtGui.QPixmap.fromImage(image))
    cv2.imshow('image:', imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
# #faces = get_encoded_faces()
# Detection().
# print(count_cameras())
# known_face_names = list(x.keys())
# print(x)
# print("-------")
# print(known_face_names)
# print(app_functions.count_cameras())

# faces = Detection.get_encoded_faces()
# print(faces)
# cap = cv2.VideoCapture(0)
# while True:
#     success, img = cap.read()
#     Detection.classify_face(img, faces)


# c.execute("create table IF NOT EXISTS test (id text,array TEXT)")
# textArray = """[-0.0921189  0.10804491  0.01206842 -0.06742766  0.02131785 -0.00944963
#  -0.08901617 -0.08837023  0.18720011 -0.10261353  0.24677983  0.09093346
#  -0.20054527 -0.15108757  0.06505425  0.11533739 -0.17863075 -0.0837366
#  -0.10707912 -0.11226226  0.01597477 -0.01571964  0.08959471  0.04245619
#  -0.13219261 -0.35358673 -0.06719842 -0.18043683 -0.00405885 -0.10557368
#  -0.0815929   0.00083615 -0.1745722  -0.11002942  0.01989344 -0.01551655
#   0.01531288  0.01455681  0.21047349  0.04439625 -0.12220585  0.08526692
#   0.00688073  0.22766992  0.29060006  0.07953011 -0.0014989  -0.08076115
#   0.1084514  -0.22958787  0.07180249  0.1551846   0.08303971  0.02995162
#   0.09462071 -0.18115211 -0.00416605  0.0856135  -0.15534748  0.01634451
#   0.00887544 -0.07963546 -0.05128211  0.04506867  0.21074614  0.12033761
#  -0.12597732 -0.05389659  0.14199698 -0.03057     0.0238723   0.01822711
#  -0.19098863 -0.20637414 -0.2397154   0.08851958  0.3598046   0.18907297
#  -0.20777099  0.00896783 -0.2062311   0.02725045  0.07220636  0.0054231
#  -0.0712443  -0.13383803 -0.02750563  0.05349731  0.07980113  0.04683068
#  -0.04179098  0.2114238  -0.03052987  0.06069869  0.00970842  0.0569739
#  -0.14218836 -0.02764065 -0.16824165 -0.06568509  0.02578323 -0.02629276
#   0.05241827  0.149819   -0.23751391  0.05948379  0.01045479 -0.03940719
#   0.03176928  0.07968393 -0.02629136 -0.05069186  0.06405118 -0.23700301
#   0.24312113  0.25118503  0.02628306  0.16499369  0.06820199  0.01882301
#  -0.0166764  -0.03251434 -0.17521317 -0.04624973  0.03823926  0.07479692
#   0.07123534  0.00535625]"""
# print(textArray)
# textArray = textArray[1:-1]
# array = textArray.split()
# jarray = json.dumps(array)
# x = "asdasd"
# c.execute("insert into test values('"+x+"','"+jarray+"')")
# c.commit()
# # l = c.execute("select array from test")
# # for row in l:
# #     print(json.loads(row[0]))

############
# encode = face_detection.unknown_image_encoded("hmara.png")
# stringArray = str((np.array2string(encode))[1:-1]).split()
# jarray = json.dumps(stringArray)
#######
# l = c.execute("select array from test")
# j = []
# for row in l:
#     j = json.loads(row[0])
# for i in range(len(j)):
#     j[i] = float(j[i])
# array = np.array(j)
# print(array)


# textArray = encode[1:-1]
# print("----\n")
# print(textArray)
# array = str(textArray).split()
# print("----\n")
# print(array)
# jarray = json.dumps(array)
# print("----\n")
# print(jarray)
