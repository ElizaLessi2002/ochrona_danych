import csv
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCloseEvent, QPixmap, QIcon, QPainter, QColor, QImage
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMessageBox, QLineEdit, QVBoxLayout, QMainWindow
import os
import random
import pandas as pd
import sys


from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self): # tworzenie interfejsu

        width=600

        pix_label = QLabel(self)

        image_path = "1.png"
        if not os.path.exists(image_path):
            QMessageBox.warning(self, "Warning", "Image file not found!")
            return

        pixmap = QPixmap("1.png").scaled(200,200) 
        # scaled tak samo jak resize podaje szerokość i wysokość
        #pix_label.resize(pixmap.width(100), pixmap.height(100))

        pix_label.setPixmap(pixmap)
        pix_label.move(int((width - 200)/2) ,50)
    
        self.login_line_edit= QLineEdit("login", self) # pole tekstowe, wypełnione słowem login
        self.login_line_edit.setFixedWidth(200) # wielkość pola
        self.login_line_edit.move(200,350)

        self.pass_line_edit= QLineEdit("password", self)
        self.pass_line_edit.setEchoMode(QLineEdit.Password) # możliwość schowania hasła
        self.pass_line_edit.setFixedWidth(200)
        self.pass_line_edit.move(200,400)

        self.submit_btn = QPushButton("Submit", self) #korzystamy z przycisku i dodajemy mu nazwę, self odwołuje się do klasy LoginWindow
        self.submit_btn.move(int((width - self.submit_btn.size().width()) /2), 450) # przesunięcie przycisku
        self.submit_btn.setStyleSheet("background-color: transparent; border: none")
        self.submit_btn.clicked.connect(self.submit) #połączenie przycisku z naciśnięciem jego

        self.setFixedSize(width,800)
        self.setWindowTitle("Password Manager")

        self.Next()
        self.show() #na samym końcu tego co chcemy wyświetlić

    def submit(self):
        login = self.login_line_edit.text()
        password = self.pass_line_edit.text()

        if login and password:
            if len(login) > 5 and len(password) > 8:
                encrypted_login = self.encrypt_data(login)
                encrypted_password = self.encrypt_data(password)
                self.save_to_csv(encrypted_login, encrypted_password)
                QMessageBox.information(self, "Information", "Login and password saved successfully")
            else:
                QMessageBox.warning(self, "Warning", "Login must be longer than 5 characters and password must be longer than 8 characters")
        else:
            QMessageBox.warning(self, "Warning", "Login and password cannot be empty")

    def encrypt_data(self, data):
        # Generowanie klucza RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Szyfrowanie danych
        encrypted_data = private_key.public_key().encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Zwrócenie zaszyfrowanych danych jako base64 string
        return encrypted_data

    def save_to_csv(self, encrypted_login, encrypted_password):
        csv_file = "basic_password.csv"
        
        # Tworzymy DataFrame z zaszyfrowanym loginem i hasłem
        df = pd.DataFrame({
            'encrypted_login': [encrypted_login.hex()],
            'encrypted_password': [encrypted_password.hex()]
        })
        
        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)

    def Next(self):
        self.next = QPushButton("Next", self)
        self.next.move(490,720)
        self.next.setFixedSize(80, 50)
        self.next.setStyleSheet("background-color: transparent; border: none;")
        self.next.clicked.connect(self.openNextWindow)

        self.next.show()

    def openNextWindow(self):
        self.next_window = FirstWindow()
        self.next_window.setup_2()
        self.close() # zamknięcie obecnego okna

    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class FirstWindow(QWidget):

    def __init__(self):
        super().__init__()
        
    
    def setup_2(self):

        width=600
        self.setFixedSize(width,800)
        self.setWindowTitle("Password Manager")

        self.name=QLabel("Welcome to password manager", self)
        self.name.move(50, 300)  # Przesunięto etykietę

        self.name_2=QLabel("If you want save your password that is great place", self)
        self.name_2.move(50, 350)  # Przesunięto etykietę

        pixmap = self.load_image("1.png", 200, 200)
        if pixmap is not None:
            pix_label = QLabel(self)
            pix_label.setPixmap(pixmap)
            pix_label.move(int((width - 200) / 2), 50)
        else:
            QMessageBox.warning(self, "Warning", "Image file not found!")

        self.Next_2()
        self.show()

    def load_image(self, path, width, height):
        full_path = os.path.join(os.path.dirname(__file__), path)
        if os.path.exists(full_path):
            pixmap = QPixmap(full_path).scaled(width, height)
            return pixmap
        else:
            return None
    
    def Next_2(self):
        self.Next_2 = QPushButton("Next", self)
        self.Next_2.move(490,720)
        self.Next_2.setFixedSize(80,50)
        self.Next_2.setStyleSheet("background-color: transparent; border: none;")
        self.Next_2.clicked.connect(self.openNextWindow_2)

        self.show()

    def openNextWindow_2(self):
        self.second_window= SecondWindow()
        self.second_window.setup_3()
        self.close()

    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()  

