import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTextBrowser
from PyQt5.QtGui import QFont
import spacy
from spacy.matcher import Matcher
import json
from datetime import datetime, timedelta
import pytz

# Set the timezone to GMT = 0
timezone = pytz.timezone('Etc/GMT')

# Get the current time in the specified timezone
current_time = datetime.now(timezone)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.nlp = spacy.load("en_core_web_sm")

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
        input_text = self.input_box.text()

        # Process input text using spaCy
        doc = self.nlp(input_text)

        # INPUT => OUTPUT

        # Force Quit using QProgram or quitprogram
        if any("qprogram" in token.text.lower() for token in doc) or any("quitprogram" in token.text.lower() for token in doc):
            self.quit_application()

        # City + Weather
        elif any(token.text.lower() == "weather" for token in doc):
            location = None
            for ent in doc.ents:
                if ent.label_ == "GPE":  # GPE: Geo-Political Entity (Location)
                    location = ent.text.lower()
                    break

            if location:
                weather_info = self.get_weather_info(location)
                if weather_info:
                    return f"The weather in {location.capitalize()} is {weather_info['weather']}, {weather_info['temperature']} Celcius Degree"
                else:
                    return f"Sorry, I couldn't find the weather information for {location.capitalize()}"
            else:
                return "I'm sorry, I didn't quite catch the location. Can you please specify it?"

        # Country + capital
        elif any(token.text.lower() == "capital" for token in doc):
            country = None
            for ent in doc.ents:
                if ent.label_ == "GPE":  # Geo-Political Entity (Location)
                    country = ent.text.lower()
                    break

            if country:
                country_info = self.get_country_info(country)
                if country_info:
                    return f"The capital of {country.capitalize()} is {country_info['capital'].capitalize()}."
                else:
                    return f"Sorry, I cannot find the capital of {country}, the entity might not be a country."
            else:
                return "I'm sorry, I didn't quite catch the country. Can you please specify it?"

        # Country + gdp
        elif any(token.text.lower() == "gdp" for token in doc):
            country = None
            for ent in doc.ents:
                if ent.label_ == "GPE":  # Geo-Political Entity (Location)
                    country = ent.text.lower()
                    break

            if country:
                country_info = self.get_country_info(country)
                if country_info:
                    return f"Up-to-date on February 2024, the recorded GDP or Gross Domestic Product of {country.capitalize()} is {country_info['GDP']}."
                else:
                    return f"Sorry, I cannot find the GDP of {country.capitalize()}, the entity might not be a country."
            else:
                return "I'm sorry, I didn't quite catch the country. Can you please specify it?"

        # Country + size/area
        elif any(token.text.lower() == "area" for token in doc) or any(token.text.lower() == "size" for token in doc):
            country = None
            for ent in doc.ents:
                if ent.label_ == "GPE":  # Geo-Political Entity (Location)
                    country = ent.text.lower()
                    break

            if country:
                country_info = self.get_country_info(country)
                if country_info:
                    area = country_info['area'].replace(',', '')        # Remove comma
                    area_number = int(area.split()[0])                  # Convert to numeric
                    if area_number >= 1000000:
                        return f"This country is so HUGE! The living area of {country} is {country_info['area']}."
                    elif 100000 <= area_number < 1000000:
                        return f"{country} has the living land area of {country_info['area']}, " \
                               f"which is a moderate-sized country."
                    else:
                        return f"The size of this country is a bit modest, {country} has the area of {country_info['area']}"
                else:
                    return f"Sorry, I cannot find the GDP of {country}, the entity might not be a country."
            else:
                return "I'm sorry, I didn't quite catch the country. Can you please specify it?"

        # Country + Population
        elif any(token.text.lower() == "population" for token in doc):
            country = None
            for ent in doc.ents:
                if ent.label_ == "GPE":  # Geo-Political Entity (Location)
                    country = ent.text.lower()
                    break

            if country:
                country_info = self.get_country_info(country)
                if country_info:
                    if country_info['population'] > 1000000000:
                        return f"The population of {country} is {country_info['population']}. " \
                               f"This is one of a few countries with more than 1 billion people."
                    else:
                        return f"The population of {country} is {country_info['population']}."
                else:
                    return f"Sorry, I cannot find the population of {country.capitalize()}, the entity might not be a country."
            else:
                return "I'm sorry, I didn't quite catch the country. Can you please specify it?"

        # Country + Timezome
        elif any(token.text.lower() == "time" for token in doc) or any(token.text.lower() == "timezone" for token in doc):
            country = None
            for ent in doc.ents:
                if ent.label_ == "GPE":  # Geo-Political Entity (Location)
                    country = ent.text.lower()
                    break

            if country:
                country_info = self.get_country_info(country)
                if country_info:
                    country_gmt = country_info['timezone']
                    new_time = current_time + timedelta(hours=country_gmt)
                    new_time = new_time.strftime("%H:%M, %d-%m-%Y")
                    return f"Currently, the time of this country is {new_time}, its timezone is GMT+{country_gmt}"
                else:
                    return f"Sorry, I cannot find the time of {country.capitalize()}, the entity might not be a country."
            else:
                return "I'm sorry, I didn't quite catch the country. Can you please specify it?"

        # Country + Sea Boundary
        elif (any(token.lemma_.lower() == "sea" for token in doc) or any(token.lemma_.lower() == "ocean" for token in doc))\
                and (any(token.text.lower() == "border" for token in doc)
                     or any(token.text.lower() == "boundary" for token in doc)):
            country = None
            for ent in doc.ents:
                if ent.label_ == "GPE":  # Geo-Political Entity (Location)
                    country = ent.text.lower()
                    break

            if country:
                country_info = self.get_country_info(country)
                if country_info:
                    if country_info['sea_boundary'] == 0:
                        return f"{country.capitalize()} does not have any sea boundary at all. How sad!"
                    else:
                        return f"{country.capitalize()}'s length of the sea borderline is {country_info['sea_boundary']}"
                else:
                    return f"Sorry, I cannot find the time of {country.capitalize()}, the entity might not be a country."
            else:
                return "I'm sorry, I didn't quite catch the country. Can you please specify it?"

        # Country + Best Ally
        elif any(token.lemma_.lower() == "good" for token in doc) \
                and (any(token.text.lower() == "ally" for token in doc) or any(token.text.lower() == "alliance" for token in doc)):
            country = None
            for ent in doc.ents:
                if ent.label_ == "GPE":  # Geo-Political Entity (Location)
                    country = ent.text.lower()
                    break

            if country:
                country_info = self.get_country_info(country)
                if country_info:
                    return f"The best alliance of this country is {country_info['best_ally']}"
                else:
                    return f"Sorry, I cannot find the time of {country.capitalize()}, the entity might not be a country."
            else:
                return "I'm sorry, I didn't quite catch the country. Can you please specify it?"

        # Country + AVG Income
        elif any(token.lemma_.lower() == "average" for token in doc) \
                and (any(token.lemma_.lower() == "income" for token in doc) or any(token.lemma_.lower() == "earn" for token in doc)):
            country = None
            for ent in doc.ents:
                if ent.label_ == "GPE":  # Geo-Political Entity (Location)
                    country = ent.text.lower()
                    break

            if country:
                country_info = self.get_country_info(country)
                if country_info:
                    return f"The average income of a {country.capitalize()} person is {country_info['average_income']} USD."
                else:
                    return f"Sorry, I cannot find the time of {country.capitalize()}, the entity might not be a country."
            else:
                return "I'm sorry, I didn't quite catch the country. Can you please specify it?"

        # Hello / Hi
        elif any(token.text.lower() in ["hello", "hi"] for token in doc):
            return "Hello my friend, welcome back. This is AssistBot 1.0"

        else:
            return "I'm sorry, I didn't quite catch that. Can you please rephrase?"


    def get_weather_info(self, location):
        with open("res.json", "r") as json_file:
            data = json.load(json_file)
            weather_data = data.get("weather")
            return weather_data.get(location.lower())

    def get_country_info(self, country):
        with open("res.json", "r") as json_file:
            data = json.load(json_file)
            country_data = data.get("country")
            return country_data.get(country.lower())

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
