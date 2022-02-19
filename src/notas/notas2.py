from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class mainApp(QMainWindow):
    LBL="""
    *{
        background: #404040;
        color: #fff;
        
    }
    """
    BTN2="""
    *{
        
        background: #b30000;
        color: #fff;
        
        
        }"""
    BTN1="""
    *{
        
        background: #004d1a;
        color: #fff;
        
        
        }
    """
    def __init__(self, *args):
        super(mainApp, self).__init__(*args)
        mensaje="mensaje enviado"
        medioalto=int(self.frameGeometry().height() /2)
        mitad= int(self.frameGeometry().width()/2)
        ancho= self.frameGeometry().width()
        
        self.setFixedSize(700,500) # tamaño fijo
        self.setWindowTitle('My App') # titulo 
        self.setStyleSheet(self.LBL)
    #-----------  creacion de botones ------------------------
        self.btnenviar= QPushButton("envia info", self) # crear botones
        self.btnmostrar= QPushButton("mostrar info", self)
        
   #---------------- formato de botones--------------------------
        self.btnenviar.setGeometry((mitad-100),medioalto,100,40) # tamaño de y posicion del boton1
        self.btnenviar.setStyleSheet(self.BTN1) #le asigno un estilo boton 1
        self.btnmostrar.setGeometry((mitad+10),medioalto,100,40) # tamaño de y posicion del boton2
        self.btnmostrar.setStyleSheet(self.BTN2) # le asigno el estilo al boton 2
    #-----------  eventos ------------------------
        self.btnenviar.clicked.connect(lambda x : self.enviarinfo(mensaje)) # el evento con mensajes
        self.btnmostrar.clicked.connect(self.mostarinfo) #  evento simple
     #-----------  label ------------------------ 
        self.label= QLabel('Hola, Esto es genial',self)
     #-----------  formato label ------------------------ 
        self.label.setGeometry(0,150,ancho,50)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont() #  variable de fuente
        font.setPointSize(16) # tamaño de letra
        font.setBold(True) # negrita
        font.setWeight(75) 
        self.label.setFont(font) # asigno la fuente
    #-----------  evento label ------------------------ 
        self.label.mousePressEvent =self.mostarinfo # tevento para el label
          # icon = QIcon()
        # icon.addPixmap(QPixmap("/home/david/pyQT/static/img/lock_outline_white_18x18.png"), QIcon.Normal, QIcon.Off)
        # self.btnlock.setIcon(icon)

    def enviarinfo(self,mensaje): # slot con mensaje
        print(mensaje)    
        
    def mostarinfo(self,event): # slot simple  recibe el evento
        if not event:
            print("has dado click en un boton") 
        else :
            print("has dado click en un label")
           
          # def mostarinfo(self,event): # slot simple  recibe el evento
        
    #     if(not self.input_usuario.isReadOnly()):
    #         self.input_usuario.setReadOnly(True)
    #         icon = QIcon()
    #         icon.addPixmap(QPixmap("/home/david/pyQT/static/img/lock_open_white_18x18.png"), QIcon.Normal, QIcon.Off)
    #         self.btnlock.setIcon(icon)
            
    #     else:
    #         icon = QIcon()
    #         icon.addPixmap(QPixmap("/home/david/pyQT/static/img/lock_outline_white_18x18.png"), QIcon.Normal, QIcon.Off)
    #         self.btnlock.setIcon(icon)
    #         self.input_usuario.setReadOnly(False)
    

if __name__ == "__main__":
    app=QApplication([])
    window= mainApp()
    window.show()
    app.exec_()



