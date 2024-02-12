import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTextBrowser
from PyQt5.QtGui import QFont

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AssistBot by tuanx18")
        self.resize(1000, 800)

        self.init_ui()

    def init_ui(self):
        self.conversation_box = QTextBrowser(self)
        self.conversation_box.setGeometry(50, 50, 900, 600)

        # Set Font Size
        font = QFont()
        font.setPointSize(14)
        self.conversation_box.setFont(font)

        self.input_box = QLineEdit(self)
        self.input_box.setGeometry(50, 670, 700, 80)
        self.input_box.setFont(QFont("Arial", 12))
        self.input_box.returnPressed.connect(self.display_input)

        self.enter_button = QPushButton("Enter", self)
        self.enter_button.setGeometry(760, 670, 80, 80)
        self.enter_button.clicked.connect(self.display_input)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.setGeometry(847, 713, 100, 37)
        self.quit_button.clicked.connect(self.quit_application)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(847, 670, 100, 37)
        self.clear_button.clicked.connect(self.clear_conversation)

    def display_input(self):
        input_text = self.input_box.text()
        if input_text:
            lines = input_text.split("|||")  # Split input by "|||"
            formatted_input = f'<font color="blue">User:</font><br/>'  # Colorize "User"
            formatted_input += "<br/>".join(lines)  # Concatenate lines with HTML line break
            if len(lines) == 1:  # Check if there's only one line
                formatted_input += "<br/>"  # Add line break after single-line prompt
            else:
                formatted_input += "<br/><br/>"  # Add two line breaks after multi-line prompt
            self.conversation_box.append(formatted_input.strip())  # Append formatted input to conversation box

            # Assist Bot response
            bot_response = self.generate_bot_response()  # Generate bot response
            formatted_bot_response = f'<font color="orange">Bot:</font><br/>{bot_response}'  # Colorize "Bot" and add line break
            self.conversation_box.append(formatted_bot_response)  # Append bot response to conversation box

            self.input_box.clear()

    def generate_bot_response(self):
        # Replace this with your actual logic to generate bot responses
        return "///"

    def quit_application(self):
        QApplication.quit()

    def clear_conversation(self):
        self.conversation_box.clear()

def main():
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
