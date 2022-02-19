import sqlite3
import re
import hashlib
import binascii
import os
import datetime
from registro import  RegistroApp
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *




class NotasApp(QMainWindow):
    LBL="""
    *{
        background: #404040;
        color: #fff;
        border:none;
        
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
    BTN2="""
    *{
        
        background: #1A5276;
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
    
    def __init__(self, *args):
        super(NotasApp, self).__init__(*args)
        mensaje="mensaje enviado"
        medioalto=int(self.frameGeometry().height() /2)
        mitad= int(self.frameGeometry().width()/2)
        ancho= self.frameGeometry().width()
        self.conn=sqlite3.connect("schema/database.sqlite3")    
        self.cur = self.conn.cursor()
        self.setStyleSheet(self.LBL)
        self.setMinimumSize(800, 500)
        self.setupUi(self)
        i=0
        j=0
        self.usuario=3 
        
        self.tags(self.usuario)
        
        
    def setupUi(self, MainWindow):
        
       
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_2 = QWidget(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QSize(200, 0))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.agregar= QPushButton("Añadir tag ",self.widget_2)
        self.add_nota= QPushButton("agregar nota",self.widget_2)
        self.agregar.clicked.connect(self.addTag)
        self.add_nota.clicked.connect(self.addNota)
        icon = QIcon()
        icon.addPixmap(QPixmap("/home/david/pyQT/static/img/add_circle_black_48dp.svg"), QIcon.Normal, QIcon.Off)
        self.add_nota.setIcon(icon)
        self.agregar.setIcon(icon)
        self.agregar.setStyleSheet("background:#232323;padding:5px; border-radius:2px; margin-bottom:2px;margin-left:5px;margin-right:5px")
        self.add_nota.setStyleSheet("background:#232323;padding:5px; border-radius:2px; margin-top:2px;margin-left:5px;margin-right:5px;margin-bottom:5px")
        self.verticalLayout_3.addWidget(self.agregar)
        self.verticalLayout_3.addWidget(self.add_nota)
        self.listWidget_2 = QListWidget(self.widget_2)
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setStyleSheet("background:#323232;padding:10px")
        self.listWidget_2.itemClicked.connect(self.mostraNotas)
        self.listWidget_2.installEventFilter(self)
        self.verticalLayout_3.addWidget(self.listWidget_2)
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.scroll = QScrollArea() 
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QFrame(self.widget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout.addWidget(self.frame, 0, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.scroll)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.mensaje = QMessageBox(self)
    
    def eventFilter(self, source, event):
        if (event.type() == QEvent.ContextMenu and
        source is self.listWidget_2):
            menu = QMenu()
            menu.addAction('editar')
            menu.addAction('eliminar')
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                print(dir(menu))
                print(item.text())
            return True
        return super(NotasApp, self).eventFilter(source, event)    
        
    def addTag(self):  
        dialog = Dialog(self)  # self hace referencia al padre
        dialog.tags(self.usuario)
        dialog.show() 

    def addNota(self):  
        tag=str(self.ListTags[self.listWidget_2.currentRow()][0])
        dialog = Dialog(self)  # self hace referencia al padre
        dialog.notas(tag)
        dialog.show() 
        
    def tags(self,usuario):
        print('e')
        self.listWidget_2.clear()
        self.ListTags=self.cur.execute("SELECT * FROM tags where  usuario_id ='%s'"%usuario).fetchall()
        
        for row in self.ListTags:
          print(row[2])
          self.listWidget_2.addItem(row[2])
    
    
    def mostraNotas(self,item):
        
        tag=str(self.ListTags[self.listWidget_2.currentRow()][0])
        self.cargar_notas(tag) 
       

    def nota(self,i,row):
        
        self.widget_3 = self.gridLayout.itemAt(i).widget()
        self.widget_3.setFixedSize(230,200)
        self.widget_3.setStyleSheet("background:rgb(223,215,160); color:#232323; ")      
        self.label = QLabel(row[1],self.widget_3)
        self.label.setGeometry(0,0,190,40)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background: #D5C55E; color:#232323; font-size:13px;text-transform:uppercase;")
        self.label2 = QLabel(row[2],self.widget_3)
        self.label2.setGeometry(10, 50,210,100)
        self.label2.setWordWrap(True)
        self.label2.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.label2.setStyleSheet("color:#676141; font-size:12px;")
        self.label3 = QLabel(row[3],self.widget_3)
        self.label3.setGeometry(10,150,80,50)
        self.label3.setStyleSheet("color:#676141; font-size:10px;")
        self.btneditar= QPushButton("",self.widget_3)
        icon = QIcon()
        icon.addPixmap(QPixmap("static/img/edit_black_24dp.svg"), QIcon.Normal, QIcon.Off)
        self.btneditar.setStyleSheet("background: #D5C55E; color:#BDAF54; ")
        self.btneditar.setIcon(icon)
        self.btneditar.setGeometry(190,0,20,40)
        self.btneditar.clicked.connect(lambda x:self.editar(row))
        self.btneliminar= QPushButton("",self.widget_3)
        icon = QIcon()
        icon.addPixmap(QPixmap("static/img/delete_black_24dp.svg"), QIcon.Normal, QIcon.Off)
        self.btneliminar.setStyleSheet("background: #D5C55E; color:#BDAF54 ")
        self.btneliminar.setIcon(icon)
        self.btneliminar.setGeometry(210,0,20,40)
        self.btneliminar.clicked.connect(lambda x:self.eliminar(row))
        
        
        
    def editar(self,row):
        print(row)
        dialog = Dialog(self)  # self hace referencia al padre
        dialog.notas(row[4],row)
        dialog.show() 
        
    def eliminar(self,id):
        self.showdialog("¿Desea eliminar la siguiente nota "+id[1]+" ?","Eliminacion",None,'acep')
        if self.valor=='&Yes':
            self.cur.execute("DELETE FROM notas WHERE id='%s'"%id[0])
            self.conn.commit()
            self.showdialog("se ha eliminado la nota "+id[1],"Eliminacion",None,'info')
            self.cargar_notas(id[4])
    
    def cargar_notas(self,tag):
       
        i=0
        curnotas= self.cur.execute("SELECT * FROM notas join tags on tags.id=notas.tags where tags.id ='%s'"%tag)
        notas=curnotas.fetchall()
        
        self.limpiar(notas.__len__())
        for row in notas:
                        
            self.nota(i,row)
            i=i+1  
            
            
    def context_menu(self):
    # from PyQt4.QtGui import QMenu
            menu = QMenu(self)
            menu.addAction('Primera opción')
            menu.addAction('Segunda opción')
            menu.addAction('Tercera opción')
            # Atamos el cierre del menu al cursor
            menu.exec_(QCursor.pos())  
        
    def showdialog(self,mensaje,titulo,extra,tipo):
        msg = QMessageBox()
                
        msg.setText(mensaje)
        msg.setInformativeText(extra)
        msg.setWindowTitle(titulo)
        if(tipo=="info"):
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok )
            
        elif tipo== "error":
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
           
        elif tipo=="acep":
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.buttonClicked.connect(self.msgbtn)
        
        retval = msg.exec_()
        return retval          

    
    def msgbtn(self,i):
        self.valor= i.text()
    
    def limpiar(self,tamano):
        for i in reversed(range(self.gridLayout.count())): 
            widgetToRemove = self.gridLayout.itemAt(i).widget()
            # remove it from the layout list
            self.gridLayout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
            
            if self.width()<=800:       
                maxh=2
                
            else:
                maxh=4  
            if tamano>0:
                numero=tamano/maxh
            else:
                numero=1
                
                
            if(numero > int(numero)):
                maxV=int(numero)+1
            else:
                maxV=int(numero)
        for  i in range(maxV):
            for j in range(maxh):
                self.grilla = QWidget(self.widget)
                self.grilla.setObjectName("widget_3")
                sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(350)
                sizePolicy.setVerticalStretch(250)
                sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
                self.grilla.setSizePolicy(sizePolicy)
                self.gridLayout.addWidget(self.grilla, i, j)
     
     
     
class Dialog(QDialog):
    def __init__(self, args, **kwargs):
        super(Dialog, self).__init__(args, **kwargs)
       
        self.conn=sqlite3.connect("schema/database.sqlite3")    
        self.cur = self.conn.cursor()
        self.main=args

    def tags(self,usuario):
        self.setWindowTitle("AGREGAR TAGS")
        self.setFixedSize(300, 200)
        self.nombre= QLineEdit(self)
        self.nombre.setStyleSheet(NotasApp.INPUT)
        self.nombre.setGeometry(30,40,250,30)
        self.nombre.setPlaceholderText("nombre del tag")
        self.btnguardar= QPushButton('Guardar',self)
        self.btnguardar.setStyleSheet(NotasApp.BTN1)
        self.btnguardar.setGeometry(50,100,100,30)
        self.btnguardar.clicked.connect(lambda x : self.guardar_tags(usuario))
        self.btncancelar= QPushButton('Cancelar',self)
        self.btncancelar.setStyleSheet(NotasApp.BTN2)
        self.btncancelar.setGeometry(160,100,100,30)
        self.btncancelar.clicked.connect(self.hide)
        
    def guardar_tags(self,usuario):
       
        if (self.nombre.text()!="" ):
            self.cur.execute("INSERT INTO tags (usuario_id,nombre_tags) values ('{}','{}')".format(usuario,self.nombre.text()))
            self.conn.commit()
            self.main.tags(usuario)
            self.main.showdialog("tag agregado","info",None,'info')
            self.hide()
        else:            
            self.hide()
    
    
    
    def notas(self, tag,row=None):
        self.setWindowTitle("AGREGAR NOTAS")
        self.setFixedSize(500,300)
        self.titulo= QLineEdit(self)
        self.titulo.setStyleSheet(NotasApp.INPUT)
        self.titulo.setGeometry(100,40,300,30)
        self.titulo.setPlaceholderText("Titulo")
        self.contenido= QTextEdit(self)
        self.contenido.setStyleSheet(NotasApp.INPUT)
        self.contenido.setGeometry(100,100,300,91)
        self.contenido.setPlaceholderText("nombre del tag")
        self.btnguardar= QPushButton('Guardar',self)
        self.btnguardar.setStyleSheet(NotasApp.BTN1)
        self.btnguardar.setGeometry(100,210,150,30)
        self.btncancelar= QPushButton('Cancelar',self)
        self.btncancelar.setStyleSheet(NotasApp.BTN2)
        self.btncancelar.setGeometry(260,210,150,30)
        self.btncancelar.clicked.connect(self.hide)
        self.tag= tag
        
        if row:
           self.id=row[0]
           self.titulo.setText(row[1])
           self.contenido.setPlainText(row[2])
           self.btnguardar.clicked.connect(lambda x:self.actualizar_notas(self.tag))
        else:
           self.btnguardar.clicked.connect(lambda x:self.guardar_notas(self.tag))
        
    def guardar_notas(self,tag):
        today = datetime.date.today()
        self.cur.execute("INSERT INTO notas (titulo,contenido,fecha,tags) values ('{}','{}','{}','{}')".format(self.titulo.text(),self.contenido.toPlainText(),today,tag))
        self.conn.commit()
        self.main.cargar_notas(tag)
        self.main.showdialog("se ha agregado una nota","info",None,'info')
        self.hide()
        
    
    def actualizar_notas(self,tag):
        today = datetime.date.today()
        self.cur.execute("UPDATE notas SET titulo='{}',contenido='{}' WHERE id='{}'".format(self.titulo.text(),self.contenido.toPlainText(),self.id))
        self.conn.commit()
        self.main.cargar_notas(tag)
        self.main.showdialog("se ha Editado la nota","info",None,'info')
        self.hide()
   
     
       

if __name__ == "__main__":
    app=QApplication([])
    window= NotasApp()
    window.show()
    app.exec_()