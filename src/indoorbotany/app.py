"""
Project for ECE196: IndoorBotany

Created By: Trevor Bonaiuto, Eric Hom, Melvin Perez, Yichen Yang
"""

#imports for Toga
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import random
import requests
from bs4 import BeautifulSoup
import mysql.connector as mysql
from functools import partial
import random

"""
TODO: 
-- ADD TUTORIALS FOR AT LEAST 3 DIFFERENT PLANTS INTO THE DATABASE
-- CHANGE THE PLANT DATA TUTORIAL REDIRECT BUTTON TO DISPLAY TUTORIAL FOR CORRECT PLANT
-- CREATE QUIZ VIEW & BUTTONS TO REDIRECT
-- CHANGE PROGRESSBARS TO GRAPHS IN PLANT DATA VIEW
-- STYLE EACH VIEW BETTER
"""


def get_info(plant):
    return random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)


def get_question():
    questions = []
    try:
        db = mysql.connect(host="sql9.freesqldatabase.com",
                           user="sql9622826",
                           password="hQNVN4TgY4",
                           database="sql9622826",
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

        #Create the main box
        self.main_box = toga.Box(
        style=Pack(direction=COLUMN)
        )

        #Create the main window to display content
        self.scroll_box = toga.ScrollContainer(
            style=Pack(direction=COLUMN, alignment="center")
        )
        self.show_intro();
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            position=(350, 0),
            size=(650, 500)
        )
        self.main_window.content = self.scroll_box
        self.main_window.show()



    #########################################################
    #                CREATE THE INTRO VIEW                  #
    #########################################################

    def show_intro(self, widget=None):

        #Create the main box for intro view
        self.main_box_intro = toga.Box(
        style=Pack(direction=COLUMN)
        )


        #Create the title content & box
        self.intro_title = toga.Label(
            text="Welcome to IndoorBotany!",
            style=Pack(font_size=36)
        )
        self.intro_title_box = toga.Box(
            style=Pack(direction=ROW, padding=20, alignment="center")
        )
        #Add the content into the box, and center it
        self.intro_title_box.add(toga.Label("", style=Pack(flex=1)))
        self.intro_title_box.add(self.intro_title)
        self.intro_title_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the subheading content & box
        self.intro_subheading = toga.Label(
            text="To get started, choose one of the follow two options:",
            style=Pack(font_size=18)
        )
        self.intro_subheading_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.intro_subheading_box.add(toga.Label("", style=Pack(flex=1)))
        self.intro_subheading_box.add(self.intro_subheading)
        self.intro_subheading_box.add(toga.Label("", style=Pack(flex=1)))
        

        #Create the button content & box
        self.intro_existing_button = toga.Button(
            text="View an existing plant profile!",
            style=Pack(padding_right=25),
            on_press=self.show_plant_data
        )
        self.intro_new_button = toga.Button(
            text="Create a new plant profile!",
            style=Pack(padding_left=25),
            on_press=self.show_plant_creation
        )
        self.intro_buttons_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.intro_buttons_box.add(toga.Label("", style=Pack(flex=1)))
        self.intro_buttons_box.add(self.intro_existing_button)
        self.intro_buttons_box.add(self.intro_new_button)
        self.intro_buttons_box.add(toga.Label("", style=Pack(flex=1)))


        #Add the separate boxes to the main box
        self.main_box_intro.add(self.intro_title_box)
        self.main_box_intro.add(self.intro_subheading_box)
        self.main_box_intro.add(self.intro_buttons_box)

        self.scroll_box.content = self.main_box_intro



    #########################################################
    #             CREATE THE PLANT DATA VIEW                #
    #########################################################

    def show_plant_data(self, widget):

        #Create the main box for plant data view
        self.main_box_plant_data = toga.Box(
        style=Pack(direction=COLUMN)
        )


        #Create the title content & box
        self.plant_view_title = toga.Label(
            text="Choose which plant you'd like to view from the selection below!",
            style=Pack(font_size=24)
        )
        self.plant_view_title_box = toga.Box(
            style=Pack(direction=ROW, padding=20, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_view_title_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_view_title_box.add(self.plant_view_title)
        self.plant_view_title_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the subheading content & box
        self.plant_view_subheading = toga.Label(
            text="Note: For accurate data, please place the device near the plant and insert the soil moisture sensor",
            style=Pack(font_size=15)
        )
        self.plant_view_subheading_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_view_subheading_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_view_subheading_box.add(self.plant_view_subheading)
        self.plant_view_subheading_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the plant selection content & box
        self.plant_view_label = toga.Label(
            text="Choose your plant:",
            style=Pack(padding=(10, 0), font_weight="bold")
        )
        self.plant_view_selection = toga.Selection(
            items=['Plant 1', 'Plant 2', 'Plant 3', 'Plant 4'],
            style=Pack(padding=10),
            on_select=self.update_data
        )
        self.plant_view_selection_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_view_selection_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_view_selection_box.add(self.plant_view_label)
        self.plant_view_selection_box.add(self.plant_view_selection)
        self.plant_view_selection_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the moisture sensor content & box
        self.moisture_sensor_label = toga.Label(
            text="Moisture: ",
            style=Pack(padding=(10, 10))
        )
        self.moisture_sensor_bar = toga.ProgressBar(
            max=100, 
            value=0,
            style=(Pack(padding=(10,10), flex=0))
        )
        self.moisture_sensor_bar.start()
        self.moisture_sensor_bar.value = 0
        self.moisture_sensor_bar.stop()
        self.moisture_sensor_box = toga.Box(
            style=Pack(direction=ROW, padding=20, alignment="center")
        )
        #Add the content into the box, and center it
        self.moisture_sensor_box.add(toga.Label("", style=Pack(flex=1)))
        self.moisture_sensor_box.add(self.moisture_sensor_label)
        self.moisture_sensor_box.add(self.moisture_sensor_bar)
        self.moisture_sensor_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the temp sensor content & box
        self.temp_sensor_label = toga.Label(
            text="Temperature: ",
            style=Pack(padding=(10, 10))
        )
        self.temp_sensor_bar = toga.ProgressBar(
            max=100, 
            value=0,
            style=(Pack(padding=(10, 10), flex=0))
        )
        self.temp_sensor_bar.start()
        self.temp_sensor_bar.value = 0
        self.temp_sensor_bar.stop()
        self.temp_sensor_box = toga.Box(
            style=Pack(direction=ROW, padding=20, alignment="center")
        )
        #Add the content into the box, and center it
        self.temp_sensor_box.add(toga.Label("", style=Pack(flex=1)))
        self.temp_sensor_box.add(self.temp_sensor_label)
        self.temp_sensor_box.add(self.temp_sensor_bar)
        self.temp_sensor_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the humidity sensor content & box
        self.humidity_sensor_label = toga.Label(
            text="Humidity: ",
            style=Pack(padding=(10, 10))
        )
        self.humidity_sensor_bar = toga.ProgressBar(
            max=100, 
            value=0,
            style=(Pack(padding=(10, 10), flex=0))
        )
        self.humidity_sensor_bar.start()
        self.humidity_sensor_bar.value = 0
        self.humidity_sensor_bar.stop()
        self.humidity_sensor_box = toga.Box(
            style=Pack(direction=ROW, padding=20, alignment="center")
        )
        #Add the content into the box, and center it
        self.humidity_sensor_box.add(toga.Label("", style=Pack(flex=1)))
        self.humidity_sensor_box.add(self.humidity_sensor_label)
        self.humidity_sensor_box.add(self.humidity_sensor_bar)
        self.humidity_sensor_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the light sensor content & box
        self.light_sensor_label = toga.Label(
            text="Sunlight: ",
            style=Pack(padding=(10, 10))
        )
        self.light_sensor_bar = toga.ProgressBar(
            max=100, 
            value=0,
            style=(Pack(padding=(10, 10), flex=0))
        )
        self.light_sensor_bar.start()
        self.light_sensor_bar.value = 0
        self.light_sensor_bar.stop()
        self.light_sensor_box = toga.Box(
            style=Pack(direction=ROW, padding=20, alignment="center")
        )
        #Add the content into the box, and center it
        self.light_sensor_box.add(toga.Label("", style=Pack(flex=1)))
        self.light_sensor_box.add(self.light_sensor_label)
        self.light_sensor_box.add(self.light_sensor_bar)
        self.light_sensor_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the plant tutorial button content & box
        self.plant_data_tutorial_button = toga.Button(
            text="Review the tutorial!",
            style=Pack(padding=10),
            on_press=self.show_tutorial
        )
        self.plant_data_tutorial_button_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_data_tutorial_button_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_data_tutorial_button_box.add(self.plant_data_tutorial_button)
        self.plant_data_tutorial_button_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the back button content & box
        self.back_button_1 = toga.Button(
            text="<-- Go Back",
            style=Pack(padding_right=25),
            on_press=self.show_intro
        )
        self.back_button_box_1 = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.back_button_box_1.add(toga.Label("", style=Pack(flex=1)))
        self.back_button_box_1.add(self.back_button_1)
        self.back_button_box_1.add(toga.Label("", style=Pack(flex=1)))


        #Add the separate boxes to the main box
        self.main_box_plant_data.add(self.plant_view_title_box)
        self.main_box_plant_data.add(self.plant_view_subheading_box)
        self.main_box_plant_data.add(self.plant_view_selection_box)
        self.main_box_plant_data.add(self.moisture_sensor_box)
        self.main_box_plant_data.add(self.temp_sensor_box)
        self.main_box_plant_data.add(self.humidity_sensor_box)
        self.main_box_plant_data.add(self.light_sensor_box)
        self.main_box_plant_data.add(self.plant_data_tutorial_button_box)
        self.main_box_plant_data.add(self.back_button_box_1)

        self.scroll_box.content = self.main_box_plant_data



    #########################################################
    #            CREATE THE PLANT CREATION VIEW             #
    #########################################################

    def show_plant_creation(self, widget):

        #Create the main box for plant creation view
        self.main_box_plant_creation = toga.Box(
            style=Pack(direction=COLUMN)
        )


        #Create the title content & box
        self.plant_creation_title = toga.Label(
            text="Create your new plant below!",
            style=Pack(font_size=24)
        )
        self.plant_creation_title_box = toga.Box(
            style=Pack(direction=ROW, padding=20, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_creation_title_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_creation_title_box.add(self.plant_creation_title)
        self.plant_creation_title_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the new plant selection content & box
        self.plant_creation_label = toga.Label(
            text="Select the type of plant:",
            style=Pack(padding=(10, 0), font_weight="bold")
        )
        self.plant_creation_selection = toga.Selection(
            items=['Cactus','Snake plant','Succulent','Pothos','Peace Lily','Spider plant','ZZ plant'],
            style=Pack(padding=10)
            #on_select=self.
        )
        self.plant_creation_selection_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_creation_selection_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_creation_selection_box.add(self.plant_creation_label)
        self.plant_creation_selection_box.add(self.plant_creation_selection)
        self.plant_creation_selection_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the new plant name content & box
        self.plant_creation_name_label = toga.Label(
            text="Choose a name for your new plant:",
            style=Pack(padding=(10, 0), font_weight="bold")
        )
        self.plant_creation_name = toga.TextInput(
            placeholder="Enter name...",
            style=Pack(padding=10, width=175)
            #on_select=self.
        )
        self.plant_creation_name_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_creation_name_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_creation_name_box.add(self.plant_creation_name_label)
        self.plant_creation_name_box.add(self.plant_creation_name)
        self.plant_creation_name_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the submit button content & box
        self.plant_creation_submit_button = toga.Button(
            text="Submit!",
            on_press=self.show_tutorial
        )
        self.plant_creation_submit_button_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_creation_submit_button_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_creation_submit_button_box.add(self.plant_creation_submit_button)
        self.plant_creation_submit_button_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the back button content & box
        self.back_button_2 = toga.Button(
            text="<-- Go Back",
            style=Pack(padding=10),
            on_press=self.show_intro
        )
        self.back_button_box_2 = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.back_button_box_2.add(toga.Label("", style=Pack(flex=1)))
        self.back_button_box_2.add(self.back_button_2)
        self.back_button_box_2.add(toga.Label("", style=Pack(flex=1)))


        #Add the separate boxes to the main box
        self.main_box_plant_creation.add(self.plant_creation_title_box)
        self.main_box_plant_creation.add(self.plant_creation_selection_box)
        self.main_box_plant_creation.add(self.plant_creation_name_box)
        self.main_box_plant_creation.add(self.plant_creation_submit_button_box)
        self.main_box_plant_creation.add(self.back_button_box_2)

        self.scroll_box.content = self.main_box_plant_creation



    #########################################################
    #             CREATE THE PLANT TUTORIAL VIEW            #
    #########################################################

    def show_tutorial(self, widget):
        
        #Create the main box for the tutorial content
        self.main_box_plant_tutorial = toga.Box(
            style=Pack(direction=COLUMN)
        )


        #Create the title content & box
        self.plant_tutorial_title = toga.Label(
            text="You've successfully created your new " + str(self.plant_creation_selection.value).lower() + " plant!",
            style=Pack(font_size=24)
        )
        self.plant_tutorial_title_box = toga.Box(
            style=Pack(direction=ROW, padding=20, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_title_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_title_box.add(self.plant_tutorial_title)
        self.plant_tutorial_title_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the subheading content & box
        self.plant_tutorial_subheading = toga.Label(
            text="Please follow the tutorial below to learn more about your " + str(self.plant_creation_selection.value).lower() + "!",
            style=Pack(font_size=15)
        )
        self.plant_tutorial_subheading_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_subheading_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_subheading_box.add(self.plant_tutorial_subheading)
        self.plant_tutorial_subheading_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the quiz button content & box
        self.plant_tutorial_quiz_button = toga.Button(
            text="Take the quiz!",
            style=Pack(padding=10),
            on_press=self.show_quiz
        )
        self.plant_tutorial_quiz_button_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_quiz_button_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_quiz_button_box.add(self.plant_tutorial_quiz_button)
        self.plant_tutorial_quiz_button_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the plant data button content & box
        self.plant_tutorial_submit_button = toga.Button(
            text="Start tracking!",
            style=Pack(padding=10),
            on_press=self.show_plant_data
        )
        self.plant_tutorial_submit_button_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_submit_button_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_submit_button_box.add(self.plant_tutorial_submit_button)
        self.plant_tutorial_submit_button_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the back button content & box
        self.back_button_3 = toga.Button(
            text="<-- Go Back",
            style=Pack(padding=10),
            on_press=self.show_plant_creation
        )
        self.back_button_box_3 = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.back_button_box_3.add(toga.Label("", style=Pack(flex=1)))
        self.back_button_box_3.add(self.back_button_3)
        self.back_button_box_3.add(toga.Label("", style=Pack(flex=1)))


        #Add the separate boxes to the main box
        self.main_box_plant_tutorial.add(self.plant_tutorial_title_box)
        self.main_box_plant_tutorial.add(self.plant_tutorial_subheading_box)
        self.main_box_plant_tutorial.add(self.plant_tutorial_quiz_button_box)
        self.main_box_plant_tutorial.add(self.plant_tutorial_submit_button_box)
        self.main_box_plant_tutorial.add(self.back_button_box_3)

        self.scroll_box.content = self.main_box_plant_tutorial



    #########################################################
    #              CREATE THE PLANT QUIZ VIEW               #
    #########################################################

    def show_quiz(self, widget):

        #Create the main box for the tutorial content
        self.main_box_plant_quiz = toga.Box(
            style=Pack(direction=COLUMN)
        )


        #Create the title content & box
        self.plant_quiz_title = toga.Label(
            text="Test your knowledge!",
            style=Pack(font_size=24)
        )
        self.plant_quiz_title_box = toga.Box(
            style=Pack(direction=ROW, padding=20, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_title_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_title_box.add(self.plant_quiz_title)
        self.plant_quiz_title_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the subheading content & box
        self.plant_quiz_subheading = toga.Label(
            text="Take the following quiz on the " + str(self.plant_creation_selection.value).lower() + " to test your knowledge",
            style=Pack(font_size=15)
        )
        self.plant_quiz_subheading_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_subheading_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_subheading_box.add(self.plant_quiz_subheading)
        self.plant_quiz_subheading_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the back button content & box
        self.back_button_4 = toga.Button(
            text="<-- Go Back",
            style=Pack(padding=10),
            on_press=self.show_tutorial
        )
        self.back_button_box_4 = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.back_button_box_4.add(toga.Label("", style=Pack(flex=1)))
        self.back_button_box_4.add(self.back_button_4)
        self.back_button_box_4.add(toga.Label("", style=Pack(flex=1)))


        #Add the separate boxes to the main box
        self.main_box_plant_quiz.add(self.plant_quiz_title_box)
        self.main_box_plant_quiz.add(self.plant_quiz_subheading_box)
        self.main_box_plant_quiz.add(self.back_button_box_4)

        self.scroll_box.content = self.main_box_plant_quiz









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



    #########################################################
    #     UPDATE PLANT DATA VIEW BASED ON PLANT PROFILE     #
    #########################################################

    def update_data(self, widget):

        #CHANGE THE DATA SHOWN BASED ON PLANT CHOSEN
        moisture, temp, humidity, light = get_info(self.plant_view_selection.value)
        print(moisture, temp)

        self.moisture_sensor_bar.value = 0
        self.moisture_sensor_bar.start()
        self.moisture_sensor_bar.value = moisture
        self.moisture_sensor_bar.stop()

        self.temp_sensor_bar.value = 0
        self.temp_sensor_bar.start()
        self.temp_sensor_bar.value = temp
        self.temp_sensor_bar.stop()

        self.humidity_sensor_bar.value = 0
        self.humidity_sensor_bar.start()
        self.humidity_sensor_bar.value = humidity
        self.humidity_sensor_bar.stop()

        self.light_sensor_bar.value = 0
        self.light_sensor_bar.start()
        self.light_sensor_bar.value = light
        self.light_sensor_bar.stop()




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



def main():
    return IndoorBotany()


    """
        self.plant_img = toga.Image('resources/indoorbotany.png')
        self.plant_img2 = toga.Image('resources/indoorbotany_2.png')

        self.imgview = toga.ImageView(self.plant_img, style=Pack(padding=10, padding_top=20))
        self.imgview.style.update(height=256)

        self.web = toga.WebView(url='https://google.com', style=Pack(flex=1, padding=10))



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
    """
