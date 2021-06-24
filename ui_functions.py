# ==> GUI FILE
from os import replace

from PyQt5.QtCore import QThread
from main import *
# from app_modules import *

# ==> GLOBALS
GLOBAL_STATE = 0


class UIFunctions(MainWindow):
    GLOBAL_STATE = 0
    # ==> RETURN STATUS

    def getStatus():
        return GLOBAL_STATE
    # ==> SET STATUS

    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    def setNomImageLabel(self, text):
        self.ui.nom_image_label.setText(text)

    def setPrenomImageLabel(self, text):
        self.ui.prenom_image_label.setText(text)

    def labelPage(self, text):
        self.ui.pageName_label.setText(text)

    def removeTitleBar(status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def scrollBar(self, status):
        self.ui.scrollBar_frame.setMaximumWidth(20*(status))

    def uiDefinitions(self):
        # creating a blur effect
        # self.blur_effect = QtWidgets.QGraphicsBlurEffect(blurRadius=5)
        # self.ui.left_frame.setGraphicsEffect(self.blur_effect)
        self.ui.btn_face_video_stop.hide()
        self.ui.btn_object_video_stop.hide()
        self.ui.btn_object_video_detect.clicked.connect(
            lambda: self.object_video_detection())
        self.ui.btn_face_video_stop.clicked.connect(
            lambda: self.stop_video_loop())
        self.ui.btn_object_video_stop.clicked.connect(
            lambda: self.stop_video_loop())
        self.ui.nom_update_lineEdit.setEnabled(False)
        self.ui.prenom_update_lineEdit.setEnabled(False)
        # btn menu
        self.ui.btn_menu.clicked.connect(
            lambda: UIFunctions.toggleMenu(self, 500, True))
        # fonctional buttons
        self.ui.btn_face_img_detect.clicked.connect(
            lambda: self.face_img_detection())
        self.ui.btn_face_video_detect.clicked.connect(
            lambda: self.face_video_detection())
        self.ui.btn_add_img.clicked.connect(lambda: self.storeFace())
        self.ui.btn_del_img.clicked.connect(lambda: self.deleteFace())
        self.ui.btn_add_person.clicked.connect(
            lambda: self.addPerson())
        self.ui.btn_delete_person.clicked.connect(
            lambda: self.deletePerson()
        )
        self.ui.person_update_comboBox.currentIndexChanged.connect(
            lambda: self.comboChanged())
        self.ui.btn_update_person.clicked.connect(lambda: self.updatePerson())

        # menu buttons actions
        self.ui.btn_images_return.clicked.connect(lambda: self.Button())
        self.ui.btn_more.clicked.connect(lambda: self.Button())
        self.ui.btn_person.clicked.connect(lambda: self.Button())
        self.ui.btn_faceDetection.clicked.connect(lambda: self.Button())
        self.ui.btn_objectDetection.clicked.connect(lambda: self.Button())
        self.ui.btn_add_person_location1.clicked.connect(lambda: self.Button())
        self.ui.btn_add_person_location2.clicked.connect(lambda: self.Button())
        self.ui.btn_person_all.clicked.connect(lambda: self.Button())
        self.ui.btn_person_add.clicked.connect(lambda: self.Button())
        self.ui.btn_person_update.clicked.connect(lambda: self.Button())
        self.ui.btn_person_delete.clicked.connect(lambda: self.Button())
        self.setWindowTitle("UxVision")
        UIFunctions.labelPage(self, "Accueil")
        self.ui.all_stackedWidget.setCurrentWidget(self.ui.welcome_page)
        self.ui.btn_add_person_location1.hide()
        # self.ui.btn_more.setEnabled(False)
        UIFunctions.scrollBar(self, False)
        # windows shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.main_frame.setGraphicsEffect(self.shadow)
        # remove default title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # table
        tableColumnWidth = self.ui.person_stackedWidget.width()*3
        self.ui.person_table.horizontalHeader().setDefaultSectionSize(tableColumnWidth)
        self.ui.images_tableWidget.verticalHeader().setDefaultSectionSize(600)
        self.ui.images_tableWidget.horizontalHeader().setDefaultSectionSize(600)
        self.ui.person_table.setColumnWidth(0, 0)
        self.ui.images_tableWidget.setColumnWidth(0, 0)
        self.loadCameras()
        self.loadPerson()
        self.loadComboBoxs()
        # ==> MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        # ==> MAXIMIZE/RESTORE
        self.ui.btn_maximize_restore.clicked.connect(
            lambda: UIFunctions.maximize_restore(self))
        # SHOW ==> CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.Button())

    def showVideo(self, imgResult):
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
        self.ui.detection_faceDetection_label.setPixmap(
            QtGui.QPixmap.fromImage(image))

    def isValideInput(widget):
        string = widget.text()
        return (string != "")

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        stylesheet = self.ui.left_frame.styleSheet()
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setIcon(
                QtGui.QIcon(u"icons/browser.png"))
            self.ui.main_frame.setStyleSheet(self.ui.main_frame.styleSheet().replace(
                "border-radius: 20px;", "border-radius: 0px;"))

            stylesheet.replace(
                "border-bottom-left-radius: 20px;", "border-bottom-left-radius: 0px;")
            stylesheet.replace(
                "border-top-left-radius: 20px;", "border-top-left-radius: 0px;")
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.ui.verticalLayout_14.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setIcon(
                QtGui.QIcon(u"icons/enlarge.png"))
            self.ui.main_frame.setStyleSheet(self.ui.main_frame.styleSheet().replace(
                "border-radius: 0px;", "border-radius: 20px;"))
            stylesheet.replace(
                "border-bottom-left-radius: 0px;", "border-bottom-left-radius: 20px;")
            stylesheet.replace(
                "border-top-left-radius: 0px;", "border-top-left-radius: 20px;")
        self.ui.left_frame.setStyleSheet(stylesheet)

    def toggleMenu(self, maxWidth, enable):
        if enable:
            width = self.ui.left_frame.width()
            maxExtend = maxWidth
            standard = 80

            if width == 80:
                widthExtended = maxExtend
                self.ui.btn_add_person_location1.show()
                self.ui.btn_add_person_location2.hide()
                self.ui.appName_label.setText(
                    "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600; color:#6d6d6d;\">Ux</span><span style=\" font-size:9pt; font-weight:600; color:#de063b;\">Vision</span></p></body></html>")
            else:
                self.ui.btn_add_person_location1.hide()
                self.ui.btn_add_person_location2.show()
                self.ui.appName_label.setText(
                    "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600; color:#6d6d6d;\">Ux</span><span style=\" font-size:9pt; font-weight:600; color:#de063b;\">V</span></p></body></html>")
                widthExtended = standard

            self.animation = QPropertyAnimation(
                self.ui.left_frame, b"minimumWidth")
            self.animation.setDuration(500)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

# styling menu default
    def selectMenu(getStyle):
        select = getStyle + \
            ("QPushButton { border-left: 3px solid rgb(222, 6, 59); }")
        return select

    def deselectMenu(getStyle):
        deselect = getStyle.replace(
            "QPushButton { border-left: 3px solid rgb(222, 6, 59); }", "")
        return deselect

    def resetStyle(self, widget):
        for w in self.ui.buttons_frame.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))
# styling menu in person page

    def selectMenu_person(getStyle):
        select = getStyle + \
            ("QPushButton { border-bottom:3px solid rgb(222, 6, 59); color: rgb(0, 0, 0); }")
        return select

    def deselectMenu_person(getStyle):
        deselect = getStyle.replace(
            "QPushButton { border-bottom:3px solid rgb(222, 6, 59); color: rgb(0, 0, 0); }", "")
        return deselect

    def resetStyle_person(self, widget):
        for w in self.ui.btns_person_frame.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(
                    UIFunctions.deselectMenu_person(w.styleSheet()))
