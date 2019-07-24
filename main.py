from shutil import copy2
from time import ctime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, \
                            QLabel, QGridLayout, QMainWindow, QDial, QComboBox, QTabWidget, \
                            QDialog, QDialogButtonBox, QGroupBox, QCheckBox, QListWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtGui
import sys
import csv
import os
import cloudinary
import cloudinary.uploader

#/Users/bestofluck/Desktop/BOL_THIS IS THE MENU 2.22.19.jpg

def update_website_menu():
    #file = "img/current_menu.jpg"
    file = "/Users/bestofluck/Desktop/MENU.jpg"

    cloudinary.config(cloud_name='',
                      api_key='',
                      api_secret='')

    cloudinary.uploader.destroy('current_menu', invalidate=True)

    cloudinary.uploader.upload(file,
                               public_id='current_menu',
                               overwrite=True,
                               invalidate=True)


def game_over_update_file(num):
    data = None
    #with open('data/item_history_chopping.txt', 'r') as file:
    with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_chopping.txt', 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    data[int(num) - 1] = "GAME OVER" + '\n'

    with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_chopping.txt', 'w') as file:
        file.writelines(data)


class TabWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.top = 200
        self.left = 500
        self.width = 1000
        self.height = 700
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("Best of Luck Beer Hall - Drink Menu Editor")
        self.icon = QIcon("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/bolt_lightblue.png")
        self.setWindowIcon(self.icon)

        tabwidget = QTabWidget()
        tabwidget.addTab(MainTab(), "Change a Drink")
        tabwidget.addTab(ChopTab(), "Chopping Block")
        tabwidget.addTab(GameOverTab(), "Game Over")
        tabwidget.addTab(HistoryTab(), "Edit History")

        vbox = QVBoxLayout()
        vbox.addWidget(tabwidget)
        self.setLayout(vbox)


