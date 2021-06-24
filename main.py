import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                          QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                         QIcon, QImage, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from app_modules import *
# Pyrcc5 app_icons.qrc -o app_icons.py
# python -m PyQt5.uic.pyuic -x gui.ui -o ui_main.py


class MainWindow(QtWidgets.QMainWindow):

    VIDEO_STATE = 0
    # <--constructor-->

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        UIFunctions.uiDefinitions(self)
        # <--drag and move event-->

        def moveWindow(event):
            # <--iF MAXIMIZED CHANGE TO NORMAL-->
            if UIFunctions.getStatus() == 1:
                UIFunctions.maximize_restore(self)
            # <--if left clicked change window position-->
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        # <--apply drag event to my frame-->
        self.ui.top_bar_drag_frame.mouseMoveEvent = moveWindow

    # <--form button handlers-->
    def Button(self):

        # <--get the clicked button-->
        btnWidget = self.sender()

        # <--check if a video detection is running ,if so press one of stop buttons to stop it-->
        if(self.VIDEO_STATE == 1):
            self.ui.btn_face_video_stop.click()

        # <--pages navigation-->

        # <--person page-->
        if btnWidget.objectName() == "btn_person":
            self.ui.person_stackedWidget.setCurrentWidget(
                self.ui.allPerson_page)
            self.ui.all_stackedWidget.setCurrentWidget(self.ui.person_page)
            UIFunctions.resetStyle(self, "btn_person")
            UIFunctions.labelPage(self, "Personnes")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu(btnWidget.styleSheet()))
            UIFunctions.resetStyle_person(self, "btn_person_all")
            self.ui.btn_person_all.setStyleSheet(
                UIFunctions.selectMenu_person(self.ui.btn_person_all.styleSheet()))
        # <--face detection page navigation-->
        if btnWidget.objectName() == "btn_faceDetection":
            self.ui.all_stackedWidget.setCurrentWidget(
                self.ui.faceDetection_page)
            UIFunctions.resetStyle(self, "btn_faceDetection")
            UIFunctions.labelPage(self, "Reconnaissance faciale")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu(btnWidget.styleSheet()))
        # object detection page
        if btnWidget.objectName() == "btn_objectDetection":
            self.ui.all_stackedWidget.setCurrentWidget(
                self.ui.objectDetection_page)
            UIFunctions.resetStyle(self, "btn_objectDetection")
            UIFunctions.labelPage(self, "Detection d'objets")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu(btnWidget.styleSheet()))
        # person page -> add
        if btnWidget.objectName() == "btn_add_person_location1":
            UIFunctions.resetStyle(self, "btn_person")
            UIFunctions.resetStyle_person(self, "btn_person_add")
            self.ui.btn_person_add.click()
        # person page -> add
        if btnWidget.objectName() == "btn_add_person_location2":
            UIFunctions.resetStyle(self, "btn_person")
            UIFunctions.resetStyle_person(self, "btn_person_add")
            self.ui.btn_person_add.click()
        # buttons in person page
        if btnWidget.objectName() == "btn_person_add":
            self.ui.all_stackedWidget.setCurrentWidget(self.ui.person_page)
            self.ui.person_stackedWidget.setCurrentWidget(
                self.ui.addPerson_page)
            UIFunctions.resetStyle_person(self, "btn_person_add")
            UIFunctions.labelPage(self, "Personnes | ajout")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu_person(btnWidget.styleSheet()))
            self.ui.btn_person.setStyleSheet(
                UIFunctions.selectMenu(self.ui.btn_person.styleSheet()))
            UIFunctions.resetStyle_person(self, "btn_person_add")
            self.ui.btn_person_add.setStyleSheet(
                UIFunctions.selectMenu_person(self.ui.btn_person_add.styleSheet()))
        if btnWidget.objectName() == "btn_person_all":
            self.ui.person_stackedWidget.setCurrentWidget(
                self.ui.allPerson_page)
            UIFunctions.resetStyle_person(self, "btn_person_all")
            UIFunctions.labelPage(self, "Personnes")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu_person(btnWidget.styleSheet()))
        if btnWidget.objectName() == "btn_person_update":
            self.ui.person_stackedWidget.setCurrentWidget(
                self.ui.updatePerson_page)
            UIFunctions.resetStyle_person(self, "btn_person_update")
            UIFunctions.labelPage(self, "Personnes | modification")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu_person(btnWidget.styleSheet()))
        if btnWidget.objectName() == "btn_person_delete":
            self.ui.person_stackedWidget.setCurrentWidget(
                self.ui.deletePerson_page)
            UIFunctions.resetStyle_person(self, "btn_person_delete")
            UIFunctions.labelPage(self, "Personnes | suppression")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu_person(btnWidget.styleSheet()))
        if btnWidget.objectName() == "btn_images_return":
            self.ui.btn_person_all.click()
        if btnWidget.objectName() == "btn_more":
            model = self.ui.person_table.selectedIndexes()
            if not model:
                self.show_popup("Personne non Selectionnée",
                                "Veuillez Selectionner une personne !")
                return None
            nom = self.ui.person_table.model().data(model[1])
            prenom = self.ui.person_table.model().data(model[2])
            UIFunctions.setNomImageLabel(self, nom)
            UIFunctions.setPrenomImageLabel(self, prenom)
            self.ui.person_stackedWidget.setCurrentWidget(
                self.ui.Images_page)
            UIFunctions.labelPage(self, "Personnes | Images")
            person = Person(nom, prenom)
            fPerson = Database().get_person(person)
            Images = Database().get_person_images(fPerson)
            tabRow = 0
            self.ui.images_tableWidget.setRowCount(tabRow)
            for image in Images:
                self.ui.images_tableWidget.setRowCount(tabRow+1)

                self.ui.images_tableWidget.setItem(
                    tabRow, 0, QtWidgets.QTableWidgetItem(str(image[0])))

                self.ui.images_tableWidget.setCellWidget(
                    tabRow, 1, self.getImageLabel(image[1]))
                tabRow += 1
        if btnWidget.objectName() == "btn_close":
            self.close()

            # mouse press event

    def face_img_detection(self):
        # try:
        print(1)
        img = self.browseImage()
        faces = Database().get_encoded_faces()
        print(2)
        imgResult, facesResult = FaceRecognition(
            faces, None, None).classify_img(img)
        width = int(imgResult.shape[1])
        height = int(imgResult.shape[0])
        width = int(
            (imgResult.shape[1] * self.ui.frame_OD.height()) / imgResult.shape[0])
        height = self.ui.frame_OD.height()
        dim = (width, height)
        imgResult = cv2.resize(
            imgResult, dim, interpolation=cv2.INTER_AREA)
        frame = cv2.cvtColor(imgResult, cv2.COLOR_BGRA2RGB)
        image = QtGui.QImage(
            frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        print(3)
        self.ui.detection_faceDetection_label.setPixmap(
            QtGui.QPixmap.fromImage(image))
        string = "Personnes : "+str(len(facesResult))
        self.ui.warning_faceDetection_label.setText(string)
        print(4)
        # except:
        #     pass

    def stop_video_loop(self):
        self.VIDEO_STATE = 0

    def object_video_detection(self):
        self.ui.btn_object_video_stop.show()
        self.ui.btn_object_video_detect.hide()
        if(self.VIDEO_STATE == 1):
            self.ui.btn_object_video_stop.click()
        else:
            self.VIDEO_STATE = 1
            x = self.ui.comboBox_camera_obj.currentIndex()
            if x != -1:
                # Detection().setupYOLO()
                cap = cv2.VideoCapture(x)

                thread = ObjectDetection(cap, self.ui)
                thread.start()
                while True:
                    if cv2.waitKey(1) & self.VIDEO_STATE == 0:
                        thread.terminate()
                        break
                cap.release()
                self.ui.btn_object_video_stop.hide()
                self.ui.btn_object_video_detect.show()
                self.ui.detection_Object_label.clear()
            else:
                self.show_popup("Camera non choisie",
                                "Veuillez Selectionner une Camera !")

    def face_video_detection(self):
        self.ui.btn_face_video_detect.hide()
        self.ui.btn_face_video_stop.show()
        if(self.VIDEO_STATE == 1):
            self.ui.btn_face_video_stop.click()
        else:
            self.VIDEO_STATE = 1
            x = self.ui.comboBox_camera.currentIndex()
            if x != -1:
                self.ui.warning_faceDetection_label.setText(
                    "Veuillez patienter...")
                faces = Database().get_encoded_faces()
                video_capture = cv2.VideoCapture(x)

                thread = FaceRecognition(
                    faces, video_capture, self.ui)
                thread.start()
                while True:
                    if cv2.waitKey(1) & self.VIDEO_STATE == 0:
                        thread.terminate()
                        break
                video_capture.release()
                self.ui.btn_face_video_detect.show()
                self.ui.btn_face_video_stop.hide()
                self.ui.detection_faceDetection_label.clear()
            else:
                self.show_popup("Camera non choisie",
                                "Veuillez Selectionner une Camera !")

    def count_cameras(self):
        max_tested = 20
        for i in range(max_tested):
            temp_camera = cv2.VideoCapture(i)
            if temp_camera.isOpened():
                temp_camera.release()
                continue
            return i

    def getImageLabel(self, image):
        imgLabel = QtWidgets.QLabel(None)
        imgLabel.setText("")
        imgLabel.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image)
        imgLabel.setPixmap(pixmap)
        return imgLabel

    def browseImage(self):
        filename = QFileDialog.getOpenFileName(
            self, 'Open File', 'c\\', 'Image files(*.jpg *.png)')
        imagePath = filename[0]
        return imagePath

    def storeFace(self):
        try:
            image = open(self.browseImage(), 'rb')
            imgBinary = Database().convertImgToBinary(image)
            nom = self.ui.nom_image_label.text()
            prenom = self.ui.prenom_image_label.text()
            person = Person(nom, prenom)
            id = Database().get_person(person).getId()
            encode = Detection().unknown_image_encoded(image)
            face = Face(id, imgBinary, encode)
            Database().add_face(face)
            self.show_popup("Success", "Entregistrement Ajouté")
            self.ui.btn_more.click()
        except:
            self.show_popup(
                "Erreur", "Aucun visage n'a été détecté ou L'image est invalide")

    def deleteFace(self):
        model = self.ui.images_tableWidget.selectedIndexes()
        if not model:
            self.show_popup("Personne non Selectionnée",
                            "Veuillez Selectionner une personne !")
            return None
        id = self.ui.images_tableWidget.model().data(model[0])
        face = Face(None, None, None)
        face.set_face_id(id)

        Database().delete_face(face)
        self.show_popup("Success", "Image Supprimée")
        self.ui.btn_more.click()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def comboChanged(self):
        etat = self.ui.person_update_comboBox.currentIndex() != -1
        self.ui.nom_update_lineEdit.setEnabled(etat)
        self.ui.prenom_update_lineEdit.setEnabled(etat)
        # load all person to person_table

    def updatePerson(self):
        if self.ui.person_update_comboBox.currentIndex() == -1:
            self.show_popup("Personne non selectionnée",
                            "veulliez choisir une personne d'abord")
            self.ui.person_update_comboBox.setFocus()
        elif not UIFunctions.isValideInput(self.ui.nom_update_lineEdit):
            self.show_popup("Erreur de saisie", "Nom invalide")
            self.ui.nom_update_lineEdit.setFocus()
        elif not UIFunctions.isValideInput(self.ui.prenom_update_lineEdit):
            self.show_popup("Erreur de saisie", "prenom invalide")
            self.ui.prenom_update_lineEdit.setFocus()
        else:
            fullname = str(
                self.ui.person_update_comboBox.currentText()).split()
            personOld = Person(fullname[0], fullname[1])
            nom = self.ui.nom_update_lineEdit.text()
            prenom = self.ui.prenom_update_lineEdit.text()
            personNew = Person(nom, prenom)
            Database().update_person(personNew, personOld)
            self.show_popup("Success", "Enregistrement modifié")
            self.loadPerson()
            self.loadComboBoxs()

    def deletePerson(self):
        if self.ui.person_delete_comboBox.currentIndex() == -1:
            self.show_popup("Personne non selectionnée",
                            "veulliez choisir une personne d'abord")
            self.ui.person_delete_comboBox.setFocus()
        else:
            fullname = str(
                self.ui.person_delete_comboBox.currentText()).split()
            person = Person(fullname[0], fullname[1])
            Database().delete_person(person)
            self.show_popup("Success", "Enregistrement supprimé")
            self.loadPerson()
            self.loadComboBoxs()

    def addPerson(self):
        if not UIFunctions.isValideInput(self.ui.nom_add_lineEdit):
            self.show_popup("Erreur de saisie", "Nom invalide")
            self.ui.nom_add_lineEdit.setFocus()
        elif not UIFunctions.isValideInput(self.ui.prenom_add_lineEdit):
            self.show_popup("Erreur de saisie", "prenom invalide")
            self.ui.prenom_add_lineEdit.setFocus()
        else:
            person = Person(self.ui.nom_add_lineEdit.text(),
                            self.ui.prenom_add_lineEdit.text())
            listPerson = Database().get_all_person()
            for per in listPerson:
                if per.__eq__(person):
                    self.show_popup("Erreur", "Cette personne existe déja !")
                    self.ui.nom_add_lineEdit.setFocus()
                    return None
            Database().add_person(person)
            self.ui.nom_add_lineEdit.setText("")
            self.ui.prenom_add_lineEdit.setText("")
            self.show_popup("Success", "Enregistrement ajouté")
            self.loadPerson()
            self.loadComboBoxs()

    def show_popup(self, title, text):
        pop = QMessageBox()
        pop.setWindowTitle(title)
        pop.setWindowIcon(QtGui.QIcon(u"icons/access-denied.png"))
        pop.setText(text)
        pop.setStyleSheet(
            "QLabel{min-width:500 px; font-size: 24px;}")
        # pop.setIcon(QMessageBox.Warning)
        pop.setStandardButtons(QMessageBox.Ok)
        pop.buttonClicked.connect(lambda: pop.close())
        pop.exec_()

    def loadCameras(self):
        self.ui.comboBox_camera.clear()
        self.ui.comboBox_camera_obj.clear()
        for i in range(0, self.count_cameras()):
            self.ui.comboBox_camera.addItem("Cam "+str(i+1))
            self.ui.comboBox_camera_obj.addItem("Cam "+str(i+1))
        self.ui.comboBox_camera.setCurrentIndex(0)
        self.ui.comboBox_camera_obj.setCurrentIndex(0)

    def loadComboBoxs(self):
        self.ui.person_update_comboBox.clear()
        self.ui.person_delete_comboBox.clear()
        persons = Database().get_all_person()
        for person in persons:
            fullname = person.getNom()+" "+person.getPrenom()
            self.ui.person_update_comboBox.addItem(fullname)
            self.ui.person_delete_comboBox.addItem(fullname)
        self.ui.person_update_comboBox.setCurrentIndex(-1)
        self.ui.person_delete_comboBox.setCurrentIndex(-1)

    def loadPerson(self):
        tabRow = 0
        persons = Database().get_all_person()
        for person in persons:
            self.ui.person_table.setRowCount(tabRow+1)
            self.ui.person_table.setItem(
                tabRow, 0, QtWidgets.QTableWidgetItem(str(person.getId())))
            self.ui.person_table.setItem(
                tabRow, 1, QtWidgets.QTableWidgetItem(str(person.getNom())))
            self.ui.person_table.setItem(
                tabRow, 2, QtWidgets.QTableWidgetItem(str(person.getPrenom())))
            tabRow += 1


def main():
    Database().initiate()
    app = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting...")


if __name__ == "__main__":
    main()
