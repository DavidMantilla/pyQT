from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class mainApp(QMainWindow):
    lbl="""
    *{
        background: #404040;
        color: #fff;
        
    }
    """
    def __init__(self, *args):
        super(mainApp, self).__init__(*args)
        # self.setMinimumSize(500,300) #tamaño minimo
        # self.setMaximumSize(700,500) # tamaño maximo
        self.setFixedSize(700,500) # tamaño fijo
        self.setWindowTitle('My App') # titulo 
        label= QLabel('Hola,\n Esto es genial',self)
        # print("El ancho del label es",label.frameGeometry().width(),"El largo del label es",label.frameGeometry().height())
        ancho=self.frameGeometry().width() #halla el ancho de la ventana
        alto=self.frameGeometry().height() #halla el ancho de la ventana
        #label.setGeometry(0,0,ancho,alto) # configura la posicion y el tamaño del label
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)
        label.setStyleSheet(self.lbl)
     
        

if __name__ == "__main__":
    app=QApplication([])
    window= mainApp()
    window.show()
    app.exec_()