class MainTab(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()

        self.number = QLabel("<strong>Number:</strong>")
        self.name = QLabel("<strong>Name:</strong>")
        self.style = QLabel("<strong>Style:</strong>")
        self.abv = QLabel("<strong>ABV:</strong> (7.5)")
        self.five_oz_price = QLabel("<strong>5oz Price:</strong> (3.50)")
        self.ten_oz_price = QLabel("<strong>10oz Price:</strong> (4.00)")
        self.sixteen_oz_price = QLabel("<strong>16oz Price:</strong> (6.50)")
        self.price_warning_1 = QLabel("Enter " + "<strong>0</strong>" +  " or the word <strong>bolt</strong> for unavailable sizes.")
        #self.price_warning_2 = QLabel(" word " + "<strong>bolt</strong>" + " for")
        #self.price_warning_3 = QLabel("unavailable sizes.")
        self.number_entry = QComboBox()
        self.number_entry.setMaximumWidth(75)
        self.number_entry.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                                    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                                    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                                    "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"])

        self.name_entry = QLineEdit()
        self.name_entry.setMaxLength(60)
        self.name_entry.setMaximumWidth(500)
        self.style_entry = QLineEdit()
        self.style_entry.setMaxLength(25)
        self.style_entry.setMaximumWidth(255)
        self.abv_entry = QLineEdit()
        self.abv_entry.setMaximumWidth(45)
        self.abv_entry.setMaxLength(4)
        self.five_oz_price_entry = QLineEdit()
        self.five_oz_price_entry.setMaximumWidth(45)
        self.five_oz_price_entry.setMaxLength(5)
        self.ten_oz_price_entry = QLineEdit()
        self.ten_oz_price_entry.setMaximumWidth(45)
        self.ten_oz_price_entry.setMaxLength(5)
        self.sixteen_oz_price_entry = QLineEdit()
        self.sixteen_oz_price_entry.setMaximumWidth(45)
        self.sixteen_oz_price_entry.setMaxLength(5)
        self.ok_button = QPushButton("Update Menu", self)
        self.confirmation = QLabel()

        self.name_limit = QLabel("<strong>60</strong> character limit.")
        self.style_limit = QLabel("<strong>25</strong> character limit.")

        grid.addWidget(self.number, 1, 0)
        grid.addWidget(self.number_entry, 1, 1)
        grid.addWidget(self.name, 2, 0)
        grid.addWidget(self.name_entry, 2, 1)
        grid.addWidget(self.name_limit, 2, 2)
        grid.addWidget(self.style, 3, 0)
        grid.addWidget(self.style_entry, 3, 1)
        grid.addWidget(self.style_limit, 3, 2)
        grid.addWidget(self.abv, 4, 0)
        grid.addWidget(self.abv_entry, 4, 1)
        grid.addWidget(self.five_oz_price, 5, 0)
        grid.addWidget(self.five_oz_price_entry, 5, 1)
        grid.addWidget(self.ten_oz_price, 6, 0)
        grid.addWidget(self.ten_oz_price_entry, 6, 1)
        grid.addWidget(self.sixteen_oz_price, 7, 0)
        grid.addWidget(self.sixteen_oz_price_entry, 7, 1)
        grid.addWidget(self.ok_button, 8, 0)
        grid.addWidget(self.confirmation, 8, 1)
        grid.addWidget(self.price_warning_1, 5, 2)
        #grid.addWidget(self.price_warning_2, 6, 2)
        #grid.addWidget(self.price_warning_3, 7, 2)

        self.setLayout(grid)
        self.ok_button.clicked.connect(self.onPress)


    def onPress(self):
        missing = "Missing: "

        if self.name_entry.text() == "":
            missing += "'Name', "
        if self.style_entry.text() == "":
            missing += "'Style', "
        if self.abv_entry.text() == "":
            missing += "'ABV', "
        if self.five_oz_price_entry.text() == "":
            missing += "'5oz Price', "
        if self.ten_oz_price_entry.text() == "":
            missing += "'10oz Price', "
        if self.sixteen_oz_price_entry.text() == "":
            missing += "'16oz Price', "

        if len(missing) == 9:
            self.generate_menu(str(self.number_entry.currentText()),
                               self.name_entry.text(),
                               self.style_entry.text(),
                               self.abv_entry.text(),
                               self.five_oz_price_entry.text(),
                               self.ten_oz_price_entry.text(),
                               self.sixteen_oz_price_entry.text())

            self.confirmation.setFont(QFont("Arial", 14, QFont.Bold))
            self.confirmation.setText("<font color='green'>Successfully added \"</font>" +
                                      self.name_entry.text() + "<font color='green'>\"<font>")

        if len(missing) > 9:
            missing = missing[9:-2]
            self.confirmation.setText("<strong><font color='red'>Missing: </font></strong>" + missing)


    def backup_menu(self):

        # Backup current menu to /past_menus
        time = ctime()
        time = time.replace(" ", "_")
        time = time.replace(":", "-")
        dest = "/Users/bestofluck/DO_NOT_TOUCH/BOL/past_menus/" + time + ".jpg"
        copy2("/Users/bestofluck/Desktop/MENU.jpg", dest)


    def clean_input(self, name: str, num: str, style: str, abv: str, five_oz: str, ten_oz: str, sixteen_oz: str):

        less_ten = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        if num in less_ten:
            num = "0" + num

        five_lst = five_oz.split(".")
        ten_lst = ten_oz.split(".")
        sixteen_lst = sixteen_oz.split(".")

        if five_oz != "bolt":
            if len(five_lst) > 1:
                if len(five_lst[1]) < 2:
                    five_oz = five_lst[0] + "." + five_lst[1] + "0"
            else:
                five_oz = five_lst[0] + ".00"

        if ten_oz != "bolt":
            if len(ten_lst) > 1:
                if len(ten_lst[1]) < 2:
                    ten_oz = ten_lst[0] + "." + ten_lst[1] + "0"
            else:
                ten_oz = ten_lst[0] + ".00"

        if sixteen_oz != "bolt":
            if len(sixteen_lst) > 1:
                if len(sixteen_lst[1]) < 2:
                    sixteen_oz = sixteen_lst[0] + "." + sixteen_lst[1] + "0"
            else:
                sixteen_oz = sixteen_lst[0] + ".00"

        if five_oz == "0" or five_oz == "0.0" or five_oz == "0.00" or five_oz == "00.00":
            five_oz = "bolt"
        if ten_oz == "0" or ten_oz == "0.0" or ten_oz == "0.00" or ten_oz == "00.00":
            ten_oz = "bolt"
        if sixteen_oz == "0" or sixteen_oz == "0.0" or sixteen_oz == "0.00" or sixteen_oz == "00.00":
            sixteen_oz = "bolt"

        if len(abv) == 1:
            abv = abv + ".0"
        if len(abv) == 2 and abv[-1] == ".":
            abv = abv + "0"

        return name.upper(), num, style.upper(), abv, five_oz, ten_oz, sixteen_oz


    def get_background_color(self, num):

        color = (0, 0, 0)
        bolt = None

        colors = {"lightgray": (139, 140, 142), "darkgray": (109, 110, 112),
                  "lightblue": (38, 103, 171), "darkblue": (18, 74, 151)}

        beer_odd = ["01", "03", "05", "11", "13", "15", "17", "19",
                    "21", "23", "25", "27", "29", "31", "33", "35"]
        beer_even = ["02", "04", "06", "12", "14", "16", "18", "20",
                     "22", "24", "26", "28", "30", "32", "34", "36"]
        punch_wine_odd = ["07", "09", "37", "39"]
        punch_wine_even = ["08", "10", "38", "40"]

        if num in beer_odd:
            bolt = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/bolt_lightblue.png")
            color = colors["lightblue"]
        elif num in beer_even:
            bolt = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/bolt_darkblue.png")
            color = colors["darkblue"]
        elif num in punch_wine_odd:
            bolt = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/bolt_lightgray.png")
            color = colors["lightgray"]
        elif num in punch_wine_even:
            bolt = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/bolt_darkgray.png")
            color = colors["darkgray"]
        else:
            print("ID Number not in given range of 1-40")

        return color, bolt


    def get_coords(self, key: str):

        menu_coords = {"01": [143, 108], "02": [143, 200], "03": [143, 292], "04": [143, 385], "05": [143, 477],
                       "06": [143, 569], "07": [143, 691], "08": [143, 776], "09": [143, 859], "10": [143, 947],
                       "11": [1064, 108], "12": [1064, 200], "13": [1064, 292], "14": [1064, 385], "15": [1064, 477],
                       "16": [1064, 569], "17": [1064, 662], "18": [1064, 754], "19": [1064, 846], "20": [1064, 938],
                       "21": [2064, 108], "22": [2064, 200], "23": [2064, 292], "24": [2064, 385], "25": [2064, 477],
                       "26": [2064, 569], "27": [2064, 662], "28": [2064, 754], "29": [2064, 846], "30": [2064, 938],
                       "31": [2984, 108], "32": [2984, 200], "33": [2984, 292], "34": [2984, 385], "35": [2984, 477],
                       "36": [2984, 569], "37": [2984, 691], "38": [2984, 776], "39": [2984, 859], "40": [2984, 947]}

        item_coords = {"name": (1, 1), "five_oz": (493, 1), "ten_oz": (598, 1), "sixteen_oz": (703, 1)}

        if key in menu_coords.keys():
            return menu_coords[key]
        elif key in item_coords.keys():
            return item_coords[key]


    def image_draw(self, template, coord, string, font, total_w, total_h):
        draw = ImageDraw.Draw(template)
        w, h = draw.textsize(string, font)

        if total_h == None or total_w == None:
            return ImageDraw.Draw(template).text(
                coord,
                string,
                (270, 270, 270),
                font=font
            )
        # Draw prices
        else:
            return draw.text(((total_w-w)/2,(total_h-h)/2), string, (270, 270, 270), font=font)


    def generate_two_lines(self, font, name):
        w, h = font.getsize(name)
        space_w, space_h = font.getsize(" ")

        line_one = []
        line_two = []

        # If line is too long, generate two lines
        if w > 466:
            name_list = name.split(" ")
            line_one_count = 466
            word_count = 0
            done = False

            while not done:

                this_w, this_h = font.getsize(name_list[word_count])
                line_one_count -= this_w

                if line_one_count >= 0:
                    line_one.append(name_list[word_count])
                    line_one_count -= space_w
                    word_count += 1
                else:
                    done = True

            for i in range(word_count, len(name_list)):
                line_two.append(name_list[i])

        return " ".join(line_one), " ".join(line_two)


    def draw(self, name: str, style: str, abv: str, five_oz: str, ten_oz: str, sixteen_oz: str, color: tuple, bolt: str):

        color_lightgray = (139, 140, 142)
        color_darkgray = (109, 110, 112)
        color_lightblue = (38, 103, 171)
        color_darkblue = (18, 74, 151)

        beer_dims = {"five_oz": (101, 88), "ten_oz": (101, 88), "sixteen_oz": (101, 88),
                     "name": (487, 88), "whole": (522, 87)}
        punchwine_dims = {"five_oz": (101, 80), "ten_oz": (101, 80), "sixteen_oz": (101, 80),
                          "name": (487, 80), "whole": (522, 80)}

        name_coord = (18, 18)
        style_abv_coord = (18, 51)
        price_coord = (17, 30)
        punchwine_name_coord = (18, 13)
        punchwine_style_abv_coord = (18, 48)
        punchwine_price_coord = (17, 30)

        style_abv = style + ": " + abv + "% ABV"
        if float(abv) <= 0:
            style_abv = style

        name_font = ImageFont.truetype("/Users/bestofluck/DO_NOT_TOUCH/BOL/fonts/Drink_trade-gothic-lt-std-bold-condensed-no-20-5872def1d27d8.otf", 34)
        style_abv_font = ImageFont.truetype("/Users/bestofluck/DO_NOT_TOUCH/BOL/fonts/LetterGothicStdBold.ttf", 22)
        price_font = ImageFont.truetype("/Users/bestofluck/DO_NOT_TOUCH/BOL/fonts/LetterGothicStdBold.ttf", 26)

        item_template = None
        if color == color_lightgray:
            item_template = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/item_templates/blank_lightgray.png")
        elif color == color_darkgray:
            item_template = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/item_templates/blank_darkgray.png")
        elif color == color_lightblue:
            item_template = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/item_templates/blank_lightblue.png")
        elif color == color_darkblue:
            item_template = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/item_templates/blank_darkblue.png")

        # Calculate if two lines are necessary
        w, h = name_font.getsize(name)
        two_line = False
        if w > 466:
            two_line = True

        # Draw 2-line item if necessary
        if two_line is True:

            line_one, line_two = self.generate_two_lines(name_font, name)

            name_coord = (18, 6)
            name_2_coord = (18, 33)
            style_abv_coord = (18, 66)

            # Draw beers (blue) text
            if color == color_lightblue or color == color_darkblue:
                total_w = beer_dims["five_oz"][0]
                total_h = beer_dims["five_oz"][1]

                # Draw Name, Style, ABV
                self.image_draw(item_template, name_coord, line_one, name_font, None, None)
                self.image_draw(item_template, name_2_coord, line_two, name_font, None, None)
                self.image_draw(item_template, style_abv_coord, style_abv, style_abv_font, None, None)

                # Draw 5oz price
                if five_oz != "bolt":
                    price_template = Image.new("RGBA", beer_dims["five_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + five_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("five_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("five_oz"))

                # Draw 10oz price
                if ten_oz != "bolt":
                    price_template = Image.new("RGBA", beer_dims["ten_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + ten_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("ten_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("ten_oz"))

                # Draw 16oz price
                if sixteen_oz != "bolt":
                    price_template = Image.new("RGBA", beer_dims["sixteen_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + sixteen_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("sixteen_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("sixteen_oz"))
            # Draw punches and wine
            else:
                total_w = punchwine_dims["five_oz"][0]
                total_h = punchwine_dims["five_oz"][1]

                punchwine_name_coord = (18, 4)
                punchwine_name_2_coord = (18, 31)
                punchwine_style_abv_coord = (18, 60)

                # Draw Name, Style, and ABV
                self.image_draw(item_template, punchwine_name_coord, line_one, name_font, None, None)
                self.image_draw(item_template, punchwine_name_2_coord, line_two, name_font, None, None)
                self.image_draw(item_template, punchwine_style_abv_coord, style_abv, style_abv_font, None, None)

                # Draw 5oz price
                if five_oz != "bolt":
                    price_template = Image.new("RGBA", punchwine_dims["five_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + five_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("five_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("five_oz"))

                # Draw 10oz price
                if ten_oz != "bolt":
                    price_template = Image.new("RGBA", punchwine_dims["ten_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + ten_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("ten_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("ten_oz"))

                # Draw 16oz price
                if sixteen_oz != "bolt":
                    price_template = Image.new("RGBA", punchwine_dims["sixteen_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + sixteen_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("sixteen_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("sixteen_oz"))


        # Otherwise, draw 1-line item
        else:
            # Draw beers (blue) text
            if color == color_lightblue or color == color_darkblue:
                total_w = beer_dims["five_oz"][0]
                total_h = beer_dims["five_oz"][1]

                # Draw Name, Style, and ABV
                self.image_draw(item_template, name_coord, name, name_font, None, None)
                self.image_draw(item_template, style_abv_coord, style_abv, style_abv_font, None, None)

                # Draw 5oz price
                if five_oz != "bolt":
                    price_template = Image.new("RGBA", beer_dims["five_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + five_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("five_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("five_oz"))

                # Draw 10oz price
                if ten_oz != "bolt":
                    price_template = Image.new("RGBA", beer_dims["ten_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + ten_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("ten_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("ten_oz"))

                # Draw 16oz price
                if sixteen_oz != "bolt":
                    price_template = Image.new("RGBA", beer_dims["sixteen_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + sixteen_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("sixteen_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("sixteen_oz"))

            # Draw punches and wines
            else:
                total_w = beer_dims["five_oz"][0]
                total_h = beer_dims["five_oz"][1]

                # Draw Name, Style, and ABV
                self.image_draw(item_template, punchwine_name_coord, name, name_font, None, None)
                self.image_draw(item_template, punchwine_style_abv_coord, style_abv, style_abv_font, None, None)

                # Draw 5oz price
                if five_oz != "bolt":
                    price_template = Image.new("RGBA", punchwine_dims["five_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + five_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("five_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("five_oz"))

                # Draw 10oz price
                if ten_oz != "bolt":
                    price_template = Image.new("RGBA", punchwine_dims["ten_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + ten_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("ten_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("ten_oz"))

                # Draw 16oz price
                if sixteen_oz != "bolt":
                    price_template = Image.new("RGBA", punchwine_dims["sixteen_oz"], color)
                    self.image_draw(price_template, price_coord, "$" + sixteen_oz, price_font, total_w, total_h)
                    item_template.paste(price_template, self.get_coords("sixteen_oz"))
                else:
                    item_template.paste(bolt, self.get_coords("sixteen_oz"))

        return item_template


    def save_item(self, item, name, style, abv):

        abv = abv.replace(".", "_")

        name = name.replace("/", "_")
        name = name.replace("\\", "_")

        item.save("/Users/bestofluck/DO_NOT_TOUCH/BOL/past_items/" + name + " - " + style + " - " + abv + ".png", "PNG")


    def overwrite_curr_menu(self, menu):

        menu.save("/Users/bestofluck/Desktop/MENU.jpg", "PNG")
        copy2("/Users/bestofluck/Desktop/MENU.jpg", "/Users/bestofluck/DO_NOT_TOUCH/BOL/current_menu_copy.jpg")
        #copy2("/Users/bestofluck/Desktop/MENU.jpg", "/Users/bestofluck/Desktop/MENU.jpg")

    def update_csv(self, num: str, name: str, style: str, abv: str, five_oz: str, ten_oz: str, sixteen_oz: str):

        time = ctime()
        time = time.replace(" ", "_")
        time = time.replace(":", "-")

        with open("/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history.csv", "a", newline='') as file:
            file.write(
                num + ',' + name + ',' + style + ',' + abv + ',' + five_oz + ',' + ten_oz + ',' + sixteen_oz + ','
                + time + '\n')

        data = None
        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_chopping.txt', 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        name_sub = name[:17]
        data[int(num) - 1] = name_sub + "..." + '\n'

        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_chopping.txt', 'w') as file:
            file.writelines(data)

        game_over_nums = None
        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_gameover_numbers.csv', 'r') as file2:
            game_over_nums = file2.readlines()


        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_gameover_numbers.csv', 'w', newline='') as csvfile:

            nums_stay = []
            for go in game_over_nums:
                if go != (num + '\n'):
                    nums_stay.append(go)

            for each in nums_stay:
                csvfile.write(each)


    def generate_menu(self, num: str, name: str, style: str, abv: str, five_oz: str, ten_oz: str, sixteen_oz: str):

        self.backup_menu()

        print(five_oz, ten_oz, sixteen_oz)
        name, num, style, abv, five_oz, ten_oz, sixteen_oz = self.clean_input(name, num, style, abv, five_oz, ten_oz, sixteen_oz)
        print(five_oz, ten_oz, sixteen_oz)

        self.update_csv(num, name, style, abv, five_oz, ten_oz, sixteen_oz)

        color, bolt = self.get_background_color(num)

        menu = Image.open("/Users/bestofluck/Desktop/MENU.jpg")
        item = self.draw(name, style, abv, five_oz, ten_oz, sixteen_oz, color, bolt)

        # Draw item to menu
        menu.paste(item, self.get_coords(num))

        # Display item to screen
        #menu.show()

        # Save current item
        self.save_item(item, name, style, abv)

        # Overwrite current menu
        self.overwrite_curr_menu(menu)

        # Update the website menu
        update_website_menu()


class ChopTab(QWidget):
    def __init__(self):
        super().__init__()

        self.data = None
        self.checked_numbers = []

        # Read in current item names
        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_chopping.txt', 'r') as file:
            # read a list of lines into data
            self.data = file.readlines()

        # Read in numbers that are already on Chopping Block
        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_chopping_numbers.csv', 'r') as file2:
            self.checked_numbers = file2.readlines()

        self.layout = QGridLayout()
        self.layout.setSpacing(0)

        # layout.addWidget(QLabel("Add and remove drinks from 'Chopping Block' status."), 0, 0)

        self.lst = [str(i) for i in range(1, 41)]
        self.lst.reverse()
        self.checkboxes = []
        self.max_height = 10

        self.one = QCheckBox("1: " + self.data[0])
        self.one.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.one, 0, 0)
        self.two = QCheckBox("2: " + self.data[1])
        self.two.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.two, 1, 0)
        self.three = QCheckBox("3: " + self.data[2])
        self.three.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.three, 2, 0)
        self.four = QCheckBox("4: " + self.data[3])
        self.four.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.four, 3, 0)
        self.five = QCheckBox("5: " + self.data[4])
        self.five.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.five, 4, 0)
        self.six = QCheckBox("6: " + self.data[5])
        self.six.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.six, 5, 0)
        self.seven = QLabel("7: <strong>CANNOT CHOP</strong>")
        self.layout.addWidget(self.seven, 6, 0)
        self.eight = QLabel("8: <strong>CANNOT CHOP</strong>")
        self.layout.addWidget(self.eight, 7, 0)
        self.nine = QLabel("9: <strong>CANNOT CHOP</strong>")
        self.layout.addWidget(self.nine, 8, 0)
        self.ten = QLabel("10: <strong>CANNOT CHOP</strong>")
        self.layout.addWidget(self.ten, 9, 0)
        self.eleven = QCheckBox("11: " + self.data[10])
        self.eleven.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.eleven, 0, 1)
        self.twelve = QCheckBox("12: " + self.data[11])
        self.twelve.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twelve, 1, 1)
        self.thirteen = QCheckBox("13: " + self.data[12])
        self.thirteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirteen, 2, 1)
        self.fourteen = QCheckBox("14: " + self.data[13])
        self.fourteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.fourteen, 3, 1)
        self.fifteen = QCheckBox("15: " + self.data[14])
        self.fifteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.fifteen, 4, 1)
        self.sixteen = QCheckBox("16: " + self.data[15])
        self.sixteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.sixteen, 5, 1)
        self.seventeen = QCheckBox("17: " + self.data[16])
        self.seventeen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.seventeen, 6, 1)
        self.eighteen = QCheckBox("18: " + self.data[17])
        self.eighteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.eighteen, 7, 1)
        self.nineteen = QCheckBox("19: " + self.data[18])
        self.nineteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.nineteen, 8, 1)
        self.twenty = QCheckBox("20: " + self.data[19])
        self.twenty.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twenty, 9, 1)
        self.twentyone = QCheckBox("21: " + self.data[20])
        self.twentyone.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyone, 0, 2)
        self.twentytwo = QCheckBox("22: " + self.data[21])
        self.twentytwo.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentytwo, 1, 2)
        self.twentythree = QCheckBox("23: " + self.data[22])
        self.twentythree.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentythree, 2, 2)
        self.twentyfour = QCheckBox("24: " + self.data[23])
        self.twentyfour.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyfour, 3, 2)
        self.twentyfive = QCheckBox("25: " + self.data[24])
        self.twentyfive.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyfive, 4, 2)
        self.twentysix = QCheckBox("26: " + self.data[25])
        self.twentysix.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentysix, 5, 2)
        self.twentyseven = QCheckBox("27: " + self.data[26])
        self.twentyseven.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyseven, 6, 2)
        self.twentyeight = QCheckBox("28: " + self.data[27])
        self.twentyeight.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyeight, 7, 2)
        self.twentynine = QCheckBox("29: " + self.data[28])
        self.twentynine.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentynine, 8, 2)
        self.thirty = QCheckBox("30: " + self.data[29])
        self.thirty.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirty, 9, 2)
        self.thirtyone = QCheckBox("31: " + self.data[30])
        self.thirtyone.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtyone, 0, 3)
        self.thirtytwo = QCheckBox("32: " + self.data[31])
        self.thirtytwo.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtytwo, 1, 3)
        self.thirtythree = QCheckBox("33: " + self.data[32])
        self.thirtythree.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtythree, 2, 3)
        self.thirtyfour = QCheckBox("34: " + self.data[33])
        self.thirtyfour.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtyfour, 3, 3)
        self.thirtyfive = QCheckBox("35: " + self.data[34])
        self.thirtyfive.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtyfive, 4, 3)
        self.thirtysix = QCheckBox("36: " + self.data[35])
        self.thirtysix.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtysix, 5, 3)
        self.thirtyseven = QLabel("37: <strong>CANNOT CHOP</strong>")
        self.layout.addWidget(self.thirtyseven, 6, 3)
        self.thirtyeight = QLabel("38: <strong>CANNOT CHOP</strong>")
        self.layout.addWidget(self.thirtyeight, 7, 3)
        self.thirtynine = QLabel("39: <strong>CANNOT CHOP</strong>")
        self.layout.addWidget(self.thirtynine, 8, 3)
        self.forty = QLabel("40: <strong>CANNOT CHOP</strong>")
        self.layout.addWidget(self.forty, 9, 3)

        for each in self.checked_numbers:
            if each == "01\n":
                self.one.setChecked(True)
            if each == "02\n":
                self.two.setChecked(True)
            if each == "03\n":
                self.three.setChecked(True)
            if each == "04\n":
                self.four.setChecked(True)
            if each == "05\n":
                self.five.setChecked(True)
            if each == "06\n":
                self.six.setChecked(True)
            if each == "11\n":
                self.eleven.setChecked(True)
            if each == "12\n":
                self.twelve.setChecked(True)
            if each == "13\n":
                self.thirteen.setChecked(True)
            if each == "14\n":
                self.fourteen.setChecked(True)
            if each == "15\n":
                self.fifteen.setChecked(True)
            if each == "16\n":
                self.sixteen.setChecked(True)
            if each == "17\n":
                self.seventeen.setChecked(True)
            if each == "18\n":
                self.eighteen.setChecked(True)
            if each == "19\n":
                self.nineteen.setChecked(True)
            if each == "20\n":
                self.twenty.setChecked(True)
            if each == "21\n":
                self.twentyone.setChecked(True)
            if each == "22\n":
                self.twentytwo.setChecked(True)
            if each == "23\n":
                self.twentythree.setChecked(True)
            if each == "24\n":
                self.twentyfour.setChecked(True)
            if each == "25\n":
                self.twentyfive.setChecked(True)
            if each == "26\n":
                self.twentysix.setChecked(True)
            if each == "27\n":
                self.twentyseven.setChecked(True)
            if each == "28\n":
                self.twentyeight.setChecked(True)
            if each == "29\n":
                self.twentynine.setChecked(True)
            if each == "30\n":
                self.thirty.setChecked(True)
            if each == "31\n":
                self.thirtyone.setChecked(True)
            if each == "32\n":
                self.thirtytwo.setChecked(True)
            if each == "33\n":
                self.thirtythree.setChecked(True)
            if each == "34\n":
                self.thirtyfour.setChecked(True)
            if each == "35\n":
                self.thirtyfive.setChecked(True)
            if each == "36\n":
                self.thirtysix.setChecked(True)

        self.update_menu = QPushButton("Update Menu", self)
        self.layout.addWidget(self.update_menu, 12, 0)
        self.confirmation = QLabel("")
        self.layout.addWidget(self.confirmation, 12, 1)

        self.update_menu.clicked.connect(self.onClick)

        self.setLayout(self.layout)


    def onClick(self):
        checked = []

        if(self.one.isChecked()):
            checked.append("01")
        if(self.two.isChecked()):
            checked.append("02")
        if(self.three.isChecked()):
            checked.append("03")
        if (self.four.isChecked()):
            checked.append("04")
        if (self.five.isChecked()):
            checked.append("05")
        if (self.six.isChecked()):
            checked.append("06")
        if (self.eleven.isChecked()):
            checked.append("11")
        if (self.twelve.isChecked()):
            checked.append("12")
        if (self.thirteen.isChecked()):
            checked.append("13")
        if (self.fourteen.isChecked()):
            checked.append("14")
        if (self.fifteen.isChecked()):
            checked.append("15")
        if (self.sixteen.isChecked()):
            checked.append("16")
        if (self.seventeen.isChecked()):
            checked.append("17")
        if (self.eighteen.isChecked()):
            checked.append("18")
        if (self.nineteen.isChecked()):
            checked.append("19")
        if (self.twenty.isChecked()):
            checked.append("20")
        if (self.twentyone.isChecked()):
            checked.append("21")
        if (self.twentytwo.isChecked()):
            checked.append("22")
        if (self.twentythree.isChecked()):
            checked.append("23")
        if (self.twentyfour.isChecked()):
            checked.append("24")
        if (self.twentyfive.isChecked()):
            checked.append("25")
        if (self.twentysix.isChecked()):
            checked.append("26")
        if (self.twentyseven.isChecked()):
            checked.append("27")
        if (self.twentyeight.isChecked()):
            checked.append("28")
        if (self.twentynine.isChecked()):
            checked.append("29")
        if (self.thirty.isChecked()):
            checked.append("30")
        if (self.thirtyone.isChecked()):
            checked.append("31")
        if (self.thirtytwo.isChecked()):
            checked.append("32")
        if (self.thirtythree.isChecked()):
            checked.append("33")
        if (self.thirtyfour.isChecked()):
            checked.append("34")
        if (self.thirtyfive.isChecked()):
            checked.append("35")
        if (self.thirtysix.isChecked()):
            checked.append("36")

        number_coords = {"01": [53, 107], "02": [53, 199], "03": [53, 291], "04": [53, 384], "05": [53, 476],
                       "06": [53, 568], "07": [53, 690], "08": [53, 775], "09": [53, 858], "10": [53, 946],
                       "11": [973, 107], "12": [973, 199], "13": [973, 291], "14": [973, 384], "15": [973, 476],
                       "16": [973, 568], "17": [973, 661], "18": [973, 753], "19": [973, 845], "20": [973, 937],
                       "21": [1973, 107], "22": [1973, 199], "23": [1973, 291], "24": [1973, 384], "25": [1973, 476],
                       "26": [1973, 568], "27": [1973, 661], "28": [1973, 753], "29": [1973, 845], "30": [1973, 937],
                       "31": [2893, 107], "32": [2893, 199], "33": [2893, 291], "34": [2893, 384], "35": [2893, 476],
                       "36": [2893, 568], "37": [2893, 689], "38": [2893, 774], "39": [2893, 859], "40": [2893, 944]}

        beer_odd = ["01", "03", "05", "11", "13", "15", "17", "19",
                    "21", "23", "25", "27", "29", "31", "33", "35"]
        beer_even = ["02", "04", "06", "12", "14", "16", "18", "20",
                     "22", "24", "26", "28", "30", "32", "34", "36"]
        menu = Image.open("/Users/bestofluck/Desktop/MENU.jpg")

        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_chopping_numbers.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n')

            for each in checked:
                chop = None
                if each in beer_odd:
                    chop = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/chop_lightblue.png")
                elif each in beer_even:
                    chop = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/chop_darkblue.png")

                menu.paste(chop, number_coords[each])

                writer.writerow([each])

        punchwines = [7, 8, 9, 10, 37, 38, 39, 40]
        for i in range(1, 41):
            num_str = str(i)
            if i < 10:
                num_str = "0" + num_str
            if num_str not in checked:
                number = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/nums/" + num_str + ".png")
                menu.paste(number, number_coords[num_str])

        # Backup current menu to /past_menus
        time = ctime()
        time = time.replace(" ", "_")
        time = time.replace(":", "-")
        dest = "/Users/bestofluck/DO_NOT_TOUCH/BOL/past_menus/" + time + ".jpg"
        copy2("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/current_menu.jpg", dest)

        # Overwrite current menu
        menu.save("/Users/bestofluck/Desktop/MENU.jpg", "PNG")
        copy2("/Users/bestofluck/Desktop/MENU.jpg", "/Users/bestofluck/DO_NOT_TOUCH/BOL/current_menu_copy.jpg")

        # Update the website menu
        update_website_menu()

        self.confirmation.setText("<strong><font color='green'>Successfully updated.</font></strong>")


