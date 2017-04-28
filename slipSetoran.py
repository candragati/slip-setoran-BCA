from PyQt4 import QtGui, QtCore
from raw_ui import utama_ui
import sys
import myDB
import sqlite3
import MSWinPrint
import sys
import string
from datetime import *
import win32con
import textwrap

h = (
    'ID',
    'Tgl Setor',
    'Penyetor',
    'Jumlah',
    'Jenis Setoran',
    'Tgl Jt.Tempo',
    'Berita',
    'Kode Bank',
    'Nomor Giro',
    'Kota',
    'Sumber Dana',
    'Tujuan Transaksi'
)

satuan = ("", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam",
          "Tujuh", "Delapan", "Sembilan", "Sepuluh", "Sebelas")
mm = 100


class QCustomTableWidgetItem (QtGui.QTableWidgetItem):

    def __init__(self, value):
        super(QCustomTableWidgetItem, self).__init__(
            QtCore.QString('%s' % value))

    def __lt__(self, other):
        if (isinstance(other, QCustomTableWidgetItem)):
            try:
                selfDataValue = float(
                    self.data(QtCore.Qt.EditRole).toString().replace(',', ''))
                otherDataValue = float(
                    other.data(QtCore.Qt.EditRole).toString().replace(',', ''))
                return selfDataValue < otherDataValue
            except:
                return QtGui.QTableWidgetItem.__lt__(self, other)
        else:
            return QtGui.QTableWidgetItem.__lt__(self, other)


