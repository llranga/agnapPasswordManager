from PyQt6.QtWidgets import (QWidget,QHBoxLayout,
                             QVBoxLayout,QTableWidget,
                             QTableWidgetItem,QLineEdit,QPushButton,
                             QTabWidget,QApplication,
                             QLabel,QSpinBox,
                             QFrame,QCheckBox,
                             QLineEdit,QPushButton,
                             QSizePolicy,QGroupBox,
                             QScrollArea,QMessageBox,
                             QTableWidget,QTableWidgetItem,
                             QMenu)
from PyQt6.QtGui import QFont,QAction
from PyQt6.QtCore import Qt
from pathlib import Path
import sys
from password import generate_password
import json
from agnapjson import read_and_ament_json,remove_and_ament_json
from datetime import date


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("agnAp Password Manager")
        self.initGUI()
        self.event_handler()
        
    def initGUI(self):
        self.main_layout=QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setGeometry(300,250,500,400)
        self.setFixedSize(500,400)
        self.password_file=Path(__file__).parent / 'Assets'/ 'data.json'
        '''self.password={"passwords":[
                        {"date":None,"service":None, "username":None,"password":None}   
                        ]}'''
        self.password={"passwords":[
                           
                        ]}
        self.init_datajson()
        
        
        #tab view
        self.tabs=QTabWidget()

        #tab1
        tab1=QWidget()
        tab1_layout=QVBoxLayout()
        tab1_layout.setContentsMargins(5,5,5,5)
        #tab1 caption
        cap_lbl=QLabel('Generate a password')
        cap_lbl.setFont(QFont('Roboto',10))
        cap_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cap_lbl.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        tab1_layout.addWidget(cap_lbl)
        #tab1 details
        desc_txt='It is recommended to generate a password with combination of numbers and special characters. minimum recommended password length is 8 character'
        desc_lbl=QLabel(desc_txt)
        desc_lbl.setWordWrap(True)
        desc_lbl.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        tab1_layout.addWidget(desc_lbl)
        #tab1 input data
        input_group_box=QGroupBox('password criteria')
        input_layout=QHBoxLayout()
        length_lbl=QLabel('length of the password ')
        input_layout.addWidget(length_lbl)
        self.length_spn_bx=QSpinBox()
        self.length_spn_bx.setRange(8,50)
        self.length_spn_bx.setSingleStep(1)
        self.length_spn_bx.setValue(8)
        #length_spn_bx.setPrefix('Password Length  ')
        #length_spn_bx.setSuffix('  chars')
        input_layout.addWidget(self.length_spn_bx)
        char_lbl=QLabel('  chars ')
        input_layout.addWidget(char_lbl)
        self.num_chbx=QCheckBox('numbers')
        self.num_chbx.setChecked(True)
        self.sp_chr_chbx=QCheckBox('special char')
        self.sp_chr_chbx.setChecked(True)
        input_layout.addWidget(self.num_chbx)
        input_layout.addWidget(self.sp_chr_chbx)
        #input_frm=QFrame()
        #input_frm.setFrameShape(QFrame.Shape.Box)
        #input_frm.setLayout(input_layout)
        input_group_box.setLayout(input_layout)
        tab1_layout.addWidget(input_group_box)
        #tab1 out put
        output_layout=QHBoxLayout()
        output_frm = QFrame()
        
        self.generate_btn=QPushButton('Generate')
        self.generate_btn.setFixedWidth(90)
        tab1_layout.addWidget(self.generate_btn)
        tab1_layout.setAlignment(self.generate_btn,Qt.AlignmentFlag.AlignCenter)

        output_frm.setFrameShape(QFrame.Shape.Box)
        self.output_lbl=QLabel()
        self.output_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.output_lbl.setText('yoUr PaSSworD')
        self.output_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_lbl.setFont(QFont('Roboto',15))
        output_layout.addWidget(self.output_lbl)
        output_frm.setLayout(output_layout)
        tab1_layout.addWidget(output_frm)
   
        
        #tab1 save to file section
        save_to_file_g_box=QGroupBox('save to file')
        save_layout=QVBoxLayout()
        #save_lbl=QLabel('Save to password file')
        #save_layout.addWidget(save_lbl)
        date_lbl=QLabel('optional')
        save_layout.addWidget(date_lbl)
        save_hor_layout=QHBoxLayout()
        self.service_txt=QLineEdit()
        self.service_txt.setPlaceholderText('service provider')
        save_hor_layout.addWidget(self.service_txt)
        self.user_name_txt=QLineEdit()
        self.user_name_txt.setPlaceholderText('user name')
        save_hor_layout.addWidget(self.user_name_txt)
        self.save_btn=QPushButton('save to file')
        save_hor_layout.addWidget(self.save_btn)
        save_layout.addLayout(save_hor_layout)
        save_to_file_g_box.setLayout(save_layout)
        tab1_layout.addWidget(save_to_file_g_box)

        tab1.setLayout(tab1_layout)

        #tab2
        tab2=QWidget()
        tab2_layout=QVBoxLayout()
        caption_lbl=QLabel('Saved passwords')
        tab2_layout.addWidget(caption_lbl)
        #password table
        self.password_table=QTableWidget(0,4)
        self.password_table.setHorizontalHeaderLabels(['Date','Service','User','Password'])
        self.load_password_table()
        tab2_layout.addWidget(self.password_table)
        #buttons
        self.del_btn=QPushButton('Delete row')
        self.del_btn.setFixedWidth(200)
        tab2_layout.addWidget(self.del_btn,alignment=Qt.AlignmentFlag.AlignCenter)
        tab2.setLayout(tab2_layout)

        #tab3
        tab3=QWidget()
        scroll_area=QScrollArea()
        tab3_layout=QVBoxLayout()
        link_txt='https://github.com/llranga/agnapPasswordManager'
        detail_txt=(f'agnAp password Manager\n\nThis is developed to generate strong password which can contain alphabetic, numeric and special character.\n\nYou may select password length as you wish, but it is recommended to use at least 8 chars long\n\noptionally you can save your password to a file with details of service and relevant user name.these details can be viewed at viewer tab\n\nThis program was developed with Python 3.13.3 using PyQt6 GUI framework. Source code is available to public at\n\n{link_txt}')
        detail_lbl=QLabel(detail_txt)
        
        #link_lbl=QLabel(link_txt)
        detail_lbl.setOpenExternalLinks(True)
        #link_lbl.setOpenExternalLinks(True)
        #link_lbl.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        detail_lbl.setWordWrap(True)
        detail_lbl.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(detail_lbl)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        tab3_layout.addWidget(scroll_area)
        #tab3_layout.addWidget(link_lbl)
        dev_txt='Developed by (under GPL)\n©agnAp\nMakola, Sri Lanka\n\nversion 0.1\nChristchurch,NZ\n27/05/2025\n\nContributors\nMH Hamil\nPathum Eranga'
        dev_lbl=QLabel(dev_txt)
        tab3_layout.addWidget(dev_lbl)
        
        tab3.setLayout(tab3_layout)

        self.tabs.addTab(tab1,"generator")
        self.tabs.addTab(tab2,"viewer")
        self.tabs.addTab(tab3,"about")
        self.main_layout.addWidget(self.tabs)

    def gen_psswrd(self):
        password_length=self.length_spn_bx.value()
        num_bool=self.num_chbx.isChecked()
        sp_char_bool=self.sp_chr_chbx.isChecked()
        password_txt=generate_password(password_length,num_bool,sp_char_bool)
        self.output_lbl.setText(password_txt)
        #print(password_txt)

    def save_to_file(self):
        # check service and user name fields are filled
        if self.service_txt.text()==''or self.user_name_txt.text()=='':
           #display error message
            msg=QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText('Please enter service/user name')
            msg.setIcon(QMessageBox.Icon.Critical)
            button=msg.exec()
        else:

            self.create_dic_item()
            #update the password table at viewer tab
            row_position=self.password_table.rowCount()
            self.password_table.insertRow(row_position)
            self.password_table.setItem(row_position,0,QTableWidgetItem(str(date.today())))
            self.password_table.setItem(row_position,1,QTableWidgetItem(self.service_txt.text()))
            self.password_table.setItem(row_position,2,QTableWidgetItem(self.user_name_txt.text()))
            self.password_table.setItem(row_position,3,QTableWidgetItem(self.output_lbl.text()))
            #display message box
            msg=QMessageBox(self)
            msg.setWindowTitle('Successful')
            msg.setText('saved to the file')
            msg.setIcon(QMessageBox.Icon.Information)
            button=msg.exec()
            if button == QMessageBox.StandardButton.Ok:
                self.service_txt.setText('')
                self.user_name_txt.setText('')

    def create_dic_item(self):
      record={"date":None,"service":"none", "username":"none","password":"none"}
      record['service']=self.service_txt.text()
      record['username']=self.user_name_txt.text()
      record['password']=self.output_lbl.text()
      record['date']=None
      read_and_ament_json(self.password_file,"passwords",record)

    def event_handler(self):
        self.generate_btn.clicked.connect(self.gen_psswrd) 
        self.save_btn.clicked.connect(self.save_to_file)
        self.del_btn.clicked.connect(self.del_table_row)

    def init_datajson(self):
        '''create data.json file if it doesn't exists'''
        try:
         with open(file=self.password_file,mode='x') as file:
            json.dump(self.password,file,indent=1)
        except Exception as e:
         #handling file already exists error
         print(e)

    def load_password_table(self):
       
        with open(file=self.password_file,mode='r') as file:
          data=json.load(file)
          temp_data=data['passwords']
          for item in temp_data:
            row_number=self.password_table.rowCount()
            date=item['date']
            service=item['service']
            username=item['username']
            password=item['password']
            self.password_table.insertRow(row_number)
            self.password_table.setItem(row_number,0,QTableWidgetItem(date))
            self.password_table.setItem(row_number,1,QTableWidgetItem(service))
            self.password_table.setItem(row_number,2,QTableWidgetItem(username))
            self.password_table.setItem(row_number,3,QTableWidgetItem(password))

    def del_table_row(self):
        dlg=QMessageBox()
        dlg.setWindowTitle('Confirm')
        dlg.setText('are you sure?')
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            row_index=self.password_table.currentRow()  
            if row_index != -1:
                self.password_table.removeRow(row_index)
                remove_and_ament_json(self.password_file,'passwords',row_index)
        else:
            pass



if __name__=="__main__":
    app=QApplication(sys.argv)
    main_window=MainWindow()
    main_window.show()
    sys.exit(app.exec())