class GameOverTab(QWidget):
    def __init__(self):
        super().__init__()

        self.data = None
        self.checked_numbers = []

        # Read in current item names
        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_chopping.txt', 'r') as file:
            # read a list of lines into data
            self.data = file.readlines()

        # Read in numbers that are already on Chopping Block
        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_gameover_numbers.csv', 'r') as file2:
            self.checked_numbers = file2.readlines()

        self.labeled_game_over = []
        for i, each in enumerate(self.data):
            each = each[:9]
            i_str = ""
            if i < 10:
                i_str = "0" + str(i+1)
            else:
                i_str = str(i+1)
            if each == "GAME OVER":
                self.labeled_game_over.append(i_str)

        self.layout = QGridLayout()
        self.layout.setSpacing(0)

        self.lst = [str(i) for i in range(1, 41)]
        self.lst.reverse()
        self.checkboxes = []
        self.max_height = 10

        self.one = QCheckBox("1: " + self.data[0])
        self.one.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.one, 0, 0)
        self.two = QCheckBox("2: " + self.data[1])
        self.two.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.two, 1, 0)
        self.three = QCheckBox("3: " + self.data[2])
        self.three.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.three, 2, 0)
        self.four = QCheckBox("4: " + self.data[3])
        self.four.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.four, 3, 0)
        self.five = QCheckBox("5: " + self.data[4])
        self.five.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.five, 4, 0)
        self.six = QCheckBox("6: " + self.data[5])
        self.six.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.six, 5, 0)
        self.seven = QCheckBox("7: " + self.data[6])
        self.seven.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.seven, 6, 0)
        self.eight = QCheckBox("8: " + self.data[7])
        self.eight.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.eight, 7, 0)
        self.nine = QCheckBox("9: " + self.data[8])
        self.nine.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.nine, 8, 0)
        self.ten = QCheckBox("10: " + self.data[9])
        self.ten.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.ten, 9, 0)
        self.eleven = QCheckBox("11: " + self.data[10])
        self.eleven.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.eleven, 0, 1)
        self.twelve = QCheckBox("12: " + self.data[11])
        self.twelve.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twelve, 1, 1)
        self.thirteen = QCheckBox("13: " + self.data[12])
        self.thirteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirteen, 2, 1)
        self.fourteen = QCheckBox("14: " + self.data[13])
        self.fourteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.fourteen, 3, 1)
        self.fifteen = QCheckBox("15: " + self.data[14])
        self.fifteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.fifteen, 4, 1)
        self.sixteen = QCheckBox("16: " + self.data[15])
        self.sixteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.sixteen, 5, 1)
        self.seventeen = QCheckBox("17: " + self.data[16])
        self.seventeen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.seventeen, 6, 1)
        self.eighteen = QCheckBox("18: " + self.data[17])
        self.eighteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.eighteen, 7, 1)
        self.nineteen = QCheckBox("19: " + self.data[18])
        self.nineteen.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.nineteen, 8, 1)
        self.twenty = QCheckBox("20: " + self.data[19])
        self.twenty.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twenty, 9, 1)
        self.twentyone = QCheckBox("21: " + self.data[20])
        self.twentyone.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyone, 0, 2)
        self.twentytwo = QCheckBox("22: " + self.data[21])
        self.twentytwo.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentytwo, 1, 2)
        self.twentythree = QCheckBox("23: " + self.data[22])
        self.twentythree.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentythree, 2, 2)
        self.twentyfour = QCheckBox("24: " + self.data[23])
        self.twentyfour.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyfour, 3, 2)
        self.twentyfive = QCheckBox("25: " + self.data[24])
        self.twentyfive.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyfive, 4, 2)
        self.twentysix = QCheckBox("26: " + self.data[25])
        self.twentysix.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentysix, 5, 2)
        self.twentyseven = QCheckBox("27: " + self.data[26])
        self.twentyseven.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyseven, 6, 2)
        self.twentyeight = QCheckBox("28: " + self.data[27])
        self.twentyeight.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentyeight, 7, 2)
        self.twentynine = QCheckBox("29: " + self.data[28])
        self.twentynine.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.twentynine, 8, 2)
        self.thirty = QCheckBox("30: " + self.data[29])
        self.thirty.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirty, 9, 2)
        self.thirtyone = QCheckBox("31: " + self.data[30])
        self.thirtyone.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtyone, 0, 3)
        self.thirtytwo = QCheckBox("32: " + self.data[31])
        self.thirtytwo.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtytwo, 1, 3)
        self.thirtythree = QCheckBox("33: " + self.data[32])
        self.thirtythree.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtythree, 2, 3)
        self.thirtyfour = QCheckBox("34: " + self.data[33])
        self.thirtyfour.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtyfour, 3, 3)
        self.thirtyfive = QCheckBox("35: " + self.data[34])
        self.thirtyfive.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtyfive, 4, 3)
        self.thirtysix = QCheckBox("36: " + self.data[35])
        self.thirtysix.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtysix, 5, 3)
        self.thirtyseven = QCheckBox("37: " + self.data[36])
        self.thirtyseven.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtyseven, 6, 3)
        self.thirtyeight = QCheckBox("38: " + self.data[37])
        self.thirtyeight.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtyeight, 7, 3)
        self.thirtynine = QCheckBox("39: " + self.data[38])
        self.thirtynine.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.thirtynine, 8, 3)
        self.forty = QCheckBox("40: " + self.data[39])
        self.forty.setMaximumHeight(self.max_height)
        self.layout.addWidget(self.forty, 9, 3)

        # Set all previously checked numbers to checked
        for each in self.checked_numbers:
            if each == "01\n":
                self.one.setChecked(True)
            if each == "02\n":
                self.two.setChecked(True)
            if each == "03\n":
                self.three.setChecked(True)
            if each == "04\n":
                self.four.setChecked(True)
            if each == "05\n":
                self.five.setChecked(True)
            if each == "06\n":
                self.six.setChecked(True)
            if each == "07\n":
                self.seven.setChecked(True)
            if each == "08\n":
                self.eight.setChecked(True)
            if each == "09\n":
                self.nine.setChecked(True)
            if each == "10\n":
                self.ten.setChecked(True)
            if each == "11\n":
                self.eleven.setChecked(True)
            if each == "12\n":
                self.twelve.setChecked(True)
            if each == "13\n":
                self.thirteen.setChecked(True)
            if each == "14\n":
                self.fourteen.setChecked(True)
            if each == "15\n":
                self.fifteen.setChecked(True)
            if each == "16\n":
                self.sixteen.setChecked(True)
            if each == "17\n":
                self.seventeen.setChecked(True)
            if each == "18\n":
                self.eighteen.setChecked(True)
            if each == "19\n":
                self.nineteen.setChecked(True)
            if each == "20\n":
                self.twenty.setChecked(True)
            if each == "21\n":
                self.twentyone.setChecked(True)
            if each == "22\n":
                self.twentytwo.setChecked(True)
            if each == "23\n":
                self.twentythree.setChecked(True)
            if each == "24\n":
                self.twentyfour.setChecked(True)
            if each == "25\n":
                self.twentyfive.setChecked(True)
            if each == "26\n":
                self.twentysix.setChecked(True)
            if each == "27\n":
                self.twentyseven.setChecked(True)
            if each == "28\n":
                self.twentyeight.setChecked(True)
            if each == "29\n":
                self.twentynine.setChecked(True)
            if each == "30\n":
                self.thirty.setChecked(True)
            if each == "31\n":
                self.thirtyone.setChecked(True)
            if each == "32\n":
                self.thirtytwo.setChecked(True)
            if each == "33\n":
                self.thirtythree.setChecked(True)
            if each == "34\n":
                self.thirtyfour.setChecked(True)
            if each == "35\n":
                self.thirtyfive.setChecked(True)
            if each == "36\n":
                self.thirtysix.setChecked(True)
            if each == "37\n":
                self.thirtyseven.setChecked(True)
            if each == "38\n":
                self.thirtyeight.setChecked(True)
            if each == "39\n":
                self.thirtynine.setChecked(True)
            if each == "40\n":
                self.forty.setChecked(True)

        # Set anything labeled "GAME OVER" to checked
        for i, each in enumerate(self.labeled_game_over):
            if each == "01":
                self.one.setChecked(True)
            if each == "02":
                self.two.setChecked(True)
            if each == "03":
                self.three.setChecked(True)
            if each == "04":
                self.four.setChecked(True)
            if each == "05":
                self.five.setChecked(True)
            if each == "06":
                self.six.setChecked(True)
            if each == "07":
                self.seven.setChecked(True)
            if each == "08":
                self.eight.setChecked(True)
            if each == "09":
                self.nine.setChecked(True)
            if each == "10":
                self.ten.setChecked(True)
            if each == "11":
                self.eleven.setChecked(True)
            if each == "12":
                self.twelve.setChecked(True)
            if each == "13":
                self.thirteen.setChecked(True)
            if each == "14":
                self.fourteen.setChecked(True)
            if each == "15":
                self.fifteen.setChecked(True)
            if each == "16":
                self.sixteen.setChecked(True)
            if each == "17":
                self.seventeen.setChecked(True)
            if each == "18":
                self.eighteen.setChecked(True)
            if each == "19":
                self.nineteen.setChecked(True)
            if each == "20":
                self.twenty.setChecked(True)
            if each == "21":
                self.twentyone.setChecked(True)
            if each == "22":
                self.twentytwo.setChecked(True)
            if each == "23":
                self.twentythree.setChecked(True)
            if each == "24":
                self.twentyfour.setChecked(True)
            if each == "25":
                self.twentyfive.setChecked(True)
            if each == "26":
                self.twentysix.setChecked(True)
            if each == "27":
                self.twentyseven.setChecked(True)
            if each == "28":
                self.twentyeight.setChecked(True)
            if each == "29":
                self.twentynine.setChecked(True)
            if each == "30":
                self.thirty.setChecked(True)
            if each == "31":
                self.thirtyone.setChecked(True)
            if each == "32":
                self.thirtytwo.setChecked(True)
            if each == "33":
                self.thirtythree.setChecked(True)
            if each == "34":
                self.thirtyfour.setChecked(True)
            if each == "35":
                self.thirtyfive.setChecked(True)
            if each == "36":
                self.thirtysix.setChecked(True)
            if each == "37":
                self.thirtyseven.setChecked(True)
            if each == "38":
                self.thirtyeight.setChecked(True)
            if each == "39":
                self.thirtynine.setChecked(True)
            if each == "40":
                self.forty.setChecked(True)

        self.update_menu = QPushButton("Update Menu", self)
        self.layout.addWidget(self.update_menu, 12, 0)
        self.confirmation = QLabel("")
        self.layout.addWidget(self.confirmation, 12, 1)

        self.update_menu.clicked.connect(self.onClick)

        self.setLayout(self.layout)


    def onClick(self):
        checked = []

        if(self.one.isChecked()):
            checked.append("01")
        if(self.two.isChecked()):
            checked.append("02")
        if(self.three.isChecked()):
            checked.append("03")
        if (self.four.isChecked()):
            checked.append("04")
        if (self.five.isChecked()):
            checked.append("05")
        if (self.six.isChecked()):
            checked.append("06")
        if (self.seven.isChecked()):
            checked.append("07")
        if (self.eight.isChecked()):
            checked.append("08")
        if (self.nine.isChecked()):
            checked.append("09")
        if (self.ten.isChecked()):
            checked.append("10")
        if (self.eleven.isChecked()):
            checked.append("11")
        if (self.twelve.isChecked()):
            checked.append("12")
        if (self.thirteen.isChecked()):
            checked.append("13")
        if (self.fourteen.isChecked()):
            checked.append("14")
        if (self.fifteen.isChecked()):
            checked.append("15")
        if (self.sixteen.isChecked()):
            checked.append("16")
        if (self.seventeen.isChecked()):
            checked.append("17")
        if (self.eighteen.isChecked()):
            checked.append("18")
        if (self.nineteen.isChecked()):
            checked.append("19")
        if (self.twenty.isChecked()):
            checked.append("20")
        if (self.twentyone.isChecked()):
            checked.append("21")
        if (self.twentytwo.isChecked()):
            checked.append("22")
        if (self.twentythree.isChecked()):
            checked.append("23")
        if (self.twentyfour.isChecked()):
            checked.append("24")
        if (self.twentyfive.isChecked()):
            checked.append("25")
        if (self.twentysix.isChecked()):
            checked.append("26")
        if (self.twentyseven.isChecked()):
            checked.append("27")
        if (self.twentyeight.isChecked()):
            checked.append("28")
        if (self.twentynine.isChecked()):
            checked.append("29")
        if (self.thirty.isChecked()):
            checked.append("30")
        if (self.thirtyone.isChecked()):
            checked.append("31")
        if (self.thirtytwo.isChecked()):
            checked.append("32")
        if (self.thirtythree.isChecked()):
            checked.append("33")
        if (self.thirtyfour.isChecked()):
            checked.append("34")
        if (self.thirtyfive.isChecked()):
            checked.append("35")
        if (self.thirtysix.isChecked()):
            checked.append("36")
        if (self.thirtyseven.isChecked()):
            checked.append("37")
        if (self.thirtyeight.isChecked()):
            checked.append("38")
        if (self.thirtynine.isChecked()):
            checked.append("39")
        if (self.forty.isChecked()):
            checked.append("40")

        item_coords = {"01": [143, 108], "02": [143, 200], "03": [143, 292], "04": [143, 385], "05": [143, 477],
                       "06": [143, 569], "07": [143, 691], "08": [143, 776], "09": [143, 859], "10": [143, 947],
                       "11": [1064, 108], "12": [1064, 200], "13": [1064, 292], "14": [1064, 385], "15": [1064, 477],
                       "16": [1064, 569], "17": [1064, 662], "18": [1064, 754], "19": [1064, 846], "20": [1064, 938],
                       "21": [2064, 108], "22": [2064, 200], "23": [2064, 292], "24": [2064, 385], "25": [2064, 477],
                       "26": [2064, 569], "27": [2064, 662], "28": [2064, 754], "29": [2064, 846], "30": [2064, 938],
                       "31": [2984, 108], "32": [2984, 200], "33": [2984, 292], "34": [2984, 385], "35": [2984, 477],
                       "36": [2984, 569], "37": [2984, 691], "38": [2984, 776], "39": [2984, 859], "40": [2984, 947]}

        beer_odd = ["01", "03", "05", "11", "13", "15", "17", "19",
                    "21", "23", "25", "27", "29", "31", "33", "35"]
        beer_even = ["02", "04", "06", "12", "14", "16", "18", "20",
                     "22", "24", "26", "28", "30", "32", "34", "36"]
        punch_wine_odd = ["07", "09", "37", "39"]
        punch_wine_even = ["08", "10", "38", "40"]
        menu = Image.open("/Users/bestofluck/Desktop/MENU.jpg")
        item_template = None
        bolt = None
        interior_coords = {"name": (0, 0), "five_oz": (492, 0), "ten_oz": (597, 0), "sixteen_oz": (702, 0)}

        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history_gameover_numbers.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n')

            for each in checked:
                gameover = None
                if each in beer_odd:
                    gameover = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/gameover_lightblue.png")
                    item_template = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/item_templates/blank_lightblue.png")
                    bolt = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/bolt_lightblue.png")
                elif each in beer_even:
                    gameover = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/gameover_darkblue.png")
                    item_template = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/item_templates/blank_darkblue.png")
                    bolt = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/bolt_darkblue.png")
                elif each in punch_wine_even:
                    gameover = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/gameover_darkgray.png")
                    item_template = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/item_templates/blank_darkgray.png")
                    bolt = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/bolt_darkgray.png")
                elif each in punch_wine_odd:
                    gameover = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/gameover_lightgray.png")
                    item_template = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/item_templates/blank_lightgray.png")
                    bolt = Image.open("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/bolt_lightgray.png")

                item_template.paste(gameover, interior_coords["name"])
                item_template.paste(bolt, interior_coords["five_oz"])
                item_template.paste(bolt, interior_coords["ten_oz"])
                item_template.paste(bolt, interior_coords["sixteen_oz"])

                menu.paste(item_template, item_coords[each])
                writer.writerow([each])

        # Write "Game Over" to current items list
        for each in checked:
            game_over_update_file(each)

        # Backup current menu to /past_menus
        time = ctime()
        time = time.replace(" ", "_")
        time = time.replace(":", "-")
        dest = "/Users/bestofluck/DO_NOT_TOUCH/BOL/past_menus/" + time + ".jpg"
        copy2("/Users/bestofluck/DO_NOT_TOUCH/BOL/img/current_menu.jpg", dest)

        # Overwrite current menu
        menu.save("/Users/bestofluck/Desktop/MENU.jpg", "PNG")
        copy2("/Users/bestofluck/Desktop/MENU.jpg", "/Users/bestofluck/DO_NOT_TOUCH/BOL/current_menu_copy.jpg")

        # Update the website menu
        update_website_menu()

        self.confirmation.setText("<strong><font color='green'>Successfully updated.</font></strong>")


class HistoryTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("History of Added Items:")
        listwidget = QListWidget()

        history = []
        with open('/Users/bestofluck/DO_NOT_TOUCH/BOL/data/item_history.csv', 'r') as textfile:
             for row in reversed(list(csv.reader(textfile))):
                history.append(row[-1] + '\t' + row[1])

        for i in range(0, len(history)):
            string = str(history[i])
            listwidget.addItem(string)

        layout.addWidget(label)
        layout.addWidget(listwidget)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tabwidget = TabWidget()
    tabwidget.show()
    sys.exit(app.exec_())