class SecondWindow(QWidget):

    def __init__(self):
        super().__init__()

    def setup_3(self):
        width=1200
        self.setFixedSize(width,800)
        self.setWindowTitle("Password Manager")

        pix_label = QLabel(self)
        image_path = "1.png"
        if not os.path.exists(image_path):
            QMessageBox.warning(self, "Warning", "Image file not found!")
            return

        pixmap = QPixmap("1.png").scaled(150,150)

        pix_label.setPixmap(pixmap)
        pix_label.move(30,30)

        self.button= QPushButton("Home",self)
        self.button.move(30,210)
        self.button.setFixedSize(150,50)
        self.button.setStyleSheet("background-color: transparent; border: none;")

        self.button= QPushButton("Favorite", self)
        self.button.move(30,270)
        self.button.setFixedSize(150,50)
        self.button.setStyleSheet("background-color: transparent; border: none;")

        self.button= QPushButton("Settings", self)
        self.button.move(30,700)
        self.button.setFixedSize(150,50)
        self.button.setStyleSheet("background-color: transparent; border: none;")
      
        self.search= QLineEdit("search", self)
        self.search.move(250,30)
        self.search.setFixedSize(700,40)


        self.button=QPushButton("Add platform", self)
        self.button.move(1000,30)
        self.button.setFixedSize(150,50)
        self.button.setStyleSheet("background-color: transparent; border: none;")

        button_icon_google= QIcon("3.png")
        button = QPushButton(self)
        button.setIcon(button_icon_google)
        button.setFixedSize(100,100)
        button.setIconSize(QSize(80,80)) #zwiększenie rozmiaru ikony w przycisku
        button.move(250,100)
        button.setStyleSheet("background-color: transparent; border: none;")
        button.show()

        button.clicked.connect(self.openNewWindow_google)
        button=self.openNewWindow_google

        button_2_icon_firefox= QIcon("4.png")
        button_2 = QPushButton(self)
        button_2.setIcon(button_2_icon_firefox)
        button_2.setFixedSize(100,100)
        button_2.setIconSize(QSize(80,80))
        button_2.move(400,100)
        button_2.setStyleSheet("background-color: transparent; border: none;")
        button_2.show()

        button_2.clicked.connect(self.openNewWindow_firefox)
        button_2=self.openNewWindow_firefox

        button_3_icon_opera= QIcon("5.png")
        button_3 = QPushButton(self)
        button_3.setIcon(button_3_icon_opera)
        button_3.setFixedSize(100,100)
        button_3.setIconSize(QSize(80,80))
        button_3.move(550,100)
        button_3.setStyleSheet("background-color: transparent; border: none;")
        button_3.show()

        button_3.clicked.connect(self.openNewWindow_opera)
        button_3=self.openNewWindow_opera

        button_4_icon_edge= QIcon("6.png")
        button_4 = QPushButton(self)
        button_4.setIcon(button_4_icon_edge)
        button_4.setFixedSize(100,100)
        button_4.setIconSize(QSize(80,80))
        button_4.move(700,100)
        button_4.setStyleSheet("background-color: transparent; border: none;")
        button_4.show()

        button_4.clicked.connect(self.openNewWindow_edge)
        button_4=self.openNewWindow_edge

        button_5_icon_safari= QIcon("7.png")
        button_5 = QPushButton(self)
        button_5.setIcon(button_5_icon_safari)
        button_5.setFixedSize(100,100)
        button_5.setIconSize(QSize(80,80))
        button_5.move(850,100)
        button_5.setStyleSheet("background-color: transparent; border: none;")
        button_5.show()

        button_5.clicked.connect(self.openNewWindow_safari)
        button_5=self.openNewWindow_safari

        button_6_icon_facebook= QIcon("8.png")
        button_6 = QPushButton(self)
        button_6.setIcon(button_6_icon_facebook)
        button_6.setFixedSize(100,100)
        button_6.setIconSize(QSize(80,80))
        button_6.move(250,250)
        button_6.setStyleSheet("background-color: transparent; border: none;")
        button_6.show()

        button_6.clicked.connect(self.openNewWindow_facebook)
        button_6=self.openNewWindow_facebook

        button_7_icon_youtube= QIcon("9.png")
        button_7 = QPushButton(self)
        button_7.setIcon(button_7_icon_youtube)
        button_7.setFixedSize(100,100)
        button_7.setIconSize(QSize(80,80))
        button_7.move(400,250)
        button_7.setStyleSheet("background-color: transparent; border: none;")
        button_7.show()
        
        button_7.clicked.connect(self.openNewWindow_youtube)
        button_7=self.openNewWindow_youtube

        button_8_icon_instagram=QIcon("10.png")
        button_8 = QPushButton(self)
        button_8.setIcon(button_8_icon_instagram)
        button_8.setFixedSize(100,100)
        button_8.setIconSize(QSize(80,80))
        button_8.move(550,250)
        button_8.setStyleSheet("background-color: transparent; border: none;")
        button_8.show()

        button_8.clicked.connect(self.openNewWindow_instagram)
        button_8=self.openNewWindow_instagram

        button_9_icon_tiktok=QIcon("11.png")
        button_9 = QPushButton(self)
        button_9.setIcon(button_9_icon_tiktok)
        button_9.setFixedSize(100,100)
        button_9.setIconSize(QSize(80,80))
        button_9.move(700,250)
        button_9.setStyleSheet("background-color: transparent; border: none;")
        button_9.show()

        button_9.clicked.connect(self.openNewWindow_tiktok)
        button_9=self.openNewWindow_tiktok

        button_10_icon_twitter=QIcon("12.png")
        button_10 = QPushButton(self)
        button_10.setIcon(button_10_icon_twitter)
        button_10.setFixedSize(100,100)
        button_10.setIconSize(QSize(80,80))
        button_10.move(850,250)
        button_10.setStyleSheet("background-color: transparent; border: none;")
        button_10.show()

        button_10.clicked.connect(self.openNewWindow_twitter)
        button_10=self.openNewWindow_twitter

        button_11_icon_whatsapp= QIcon("13.png")
        button_11 = QPushButton(self)
        button_11.setIcon(button_11_icon_whatsapp)
        button_11.setFixedSize(100,100)
        button_11.setIconSize(QSize(80,80))
        button_11.move(250,400)
        button_11.setStyleSheet("background-color: transparent; border: none;")
        button_11.show()

        button_11.clicked.connect(self.openNewWindow_whatsapp)
        button_11=self.openNewWindow_whatsapp

        button_12_icon_telegram=QIcon("14.png")
        button_12 = QPushButton(self)
        button_12.setIcon(button_12_icon_telegram)
        button_12.setFixedSize(100,100)
        button_12.setIconSize(QSize(80,80))
        button_12.move(400,400)
        button_12.setStyleSheet("background-color: transparent; border: none;")
        button_12.show()

        button_12.clicked.connect(self.openNewWindow_telegram)
        button_12=self.openNewWindow_telegram

        button_13_icon_snapchat= QIcon("15.png")
        button_13 = QPushButton(self)
        button_13.setIcon(button_13_icon_snapchat)
        button_13.setFixedSize(100,100)
        button_13.setIconSize(QSize(80,80))
        button_13.move(550,400)
        button_13.setStyleSheet("background-color: transparent; border: none;")
        button_13.show()

        button_13.clicked.connect(self.openNewWindow_snapchat)
        button_13=self.openNewWindow_snapchat
      
        button_14_icon_zoom= QIcon("16.png")
        button_14 = QPushButton(self)
        button_14.setIcon(button_14_icon_zoom)
        button_14.setFixedSize(100,100)
        button_14.setIconSize(QSize(80,80))
        button_14.move(700,400)
        button_14.setStyleSheet("background-color: transparent; border: none;")
        button_14.show()

        button_14.clicked.connect(self.openNewWindow_zoom)
        button_14=self.openNewWindow_zoom

        button_15_icon_skype= QIcon("17.png")
        button_15 = QPushButton(self)
        button_15.setIcon(button_15_icon_skype)
        button_15.setFixedSize(100,100)
        button_15.setIconSize(QSize(80,80))
        button_15.move(850,400)
        button_15.setStyleSheet("background-color: transparent; border: none;")
        button_15.show()

        button_15.clicked.connect(self.openNewWindow_skype)
        button_15=self.openNewWindow_skype

        button_16_icon_netflix= QIcon("18.png")
        button_16 = QPushButton(self)
        button_16.setIcon(button_16_icon_netflix)
        button_16.setFixedSize(100,100)
        button_16.setIconSize(QSize(80,80))
        button_16.move(250, 550)
        button_16.setStyleSheet("background-color: transparent; border: none;")
        button_16.show()

        button_16.clicked.connect(self.openNewWindow_netflix)
        button_16=self.openNewWindow_netflix

        button_17_icon_hbo_max= QIcon("19.png")
        button_17 = QPushButton(self)
        button_17.setIcon(button_17_icon_hbo_max)
        button_17.setFixedSize(100,100)
        button_17.setIconSize(QSize(80,80))
        button_17.move(400, 550)
        button_17.setStyleSheet("background-color: transparent; border: none;")
        button_17.show()

        button_17.clicked.connect(self.openNewWindow_hbo_max)
        button_17=self.openNewWindow_hbo_max

        button_18_icon_disney_plus= QIcon("20.png")
        button_18 = QPushButton(self)
        button_18.setIcon(button_18_icon_disney_plus)
        button_18.setFixedSize(100,100)
        button_18.setIconSize(QSize(80,80))
        button_18.move(550, 550)
        button_18.setStyleSheet("background-color: transparent; border:none;")
        button_18.show()

        button_18.clicked.connect(self.openNewWindow_disney_plus)
        button_18=self.openNewWindow_disney_plus

        button_19_icon_amazon_prime_video= QIcon("21.png")
        button_19 = QPushButton(self)
        button_19.setIcon(button_19_icon_amazon_prime_video)
        button_19.setFixedSize(100,100)
        button_19.setIconSize(QSize(80,80))
        button_19.move(700, 550)
        button_19.setStyleSheet("background-color: transparent; border:none;")
        button_19.show()

        button_19.clicked.connect(self.openNewWindow_amazon_prime_video)
        button_19=self.openNewWindow_amazon_prime_video

        button_20_icon_player=QIcon("22.png")
        button_20 = QPushButton(self)
        button_20.setIcon(button_20_icon_player)
        button_20.setFixedSize(100,100)
        button_20.setIconSize(QSize(80,80))
        button_20.move(850, 550)
        button_20.setStyleSheet("background-color: transparent; border: none;")
        button_20.show()

        button_20.clicked.connect(self.openNewWindow_player)
        button_20=self.openNewWindow_player

        self.show()

    def openNewWindow_google(self):
        self.new_window = NewWindow()
        self.new_window.setup_google()
        self.new_window.show()

    def openNewWindow_firefox(self):
        self.new_window_2 = NewWindow_2()
        self.new_window_2.setup_firefox()
        self.new_window_2.show()

    def openNewWindow_opera(self):
        self.new_window_3 = NewWindow_3()
        self.new_window_3.setup_opera()
        self.new_window_3.show()

    def openNewWindow_edge(self):
        self.new_window_4 = NewWindow_4()
        self.new_window_4.setup_edge()
        self.new_window_4.show()

    def openNewWindow_safari(self):
        self.new_window_5 = NewWindow_5()
        self.new_window_5.setup_safari()
        self.new_window_5.show()
    
    def openNewWindow_facebook(self):
        self.new_window_6 = NewWindow_6()
        self.new_window_6.setup_facebook()
        self.new_window_6.show()

    def openNewWindow_youtube(self):
        self.new_window_7 = NewWindow_7()
        self.new_window_7.setup_youtube()
        self.new_window_7.show()

    def openNewWindow_instagram(self):
        self.new_window_8 = NewWindow_8()
        self.new_window_8.setup_instagram()
        self.new_window_8.show()

    def openNewWindow_tiktok(self):
        self.new_window_9 = NewWindow_9()
        self.new_window_9.setup_tiktok()
        self.new_window_9.show()

    def openNewWindow_twitter(self):
        self.new_window_10 = NewWindow_10()
        self.new_window_10.setup_twitter()
        self.new_window_10.show()

    def openNewWindow_whatsapp(self):
        self.new_window_11 = NewWindow_11()
        self.new_window_11.setup_whatsapp()
        self.new_window_11.show()

    def openNewWindow_telegram(self):
        self.new_window_12 = NewWindow_12()
        self.new_window_12.setup_telegram()
        self.new_window_12.show()

    def openNewWindow_snapchat(self):
        self.new_window_13 = NewWindow_13()
        self.new_window_13.setup_snapchat()
        self.new_window_13.show()
 
    def openNewWindow_zoom(self):
        self.new_window_14 = NewWindow_14()
        self.new_window_14.setup_zoom()
        self.new_window_14.show()

    def openNewWindow_skype(self):
        self.new_window_15 = NewWindow_15()
        self.new_window_15.setup_skype()
        self.new_window_15.show()

    def openNewWindow_netflix(self):
        self.new_window_16 = NewWindow_16()
        self.new_window_16.setup_netflix()
        self.new_window_16.show()

    def openNewWindow_hbo_max(self):
        self.new_window_17 = NewWindow_17()
        self.new_window_17.setup_hbo_max()
        self.new_window_17.show()

    def openNewWindow_disney_plus(self):
        self.new_window_18 = NewWindow_18()
        self.new_window_18.setup_disney_plus()
        self.new_window_18.show()

    def openNewWindow_amazon_prime_video(self):
        self.new_window_19 = NewWindow_19()
        self.new_window_19.setup_amazon_prime_video()
        self.new_window_19.show()

    def openNewWindow_player(self):
        self.new_window_20 = NewWindow_20()
        self.new_window_20.setup_player()
        self.new_window_20.show()


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()  

