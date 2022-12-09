from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from mycanvas import *
from mymodel import *
from tkinter.simpledialog import askfloat

class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")
        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        self.model = MyModel()
        self.canvas.setModel(self.model)
        # create a Toolbar
        tb = self.addToolBar("File")
        fit = QAction(QIcon(),"fit",self)
        tb.addAction(fit)

        # criar botao para exportar para json
        json = QAction(QIcon(),"json",self)
        tb.addAction(json)

        # cria as condições de contorno
        contorno = QAction(QIcon(),"contorno",self)
        tb.addAction(contorno)

        # cria as condições iniciais
        inicial = QAction(QIcon(),"inicial",self)
        tb.addAction(inicial)

        # confirmar as condições
        confirmar = QAction(QIcon(),"confirmar",self)
        tb.addAction(confirmar)

        tb.actionTriggered[QAction].connect(self.tbpressed)



    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
        elif a.text() == "json":
            print("exportar para json")
            # pede ao usuario um n
            # cria um grid com espaçamento n
            # comparar os pontos do modelo e do grid e ver quais pontos do grid estão dentro do modelo
            # cria outras estruturas para o json
            # exportar para json
            self.canvas.exportJson(n)
            
        elif a.text() == "contorno":
            print("criar as condições de contorno")
            n = askfloat("N", "Insira o valor de N", initialvalue=1.0)
            self.canvas.create_outline(n)

        elif a.text() == "inicial":
            print("criar as condições iniciais")
            
        elif a.text() == "confirmar":
            print("confirmar as condições")
            self.canvas.confirm()
            

