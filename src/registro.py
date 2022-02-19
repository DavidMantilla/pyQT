import sqlite3
import re
import hashlib
import binascii
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *




class RegistroApp(QMainWindow):
    LBL="""
    *{
        background: #404040;
        color: #fff;
        
    }
    """
    LBL_ERROR="""
    *{
        background: #404040;
        color: #DE0000;
        
    }
    """
    BTN1="""
    *{
        
        background: #b30000;
        color: #fff;
        
        
        }"""
    INPUT="""
    *{
        
        
        color: #DEDEDE;
       border-top: none;
       border-right: none;
       border-bottom: 1px solid #DEDEDE;
       border-left: none;
        
        
        }
    """
    INPUT_ERROR="""
    *{
        
        
        color: #DE0000;
       border-top: none;
       border-right: none;
       border-bottom: 1px solid #DE0000;
       border-left: none;
        
        
        }
    """
    
    def __init__(self,padre,*args):
        super(RegistroApp, self).__init__(*args)
        mensaje="mensaje enviado"
        self.padre=padre
        medioalto=int(self.frameGeometry().height() /2)
        mitad= int(self.frameGeometry().width()/2)
        ancho= self.frameGeometry().width()
        self.conn=sqlite3.connect("schema/database.sqlite3")    
        self.cur = self.conn.cursor()
        self.setFixedSize(700,500) # tamaño fijo
        self.setWindowTitle('Registro') # titulo 
        self.setStyleSheet(self.LBL)
        
        self.Widget=QWidget()
        self.setCentralWidget(self.Widget)
    #-----------  creacion de botones ------------------------
        self.btnenviar= QPushButton("Registrarse", self.Widget) # crear botones
        self.btncancel= QPushButton("cancel", self.Widget)
   #---------------- formato de botones--------------------------
        self.btnenviar.setGeometry((mitad-110),350,100,40) # tamaño de y posicion del boton1
        self.btnenviar.setStyleSheet(self.BTN1)
        # icon = QIcon()
        # icon.addPixmap(QPixmap("/home/david/pyQT/static/img/lock_outline_white_18x18.png"), QIcon.Normal, QIcon.Off)
        # self.btnlock.setIcon(icon)
        self.btncancel.setGeometry((mitad),350,100,40)
      
     #-----------  label ------------------------ 
        self.label= QLabel('Registro',self.Widget)
        self.lblver= QLabel('',self.Widget)
        self.lblver2= QLabel('',self.Widget)
        self.lblerror= QLabel('',self.Widget)
        
     #-----------  formato label ------------------------ 
        self.label.setGeometry(0,50,ancho,50)
        self.label.setAlignment(Qt.AlignCenter)
        self.lblerror.setGeometry(0,110,ancho,50)
        self.lblerror.setAlignment(Qt.AlignCenter)
        self.lblerror.setStyleSheet(self.LBL_ERROR)
        font = QFont() #  variable de fuente
        font.setPointSize(16) # tamaño de letra
        font.setBold(True) # negrita
        font.setWeight(75) 
        self.label.setFont(font) # asigno la fuente
        self.lblver.setPixmap(QPixmap("../static/img/visibility_white_18x18.png"))
        self.lblver.setGeometry((mitad+150),212,20,20)
        self.lblver2.setPixmap(QPixmap("../static/img/visibility_white_18x18.png"))
        self.lblver2.setGeometry((mitad+150),272,20,20)
    #-----------  input usuario ------------------------ 
        self.input_usuario= QLineEdit(self.Widget)
        self.input_usuario.setPlaceholderText("usuario")
        self.input_usuario.setStyleSheet(self.INPUT)
        self.input_usuario.setClearButtonEnabled(True)
        self.input_usuario.setGeometry((mitad-150),150,300,40)
        self.input_usuario.setMaxLength(45)
        
         #-----------  input password------------------------ 
        self.input_password= QLineEdit(self.Widget)
        self.input_password.setPlaceholderText("contraseña")
        self.input_password.setStyleSheet(self.INPUT)
        self.input_password.setClearButtonEnabled(True)
        self.input_password.setGeometry((mitad-150),200,300,40)
        self.input_password.setMaxLength(45)
        self.input_password.setEchoMode(QLineEdit.Password)
        
        self.input_password2= QLineEdit(self.Widget)
        self.input_password2.setPlaceholderText("contraseña")
        self.input_password2.setStyleSheet(self.INPUT)
        self.input_password2.setClearButtonEnabled(True)
        self.input_password2.setGeometry((mitad-150),250,300,40)
        self.input_password2.setMaxLength(45)
        self.input_password2.setEchoMode(QLineEdit.Password)
       
     #-----------  eventos ------------------------
        self.btnenviar.clicked.connect(self.enviarinfo) # el evento con mensajes
        self.btncancel.clicked.connect(self.cancel) 
        self.input_usuario.returnPressed.connect(self.validarUsuario)
        # self.input_password.returnPressed.connect(self.enviarinfo)
        self.lblver.mousePressEvent =self.mostrarContrasena 
        self.lblver2.mousePressEvent =self.mostrarContrasena2 
       
   
        
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
    
    def cancel(self):
        self.hide()
        self.padre.show()
        
    
    def enviarinfo(self):
        self.validarUsuario()
        email=self.input_usuario.text()
        password=self.input_password.text()
        password2=self.input_password2.text()
        
        if password==password2:
        
            if email !='' and password != '' :
                password=  self.hash_password(self.input_password.text()) 
                self.cur.execute("INSERT INTO usuarios (email,password) VALUES ('{}','{}')".format(email,password))
                self.conn.commit()
                self.lblerror.setStyleSheet(self.LBL)
                self.lblerror.setText("usuario registrado correctamente")
                self.padre.show()
                self.hide()
        else:
            self.lblerror.setText("las contraseñas no coinciden")       
            
    
    def mostrarContrasena(self,event):
        
        if self.input_password.echoMode()== 2:
           self.input_password.setEchoMode(QLineEdit.Normal)
           self.lblver.setPixmap(QPixmap("../static/img/visibility_off_white_18x18.png"))
        else:
           self.lblver.setPixmap(QPixmap("../static/img/visibility_white_18x18.png"))
           self.input_password.setEchoMode(QLineEdit.Password)
        
    def mostrarContrasena2(self,event):
            
        if self.input_password2.echoMode()== 2:
           self.input_password2.setEchoMode(QLineEdit.Normal)
           self.lblver2.setPixmap(QPixmap("../static/img/visibility_off_white_18x18.png"))
        else:
           self.lblver2.setPixmap(QPixmap("../static/img/visibility_white_18x18.png"))
           self.input_password2.setEchoMode(QLineEdit.Password)  
        
    def validarUsuario(self):
        if not re.match('[^\@\s]*?@[^\@\s]+\.[^\@\s]',self.input_usuario.text()) :
            self.input_usuario.setText('')
            self.input_usuario.setStyleSheet(self.INPUT_ERROR)
            self.lblerror.setText("usuario incorrecto")
        else:
            self.input_usuario.setStyleSheet(self.INPUT)
          #  self.input_usuario.setReadOnly(True)
            self.input_password.setFocus(True)
            self.lblerror.setText("")
                
        
    def hash_password(self,password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')       
            
    def verify_password(self,stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                    provided_password.encode('utf-8'), 
                                    salt.encode('ascii'), 
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
        
        