class Main(QtGui.QMainWindow, utama_ui.Ui_MainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        self.koneksiDatabase()
        self.setupUi(self)
        self.showMaximized()
        myDB.tampilan()
        self.setWindowTitle('Slip Setoran')
        self.aksi()
        self.isiComboBox()
        self.isiInformasi()
        self.tableWidget.setColumnCount(len(h))
        self.tableWidget.setHorizontalHeaderLabels(h)
        self.formNormal()
        self.sumber_dana = ""
        self.tujuan_transaksi = ""

    def formNormal(self):
        self.comboBerita()
        self.comboKodeBank()
        self.comboKota()

        self.comboBoxCekOpik.setEnabled(True)
        self.lineEditJumlah.setEnabled(True)
        self.comboBoxJenisSetoran.setEnabled(True)

        self.lineEdit100k.clear()
        self.lineEdit50k.clear()
        self.lineEdit20k.clear()
        self.lineEdit10k.clear()
        self.lineEdit5k.clear()
        self.lineEdit2k.clear()
        self.lineEdit1k.clear()
        self.lineEditKoin1000.clear()
        self.lineEditKoin500.clear()
        self.lineEditKoin200.clear()
        self.lineEditKoin100.clear()
        self.lineEditKoin50.clear()
        self.lineEditKoin25.clear()
        self.lineEditTas1.clear()
        self.lineEditSegel1.clear()
        self.lineEditSticker1.clear()
        self.lineEditTas2.clear()
        self.lineEditSegel2.clear()
        self.lineEditSticker2.clear()
        self.lineEditTas3.clear()
        self.lineEditSegel3.clear()
        self.lineEditSticker3.clear()
        self.lineEditTas4.clear()
        self.lineEditSegel4.clear()
        self.lineEditSticker4.clear()
        self.lineEditTas5.clear()
        self.lineEditSegel5.clear()
        self.lineEditSticker5.clear()
        self.lineEditCatatan.clear()
        self.lineEditGrandTotal.clear()

        self.lineEdit100k.setEnabled(True)
        self.lineEdit50k.setEnabled(True)
        self.lineEdit20k.setEnabled(True)
        self.lineEdit10k.setEnabled(True)
        self.lineEdit5k.setEnabled(True)
        self.lineEdit2k.setEnabled(True)
        self.lineEdit1k.setEnabled(True)
        self.lineEditKoin1000.setEnabled(True)
        self.lineEditKoin500.setEnabled(True)
        self.lineEditKoin200.setEnabled(True)
        self.lineEditKoin100.setEnabled(True)
        self.lineEditKoin50.setEnabled(True)
        self.lineEditKoin25.setEnabled(True)
        self.lineEditTas1.setEnabled(True)
        self.lineEditSegel1.setEnabled(True)
        self.lineEditSticker1.setEnabled(True)
        self.lineEditTas2.setEnabled(True)
        self.lineEditSegel2.setEnabled(True)
        self.lineEditSticker2.setEnabled(True)
        self.lineEditTas3.setEnabled(True)
        self.lineEditSegel3.setEnabled(True)
        self.lineEditSticker3.setEnabled(True)
        self.lineEditTas4.setEnabled(True)
        self.lineEditSegel4.setEnabled(True)
        self.lineEditSticker4.setEnabled(True)
        self.lineEditTas5.setEnabled(True)
        self.lineEditSegel5.setEnabled(True)
        self.lineEditSticker5.setEnabled(True)
        self.lineEditCatatan.setEnabled(True)

        self.comboBoxBerita.setEnabled(True)
        self.comboBoxKodeBank.setEnabled(True)
        self.lineEditNomorGiro.setEnabled(True)
        self.comboBoxKota.setEnabled(True)
        self.pushButtonSimpan.setEnabled(True)
        self.dateEditTglSetor.setEnabled(True)
        # self.comboBoxJenisTransaksi.setEnabled(True)
        self.dateEditTglJtTempo.setEnabled(True)
        self.dateEditTglSetor.setEnabled(True)
        self.comboBoxTujuanTrans.setEnabled(True)
        self.lineEditTujuanTrans.setEnabled(True)
        self.comboBoxSumberDana.setEnabled(True)
        self.lineEditSumberDana.setEnabled(True)

        self.comboBoxCekOpik.setFocus()
        self.lineEditID.clear()
        self.lineEditJumlah.clear()
        self.lineEditTerbilang.clear()
        self.lineEditNomorGiro.clear()
        self.lineEditSumberDana.clear()
        self.lineEditTujuanTrans.clear()

        self.dateEditTglSetor.setDate(QtCore.QDate.currentDate())
        self.comboBoxJenisSetoran.setEnabled(False)
        self.comboBoxJenisSetoran.setCurrentIndex(0)
        # self.comboBoxJenisTransaksi.setCurrentIndex(0)
        self.comboBoxSumberDana.setCurrentIndex(0)
        self.comboBoxTujuanTrans.setCurrentIndex(0)
        self.comboBoxCekOpik.setCurrentIndex(0)
        self.labelSumberDana.hide()
        self.lineEditSumberDana.hide()
        self.lineEditTujuanTrans.hide()
        self.labelTujuanTransaksi.hide()
        self.groupBoxGiro.hide()
        self.groupBoxTunai.hide()

        self.lineEditTot100k.setText('0')
        self.lineEditTot50k.setText('0')
        self.lineEditTot20k.setText('0')
        self.lineEditTot10k.setText('0')
        self.lineEditTot5k.setText('0')
        self.lineEditTot2k.setText('0')
        self.lineEditTot1k.setText('0')
        self.lineEditTotKoin1k.setText('0')
        self.lineEditTotKoin500.setText('0')
        self.lineEditTotKoin200.setText('0')
        self.lineEditTotKoin100.setText('0')
        self.lineEditTotKoin50.setText('0')
        self.lineEditTotKoin25.setText('0')
        self.lineEditTotKertasValue.setText('0')
        self.lineEditTotKoinValue.setText('0')

    def isiComboBox(self):
        penyetor = "SELECT nama FROM penyetor"
        bar, jum = self.eksekusi(penyetor)
        nama = [str(bar[i][0]) for i in range(jum)]
        self.comboBoxCekOpik.addItems(nama)

    def comboBerita(self):
        self.comboBoxBerita.clear()
        barEx, jumEx = self.eksekusi("SELECT * FROM berita")
        isi = [barEx[i][0] for i in range(jumEx)]
        self.comboBoxBerita.addItems(isi)

    def comboKodeBank(self):
        self.comboBoxKodeBank.clear()
        barEx, jumEx = self.eksekusi("SELECT * FROM kode_bank")
        isi = [barEx[i][0] for i in range(jumEx)]
        self.comboBoxKodeBank.addItems(isi)

    def comboKota(self):
        self.comboBoxKota.clear()
        barEx, jumEx = self.eksekusi("SELECT * FROM kota")
        isi = [barEx[i][0] for i in range(jumEx)]
        self.comboBoxKota.addItems(isi)

    def aksi(self):
        self.tabWidget.currentChanged.connect(self.cek)
        self.lineEditJumlah.textEdited.connect(self.tulisTerbilang)
        # self.comboBoxJenisSetoran.currentIndexChanged.connect(
        #     self.onJenisSetoran)
        QtGui.QShortcut(QtGui.QKeySequence(
            "Enter"), self.comboBoxJenisSetoran, self.onJenisSetoran, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence(
            "Return"), self.comboBoxJenisSetoran, self.onJenisSetoran, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence(
            "Enter"), self.comboBoxCekOpik, self.onCekOpik, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence(
            "Return"), self.comboBoxCekOpik, self.onCekOpik, context=QtCore.Qt.WidgetShortcut)
        # QtGui.QShortcut(QtGui.QKeySequence("Enter"), self.comboBoxJenisTransaksi, self.dateEditTglTransTunai.setFocus, context=QtCore.Qt.WidgetShortcut)
        # QtGui.QShortcut(QtGui.QKeySequence("Return"), self.comboBoxJenisTransaksi, self.dateEditTglTransTunai.setFocus, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence("Enter"), self.comboBoxBerita, self.comboBoxKodeBank.setFocus, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence("Return"), self.comboBoxBerita, self.comboBoxKodeBank.setFocus, context=QtCore.Qt.WidgetShortcut)

        QtGui.QShortcut(QtGui.QKeySequence("Enter"), self.dateEditTglJtTempo,
                        self.pushButtonSimpan.setFocus, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence("Return"), self.dateEditTglJtTempo,
                        self.pushButtonSimpan.setFocus, context=QtCore.Qt.WidgetShortcut)

        QtGui.QShortcut(QtGui.QKeySequence("Enter"), self.comboBoxKodeBank,
                        self.lineEditNomorGiro.setFocus, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence("Return"), self.comboBoxKodeBank,
                        self.lineEditNomorGiro.setFocus, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence("Enter"), self.comboBoxKota,
                        self.dateEditTglJtTempo.setFocus, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence("Return"), self.comboBoxKota,
                        self.dateEditTglJtTempo.setFocus, context=QtCore.Qt.WidgetShortcut)
        self.lineEditJumlah.returnPressed.connect(self.onJumlahEnter)
        self.lineEditNomorGiro.returnPressed.connect(
            self.comboBoxKota.setFocus)

        QtGui.QShortcut(QtGui.QKeySequence(
            "Enter"), self.comboBoxSumberDana, self.onSumberDana, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence(
            "Return"), self.comboBoxSumberDana, self.onSumberDana, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence(
            "Enter"), self.comboBoxTujuanTrans, self.onTujuanTrans, context=QtCore.Qt.WidgetShortcut)
        QtGui.QShortcut(QtGui.QKeySequence(
            "Return"), self.comboBoxTujuanTrans, self.onTujuanTrans, context=QtCore.Qt.WidgetShortcut)
        self.comboBoxSumberDana.currentIndexChanged.connect(self.onSumberDana)
        self.comboBoxTujuanTrans.currentIndexChanged.connect(
            self.onTujuanTrans)
        self.pushButtonSimpan.pressed.connect(self.onSimpanKlik)
        self.pushButtonRefresh.pressed.connect(self.isiTabel)
        self.lineEditID.returnPressed.connect(self.onKodeEnter)
        self.pushButtonBatal.pressed.connect(self.formNormal)
        self.pushButtonSimpanInformasi.pressed.connect(self.onSimpanInformasi)
        self.pushButtonCetak.pressed.connect(self.cetakPrinter)

        self.tableWidget.itemDoubleClicked.connect(self.cekID)

        self.lineEdit100k.textEdited.connect(self.EditKertas100k)
        self.lineEdit100k.returnPressed.connect(self.lineEdit50k.setFocus)
        self.lineEdit50k.textEdited.connect(self.EditKertas50k)
        self.lineEdit50k.returnPressed.connect(self.lineEdit20k.setFocus)
        self.lineEdit20k.textEdited.connect(self.EditKertas20k)
        self.lineEdit20k.returnPressed.connect(self.lineEdit10k.setFocus)
        self.lineEdit10k.textEdited.connect(self.EditKertas10k)
        self.lineEdit10k.returnPressed.connect(self.lineEdit5k.setFocus)
        self.lineEdit5k.textEdited.connect(self.EditKertas5k)
        self.lineEdit5k.returnPressed.connect(self.lineEdit2k.setFocus)
        self.lineEdit2k.textEdited.connect(self.EditKertas2k)
        self.lineEdit2k.returnPressed.connect(self.lineEdit1k.setFocus)
        self.lineEdit1k.textEdited.connect(self.EditKertas1k)
        self.lineEdit1k.returnPressed.connect(self.lineEditKoin1000.setFocus)

        self.lineEditKoin1000.textEdited.connect(self.EditKoin1k)
        self.lineEditKoin1000.returnPressed.connect(
            self.lineEditKoin500.setFocus)

        self.lineEditKoin500.textEdited.connect(self.EditKoin500)
        self.lineEditKoin500.returnPressed.connect(
            self.lineEditKoin200.setFocus)

        self.lineEditKoin200.textEdited.connect(self.EditKoin200)
        self.lineEditKoin200.returnPressed.connect(
            self.lineEditKoin100.setFocus)

        self.lineEditKoin100.textEdited.connect(self.EditKoin100)
        self.lineEditKoin100.returnPressed.connect(
            self.lineEditKoin50.setFocus)

        self.lineEditKoin50.textEdited.connect(self.EditKoin50)
        self.lineEditKoin50.returnPressed.connect(self.lineEditKoin25.setFocus)

        self.lineEditKoin25.textEdited.connect(self.EditKoin25)
        self.lineEditKoin50.returnPressed.connect(self.lineEditTas1.setFocus)
        self.lineEditTas1.returnPressed.connect(self.lineEditSegel1.setFocus)
        self.lineEditTas2.returnPressed.connect(self.lineEditSegel2.setFocus)
        self.lineEditTas3.returnPressed.connect(self.lineEditSegel3.setFocus)
        self.lineEditTas4.returnPressed.connect(self.lineEditSegel4.setFocus)
        self.lineEditTas5.returnPressed.connect(self.lineEditSegel5.setFocus)

        self.lineEditSegel1.returnPressed.connect(
            self.lineEditSticker1.setFocus)
        self.lineEditSegel2.returnPressed.connect(
            self.lineEditSticker2.setFocus)
        self.lineEditSegel3.returnPressed.connect(
            self.lineEditSticker3.setFocus)
        self.lineEditSegel4.returnPressed.connect(
            self.lineEditSticker4.setFocus)
        self.lineEditSegel5.returnPressed.connect(
            self.lineEditSticker5.setFocus)

        self.lineEditSticker1.returnPressed.connect(self.lineEditTas2.setFocus)
        self.lineEditSticker2.returnPressed.connect(self.lineEditTas3.setFocus)
        self.lineEditSticker3.returnPressed.connect(self.lineEditTas4.setFocus)
        self.lineEditSticker4.returnPressed.connect(self.lineEditTas5.setFocus)
        self.lineEditSticker5.returnPressed.connect(
            self.lineEditCatatan.setFocus)
        self.lineEditCatatan.returnPressed.connect(
            self.pushButtonSimpan.setFocus)

    def hitungTotalKertas(self):
        a = int(self.lineEditTot100k.text().replace(',', ''))
        b = int(self.lineEditTot50k.text().replace(',', ''))
        c = int(self.lineEditTot20k.text().replace(',', ''))
        d = int(self.lineEditTot10k.text().replace(',', ''))
        e = int(self.lineEditTot5k.text().replace(',', ''))
        f = int(self.lineEditTot2k.text().replace(',', ''))
        g = int(self.lineEditTot1k.text().replace(',', ''))
        jum = a + b + c + d + e + f + g
        self.lineEditTotKertasValue.setText(format(jum, ',.0f'))
        self.hitungGrandTotal()

    def hitungTotalKoin(self):
        a = int(self.lineEditTotKoin1k.text().replace(',', ''))
        b = int(self.lineEditTotKoin500.text().replace(',', ''))
        c = int(self.lineEditTotKoin200.text().replace(',', ''))
        d = int(self.lineEditTotKoin100.text().replace(',', ''))
        e = int(self.lineEditTotKoin50.text().replace(',', ''))
        f = int(self.lineEditTotKoin25.text().replace(',', ''))
        jum = a + b + c + d + e + f
        self.lineEditTotKoinValue.setText(format(jum, ',.0f'))
        self.hitungGrandTotal()

    def hitungGrandTotal(self):
        totalKertas = int(self.lineEditTotKertasValue.text().replace(',', ''))
        totalKoin = int(self.lineEditTotKoinValue.text().replace(',', ''))
        jumlah = int(self.lineEditJumlah.text().replace(',', ''))
        grandTotal = totalKertas + totalKoin
        self.lineEditGrandTotal.setText(format(grandTotal, ',.0f'))
        if jumlah == grandTotal:
            self.lineEditGrandTotal.setStyleSheet(
                "background:rgba(14,255,14,125)")
        else:
            self.lineEditGrandTotal.setStyleSheet(
                "background:rgba(255,14,14,125)")

    def EditKertas100k(self, item):
        try:
            self.lineEdit100k.setText(format(int(item), ',.0f'))
            jum = int(item) * 100000
            self.lineEditTot100k.setText(format(jum, ',.0f'))
            self.hitungTotalKertas()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEdit100k.setText(format(int(a), ',.0f'))
                jum = int(a) * 100000
                self.lineEditTot100k.setText(format(jum, ',.0f'))
                self.hitungTotalKertas()
            except:
                self.lineEdit100k.backspace()
                if str(self.lineEdit100k.text()) == "":
                    self.lineEdit100k.setText('0')
                    self.lineEditTot100k.setText('0')
                    self.hitungTotalKertas()

    def EditKertas50k(self, item):
        try:
            self.lineEdit50k.setText(format(int(item), ',.0f'))
            jum = int(item) * 50000
            self.lineEditTot50k.setText(format(jum, ',.0f'))
            self.hitungTotalKertas()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEdit50k.setText(format(int(a), ',.0f'))
                jum = int(a) * 50000
                self.lineEditTot50k.setText(format(jum, ',.0f'))
                self.hitungTotalKertas()
            except:
                self.lineEdit50k.backspace()
                if str(self.lineEdit50k.text()) == "":
                    self.lineEdit50k.setText('0')
                    self.lineEditTot50k.setText('0')
                    self.hitungTotalKertas()

    def EditKertas20k(self, item):
        try:
            self.lineEdit20k.setText(format(int(item), ',.0f'))
            jum = int(item) * 20000
            self.lineEditTot20k.setText(format(jum, ',.0f'))
            self.hitungTotalKertas()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEdit20k.setText(format(int(a), ',.0f'))
                jum = int(a) * 20000
                self.lineEditTot20k.setText(format(jum, ',.0f'))
                self.hitungTotalKertas()
            except:
                self.lineEdit20k.backspace()
                if str(self.lineEdit20k.text()) == "":
                    self.lineEdit20k.setText('0')
                    self.lineEditTot20k.setText('0')
                    self.hitungTotalKertas()

    def EditKertas10k(self, item):
        try:
            self.lineEdit10k.setText(format(int(item), ',.0f'))
            jum = int(item) * 10000
            self.lineEditTot10k.setText(format(jum, ',.0f'))
            self.hitungTotalKertas()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEdit10k.setText(format(int(a), ',.0f'))
                jum = int(a) * 10000
                self.lineEditTot10k.setText(format(jum, ',.0f'))
                self.hitungTotalKertas()
            except:
                self.lineEdit10k.backspace()
                if str(self.lineEdit10k.text()) == "":
                    self.lineEdit10k.setText('0')
                    self.lineEditTot10k.setText('0')
                    self.hitungTotalKertas()

    def EditKertas5k(self, item):
        try:
            self.lineEdit5k.setText(format(int(item), ',.0f'))
            jum = int(item) * 5000
            self.lineEditTot5k.setText(format(jum, ',.0f'))
            self.hitungTotalKertas()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEdit5k.setText(format(int(a), ',.0f'))
                jum = int(a) * 5000
                self.lineEditTot5k.setText(format(jum, ',.0f'))
                self.hitungTotalKertas()
            except:
                self.lineEdit5k.backspace()
                if str(self.lineEdit5k.text()) == "":
                    self.lineEdit5k.setText('0')
                    self.lineEditTot5k.setText('0')
                    self.hitungTotalKertas()

    def EditKertas2k(self, item):
        try:
            self.lineEdit2k.setText(format(int(item), ',.0f'))
            jum = int(item) * 2000
            self.lineEditTot2k.setText(format(jum, ',.0f'))
            self.hitungTotalKertas()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEdit2k.setText(format(int(a), ',.0f'))
                jum = int(a) * 2000
                self.lineEditTot2k.setText(format(jum, ',.0f'))
                self.hitungTotalKertas()
            except:
                self.lineEdit2k.backspace()
                if str(self.lineEdit2k.text()) == "":
                    self.lineEdit2k.setText('0')
                    self.lineEditTot2k.setText('0')
                    self.hitungTotalKertas()

    def EditKertas1k(self, item):
        try:
            self.lineEdit10k.setText(format(int(item), ',.0f'))
            jum = int(item) * 1000
            self.lineEditTot10k.setText(format(jum, ',.0f'))
            self.hitungTotalKertas()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEdit10k.setText(format(int(a), ',.0f'))
                jum = int(a) * 1000
                self.lineEditTot10k.setText(format(jum, ',.0f'))
                self.hitungTotalKertas()
            except:
                self.lineEdit10k.backspace()
                if str(self.lineEdit10k.text()) == "":
                    self.lineEdit10k.setText('0')
                    self.lineEditTot10k.setText('0')
                    self.hitungTotalKertas()

    def EditKoin1k(self, item):
        try:
            self.lineEditKoin1000.setText(format(int(item), ',.0f'))
            jum = int(item) * 1000
            self.lineEditTotKoin1k.setText(format(jum, ',.0f'))
            self.hitungTotalKoin()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEditKoin1000.setText(format(int(a), ',.0f'))
                jum = int(a) * 1000
                self.lineEditTotKoin1k.setText(format(jum, ',.0f'))
                self.hitungTotalKoin()
            except:
                self.lineEditKoin1000.backspace()
                if str(self.lineEditKoin1000.text()) == "":
                    self.lineEditKoin1000.setText('0')
                    self.lineEditTotKoin1k.setText('0')
                    self.hitungTotalKoin()

    def EditKoin500(self, item):
        try:
            self.lineEditKoin500.setText(format(int(item), ',.0f'))
            jum = int(item) * 500
            self.lineEditTotKoin500.setText(format(jum, ',.0f'))
            self.hitungTotalKoin()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEditKoin500.setText(format(int(a), ',.0f'))
                jum = int(a) * 500
                self.lineEditTotKoin500.setText(format(jum, ',.0f'))
                self.hitungTotalKoin()
            except:
                self.lineEditKoin500.backspace()
                if str(self.lineEditKoin500.text()) == "":
                    self.lineEditKoin500.setText('0')
                    self.lineEditTotKoin500.setText('0')
                    self.hitungTotalKoin()

    def EditKoin200(self, item):
        try:
            self.lineEditKoin200.setText(format(int(item), ',.0f'))
            jum = int(item) * 200
            self.lineEditTotKoin200.setText(format(jum, ',.0f'))
            self.hitungTotalKoin()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEditKoin200.setText(format(int(a), ',.0f'))
                jum = int(a) * 200
                self.lineEditTotKoin200.setText(format(jum, ',.0f'))
                self.hitungTotalKoin()
            except:
                self.lineEditKoin200.backspace()
                if str(self.lineEditKoin200.text()) == "":
                    self.lineEditKoin200.setText('0')
                    self.lineEditTotKoin200.setText('0')
                    self.hitungTotalKoin()

    def EditKoin100(self, item):
        try:
            self.lineEditKoin100.setText(format(int(item), ',.0f'))
            jum = int(item) * 100
            self.lineEditTotKoin100.setText(format(jum, ',.0f'))
            self.hitungTotalKoin()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEditKoin100.setText(format(int(a), ',.0f'))
                jum = int(a) * 100
                self.lineEditTotKoin100.setText(format(jum, ',.0f'))
                self.hitungTotalKoin()
            except:
                self.lineEditKoin100.backspace()
                if str(self.lineEditKoin100.text()) == "":
                    self.lineEditKoin100.setText('0')
                    self.lineEditTotKoin100.setText('0')
                    self.hitungTotalKoin()

    def EditKoin50(self, item):
        try:
            self.lineEditKoin50.setText(format(int(item), ',.0f'))
            jum = int(item) * 50
            self.lineEditTotKoin50.setText(format(jum, ',.0f'))
            self.hitungTotalKoin()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEditKoin50.setText(format(int(a), ',.0f'))
                jum = int(a) * 50
                self.lineEditTotKoin50.setText(format(jum, ',.0f'))
                self.hitungTotalKoin()
            except:
                self.lineEditKoin50.backspace()
                if str(self.lineEditKoin50.text()) == "":
                    self.lineEditKoin50.setText('0')
                    self.lineEditTotKoin50.setText('0')
                    self.hitungTotalKoin()

    def EditKoin25(self, item):
        try:
            self.lineEditKoin25.setText(format(int(item), ',.0f'))
            jum = int(item) * 25
            self.lineEditTotKoin25.setText(format(jum, ',.0f'))
            self.hitungTotalKoin()
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEditKoin25.setText(format(int(a), ',.0f'))
                jum = int(a) * 25
                self.lineEditTotKoin25.setText(format(jum, ',.0f'))
                self.hitungTotalKoin()
            except:
                self.lineEditKoin25.backspace()
                if str(self.lineEditKoin25.text()) == "":
                    self.lineEditKoin25.setText('0')
                    self.lineEditTotKoin25.setText('0')
                    self.hitungTotalKoin()

    def cekID(self):
        r = self.tableWidget.currentRow()
        self.tabWidget.setCurrentIndex(0)
        ID = str(self.tableWidget.item(r, 0).text())
        self.lineEditID.setText(ID)
        self.onKodeEnter()

    def onSimpanInformasi(self):
        try:
            nm_pemilik = self.lineEditNmPemilik.text()
            alamat = self.lineEditAlamatPemilik.text()
            rek_pemilik = self.lineEditRekPemilik.text()
            rek_giro = self.lineEditRekGiro.text()
            rek_penjualan = self.lineEditRekPenjualan.text()
            rek_pelunasan = self.lineEditRekPelunasan.text()
            telp = self.lineEditTelpPemilik.text()
            picker = self.lineEditPengambil.text()
            alamat_picker = self.lineEditAlamatPengambil.text()
            bar, jum = self.eksekusi(
                "SELECT nama FROM penyetor WHERE rowid = 1")
            nm1asli = bar[0][0]

            bar, jum = self.eksekusi(
                "SELECT nama FROM penyetor WHERE rowid = 2")
            nm2asli = bar[0][0]

            nm1 = self.lineEditNm1.text()
            alamat1 = self.lineEditAlamat1.text()
            telp1 = self.lineEditTelp1.text()
            norek1 = self.lineEditNoRek1.text()

            nm2 = self.lineEditNm2.text()
            alamat2 = self.lineEditAlamat2.text()
            telp2 = self.lineEditTelp2.text()
            norek2 = self.lineEditNoRek2.text()

            printer = str(self.comboBoxListPrinter.currentText())

            sql = """UPDATE informasi SET 
                nm_pemilik = '%s',
                alamat_pemilik = '%s',
                norek_pemilik = '%s',
                norek_giro = '%s',
                norek_penjualan = '%s',
                norek_pelunasan  = '%s',
                printer = '%s',
                telp = '%s',
                picker = '%s',
                alamat_picker = '%s'      
            """ % (nm_pemilik, alamat, rek_pemilik, rek_giro, rek_penjualan, rek_pelunasan, printer, telp,picker,alamat_picker)
            self.cur.execute(sql)
            self.db.commit()

            penyetor1 = """UPDATE penyetor SET
                nama = '%s',
                alamat = '%s',
                telp = '%s',
                norek = '%s' 
                WHERE nama = '%s'
            """ % (nm1, alamat1, telp1, norek1, nm1asli)
            self.cur.execute(penyetor1)
            self.db.commit()

            penyetor2 = """UPDATE penyetor SET
                nama = '%s',
                alamat = '%s',
                telp = '%s',
                norek = '%s' 
                WHERE nama = '%s'
            """ % (nm2, alamat2, telp2, norek2, nm2asli)
            self.cur.execute(penyetor2)
            self.db.commit()
            QtGui.QMessageBox.information(
                self, "Informasi", "Data berhasil disimpan")
            self.isiInformasi()
        except Exception, e:
            QtGui.QMessageBox.critical(
                self, "Error", "Tidak dapat menyimpan data!\n%s" % e)

    def cek(self):
        alfabet = self.tabWidget.tabText(self.tabWidget.currentIndex())
        if alfabet == 'Data':
            self.isiTabel()
        elif alfabet == 'Informasi':
            self.isiInformasi()

    def onSumberDana(self):
        a = self.comboBoxSumberDana.currentIndex()
        if a == 0:
            self.lineEditSumberDana.hide()
            self.labelSumberDana.hide()
            self.sumber_dana = str(self.comboBoxSumberDana.currentText())
        else:
            self.lineEditSumberDana.show()
            self.labelSumberDana.show()
            self.lineEditSumberDana.setFocus()
            self.sumber_dana = str(self.lineEditSumberDana.text())

    def onTujuanTrans(self):
        a = self.comboBoxTujuanTrans.currentIndex()
        if a == 0:
            self.lineEditTujuanTrans.hide()
            self.labelTujuanTransaksi.hide()
            self.tujuan_transaksi = str(self.comboBoxTujuanTrans.currentText())
        else:
            self.lineEditTujuanTrans.show()
            self.labelTujuanTransaksi.show()
            self.lineEditTujuanTrans.setFocus()
            self.tujuan_transaksi = str(self.lineEditTujuanTrans.text())

    def listprinter(self):
        a = MSWinPrint.listprinters()
        self.comboBoxListPrinter.clear()
        self.comboBoxListPrinter.addItems(a)
        if self.printer != None:
            self.comboBoxListPrinter.setCurrentIndex(
                self.comboBoxListPrinter.findText(self.printer))

    def onJumlahEnter(self):
        if self.comboBoxJenisSetoran.isEnabled():
            self.comboBoxJenisSetoran.setFocus()
            self.comboBoxJenisSetoran.showPopup()

    def onCekOpik(self):
        self.lineEditJumlah.setFocus()

    def onJenisSetoran(self):
        jenis_setor = self.comboBoxJenisSetoran.currentIndex()
        if jenis_setor == 0:
            self.inputTunai()
        else:
            self.inputGiro()
        self.comboBoxJenisSetoran.setEnabled(False)

    def isiTabel(self):
        self.lineEditCari.setFocus()
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(len(h))
        self.tableWidget.setHorizontalHeaderLabels(h)

        sql = """SELECT 
            data.ID,
            tgl_setor,
            nm_penyetor,
            jumlah,
            jenis_setoran,
            tgl_jatuhtempo,
            berita,
            kode_bank,
            nomor_giro,
            kota,
            sumber_dana,
            tujuan_transaksi
            FROM data LEFT JOIN setoran WHERE data.ID = setoran.ID
            """
        bar, jum = self.eksekusi(sql)
        self.tableWidget.setRowCount(jum)
        self.tableWidget.setSortingEnabled(False)

        for data in range(jum):
            teks = (
                bar[data][0],
                bar[data][1],
                bar[data][2],
                format(bar[data][3],',.0f'),
                bar[data][4],
                bar[data][5],
                bar[data][6],
                bar[data][7],
                bar[data][8],
                bar[data][9],
                bar[data][10],
                bar[data][11],
            )
            for i in range(len(teks)):
                item = QCustomTableWidgetItem(QtCore.QString(str(teks[i])))
                item.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                item.setToolTip(str(teks[i]))
                item.setText(str(teks[i]))
                self.tableWidget.setItem(data, i, item)
            self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setSortingEnabled(True)
        self.warnaTabel()

    def warnaTabel(self):
        r = self.tableWidget.rowCount()
        for i in range(r):
            self.tableWidget.item(i, 3).setTextAlignment(
                QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tableWidget.resizeColumnsToContents()

    def inputGiro(self):
        self.groupBoxGiro.show()
        self.groupBoxTunai.hide()
        self.dateEditTglJtTempo.setDate(QtCore.QDate.currentDate())
        self.comboBoxKota.addItem('')
        self.comboBoxKota.setCurrentIndex(self.comboBoxKota.findText(''))
        self.comboBoxKodeBank.addItem('')
        self.comboBoxKodeBank.setCurrentIndex(
            self.comboBoxKodeBank.findText(''))
        self.comboBoxBerita.addItem('')
        self.comboBoxBerita.setCurrentIndex(self.comboBoxBerita.findText(''))
        jumlah = int(self.lineEditJumlah.text().replace(',', ''))
        if jumlah >= 100000000:
            self.groupBoxGiroBanyak.show()
        else:
            self.groupBoxGiroBanyak.hide()
        self.comboBoxBerita.setFocus()

    def inputTunai(self):
        self.groupBoxGiro.hide()
        self.groupBoxTunai.show()
        self.lineEdit100k.setFocus()
        # self.comboBoxJenisTransaksi.setFocus()
        # self.comboBoxJenisTransaksi.showPopup()
        # self.dateEditTglTransTunai.setDate(QtCore.QDate.currentDate())

    def tulisTerbilang(self, item):
        try:
            self.lineEditJumlah.setText(format(int(item), ',.0f'))
            self.lineEditTerbilang.setText(self.Terbilang(int(item)))
            self.comboBoxJenisSetoran.setEnabled(True)
        except ValueError:
            a = item.replace(',', '')
            try:
                self.lineEditJumlah.setText(format(int(a), ',.0f'))
                self.lineEditTerbilang.setText(self.Terbilang(int(a)))
                self.comboBoxJenisSetoran.setEnabled(True)
            except:
                self.lineEditJumlah.backspace()
                if str(self.lineEditJumlah.text()) == "":
                    self.lineEditJumlah.setText('0')
                    self.lineEditTerbilang.setText("Nol")
                    self.comboBoxJenisSetoran.setEnabled(False)

    def Terbilang(self, n):
        satuan = ("", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam",
                  "Tujuh", "Delapan", "Sembilan", "Sepuluh", "Sebelas")

        if 0 <= n <= 11:
            return " " + satuan[n]
        elif 12 <= n <= 19:
            return self.Terbilang(n % 10) + " Belas"
        elif 20 <= n <= 99:
            return self.Terbilang(n / 10) + " Puluh" + self.Terbilang(n % 10)
        elif 100 <= n <= 199:
            return " Seratus" + self.Terbilang(n - 100)
        elif 200 <= n <= 999:
            return self.Terbilang(n / 100) + " Ratus" + self.Terbilang(n % 100)
        elif 1000 <= n <= 1999:
            return " Seribu" + self.Terbilang(n - 1000)
        elif 2000 <= n <= 999999:
            return self.Terbilang(n / 1000) + " Ribu" + self.Terbilang(n % 1000)
        elif 1000000 <= n <= 999999999:
            return self.Terbilang(n / 1000000) + " Juta" + self.Terbilang(n % 1000000)
        else:
            return self.Terbilang(n / 1000000000) + " Milyar" + self.Terbilang(n % 1000000000)

    def isiInformasi(self):
        sql = "SELECT * FROM informasi"
        bar, jum = self.eksekusi(sql)
        self.lineEditNmPemilik.setText(str(bar[0][0]))
        self.lineEditAlamatPemilik.setText(str(bar[0][1]))
        self.lineEditTelpPemilik.setText(str(bar[0][2]))
        self.lineEditRekPemilik.setText(str(bar[0][3]))
        self.lineEditRekGiro.setText(str(bar[0][4]))
        self.lineEditRekPenjualan.setText(str(bar[0][5]))
        self.lineEditRekPelunasan.setText(str(bar[0][6]))
        self.printer = bar[0][7]
        self.lineEditPengambil.setText(str(bar[0][8]))
        self.lineEditAlamatPengambil.setText(str(bar[0][9]))

        sqlPenyetor = "SELECT * FROM penyetor"
        bar, jum = self.eksekusi(sqlPenyetor)

        self.lineEditNm1.setText(str(bar[0][0]))
        self.lineEditAlamat1.setText(str(bar[0][1]))
        self.lineEditTelp1.setText(str(bar[0][2]))
        self.lineEditNoRek1.setText(str(bar[0][3]))

        self.lineEditNm2.setText(str(bar[1][0]))
        self.lineEditAlamat2.setText(str(bar[1][1]))
        self.lineEditTelp2.setText(str(bar[1][2]))
        self.lineEditNoRek2.setText(str(bar[1][3]))
        self.listprinter()

    def onSimpanKlik(self):
        ID = str(self.buatKode())
        penyetor = str(self.comboBoxCekOpik.currentText())
        jumlah = int(self.lineEditJumlah.text().replace(',', ''))
        tgl_setor = str(self.dateEditTglSetor.date().toPyDate())
        jenis_setoran = str(self.comboBoxJenisSetoran.currentText())
        if self.groupBoxGiroBanyak.isHidden():
            sumber_dana = ""
            tujuan_transaksi = ""
        else:
            a = self.comboBoxSumberDana.currentIndex()
            if a == 0:
                sumber_dana = str(self.comboBoxSumberDana.currentText())
            else:
                sumber_dana = str(self.lineEditSumberDana.text())
            b = self.comboBoxTujuanTrans.currentIndex()
            if b == 0:
                tujuan_transaksi = str(
                    self.comboBoxTujuanTrans.currentText())
            else:
                tujuan_transaksi = str(self.lineEditTujuanTrans.text())


        kertas100k = self.lineEdit100k.text()
        if kertas100k =="":
            kertas100k = '0'
        else:
            kertas100k = int(self.lineEdit100k.text().replace(',',''))
        kertas50k = self.lineEdit50k.text()
        if kertas50k =="":
            kertas50k = '0'
        else:
            kertas50k = int(self.lineEdit50k.text().replace(',',''))
        kertas20k = self.lineEdit20k.text()
        if kertas20k =="":
            kertas20k = '0'
        else:
            kertas20k = int(self.lineEdit20k.text().replace(',',''))
        kertas10k = self.lineEdit10k.text()
        if kertas10k =="":
            kertas10k = '0'
        else:
            kertas10k = int(self.lineEdit10k.text().replace(',',''))
        kertas5k = self.lineEdit5k.text()
        if kertas5k =="":
            kertas5k = '0'
        else:
            kertas5k = int(self.lineEdit5k.text().replace(',',''))
        kertas2k = self.lineEdit2k.text()
        if kertas2k =="":
            kertas2k = '0'
        else:
            kertas2k = int(self.lineEdit2k.text().replace(',',''))
        kertas1k = self.lineEdit1k.text()
        if kertas1k =="":
            kertas1k = '0'
        else:
            kertas1k = int(self.lineEdit1k.text().replace(',',''))
        koin1000 = self.lineEditKoin1000.text()
        if koin1000 =="":
            koin1000 = '0'
        else:
            koin1000 = int(self.lineEditKoin1000.text().replace(',',''))
        koin500 = self.lineEditKoin500.text()
        if koin500 =="":
            koin500 = '0'
        else:
            koin500 = int(self.lineEditKoin500.text().replace(',',''))
        koin200 = self.lineEditKoin200.text()
        if koin200 =="":
            koin200 = '0'
        else:
            koin200 = int(self.lineEditKoin200.text().replace(',',''))
        koin100 = self.lineEditKoin100.text()
        if koin100 =="":
            koin100 = '0'
        else:
            koin100 = int(self.lineEditKoin100.text().replace(',',''))
        koin50 = self.lineEditKoin50.text()
        if koin50 =="":
            koin50 = '0'
        else:
            koin50 = int(self.lineEditKoin50.text().replace(',',''))
        koin25 = self.lineEditKoin25.text()
        if koin25 =="":
            koin25 = '0'
        else:
            koin25 = int(self.lineEditKoin25.text().replace(',',''))


        tas1 = ""
        segel1 = ""
        sticker1 = ""
        tas2 = ""
        segel2 = ""
        sticker2 = ""
        tas3 = ""
        segel3 = ""
        sticker3 = ""
        tas4 = ""
        segel4 = ""
        sticker4 = ""
        tas5 = ""
        segel5 = ""
        sticker5 = ""
        if jenis_setoran == 'Setor Giro':
            tgl_jatuhtempo = str(self.dateEditTglJtTempo.date().toPyDate())
            berita = str(self.comboBoxBerita.currentText()).upper()
            kode_bank = str(self.comboBoxKodeBank.currentText()).upper()
            nomor_giro = str(self.lineEditNomorGiro.text()).upper()
            kota = str(self.comboBoxKota.currentText()).upper()
            
        else:
            
            tas1 = self.lineEditTas1.text()
            segel1 = self.lineEditSegel1.text()
            sticker1 = self.lineEditSticker1.text()
            tas2 = self.lineEditTas2.text()
            segel2 = self.lineEditSegel2.text()
            sticker2 = self.lineEditSticker2.text()
            tas3 = self.lineEditTas3.text()
            segel3 = self.lineEditSegel3.text()
            sticker3 = self.lineEditSticker3.text()
            tas4 = self.lineEditTas4.text()
            segel4 = self.lineEditSegel4.text()
            sticker4 = self.lineEditSticker4.text()
            tas5 = self.lineEditTas5.text()
            segel5 = self.lineEditSegel5.text()
            sticker5 = self.lineEditSticker5.text()
            
            tgl_jatuhtempo = ""
            berita = ""
            kode_bank = ""
            nomor_giro = ""
            kota = ""

        tanya = QtGui.QMessageBox.question(
            self, "Konfirmasi", "Anda yakin akan menyimpan data?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if tanya == QtGui.QMessageBox.Yes:
            try:
                simpan = "INSERT INTO data (ID,nm_penyetor,jumlah,jenis_setoran,tgl_setor) VALUES ('%s','%s','%s','%s','%s')" % (
                    ID, penyetor, jumlah, jenis_setoran, tgl_setor)
                self.cur.execute(simpan)
                self.db.commit()

                setoran = """
                INSERT INTO setoran (
                    ID,
                    tgl_jatuhtempo,
                    berita,
                    kode_bank,
                    nomor_giro,
                    kota,
                    sumber_dana,
                    tujuan_transaksi,
                    kertas100k,
                    kertas50k,
                    kertas20k,
                    kertas10k,
                    kertas5k,
                    kertas2k,
                    kertas1k,
                    koin1000,
                    koin500,
                    koin200,
                    koin100,
                    koin50,
                    koin25,
                    tas1,
                    segel1,
                    sticker1,
                    tas2,
                    segel2,
                    sticker2,
                    tas3,
                    segel3,
                    sticker3,
                    tas4,
                    segel4,
                    sticker4,
                    tas5,
                    segel5,
                    sticker5

                ) VALUES (
                '%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s')
                """ % (
                    ID,
                    tgl_jatuhtempo,
                    berita,
                    kode_bank,
                    nomor_giro,
                    kota,
                    sumber_dana,
                    tujuan_transaksi,
                    kertas100k,
                    kertas50k,
                    kertas20k,
                    kertas10k,
                    kertas5k,
                    kertas2k,
                    kertas1k,
                    koin1000,
                    koin500,
                    koin200,
                    koin100,
                    koin50,
                    koin25,
                    tas1,
                    segel1,
                    sticker1,
                    tas2,
                    segel2,
                    sticker2,
                    tas3,
                    segel3,
                    sticker3,
                    tas4,
                    segel4,
                    sticker4,
                    tas5,
                    segel5,
                    sticker5)
                self.cur.execute(setoran)
                self.db.commit()

                cekBerita = "SELECT isi FROM berita WHERE isi='%s'" % (berita)
                ber, jum = self.eksekusi(cekBerita)
                if jum == 0:
                    insertBerita = "INSERT INTO berita (isi) VALUES ('%s')" % (
                        berita)
                    self.cur.execute(insertBerita)
                    self.db.commit()

                cekKodeBank = "SELECT isi FROM kode_bank WHERE isi='%s'" % (
                    kode_bank)
                ber, jum = self.eksekusi(cekKodeBank)
                if jum == 0:
                    insertKodeBank = "INSERT INTO kode_bank (isi) VALUES ('%s')" % (
                        kode_bank)
                    self.cur.execute(insertKodeBank)
                    self.db.commit()

                cekKota = "SELECT isi FROM kota WHERE isi='%s'" % (kota)
                ber, jum = self.eksekusi(cekKota)
                if jum == 0:
                    insertKota = "INSERT INTO kota (isi) VALUES ('%s')" % (
                        kota)
                    self.cur.execute(insertKota)
                    self.db.commit()
                QtGui.QMessageBox.information(
                    self, "Informasi", "Data disimpan!")
                self.cetakPrinter()
                self.formNormal()
                self.comboBoxCekOpik.setFocus()
            except Exception, e:
                QtGui.QMessageBox.critical(
                    self, "Error", "Tidak dapat menyimpan data!\n%s" % e)

    def cetakPrinter(self):
        jenis_setoran = self.comboBoxJenisSetoran.currentText()
        nm_atri = str(self.lineEditNmPemilik.text())
        alamat_atri = str(self.lineEditAlamatPemilik.text())
        jumlah_tunai = str(self.lineEditJumlah.text())
        tgl = datetime.strptime(
            str(self.dateEditTglSetor.date().toPyDate()), "%Y-%m-%d")
        tanggal_setor = tgl.strftime(" %d-%m-%Y")
        Terbilang = str(self.lineEditTerbilang.text())
        wrap_terbilang = textwrap.fill(Terbilang + " Rupiah", width=36)
        printer = str(self.comboBoxListPrinter.currentText())
        picker = str(self.lineEditPengambil.text())
        alamat_picker = str(self.lineEditAlamatPengambil.text())
        kertas100k = str(self.lineEdit100k.text())
        kertas50k = str(self.lineEdit50k.text())
        kertas20k = str(self.lineEdit20k.text())
        kertas10k = str(self.lineEdit10k.text())
        kertas5k = str(self.lineEdit5k.text())
        kertas2k = str(self.lineEdit2k.text())
        kertas1k = str(self.lineEdit1k.text())
        koin1000 = str(self.lineEditKoin1000.text())
        koin500 = str(self.lineEditKoin500.text())
        koin200 = str(self.lineEditKoin200.text())
        koin100 = str(self.lineEditKoin100.text())
        koin50 = str(self.lineEditKoin50.text())
        koin25 = str(self.lineEditKoin25.text())

        TotalKertas100k = str(self.lineEditTot100k.text())
        TotalKertas50k = str(self.lineEditTot50k.text())
        TotalKertas20k = str(self.lineEditTot20k.text())
        TotalKertas10k = str(self.lineEditTot10k.text())
        TotalKertas5k = str(self.lineEditTot5k.text())
        TotalKertas2k = str(self.lineEditTot2k.text())
        TotalKertas1k = str(self.lineEditTot1k.text())
        TotalKoin1000 = str(self.lineEditTotKoin1k.text())
        TotalKoin500 = str(self.lineEditTotKoin500.text())
        TotalKoin200 = str(self.lineEditTotKoin200.text())
        TotalKoin100 = str(self.lineEditTotKoin100.text())
        TotalKoin50 = str(self.lineEditTotKoin50.text())
        TotalKoin25 = str(self.lineEditTotKoin25.text())

        tas1 = self.lineEditTas1.text()
        segel1 = self.lineEditSegel1.text()
        sticker1 = self.lineEditSticker1.text()
        tas2 = self.lineEditTas2.text()
        segel2 = self.lineEditSegel2.text()
        sticker2 = self.lineEditSticker2.text()
        tas3 = self.lineEditTas3.text()
        segel3 = self.lineEditSegel3.text()
        sticker3 = self.lineEditSticker3.text()
        tas4 = self.lineEditTas4.text()
        segel4 = self.lineEditSegel4.text()
        sticker4 = self.lineEditSticker4.text()
        tas5 = self.lineEditTas5.text()
        segel5 = self.lineEditSegel5.text()
        sticker5 = self.lineEditSticker5.text()

        doc = MSWinPrint.document(
            papersize="a4", printer=printer, orientation="portrait")
        doc.begin_document()
        doc.setfont("Lucida Console", 16, bold=0)

        if jenis_setoran == 'Setor Tunai':
            nm_penyetor = str(self.comboBoxCekOpik.currentText())

            doc.gambartext(nm_atri, (mm * 43, mm * -43, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(alamat_atri, (mm * 43, mm * -47, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(picker, (mm * 139, mm * -43, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(alamat_picker, (mm * 139, mm * -47, mm * 200, mm * -150), win32con.DT_LEFT)
            
            doc.gambartext(kertas100k, (mm * 28, mm * -65, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas50k, (mm * 28, mm * -69, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas20k, (mm * 28, mm * -73, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas10k, (mm * 28, mm * -77, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas5k, (mm * 28, mm * -81, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas2k, (mm * 28, mm * -84, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas1k, (mm * 28, mm * -87, mm * 40, mm * -150), win32con.DT_RIGHT)

            doc.gambartext(TotalKertas100k, (mm * 44, mm * -65, mm * 69, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(TotalKertas50k, (mm * 44, mm * -69, mm * 69, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(TotalKertas20k, (mm * 44, mm * -73, mm * 69, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(TotalKertas10k, (mm * 44, mm * -77, mm * 69, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(TotalKertas5k, (mm * 44, mm * -81, mm * 69, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(TotalKertas2k, (mm * 44, mm * -84, mm * 69, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(TotalKertas1k, (mm * 44, mm * -87, mm * 69, mm * -150), win32con.DT_RIGHT)

            doc.gambartext(kertas100k, (mm * 28, mm * -65, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas50k, (mm * 28, mm * -69, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas20k, (mm * 28, mm * -73, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas10k, (mm * 28, mm * -77, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas5k, (mm * 28, mm * -81, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas2k, (mm * 28, mm * -84, mm * 40, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(kertas1k, (mm * 28, mm * -87, mm * 40, mm * -150), win32con.DT_RIGHT)


            doc.gambartext("%s %s"%(nm_penyetor,tanggal_setor), (mm * 21, mm * -134, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(jumlah_tunai, (mm * 77, mm * -98, mm * 125, mm * -150), win32con.DT_RIGHT)
            doc.gambartext(wrap_terbilang, (mm * 110, mm * -113, mm * 200, mm * -150), win32con.DT_LEFT)

        else:
            alamat_atri = str(self.lineEditAlamatPemilik.text())
            telp_atri = str(self.lineEditTelpPemilik.text())
            tgl = datetime.strptime(
                str(self.dateEditTglJtTempo.date().toPyDate()), "%Y-%m-%d")
            tgl_JT = tgl.strftime(" %d-%m-%Y")

            no_warkat = str(self.lineEditNomorGiro.text())
            kota = str(self.comboBoxKota.currentText())
            berita = str(self.comboBoxBerita.currentText())
            norek = str(self.lineEditRekGiro.text())
            norek_atri = str(self.lineEditRekPemilik.text())
            warkat_bank = str(self.comboBoxKodeBank.currentText())
            giro = warkat_bank.upper() + " / " + no_warkat

            doc.gambartext(
                norek, (mm * 50, mm * -50, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(
                nm_atri, (mm * 50, mm * -55, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(
                berita.upper(), (mm * 50, mm * -59, mm * 200, mm * -150), win32con.DT_LEFT)

            doc.gambartext(
                nm_atri, (mm * 50, mm * -67, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(textwrap.fill(
                alamat_atri, width=24), (mm * 50, mm * -71, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(
                telp_atri, (mm * 77, mm * -75, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(
                norek_atri, (mm * 56, mm * -84, mm * 200, mm * -150), win32con.DT_LEFT)

            if int(jumlah_tunai.replace(',', '')) >= 100000000:
                a = self.comboBoxSumberDana.currentIndex()
                if a == 0:
                    sumber_dana = str(self.comboBoxSumberDana.currentText())
                else:
                    sumber_dana = str(self.lineEditSumberDana.text())
                b = self.comboBoxTujuanTrans.currentIndex()
                if b == 0:
                    tujuan_transaksi = str(
                        self.comboBoxTujuanTrans.currentText())
                else:
                    tujuan_transaksi = str(self.lineEditTujuanTrans.text())

                doc.gambartext(
                    sumber_dana, (mm * 40, mm * -22, mm * 200, mm * -150), win32con.DT_LEFT)
                doc.gambartext(
                    tujuan_transaksi, (mm * 40, mm * -26, mm * 200, mm * -150), win32con.DT_LEFT)

            if warkat_bank.upper() == "BCA":
                doc.gambartext(
                    tgl_JT, (mm * 124, mm * -37, mm * 200, mm * -150), win32con.DT_LEFT)
            else:
                doc.gambartext(
                    tgl_JT, (mm * 115, mm * -32, mm * 200, mm * -150), win32con.DT_LEFT)

            doc.gambartext(
                tanggal_setor, (mm * 160, mm * -28, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(
                giro, (mm * 29, mm * -57, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(
                kota.upper(), (mm * 138, mm * -57, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(
                jumlah_tunai, (mm * 162, mm * -57, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(
                jumlah_tunai, (mm * 162, mm * -77, mm * 200, mm * -150), win32con.DT_LEFT)
            doc.gambartext(
                wrap_terbilang, (mm * 119, mm * -91, mm * 200, mm * -150), win32con.DT_LEFT)
        doc.end_document()

    def buatKode(self):
        bar, jum = self.eksekusi("SELECT ID from data")
        return int(jum) + 1

    def onKodeEnter(self):
        ID = str(self.lineEditID.text())
        cek = "SELECT * FROM data WHERE ID = '%s'" % (ID)
        bar, jum = self.eksekusi(cek)
        if jum == 0:
            QtGui.QMessageBox.warning(self, "Perhatian", "ID ini tidak ada")
        else:
            self.comboBoxCekOpik.setCurrentIndex(
                self.comboBoxCekOpik.findText(bar[0][1]))
            self.lineEditJumlah.setText(format(bar[0][2], ',.0f'))
            self.tulisTerbilang(bar[0][2])
            self.comboBoxJenisSetoran.setCurrentIndex(
                self.comboBoxJenisSetoran.findText(bar[0][3]))
            self.onJenisSetoran()
            tgl_setor = str(bar[0][4])
            if tgl_setor == "":
                pass
            else:
                tahun, bulan, hari = string.split(tgl_setor, '-')
                some_date = QtCore.QDate(
                    int(tahun), int(bulan), int(hari))  # Year, Month, Day
                self.dateEditTglSetor.setDate(some_date)

            setoran = "SELECT * FROM setoran WHERE ID = '%s'" % (ID)
            bar, jum = self.eksekusi(setoran)
            
            tgl_jatuhtempo = str(bar[0][1])
            if tgl_jatuhtempo == "":
                pass
            else:
                tahun, bulan, hari = string.split(tgl_jatuhtempo, '-')
                some_date = QtCore.QDate(
                    int(tahun), int(bulan), int(hari))  # Year, Month, Day
                self.dateEditTglJtTempo.setDate(some_date)

            self.comboBoxBerita.setCurrentIndex(
                self.comboBoxBerita.findText(bar[0][2]))
            self.comboBoxKodeBank.setCurrentIndex(
                self.comboBoxKodeBank.findText(bar[0][3]))
            self.lineEditNomorGiro.setText(bar[0][4])
            self.comboBoxKota.setCurrentIndex(
                self.comboBoxKota.findText(bar[0][5]))

            if self.comboBoxSumberDana.findText(bar[0][6]) == 0:
                pass
            else:
                self.comboBoxSumberDana.setCurrentIndex(1)
                self.onSumberDana()
                self.lineEditSumberDana.setText(bar[0][6])

            if self.comboBoxTujuanTrans.findText(bar[0][7]) == 0:
                pass
            else:
                self.comboBoxTujuanTrans.setCurrentIndex(1)
                self.onTujuanTrans()
                self.lineEditTujuanTrans.setText(bar[0][7])

            self.lineEdit100k.setText(format(bar[0][8],',.0f'))
            self.lineEdit50k.setText(format(bar[0][9],',.0f'))
            self.lineEdit20k.setText(format(bar[0][10],',.0f'))
            self.lineEdit10k.setText(format(bar[0][11],',.0f'))
            self.lineEdit5k.setText(format(bar[0][12],',.0f'))
            self.lineEdit2k.setText(format(bar[0][13],',.0f'))
            self.lineEdit1k.setText(format(bar[0][14],',.0f'))
            self.lineEditKoin1000.setText(format(bar[0][15],',.0f'))
            self.lineEditKoin500.setText(format(bar[0][16],',.0f'))
            self.lineEditKoin200.setText(format(bar[0][17],',.0f'))
            self.lineEditKoin100.setText(format(bar[0][18],',.0f'))
            self.lineEditKoin50.setText(format(bar[0][19],',.0f'))
            self.lineEditKoin25.setText(format(bar[0][20],',.0f'))
            self.lineEditTas1.setText(bar[0][21])
            self.lineEditSegel1.setText(bar[0][22])
            self.lineEditSticker1.setText(bar[0][23])
            self.lineEditTas2.setText(bar[0][24])
            self.lineEditSegel2.setText(bar[0][25])
            self.lineEditSticker2.setText(bar[0][26])
            self.lineEditTas3.setText(bar[0][27])
            self.lineEditSegel3.setText(bar[0][28])
            self.lineEditSticker3.setText(bar[0][29])
            self.lineEditTas4.setText(bar[0][30])
            self.lineEditSegel4.setText(bar[0][31])
            self.lineEditSticker4.setText(bar[0][32])
            self.lineEditTas5.setText(bar[0][33])
            self.lineEditSegel5.setText(bar[0][34])
            self.lineEditSticker5.setText(bar[0][35])
            self.lineEditCatatan.setText(bar[0][35])

            self.lineEdit100k.setEnabled(False)
            self.lineEdit50k.setEnabled(False)
            self.lineEdit20k.setEnabled(False)
            self.lineEdit10k.setEnabled(False)
            self.lineEdit5k.setEnabled(False)
            self.lineEdit2k.setEnabled(False)
            self.lineEdit1k.setEnabled(False)
            self.lineEditKoin1000.setEnabled(False)
            self.lineEditKoin500.setEnabled(False)
            self.lineEditKoin200.setEnabled(False)
            self.lineEditKoin100.setEnabled(False)
            self.lineEditKoin50.setEnabled(False)
            self.lineEditKoin25.setEnabled(False)
            self.lineEditTas1.setEnabled(False)
            self.lineEditSegel1.setEnabled(False)
            self.lineEditSticker1.setEnabled(False)
            self.lineEditTas2.setEnabled(False)
            self.lineEditSegel2.setEnabled(False)
            self.lineEditSticker2.setEnabled(False)
            self.lineEditTas3.setEnabled(False)
            self.lineEditSegel3.setEnabled(False)
            self.lineEditSticker3.setEnabled(False)
            self.lineEditTas4.setEnabled(False)
            self.lineEditSegel4.setEnabled(False)
            self.lineEditSticker4.setEnabled(False)
            self.lineEditTas5.setEnabled(False)
            self.lineEditSegel5.setEnabled(False)
            self.lineEditSticker5.setEnabled(False)
            self.lineEditCatatan.setEnabled(False)


            self.EditKertas100k(bar[0][8])
            self.EditKertas50k(bar[0][9])
            self.EditKertas20k(bar[0][10])
            self.EditKertas10k(bar[0][11])
            self.EditKertas5k(bar[0][12])
            self.EditKertas2k(bar[0][13])
            self.EditKertas1k(bar[0][14])
            self.EditKoin1k(bar[0][15])
            self.EditKoin500(bar[0][16])
            self.EditKoin200(bar[0][17])
            self.EditKoin100(bar[0][18])
            self.EditKoin50(bar[0][19])
            self.EditKoin25(bar[0][20])
            

            self.comboBoxCekOpik.setEnabled(False)
            self.lineEditJumlah.setEnabled(False)
            self.comboBoxJenisSetoran.setEnabled(False)
            self.comboBoxBerita.setEnabled(False)
            self.comboBoxKodeBank.setEnabled(False)
            self.lineEditNomorGiro.setEnabled(False)
            self.comboBoxKota.setEnabled(False)
            self.pushButtonSimpan.setEnabled(False)
            self.dateEditTglSetor.setEnabled(False)
            self.dateEditTglJtTempo.setEnabled(False)
            self.dateEditTglSetor.setEnabled(False)
            self.comboBoxTujuanTrans.setEnabled(False)
            self.lineEditTujuanTrans.setEnabled(False)
            self.comboBoxSumberDana.setEnabled(False)
            self.lineEditSumberDana.setEnabled(False)
            self.pushButtonCetak.setFocus()

    def koneksiDatabase(self):
        self.db = sqlite3.connect("data/slipSetoran.db")
        self.cur = self.db.cursor()

    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        return lineData, totData

    def onClose(self):
        self.db.close()
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Main()
    form.show()
    sys.exit(app.exec_())
