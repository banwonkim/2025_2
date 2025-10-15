import cv2
import numpy as np
import sys
from PySide6.QtWidgets import (QApplication,QWidget,
    QSizePolicy,
    QHBoxLayout,QVBoxLayout,QGridLayout,
    QLabel,
    QLineEdit,QPushButton,QComboBox,
    QMainWindow)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage,QPixmap
def try_float(v):
    try:
        v=float(v)
    except:
        v=0.0
    return v


class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.addWidget()
    def conv_to_pixmap(self,img):
        if len(img.shape)<3:
            h, w= img.shape
            ch=1
            form=QImage.Format.Format_Grayscale8

        else:
            h,w,ch=img.shape
            form = QImage.Format.Format_RGB888
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        qimg = QImage(img.data, w, h, ch * w, form)

        scaled_img = qimg.scaled(640, 480, Qt.KeepAspectRatio)

        self.label_img.setPixmap(QPixmap.fromImage(scaled_img))

    def show_image(self,img):

        #cv2.imshow("",img)
        #cv2.waitKey(0)
        self.conv_to_pixmap(img)
        #self.label_img.setPixmap(QPixmap(self.edit_path.text()))

    def connect_btn_loadimage(self):
        print(self.edit_path.text())
        try:
            self.img = cv2.imread(self.edit_path.text(), cv2.IMREAD_COLOR)
            self.img_org=self.img
            self.show_image(self.img)
        except:
            print('failed to load image')
    def connect_btn_binaryimage(self):
        try:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.show_image(self.img)
        except:
            print('failed to convert binary image')
    def connect_btn_geometryimage(self):
        pass
    def connect_btn_initpos(self):
        for i in range(8):
            #
            y=i//2
            x=i%2
            gy=(y // 2)
            gx=(y % 2) * 3 + (x + 1)
            #print('(',gy,gx,')')
            #12 45 gy
            self.grid_widgets[gy*6+gx].setText("0")
            #self.grid_widgets[2].setText("0")
        self.connect_btn_persimg()
        self.show_image(self.img)
    def get_pos(self):
        self.pos = [[try_float(self.grid_widgets[1].text()),
                try_float(self.grid_widgets[2].text())],

               [try_float(self.grid_widgets[4].text()),
                try_float(self.grid_widgets[5].text())],

               [try_float(self.grid_widgets[6 + 1].text()),
                try_float(self.grid_widgets[6 + 2].text())],

               [try_float(self.grid_widgets[6 + 4].text()),
                try_float(self.grid_widgets[6 + 5].text())]]
    def draw_point(self,point,num):
        match num:
            case 0:
                color = (255, 0, 0)
            case 1:
                color   = (0, 255, 0)
            case 2:
                color = (0, 0, 255)
            case 3:
                color = (0, 255, 255)
        cv2.circle(self.img, (int(point[0]), int(point[1])),
                   9, color, -1)
    def connect_btn_persimg(self):
        self.get_pos()
        rows,cols=self.img.shape[:2]
        img_org=self.img.copy()
        i=0
        for p in self.pos:
            print(p)
            self.draw_point(p,i)
            i += 1
        self.show_image(self.img)
        self.img=img_org
    #def checkFocus(self):

    def mousePressEvent(self, event):
        focus_widget=QApplication.instance().focusWidget()
        found=-1
        for p in range(len(self.grid_widgets)):
            if focus_widget==self.grid_widgets[p]:
                print(p//3,'번째다 야')
                found=p//3
        if found==-1:
            print('못 찾음')
            return
        x=event.position().x()-self.label_img.x()
        y = event.position().y() - self.label_img.y()

        p1=self.grid_widgets[found * 3 + 1]
        p2=self.grid_widgets[found*3+2]
        p1.setText(f"{x}")
        p2.setText(f"{y}")

        self.draw_point((float(p1.text()),float(p2.text())),found)
        #cv2.getPerspectiveTransform()
    def addWidget(self):

        self.btn_loadimage=QPushButton("Load Image")
        self.btn_loadimage.clicked.connect(self.connect_btn_loadimage)

        self.btn_binaryimage = QPushButton("Binary Image")
        self.btn_binaryimage.clicked.connect(self.connect_btn_binaryimage)

        self.edit_path=QLineEdit("./road_30.jpg")


        #main{label,layout1, layout2, {grid_layout,btn,btn}}
        v_layout=QVBoxLayout()
        self.label_img=QLabel("Enter a PATH of image")
        #layout1
        h_layout1=QHBoxLayout()
        h_layout1.addWidget(self.edit_path)
        h_layout1.addWidget(self.btn_loadimage)
        h_layout1.addWidget(self.btn_binaryimage)

        #layout2
        self.combo_geometry=QComboBox()
        self.combo_geometry.addItem("none")
        self.combo_geometry.addItem("flip")
        self.combo_geometry.addItem("translation")


        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(QLabel("Geometry type:"))
        h_layout2.addWidget(self.combo_geometry)
        h_layout2.addWidget(QPushButton("Geometry Image"))

        h_layout3=QHBoxLayout()

        #layout3_1
        #layout3_2

        self.grid_widgets=[QLabel("Pos1"),QLineEdit(), QLineEdit(),
                            QLabel("Pos2"),QLineEdit(),QLineEdit(),
                           QLabel("Pos3"),QLineEdit(), QLineEdit(),
                           QLabel("Pos4"),QLineEdit(), QLineEdit()]

        #self.edit_pos[0][0]

        grid_layout=QGridLayout()
        for pos in range(len(self.grid_widgets)):
            grid_layout.addWidget(self.grid_widgets[pos], pos//6, pos%6)
            if(pos%3!=0):
                self.grid_widgets[pos].setReadOnly(True)
            '''
                (y//2),(y%2)*3+(x+1)
                
                y=0 x=0 (0,1) ,0+1
                y=0 x=1 (0,2) ,0+2
                y=1 x=0 (0,4) ,3+1
                y=1 x=1 (0,5) ,3+2
                y=2 x=0 (1,1)
                y=2 x=1
                y=3
            '''

        btn_initpos=QPushButton("Initialize Pos")
        btn_initpos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_initpos.clicked.connect(self.connect_btn_initpos)


        btn_persimg=QPushButton("Perspective Image")
        btn_persimg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_persimg.clicked.connect(self.connect_btn_persimg)

        h_layout3.addLayout(grid_layout)
        h_layout3.addWidget(btn_initpos)
        h_layout3.addWidget(btn_persimg)

        v_layout.addWidget(self.label_img)
        v_layout.addLayout(h_layout1)
        v_layout.addLayout(h_layout2)
        v_layout.addLayout(h_layout3)

        widget=QWidget(self)
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

if __name__=='__main__':
    app=QApplication()
    w=Form()
    w.show()

    sys.exit(app.exec())