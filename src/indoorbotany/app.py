"""
Project for ECE196
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import random
import requests
from bs4 import BeautifulSoup
import mysql.connector as mysql
from functools import partial
import random


def get_info(name):
    return random.randint(0, 100), random.randint(0, 100)


def get_question():
    questions = []
    try:
        db = mysql.connect(host="sql9.freemysqlhosting.net",
                           user="sql9614741",
                           password="gNXJLalcwM",
                           database="sql9614741",
                           port=3306)
        cursor = db.cursor()
        query = "SELECT COUNT(*) FROM quiz;"
        cursor.execute(query)
        total_row = cursor.fetchone()[0]
        random_list = random.sample(range(1, total_row+1), 3)
        query = "SELECT * FROM quiz WHERE id IN (" + ','.join(map(str, random_list)) + ")"
        cursor.execute(query)
        results = cursor.fetchall()
        for i in results:
            questions.append(i)
        cursor.close()
        db.close()
    except:
        raise ConnectionError('Cannot connect to the database')
    return questions


class IndoorBotany(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        self.plant_selection = toga.Selection(items=['Plant 1', 'Plant 2', 'Plant 3', 'Plant 4'],
                                              on_select=self.show_info,
                                              style=Pack(padding=10, padding_right=300))

        self.plant_type = toga.Selection(items=['Cactus',
                                                'Snake plants',
                                                'Succulents',
                                                'Pothos',
                                                'Peace lilies',
                                                'Spider plants',
                                                'ZZ plants'],
                                         style=Pack(padding=10))

        self.plant_button = toga.Button(
            'Set up your plant!',
            on_press=self.setup_plant,
            style=Pack(padding=10, padding_right=200),
        )

        self.p_box = toga.Box(style=Pack(direction=ROW),
                              children=[self.plant_type, self.plant_button])

        self.m_label = toga.Label(
            "Moisture level: ",
            style=Pack(padding=(5, 5), padding_right=20, padding_top=10)
        )
        self.moisture_bar = toga.ProgressBar(max=100, value=0,
                                             style=(Pack(flex=1, padding_right=100, padding_left=20)))
        self.moisture_bar.start()
        self.moisture_bar.value = 50
        self.moisture_bar.stop()

        self.t_label = toga.Label(
            "Temperature: ",
            style=Pack(padding=(5, 5), padding_right=20, padding_top=20)
        )
        self.temp = toga.Label(
            "30C ",
            style=Pack(padding=(5, 5), padding_right=20)
        )
        self.temperature_bar = toga.ProgressBar(max=100, value=0,
                                                style=(Pack(flex=1, padding_right=100, padding_left=20)))
        self.temperature_bar.start()
        self.temperature_bar.value = 80
        self.temperature_bar.stop()

        self.plant_img = toga.Image('resources/indoorbotany.png')
        self.plant_img2 = toga.Image('resources/indoorbotany_2.png')

        self.imgview = toga.ImageView(self.plant_img, style=Pack(padding=10, padding_top=20))
        self.imgview.style.update(height=256)

        self.web = toga.WebView(url='https://google.com', style=Pack(flex=1, padding=10))

        self.quiz_button = toga.Button(
            'Take a quiz!',
            on_press=self.take_quiz,
            style=Pack(padding=5, padding_left=100, padding_right=100),
        )

        self.main_box.add(self.plant_selection)
        self.main_box.add(self.p_box)
        self.main_box.add(self.m_label)
        self.main_box.add(self.moisture_bar)
        self.main_box.add(self.t_label)
        self.main_box.add(self.temp)
        self.main_box.add(self.temperature_bar)
        self.main_box.add(self.imgview)
        self.main_box.add(self.quiz_button)
        self.main_box.add(self.web)

        self.scroll_box = toga.ScrollContainer(content=self.main_box,
                                               style=Pack(flex=1))
        self.main_window = toga.MainWindow(title=self.formal_name,
                                           size=(640, 800))
        self.main_window.content = self.scroll_box
        self.main_window.show()

    def show_info(self, widget):
        mois, temp = get_info(self.plant_selection.value)
        print(mois, temp)

        self.moisture_bar.value = 0
        self.moisture_bar.start()
        self.moisture_bar.value = mois
        self.moisture_bar.stop()

        self.temperature_bar.value = 0
        self.temperature_bar.start()
        self.temperature_bar.value = temp
        self.temperature_bar.stop()

        self.main_box.remove(self.imgview)
        self.main_box.remove(self.quiz_button)
        self.main_box.remove(self.web)

        if mois < 50 and temp > 50:
            self.imgview = toga.ImageView(self.plant_img2, style=Pack(padding=10, padding_top=20))
            self.imgview.style.update(height=256)
        else:
            self.imgview = toga.ImageView(self.plant_img, style=Pack(padding=10, padding_top=20))
            self.imgview.style.update(height=256)

        self.main_box.add(self.imgview)
        self.main_box.add(self.quiz_button)
        self.main_box.add(self.web)

        self.scroll_box.content = self.main_box
        self.main_window.content = self.scroll_box

    def take_quiz(self, widget):
        questions = get_question()
        q, option1, option2, option3, self.choice, self.q_box = [], [], [], [], [], []
        self.quiz_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        self.answers = [x[-1] for x in questions]
        self.user_ans = [''] * len(questions)
        # print(self.answers, self.user_ans)

        for idx, question in enumerate(questions):
            q.append(toga.Label(
                question[1],
                style=Pack(padding=(5, 5), padding_top=20)
            )
            )
            option1.append(toga.Button(
                question[2],
                on_press=partial(self.change_answer, idx, 'A'),
                style=Pack(padding=5),
            )
            )
            option2.append(toga.Button(
                question[3],
                on_press=partial(self.change_answer, idx, 'B'),
                style=Pack(padding=5),
            )
            )
            option3.append(toga.Button(
                question[4],
                on_press=partial(self.change_answer, idx, 'C'),
                style=Pack(padding=5),
            )
            )
            self.choice.append(toga.Label(
                'Your answer: ',
                style=Pack(padding=5),
            )
            )
            self.q_box.append(toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1),
                                       children=[q[-1], option1[-1], option2[-1], option3[-1], self.choice[-1]]))

        return_button = toga.Button(
            'Submit',
            on_press=self.return_main,
            style=Pack(padding=5, padding_top=20)
        )

        for item in self.q_box:
            self.quiz_box.add(item)
        self.quiz_box.add(return_button)
        self.quiz_scroll_box = toga.ScrollContainer(content=self.quiz_box)
        self.main_window.content = self.quiz_scroll_box
        # self.main_window.content = self.quiz_box

    def change_answer(self, id, value, widget=None):
        assert isinstance(id, int)
        # print(id, type(self.choice), bool(self.choice))
        # for idx, i in enumerate(self.choice):
        #     print(idx, i.text)
        self.choice[id].text = 'Your answer: {}'.format(value)
        self.user_ans[id] = value
        # print(self.user_ans)
        self.main_window.content = self.quiz_scroll_box

    def return_main(self, widget):
        cnt = 0
        for x, y in zip(self.answers, self.user_ans):
            if x == y:
                cnt += 1
        if cnt > 1:
            self.main_window.info_dialog(
                ':)',
                'You got {}/3 correct'.format(int(cnt)),
            )
        else:
            self.main_window.info_dialog(
                ':(',
                'You got {}/3 correct'.format(int(cnt)),
            )
        self.main_window.content = self.scroll_box

    def setup_plant(self, widget):
        pass


def main():
    return IndoorBotany()
