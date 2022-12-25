import sys
from re import search
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui,QtCore
from time import sleep
from PyQt5.QtWidgets import QMainWindow,QApplication
from zamanlayici_main import Ui_MainWindow

#----------------------------------------------#

try:
    class zamanlayici_uygulama(QMainWindow):

        def __init__(self):
            super(zamanlayici_uygulama,self).__init__()

            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            
            self.setWindowTitle("Zamanlayıcı")
            self.setWindowIcon(QIcon("Resimler/saat.ico"))


            self.ui.baslat.clicked.connect(self.start)
            self.ui.durdur.clicked.connect(self.stop)
            self.ui.duraklat_devam_et.clicked.connect(self.duraklat_and_devam_et)

            self.karar = True
            self.karari = False
            self.anlik = 0


        def duraklat_and_devam_et(self):

            try:
                anlik_bilgiler = self.ui.label.text().strip().split(":")

                if self.karari:

                    self.saat = int(anlik_bilgiler[0])
                    self.dakika = int(anlik_bilgiler[1])
                    self.saniye = int(anlik_bilgiler[2])

                    self.anlik =  float(self.ui.yazilacak_3.text().split(" ")[0])

                    self.timer()
                    self.timer_q.start()


                    self.ui.duraklat_devam_et.setIcon(QIcon("Resimler/duraklat.png"))
                    self.karari = False
                else:

                    self.timer_q.stop()

                    self.ui.duraklat_devam_et.setIcon(QIcon("Resimler/devam_et.png"))
                    self.karari = True
            except Exception as ex:
                print(f"Hata mesajı : {ex}")

        def timer(self):

            try:

                self.timer_q = QTimer()
                self.timer_q.setInterval(1000)

                if self.saniye < 0 or self.dakika < 0 or self.saat < 0:
                    self.timer_q.stop()
                else:
                    self.timer_q.timeout.connect(self.counter)
            except Exception as ex:
                print(f"Hata mesajı : {ex}")

        def start(self):

            try:

                self.anlik = 0

                if len(self.ui.line_saat.text()) == 0:
                    self.saat = 0
                else:
                    self.saat = int(self.ui.line_saat.text().strip())
                
                if len(self.ui.line_dakika.text()) == 0:
                    self.dakika = 0
                else:
                    self.dakika = int(self.ui.line_dakika.text().strip())

                if len(self.ui.line_saniye.text()) == 0:
                    self.saniye = 0
                else:
                    self.saniye = int(self.ui.line_saniye.text().strip())

                toplam_saniye = (self.saat * 3600) + (self.dakika * 60) + self.saniye

                self.arttirma_miktari = 100 / toplam_saniye

                self.timer()
                self.timer_q.start()

            except Exception as ex:
                print(f"Hata mesajı : {ex}")

        def stop(self):

            try:

                self.timer_q.stop()

                self.saat = 00
                self.dakika = 00
                self.saniye = 00

                self.ui.label.setText(f"00:00:00")

                self.ui.line_saat.clear()
                self.ui.line_dakika.clear()
                self.ui.line_saniye.clear()

                self.ui.pro_2.setStyleSheet("""
                QFrame {
	border-radius: 125px;
	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:0.748 rgba(0, 0, 0, 0), stop:0.75 rgba(133, 133, 133, 0.8) );
}
                """)
                self.ui.yazilacak_3.setText("0 %")

            except Exception as ex:
                print(f"Hata mesajı : {ex}")

        def counter(self):

            try:

                saat_control,dakika_control,saniye_control = len(str(self.saat)),len(str(self.dakika)),len(str(self.saniye))
                x,y,z = '','',''

                if saat_control == 1:
                    x = '0'
                if dakika_control == 1:
                    y = '0'
                if saniye_control == 1:
                    z = '0'

                self.ui.label.setText(f"{x}{self.saat}:{y}{self.dakika}:{z}{self.saniye}")

                if self.saniye == 0:

                    if self.saat == 0 and self.dakika == 0:

                        self.timer_q.stop()


                    elif self.dakika == 0:

                        if self.saat != 0:

                            self.saat -= 1
                            self.dakika = 59
                            self.saniye = 60

                        else:

                            self.timer_q.stop()

                    elif self.dakika != 0:
                        self.dakika -= 1
                        self.saniye = 60

                self.saniye -= 1

                

                self.ui.yazilacak_3.setText(f"{int(self.anlik)} %")


                stylesheet = """
                        QFrame {
                            border-radius: 125px;
                            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_V1} rgba(0, 0, 0, 0), stop:{STOP_V2} rgba(133, 133, 133, 0.8));
                        }
                        """

                progress = (100 - self.anlik) / 100.0

                # Get Stops Value
                stop_v1 = str(progress - 0.001)
                stop_v2 = str(progress)

                newStyleSheet = stylesheet.replace("{STOP_V1}", stop_v1).replace("{STOP_V2}", stop_v2)

                self.ui.pro_2.setStyleSheet(newStyleSheet)
                
                self.anlik += self.arttirma_miktari

                if int(self.ui.yazilacak_3.text().split(" ")[0]) == 99:
                    self.ui.yazilacak_3.setText("100 %")

            except Exception as ex:
                print(f"Hata Mesajı : {ex}")


    def Application():

        application = QApplication(sys.argv)
        window = zamanlayici_uygulama()
        window.show()
        sys.exit(application.exec_())

    Application()

except:
    pass