class NewWindow(QWidget):

    def __init__(self):
        super().__init__()

    def setup_google(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("3.png")) # dodawanie ikony do nowego okna
        self.setWindowTitle("Google")
        google_label =QLabel(self)
        pixmap= QPixmap("3.png").scaled(50,50)
        google_label.setPixmap(pixmap)
        google_label.move(30,30)
        google_label.show()

        label= QLabel("Google",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)


        self.random_button()


    def random_button(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)


    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")



    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore() 


class NewWindow_2(QWidget):
    def __init__(self):
        super().__init__()

    def setup_firefox(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("4.png"))
        self.setWindowTitle("Firefox")
        firefox_label =QLabel(self)
        pixmap= QPixmap("4.png").scaled(50,50)
        firefox_label.setPixmap(pixmap)
        firefox_label.move(30,30)
        firefox_label.show()

        label= QLabel("Firefox",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)


        self.random_button_2()

    def random_button_2(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    
    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()

class NewWindow_3(QWidget):
    def __init__(self):
        super().__init__()

    def setup_opera(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("5.png"))
        self.setWindowTitle("Opera")
        opera_label =QLabel(self)
        pixmap= QPixmap("5.png").scaled(50,50)
        opera_label.setPixmap(pixmap)
        opera_label.move(30,30)
        opera_label.show()

        label= QLabel("Opera",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)


        self.random_button_3()

    def random_button_3(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)


    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_4(QWidget):
    def __init__(self):
        super().__init__()

    def setup_edge(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("6.png"))
        self.setWindowTitle("Edge")
        edge_label =QLabel(self)
        pixmap= QPixmap("6.png").scaled(50,50)
        edge_label.setPixmap(pixmap)
        edge_label.move(30,30)
        edge_label.show()

        label= QLabel("Edge",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)


        self.random_button_4()

    def random_button_4(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")

    
    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()

class NewWindow_5(QWidget):
    def __init__(self):
        super().__init__()

    def setup_safari(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("7.png"))
        self.setWindowTitle("Safari")
        safari_label =QLabel(self)
        pixmap= QPixmap("7.png").scaled(50,50)
        safari_label.setPixmap(pixmap)
        safari_label.move(30,30)
        safari_label.show()

        label= QLabel("Safari",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)


        self.random_button_5()

    def random_button_5(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_6(QWidget):
    def __init__(self):
        super().__init__()

    def setup_facebook(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("8.png"))
        self.setWindowTitle("Facebook")
        facebook_label =QLabel(self)
        pixmap= QPixmap("8.png").scaled(50,50)
        facebook_label.setPixmap(pixmap)
        facebook_label.move(30,30)
        facebook_label.show()

        label= QLabel("Facebook",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_6()

    def random_button_6(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()

class NewWindow_7(QWidget):
    def __init__(self):
        super().__init__()

    def setup_youtube(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("9.png"))
        self.setWindowTitle("Youtube")
        youtube_label =QLabel(self)
        pixmap= QPixmap("9.png").scaled(50,50)
        youtube_label.setPixmap(pixmap)
        youtube_label.move(30,30)
        youtube_label.show()

        label= QLabel("Youtube",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_7()

    def random_button_7(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()

class NewWindow_8(QWidget):
    def __init__(self):
        super().__init__()

    def setup_instagram(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("10.png"))
        self.setWindowTitle("Instagram")
        instagram_label =QLabel(self)
        pixmap= QPixmap("10.png").scaled(50,50)
        instagram_label.setPixmap(pixmap)
        instagram_label.move(30,30)
        instagram_label.show()

        label= QLabel("Instagram",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)


        self.random_button_8()

    def random_button_8(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_9(QWidget):
    def __init__(self):
        super().__init__()

    def setup_tiktok(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("11.png"))
        self.setWindowTitle("Tiktok")
        tiktok_label =QLabel(self)
        pixmap= QPixmap("11.png").scaled(50,50)
        tiktok_label.setPixmap(pixmap)
        tiktok_label.move(30,30)
        tiktok_label.show()

        label= QLabel("Tiktok",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)


        self.random_button_9()

    def random_button_9(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_10(QWidget):
    def __init__(self):
        super().__init__()

    def setup_twitter(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("12.png"))
        self.setWindowTitle("Twitter")
        twitter_label =QLabel(self)
        pixmap= QPixmap("12.png").scaled(50,50)
        twitter_label.setPixmap(pixmap)
        twitter_label.move(30,30)
        twitter_label.show()

        label= QLabel("Twitter",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_10()

    def random_button_10(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()



class NewWindow_11(QWidget):
    def __init__(self):
        super().__init__()

    def setup_whatsapp(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("13.png"))
        self.setWindowTitle("Whatsapp")
        whatsapp_label =QLabel(self)
        pixmap= QPixmap("13.png").scaled(50,50)
        whatsapp_label.setPixmap(pixmap)
        whatsapp_label.move(30,30)
        whatsapp_label.show()

        label= QLabel("Whatsapp",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_11()

    def random_button_11(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_12(QWidget):
    def __init__(self):
        super().__init__()

    def setup_telegram(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("14.png"))
        self.setWindowTitle("Telegram")
        telegram_label =QLabel(self)
        pixmap= QPixmap("14.png").scaled(50,50)
        telegram_label.setPixmap(pixmap)
        telegram_label.move(30,30)
        telegram_label.show()

        label= QLabel("Telegram",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_12()

    def random_button_12(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()

class NewWindow_13(QWidget):
    def __init__(self):
        super().__init__()

    def setup_snapchat(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("15.png"))
        self.setWindowTitle("Snapchat")
        snapchat_label =QLabel(self)
        pixmap= QPixmap("15.png").scaled(50,50)
        snapchat_label.setPixmap(pixmap)
        snapchat_label.move(30,30)
        snapchat_label.show()

        label= QLabel("Snapchat",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_13()

    def random_button_13(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)
    
    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")



    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_14(QWidget):
    def __init__(self):
        super().__init__()

    def setup_zoom(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("16.png"))
        self.setWindowTitle("Zoom")
        zoom_label =QLabel(self)
        pixmap= QPixmap("16.png").scaled(50,50)
        zoom_label.setPixmap(pixmap)
        zoom_label.move(30,30)
        zoom_label.show()

        label= QLabel("Zoom",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_14()

    def random_button_14(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)
    
    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_15(QWidget):
    def __init__(self):
        super().__init__()

    def setup_skype(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("17.png"))
        self.setWindowTitle("Skype")
        skype_label =QLabel(self)
        pixmap= QPixmap("17.png").scaled(50,50)
        skype_label.setPixmap(pixmap)
        skype_label.move(30,30)
        skype_label.show()

        label= QLabel("Skype",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_15()

    def random_button_15(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)
    
    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_16(QWidget):
    def __init__(self):
        super().__init__()

    def setup_netflix(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("18.png"))
        self.setWindowTitle("Netflix")
        netflix_label =QLabel(self)
        pixmap= QPixmap("18.png").scaled(50,50)
        netflix_label.setPixmap(pixmap)
        netflix_label.move(30,30)
        netflix_label.show()

        label= QLabel("Netflix",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_16()

    def random_button_16(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)
    
    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()

    
class NewWindow_17(QWidget):
    def __init__(self):
        super().__init__()

    def setup_hbo_max(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("19.png"))
        self.setWindowTitle("Hbo Max")
        hbo_max_label =QLabel(self)
        pixmap= QPixmap("19.png").scaled(50,50)
        hbo_max_label.setPixmap(pixmap)
        hbo_max_label.move(30,30)
        hbo_max_label.show()

        label= QLabel("Hbo Max",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_17()

    def random_button_17(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)
    
    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_18(QWidget):
    def __init__(self):
        super().__init__()

    def setup_disney_plus(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("20.png"))
        self.setWindowTitle("Disney +")
        disney_plus_label =QLabel(self)
        pixmap= QPixmap("20.png").scaled(50,50)
        disney_plus_label.setPixmap(pixmap)
        disney_plus_label.move(30,30)
        disney_plus_label.show()

        label= QLabel("Disney +",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_18()

    def random_button_18(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)
    
    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"
        
        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")


    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_19(QWidget):
    def __init__(self):
        super().__init__()

    def setup_amazon_prime_video(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("21.png"))
        self.setWindowTitle("Amazon")
        amazon_prime_video_label =QLabel(self)
        pixmap= QPixmap("21.png").scaled(50,50)
        amazon_prime_video_label.setPixmap(pixmap)
        amazon_prime_video_label.move(30,30)
        amazon_prime_video_label.show()

        label= QLabel("Prime Video",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_19()

    def random_button_19(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)

    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"

        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")

    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class NewWindow_20(QWidget):
    def __init__(self):
        super().__init__()

    def setup_player(self):
        width=250
        height=250
        self.setFixedSize(width,height)
        self.setWindowIcon(QIcon("22.png"))
        self.setWindowTitle("Player")
        player_label =QLabel(self)
        pixmap= QPixmap("22.png").scaled(50,50)
        player_label.setPixmap(pixmap)
        player_label.move(30,30)
        player_label.show()

        label= QLabel("Player",self)
        label.move(100,30)
        label.show()

        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.random_button_20()

    def random_button_20(self):
        button= QPushButton(str(random.randint(100000,999999)), self)
        button.clicked.connect(self.button_clicked)
        button.move(100,90)
    
    def save_to_code(self, encrypted_message):
        csv_file = "code.csv"

        # Tworzymy DataFrame z zaszyfrowaną wiadomością
        df = pd.DataFrame({'encrypted_message': [encrypted_message.hex()]})

        # Zapisujemy DataFrame do pliku CSV
        df.to_csv(csv_file, mode='a', header=False, index=False)
        

    def button_clicked(self):
        sender = self.sender()
        plaintext_message = sender.text()

        # Szyfrowanie
        encryption = SymmetricEncryption()
        encrypted_message = encryption.encrypt(plaintext_message)
        
        # Zapis do pliku CSV
        self.save_to_code(encrypted_message)

        QMessageBox.information(self, "Button Clicked", f"Clicked button with text: {plaintext_message}")

    def closeEvent(self, event:QCloseEvent):
        should_close= QMessageBox.question(self,"Close App", "Do you want to close",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else: 
            event.ignore()


class csv(NewWindow, NewWindow_2, NewWindow_3, NewWindow_4, NewWindow_5, NewWindow_6, NewWindow_7, NewWindow_8,
          NewWindow_9, NewWindow_10, NewWindow_11, NewWindow_12, NewWindow_13, NewWindow_14, NewWindow_15,
          NewWindow_16, NewWindow_17, NewWindow_18, NewWindow_19, NewWindow_20 ):
    
    def __init__(self):
        super().__init__()
    
    def csv(self):
        self.button

class SymmetricEncryption:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.generate_key_pair()

    def generate_key_pair(self):
        """
        Generates RSA key pair (public and private keys).
        """
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, plaintext):
        """
        Encrypts data using RSA public key.
        Returns encrypted ciphertext.
        """
        ciphertext = self.public_key.encrypt(
            plaintext.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    def decrypt(self, ciphertext):
        """
        Decrypts encrypted data using RSA private key.
        Returns original plaintext.
        """
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())