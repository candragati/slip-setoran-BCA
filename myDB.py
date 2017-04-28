from PyQt4 import QtCore, QtGui
import socket
import time

filekonfig = "db.ini"
def getIp():
    nama_pc = socket.gethostname()
    ip_pc = socket.gethostbyname(nama_pc)
    waktu = time.strftime('%Y-%m-%d %H:%M:%S')
    pc = nama_pc+"@"+ip_pc
    return pc,waktu

def bagi(isi = None,jumlah=None):
    pcs = jumlah
    if pcs ==None:
        pcs = 0            
    else:            
        pcs = int(pcs)
        karton = pcs / isi
        if karton > 0:
            pcs = pcs % isi                
    return karton,pcs

def kali(isi=None, karton=None, pcs=None):
    jumlah = (int(karton)*int(isi))+int(pcs)
    return jumlah


def tampilan():    
    file = QtCore.QFile('style.css')
    file.open(QtCore.QFile.ReadOnly)
    styleSheet = file.readAll()
    try:
        # Python v2.
        styleSheet = unicode(styleSheet, encoding='utf8')
    except NameError:
        # Python v3.
        styleSheet = str(styleSheet, encoding='utf8')
    QtGui.qApp.setStyleSheet(styleSheet)        

def bg_kuning():
    return "QLineEdit{background-color: rgb(255, 255, 142);}QLineEdit:focus{background-color: rgb(70, 255, 85);} QLineEdit:disabled{background-color: rgb(201, 201, 201);}"

def brushabu():
    brush = QtGui.QBrush(QtGui.QColor(100, 100, 100, 50))
    brush.setStyle(QtCore.Qt.SolidPattern)
    return brush

def brushkuning():
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 127, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    return brush    

def brushijo():
    brush = QtGui.QBrush(QtGui.QColor(70, 255, 185,150))
    brush.setStyle(QtCore.Qt.SolidPattern)
    return brush    
