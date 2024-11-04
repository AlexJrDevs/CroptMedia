# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pagesxGDlqD.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLayout, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(795, 661)
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setBold(True)
        MainPages.setFont(font)
        self.gridLayout_2 = QGridLayout(MainPages)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setEnabled(True)
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setBold(False)
        self.page_1.setFont(font1)
        self.page_1.setStyleSheet(u"#page_1{\n"
"background: #343b48;\n"
"border-radius: 15px;\n"
"}\n"
"")
        self.gridLayout = QGridLayout(self.page_1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.login_and_register = QStackedWidget(self.page_1)
        self.login_and_register.setObjectName(u"login_and_register")
        self.reset_pass_page_parent = QWidget()
        self.reset_pass_page_parent.setObjectName(u"reset_pass_page_parent")
        self.gridLayout_20 = QGridLayout(self.reset_pass_page_parent)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.reset_pass_page_layout = QHBoxLayout()
        self.reset_pass_page_layout.setObjectName(u"reset_pass_page_layout")

        self.gridLayout_20.addLayout(self.reset_pass_page_layout, 0, 0, 1, 1)

        self.login_and_register.addWidget(self.reset_pass_page_parent)
        self.register_page_parent = QWidget()
        self.register_page_parent.setObjectName(u"register_page_parent")
        self.gridLayout_19 = QGridLayout(self.register_page_parent)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.register_page_layout = QHBoxLayout()
        self.register_page_layout.setObjectName(u"register_page_layout")

        self.gridLayout_19.addLayout(self.register_page_layout, 0, 0, 1, 1)

        self.login_and_register.addWidget(self.register_page_parent)
        self.login_page_parent = QWidget()
        self.login_page_parent.setObjectName(u"login_page_parent")
        self.gridLayout_9 = QGridLayout(self.login_page_parent)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.login_page_layout = QHBoxLayout()
        self.login_page_layout.setObjectName(u"login_page_layout")

        self.gridLayout_9.addLayout(self.login_page_layout, 0, 0, 1, 1)

        self.login_and_register.addWidget(self.login_page_parent)

        self.gridLayout.addWidget(self.login_and_register, 0, 0, 1, 1)

        self.pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setStyleSheet(u"#page_2{\n"
"border-radius: 15px;\n"
"background: #343b48;\n"
"}\n"
"\n"
"\n"
"QLineEdit{\n"
"border:2px solid black;\n"
"background: #343B48;\n"
"}\n"
"\n"
"\n"
"QLabel{\n"
"color: white;\n"
"}\n"
"\n"
"QPushButton{\n"
"background-color:#3c4454;\n"
"}\n"
"\n"
"\n"
"#transcript_label{\n"
"background: #1B1E23;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.gridLayout_3 = QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setContentsMargins(15, 15, 15, 15)
        self.page_2_layout = QStackedWidget(self.page_2)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setStyleSheet(u"")
        self.main_page_2 = QWidget()
        self.main_page_2.setObjectName(u"main_page_2")
        self.horizontalLayout = QHBoxLayout(self.main_page_2)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.transcript_field = QWidget(self.main_page_2)
        self.transcript_field.setObjectName(u"transcript_field")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(9)
        sizePolicy.setVerticalStretch(16)
        sizePolicy.setHeightForWidth(self.transcript_field.sizePolicy().hasHeightForWidth())
        self.transcript_field.setSizePolicy(sizePolicy)
        self.transcript_field.setStyleSheet(u"")
        self.gridLayout_4 = QGridLayout(self.transcript_field)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.transcript_label = QWidget(self.transcript_field)
        self.transcript_label.setObjectName(u"transcript_label")
        self.gridLayout_8 = QGridLayout(self.transcript_label)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.transcript = QGridLayout()
        self.transcript.setSpacing(0)
        self.transcript.setObjectName(u"transcript")
        self.transcript.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_8.addLayout(self.transcript, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.transcript_label, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.transcript_field)

        self.video_field = QFrame(self.main_page_2)
        self.video_field.setObjectName(u"video_field")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(9)
        sizePolicy1.setVerticalStretch(16)
        sizePolicy1.setHeightForWidth(self.video_field.sizePolicy().hasHeightForWidth())
        self.video_field.setSizePolicy(sizePolicy1)
        self.horizontalLayout_4 = QHBoxLayout(self.video_field)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.video_label = QWidget(self.video_field)
        self.video_label.setObjectName(u"video_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.video_label.sizePolicy().hasHeightForWidth())
        self.video_label.setSizePolicy(sizePolicy2)
        self.gridLayout_6 = QGridLayout(self.video_label)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.video_pages = QStackedWidget(self.video_label)
        self.video_pages.setObjectName(u"video_pages")
        self.video_pages.setStyleSheet(u"#load_bg{\n"
"border-radius: 15px;\n"
"background: #343B48;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"\n"
"\n"
"#video_bg{\n"
"border-radius: 15px;\n"
"background: #343B48;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"#loading_video{\n"
"background: #1B1E23;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"#upload_page{\n"
"background: #1B1E23;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"#video_page_bg{\n"
"background: #1B1E23;\n"
"border-bottom-right-radius: 15px;\n"
"border-top-right-radius: 15px;\n"
"}\n"
"\n"
"#text_settings_label{\n"
"background-color: #1B1E23;\n"
"border-bottom-left-radius: 15px;\n"
"border-top-left-radius: 15px;\n"
"}\n"
"\n"
"#text_settings_bg{\n"
"background-color: #343B48;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.video_pages.setFrameShape(QFrame.Box)
        self.video_pages.setFrameShadow(QFrame.Plain)
        self.video_pages.setLineWidth(0)
        self.upload_page = QWidget()
        self.upload_page.setObjectName(u"upload_page")
        self.upload_page.setStyleSheet(u"")
        self.gridLayout_14 = QGridLayout(self.upload_page)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.upload_layout = QVBoxLayout()
        self.upload_layout.setObjectName(u"upload_layout")

        self.gridLayout_14.addLayout(self.upload_layout, 2, 0, 1, 1)

        self.gridWidget = QWidget(self.upload_page)
        self.gridWidget.setObjectName(u"gridWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.gridWidget.sizePolicy().hasHeightForWidth())
        self.gridWidget.setSizePolicy(sizePolicy3)
        self.gridWidget.setBaseSize(QSize(0, 0))
        self.gridLayout_17 = QGridLayout(self.gridWidget)
        self.gridLayout_17.setSpacing(0)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(80, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.create_subclips_btn = QPushButton(self.gridWidget)
        self.create_subclips_btn.setObjectName(u"create_subclips_btn")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.create_subclips_btn.sizePolicy().hasHeightForWidth())
        self.create_subclips_btn.setSizePolicy(sizePolicy4)
        self.create_subclips_btn.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_17.addWidget(self.create_subclips_btn, 1, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(80, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)


        self.gridLayout_14.addWidget(self.gridWidget, 3, 0, 1, 1)

        self.video_pages.addWidget(self.upload_page)
        self.loading_video = QWidget()
        self.loading_video.setObjectName(u"loading_video")
        self.loading_video.setStyleSheet(u"")
        self.gridLayout_15 = QGridLayout(self.loading_video)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.load_bg = QWidget(self.loading_video)
        self.load_bg.setObjectName(u"load_bg")
        self.gridLayout_13 = QGridLayout(self.load_bg)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.load_layout = QGridLayout()
        self.load_layout.setObjectName(u"load_layout")

        self.gridLayout_13.addLayout(self.load_layout, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.load_bg, 0, 0, 1, 1)

        self.video_pages.addWidget(self.loading_video)
        self.video_page = QWidget()
        self.video_page.setObjectName(u"video_page")
        self.gridLayout_16 = QGridLayout(self.video_page)
        self.gridLayout_16.setSpacing(0)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.video_page_bg = QWidget(self.video_page)
        self.video_page_bg.setObjectName(u"video_page_bg")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.video_page_bg.sizePolicy().hasHeightForWidth())
        self.video_page_bg.setSizePolicy(sizePolicy5)
        self.gridLayout_11 = QGridLayout(self.video_page_bg)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(0)
        self.video_bg = QWidget(self.video_page_bg)
        self.video_bg.setObjectName(u"video_bg")
        self.video_player = QGridLayout(self.video_bg)
        self.video_player.setSpacing(0)
        self.video_player.setObjectName(u"video_player")
        self.video_player.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.video_player.setContentsMargins(0, 0, 0, 0)
        self.video_play = QGridLayout()
        self.video_play.setSpacing(0)
        self.video_play.setObjectName(u"video_play")

        self.video_player.addLayout(self.video_play, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.video_bg, 0, 0, 1, 1)

        self.gridWidget1 = QWidget(self.video_page_bg)
        self.gridWidget1.setObjectName(u"gridWidget1")
        sizePolicy3.setHeightForWidth(self.gridWidget1.sizePolicy().hasHeightForWidth())
        self.gridWidget1.setSizePolicy(sizePolicy3)
        self.gridLayout_18 = QGridLayout(self.gridWidget1)
        self.gridLayout_18.setSpacing(0)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(60, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_5, 0, 2, 1, 1)

        self.create_next_button = QPushButton(self.gridWidget1)
        self.create_next_button.setObjectName(u"create_next_button")
        self.create_next_button.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setBold(True)
        self.create_next_button.setFont(font2)

        self.gridLayout_18.addWidget(self.create_next_button, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(60, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.gridWidget1, 1, 0, 1, 1)


        self.gridLayout_16.addWidget(self.video_page_bg, 0, 1, 1, 1)

        self.text_settings_label = QWidget(self.video_page)
        self.text_settings_label.setObjectName(u"text_settings_label")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Ignored)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.text_settings_label.sizePolicy().hasHeightForWidth())
        self.text_settings_label.setSizePolicy(sizePolicy6)
        self.text_settings_label.setMinimumSize(QSize(100, 0))
        self.gridLayout_41 = QGridLayout(self.text_settings_label)
        self.gridLayout_41.setSpacing(0)
        self.gridLayout_41.setObjectName(u"gridLayout_41")
        self.gridLayout_41.setSizeConstraint(QLayout.SetMinimumSize)
        self.text_settings_bg = QWidget(self.text_settings_label)
        self.text_settings_bg.setObjectName(u"text_settings_bg")
        self.gridLayout_5 = QGridLayout(self.text_settings_bg)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.text_settings_layout = QHBoxLayout()
        self.text_settings_layout.setSpacing(0)
        self.text_settings_layout.setObjectName(u"text_settings_layout")
        self.text_settings_layout.setContentsMargins(4, 4, 4, 4)

        self.gridLayout_5.addLayout(self.text_settings_layout, 0, 0, 1, 1)


        self.gridLayout_41.addWidget(self.text_settings_bg, 0, 0, 1, 1)


        self.gridLayout_16.addWidget(self.text_settings_label, 0, 0, 1, 1)

        self.video_pages.addWidget(self.video_page)

        self.gridLayout_6.addWidget(self.video_pages, 0, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.video_label)


        self.horizontalLayout.addWidget(self.video_field)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.page_2_layout.addWidget(self.main_page_2)
        self.subclip_page_2 = QWidget()
        self.subclip_page_2.setObjectName(u"subclip_page_2")
        self.verticalLayout_2 = QVBoxLayout(self.subclip_page_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.subclip_layout = QVBoxLayout()
        self.subclip_layout.setSpacing(0)
        self.subclip_layout.setObjectName(u"subclip_layout")
        self.widget = QWidget(self.subclip_page_2)
        self.widget.setObjectName(u"widget")
        self.gridLayout_10 = QGridLayout(self.widget)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(0)

        self.subclip_layout.addWidget(self.widget)


        self.verticalLayout_2.addLayout(self.subclip_layout)

        self.page_2_layout.addWidget(self.subclip_page_2)

        self.gridLayout_3.addWidget(self.page_2_layout, 0, 0, 1, 1)

        self.pages.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(9)
        sizePolicy7.setVerticalStretch(16)
        sizePolicy7.setHeightForWidth(self.page_3.sizePolicy().hasHeightForWidth())
        self.page_3.setSizePolicy(sizePolicy7)
        self.page_3.setStyleSheet(u"#page_3{\n"
"background: #343b48;\n"
"}\n"
"\n"
"")
        self.gridLayout_7 = QGridLayout(self.page_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")

        self.gridLayout_7.addLayout(self.gridLayout_12, 1, 0, 1, 1)

        self.pages.addWidget(self.page_3)

        self.gridLayout_2.addWidget(self.pages, 0, 0, 1, 1)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)
        self.login_and_register.setCurrentIndex(2)
        self.page_2_layout.setCurrentIndex(0)
        self.video_pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.create_subclips_btn.setText(QCoreApplication.translate("MainPages", u"Create Subclips", None))
        self.create_next_button.setText(QCoreApplication.translate("MainPages", u"Next", None))
    # retranslateUi

