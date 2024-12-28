from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QCheckBox, QRadioButton, QComboBox
from PyQt6.QtCore import Qt
import json
import os
import json
from modern_ui import UIStyles
import time


class ScriptLauncherUI:
    def __init__(self, style='simple', width=400, height=300):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle('SimpleUI')
        self.window.resize(width, height)  # 设置自定义窗口大小
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)  # 设置边距
        self.layout.setSpacing(15)  # 设置组件间距
        self.window.setLayout(self.layout)
        self.style = style
        self.input_fields = {}
        self.set_style(style)
        
    def set_style(self, style):
        """设置UI样式"""
        self.style = style
        if style == 'modern':
            styles = UIStyles.modern()
        elif style == 'light':
            styles = UIStyles.light()
        elif style == 'dark':
            styles = UIStyles.dark()
        else:  # simple style
            styles = {'window': '', 'button': '', 'input': '', 'label': ''}
            
        self.window.setStyleSheet(styles['window'])
        for widget in self.window.findChildren(QPushButton):
            widget.setStyleSheet(styles['button'])
        for widget in self.window.findChildren(QLineEdit):
            widget.setStyleSheet(styles['input'])
        for widget in self.window.findChildren(QLabel):
            widget.setStyleSheet(styles['label'])
        
    def add_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return self
        
    def add_text_input(self, placeholder=''):
        text_input = QLineEdit()
        text_input.setPlaceholderText(placeholder)
        self.layout.addWidget(text_input)
        return self
        
    def add_label(self, text):
        label = QLabel(text)
        self.layout.addWidget(label)
        return self
        
    def add_checkbox(self, text):
        checkbox = QCheckBox(text)
        self.layout.addWidget(checkbox)
        return self
        
    def add_radio_button(self, text):
        radio = QRadioButton(text)
        self.layout.addWidget(radio)
        return self
        
    def add_dropdown(self, items):
        dropdown = QComboBox()
        dropdown.addItems(items)
        self.layout.addWidget(dropdown)
        return self
        
    def add_text_input_module(self, var_name, title, placeholder=''):
        """封装文本输入功能模块
        :param var_name: 变量名，用于标识输入框
        :param title: 输入框标题
        :param placeholder: 空白提示符
        """
        # 创建水平布局
        hbox = QHBoxLayout()
        
        # 添加标签
        label = QLabel(title)
        hbox.addWidget(label)
        
        # 添加输入框
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        hbox.addWidget(input_field)
        
        # 将水平布局添加到主布局
        self.layout.addLayout(hbox)
        self.input_fields[var_name] = input_field
        return self
        
    def save_config(self):
        """保存当前配置到zxconfig.json"""
        config = {}
        if os.path.exists('zxconfig.json'):
            with open('zxconfig.json', 'r') as f:
                config = json.load(f)
        
        # 更新或添加新配置项
        for field_name, input_field in self.input_fields.items():
            config[field_name] = input_field.text()
        
        with open('zxconfig.json', 'w') as f:
            json.dump(config, f, indent=4)
            
    def load_config(self):
        """从zxconfig.json加载配置"""
        if not os.path.exists('zxconfig.json'):
            # 如果文件不存在，创建空配置
            with open('zxconfig.json', 'w') as f:
                json.dump({}, f)
            return
        
        with open('zxconfig.json', 'r') as f:
            config = json.load(f)
            # 处理self.input_fields字典中的所有输入字段
            for field_name, input_field in self.input_fields.items():
                if field_name in config:
                    input_field.setText(config[field_name])
                else:
                    config[field_name] = ''  # 默认空值
                    input_field.setText('')
            
            # 保存更新后的配置
            with open('zxconfig.json', 'w') as f:
                json.dump(config, f, indent=4)
            
    def start(self):
        self.load_config()
        self.window.show()
        self.app.exec()
        self.save_config()
        # 延迟1秒关闭窗口，给用户确认时间
        self.window.setWindowTitle("配置已保存，窗口即将关闭...")
        self.app.processEvents()
        self.app.quit()

if __name__ == '__main__':
    def on_submit():
        print("Username:", ui.input_fields['username_input'].text())
        print("Email:", ui.input_fields['email_input'].text())
        ui.save_config()
        ui.window.close()  # 仅关闭窗口，不退出程序

    # 创建UI实例
    ui = ScriptLauncherUI(style='light')
    ui.window.setWindowTitle('脚本UI启动器 - 配置页面')
    
    # 添加UI组件
    ui.add_label('欢迎使用SimpleUI库')
    ui.add_text_input_module('username_input', '用户名', '请输入用户名')
    ui.add_text_input_module('email_input', '邮箱地址', '请输入邮箱')
    ui.add_button("提交", on_submit)
    ui.start()
