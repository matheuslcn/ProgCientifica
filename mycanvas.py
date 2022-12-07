from operator import pos
from PyQt5 import QtOpenGL, QtCore
from PyQt5.QtWidgets import *
from OpenGL.GL import *

from he.hecontroller import HeController
from he.hemodel import HeModel
from geometry.segments.line import Line
from geometry.point import Point
from compgeom.tesselation import Tesselation

import json
from pprint import pprint
from mygrid import MyGrid

from tkinter.messagebox import showinfo
from tkinter.simpledialog import Tk

class MyCanvas(QtOpenGL.QGLWidget):
    
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.m_model = None
        self.m_w = 0 # width: GL canvas horizontal size
        self.m_h = 0 # height: GL canvas vertical size
        self.m_L = -50.0
        self.m_R = 50.0
        self.m_B = -50.0
        self.m_T = 50.0
        self.list = None
        self.m_buttonPressed = False
        self.m_pt0 = QtCore.QPointF(0.0,0.0)
        self.m_pt1 = QtCore.QPointF(0.0,0.0)
        self.m_hmodel = HeModel()
        self.m_controller = HeController(self.m_hmodel)
        self.colorList = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,0.5,0.5),(0.5,1,0.5),(0.5,0.5,1)]
        self.grid = None
        self.is_getting_shape = False

    def initializeGL(self):
        #glClearColor(1.0,1.0,1.0,1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)

        self.list = glGenLists(1)
        
        
    def resizeGL(self, _width, _height):
        self.m_w = _width
        self.m_h = _height
        if(self.m_model==None)or(self.m_model.isEmpty()): self.scaleWorldWindow(1.0)
        else:
            self.m_L,self.m_R,self.m_B,self.m_T = self.m_model.getBoundBox()
            self.scaleWorldWindow(1.1)

        glViewport (0, 0, self.m_w, self.m_h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(self.m_L,self.m_R,self.m_B,self.m_T,-1.0,1.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        # if (self.m_model==None)or(self.m_model.isEmpty()):
            # return
        glCallList(self.list)
        glDeleteLists(self.list, 1)
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)

        # Display model polygon RGB color at its vertices
        # interpolating smoothly the color in the interior
        # verts = self.m_model.getVerts()
        # glShadeModel(GL_SMOOTH)
        # glColor3f(0.0, 1.0, 0.0) # green
        # glBegin(GL_TRIANGLES)
        # for vtx in verts:
        #     glVertex2f(vtx.getX(), vtx.getY())
        # glEnd()
        glColor(1.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        if self.is_getting_shape:
            glVertex2f(pt0_U.x(), pt0_U.y())
            glVertex2f(pt0_U.x(), pt1_U.y())
            glVertex2f(pt1_U.x(), pt1_U.y())
            glVertex2f(pt1_U.x(), pt0_U.y())
            glVertex2f(pt0_U.x(), pt0_U.y())

        else:
            glVertex2f(pt0_U.x(), pt0_U.y())
            glVertex2f(pt1_U.x(), pt1_U.y())
            # glVertex2f(self.m_pt0.x(), self.m_pt0.y())
            # glVertex2f(self.m_pt1.x(), self.m_pt1.y())
        glEnd()
        if not((self.m_model == None) and (self.m_model.isEmpty())):
            verts = self.m_model.getVerts()
            glColor3f(0.0, 1.0, 0.0) # green
            glBegin(GL_TRIANGLES)
            for vtx in verts:
                glVertex2f(vtx.getX(), vtx.getY())
            glEnd()
            curves = self.m_model.getCurves()
            glColor3f(0.0, 0.0, 1.0) # blue
            glBegin(GL_LINES)
            for curv in curves:
                glVertex2f(curv.getP1().getX(), curv.getP1().getY())
                glVertex2f(curv.getP2().getX(), curv.getP2().getY())
            glEnd()
        
        if not (self.m_hmodel.isEmpty()):
            patches = self.m_hmodel.getPatches()
            for index, pat in enumerate(patches):
                pts = pat.getPoints()
                triangs = Tesselation.tessellate(pts)
                color_R = self.colorList[index%len(self.colorList)][0]
                color_G = self.colorList[index%len(self.colorList)][1]
                color_B = self.colorList[index%len(self.colorList)][2]
                for j in range(0, len(triangs)):
                    glColor3f(color_R, color_G, color_B)
                    glBegin(GL_TRIANGLES)
                    glVertex2d(pts[triangs[j][0]].getX(), pts[triangs[j][0]].getY())
                    glVertex2d(pts[triangs[j][1]].getX(), pts[triangs[j][1]].getY())
                    glVertex2d(pts[triangs[j][2]].getX(), pts[triangs[j][2]].getY())
                    glEnd()
            segments = self.m_hmodel.getSegments()
            for curv in segments:
                ptc = curv.getPointsToDraw()
                glColor3f(0.0, 1.0, 1.0)
                glBegin(GL_LINES)
                for curv in curves:
                    glVertex2f(ptc[0].getX(), ptc[0].getY())
                    glVertex2f(ptc[1].getX(), ptc[1].getY())
                glEnd()

        if self.grid:
            for line in self.grid.grid:
                for point in line:
                    if point[2]:
                        glColor3f(0.0, 0.0, 0.0)
                        glBegin(GL_POINTS)
                        glVertex2f(point[0], point[1])
                        glEnd()

        
        glEndList()


    def setModel(self,_model):
        self.m_model = _model

    def fitWorldToViewport(self):
        print("fitWorldToViewport")
        if self.m_model == None:
            return
        self.m_L,self.m_R,self.m_B,self.m_T=self.m_model.getBoundBox()
        self.scaleWorldWindow(1.10)
        self.update()

    def scaleWorldWindow(self,_scaleFac):
        # Compute canvas viewport distortion ratio.
        vpr = self.m_h / self.m_w
        # Get current window center.
        cx = (self.m_L + self.m_R) / 2.0
        cy = (self.m_B + self.m_T) / 2.0
        # Set new window sizes based on scaling factor.
        sizex = (self.m_R - self.m_L) * _scaleFac
        sizey = (self.m_T - self.m_B) * _scaleFac
        # Adjust window to keep the same aspect ratio of the viewport.
        if sizey > (vpr*sizex):
            sizex = sizey / vpr
        else:
            sizey = sizex * vpr
        self.m_L = cx - (sizex * 0.5)
        self.m_R = cx + (sizex * 0.5)
        self.m_B = cy - (sizey * 0.5)
        self.m_T = cy + (sizey * 0.5)
        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def panWorldWindow(self, _panFacX, _panFacY):
        # Compute pan distances in horizontal and vertical directions.
        panX = (self.m_R - self.m_L) * _panFacX
        panY = (self.m_T - self.m_B) * _panFacY
        # Shift current window.
        self.m_L += panX
        self.m_R += panX
        self.m_B += panY
        self.m_T += panY
        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * dX / self.m_w
        mY = (self.m_h - _pt.y()) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QtCore.QPointF(x,y)


    def mousePressEvent(self, event):
        self.m_buttonPressed = True
        self.m_pt0 = event.pos()
        
        
    def mouseMoveEvent(self, event):
        if self.m_buttonPressed:
            self.m_pt1 = event.pos()
            self.update()


    def mouseReleaseEvent(self, event):
        self.m_pt1 = event.pos()
        if self.m_pt0 == self.m_pt1:
            return
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)

        if self.is_getting_shape:
            self.set_curve_on_shape(pt0_U, pt1_U)
        else:
            self.set_curve_on_model(pt0_U, pt1_U)

        self.update()
        self.repaint()

        # self.m_model.setCurve(self.m_pt0.x(),self.m_pt0.y(),self.m_pt1.x(),self.m_pt1.y())
        self.m_buttonPressed = False
        self.m_pt0 = self.m_pt1 = QtCore.QPointF(0.0, 0.0)

    
    # preencher o bounding box com pontos de raio x 
    def fillBB(self, _r):
        x_min,x_max,y_min,y_max = self.m_model.getBoundBox()
        model = HeModel()
        control = HeController(model)
        qt_x = int(x_max - x_min)
        qt_y = int(y_max - y_min)
        for i in range(0,int(qt_x/_r)):
            for j in range(0,int(qt_y/_r)):
                control.insertPoint([x_min+((i+1)*_r),y_min+((j+1)*_r)], _r)
        points = model.getPoints()
        return points

    def exportJson(self, espacamento):
        print(espacamento)
        self.grid = MyGrid()
        pudim = self.m_hmodel.getPatches()
        if len(pudim) == 0:
            root = Tk()
            root._temporary_ = True
            root.withdraw()
            showinfo("Erro", "Nenhuma região foi gerada")
            # msgBox = QMessageBox()
            # msgBox.setIcon(QMessageBox.Information)
            # msgBox.setText("Nenhuma região foi gerada")
            # msgBox.setWindowTitle("Erro")
            # msgBox.setStandardButtons(QMessageBox.Ok)
        # msgBox.buttonClicked.connect(msgButtonClick)

            # returnValue = msgBox.exec()
            return
        BBs = []
        for bb in pudim:
            BBs.append(bb.getBoundBox())
        pprint(BBs)
        self.grid.pega_bordas(BBs)
        print(f"ponto minimo ({self.grid.min_x}, {self.grid.min_y}), ponto maximo ({self.grid.max_x}, {self.grid.max_y})\n")
        self.grid.preencheBB(espacamento)
        # pprint(self.grid.grid)
        self.grid.atualiza_grid(pudim)
        self.update()
        self.repaint()
        connect = self.grid.pega_matriz_connect()
        # pprint(connect)
        pontos = self.grid.gera_pontos()
        # pprint(pontos)
        restricao = self.grid.gera_restricoes()
        # pprint(restricao)
        forca = self.grid.gera_forca() 
        # pprint(forca)

        print(f"quantidade de pontos ({self.grid.qtd_x * self.grid.qtd_y}, pontos em x {self.grid.qtd_x}, pontos em y {self.grid.qtd_y})\n")

        
        # points = self.fillBB(_r)
        json_data = {}
        json_data["coords"] = pontos
        json_data["connect"] = connect
        json_data["F"] = forca
        json_data["restrs"] = restricao

        with open(f'data({self.grid.qtd_x * self.grid.qtd_y}p).json', 'w') as outfile:
            json.dump(json_data, outfile)

    def create_shape(self):
        self.is_getting_shape = True
        patches = self.m_hmodel.getPatches()
        # desenha ou pega o bounding box
        bb = self.m_hmodel.getBoundBox()
        print(bb)
        p1 = QtCore.QPointF(bb[0]-1, bb[2]-1)
        p2 = QtCore.QPointF(bb[0]-1, bb[3]+1)
        p3 = QtCore.QPointF(bb[1]+1, bb[3]+1)
        p4 = QtCore.QPointF(bb[1]+1, bb[2]-1)
        self.set_curve_on_model(p1, p2)
        self.set_curve_on_model(p2, p3)
        self.set_curve_on_model(p3, p4)
        self.set_curve_on_model(p4, p1)
        # pega o patch do contorno
        patches2 = self.m_hmodel.getPatches()

        p = [p for p in patches2 if p not in patches][0]

        pts = p.getPoints()
        for pt in pts:
            print(f"({pt.getX()}, {pt.getY()})")
        
        

    def set_curve_on_model(self, pt0_U, pt1_U):
        self.m_model.setCurve(pt0_U.x(),pt0_U.y(),pt1_U.x(),pt1_U.y())
        p0 = Point(pt0_U.x(), pt0_U.y())
        p1 = Point(pt1_U.x(), pt1_U.y())
        segment = Line(p0, p1)
        self.m_controller.insertSegment(segment, 0.01)

    def set_curve_on_shape(self, pt0_U, pt1_U):
        pass

    def confirm(self):
        self.is_getting_shape = False
        self.update()
        self.repaint()

