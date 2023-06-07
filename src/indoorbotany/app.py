"""
Project for ECE196: IndoorBotany

Created By: Trevor Bonaiuto, Eric Hom, Melvin Perez, Yichen Yang
"""

#imports for Toga
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

#import database query helpers
import dbutils

import random
import requests
from bs4 import BeautifulSoup
import mysql.connector as mysql
from functools import partial
import random

"""
TODO:
-- CHANGE THE PLANT DATA TUTORIAL REDIRECT BUTTON TO DISPLAY TUTORIAL FOR CORRECT PLANT
-- CREATE QUIZ VIEW & BUTTONS TO REDIRECT
-- CHANGE PROGRESSBARS TO GRAPHS IN PLANT DATA VIEW
-- STYLE EACH VIEW BETTER
"""


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
            position=(320, 0),
            size=(850, 650)
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

        #Call the database query to grab the plant profiles for selection
        profiles = dbutils.grab_plant_profiles()
        list_profiles = []
        for i in profiles:
            list_profiles.append(i[0])


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
            items=list_profiles,
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


        #Add refresh button to update the plant data
        self.refresh_button = toga.Button(
            text="Refresh Data",
            on_press=self.update_data
        )
        self.refresh_button_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.refresh_button_box.add(toga.Label("", style=Pack(flex=1)))
        self.refresh_button_box.add(self.refresh_button)
        self.refresh_button_box.add(toga.Label("", style=Pack(flex=1)))



        self.moisture_sensor_bar = toga.ProgressBar(
            max=4095, 
            value=0,
            style=(Pack(flex=0, width=350))
        )
        self.moisture_sensor_bar.start()
        self.moisture_sensor_bar.value = 0
        self.moisture_sensor_bar.stop()
        self.moisture_sensor_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.moisture_sensor_box.add(toga.Label("", style=Pack(flex=1)))
        self.moisture_sensor_box.add(self.moisture_sensor_bar)
        self.moisture_sensor_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the moisture sensor content & box
        self.moisture_sensor_label = toga.Label(
            text=("Moisture: " + str(self.moisture_sensor_bar.value))
        )
        self.moisture_sensor_label_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.moisture_sensor_label_box.add(toga.Label("", style=Pack(flex=1)))
        self.moisture_sensor_label_box.add(self.moisture_sensor_label)
        self.moisture_sensor_label_box.add(toga.Label("", style=Pack(flex=1)))



        self.temp_sensor_bar = toga.ProgressBar(
            max=40, 
            value=0,
            style=(Pack(flex=0, width=350))
        )
        self.temp_sensor_bar.start()
        self.temp_sensor_bar.value = 0
        self.temp_sensor_bar.stop()
        self.temp_sensor_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.temp_sensor_box.add(toga.Label("", style=Pack(flex=1)))
        self.temp_sensor_box.add(self.temp_sensor_bar)
        self.temp_sensor_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the temp sensor content & box
        self.temp_sensor_label = toga.Label(
            text=("Temperature: " + str(self.temp_sensor_bar.value) + " Celsius")
        )
        self.temp_sensor_label_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.temp_sensor_label_box.add(toga.Label("", style=Pack(flex=1)))
        self.temp_sensor_label_box.add(self.temp_sensor_label)
        self.temp_sensor_label_box.add(toga.Label("", style=Pack(flex=1)))


        self.humidity_sensor_bar = toga.ProgressBar(
            max=100, 
            value=0,
            style=(Pack(flex=0, width=350))
        )
        self.humidity_sensor_bar.start()
        self.humidity_sensor_bar.value = 0
        self.humidity_sensor_bar.stop()
        self.humidity_sensor_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.humidity_sensor_box.add(toga.Label("", style=Pack(flex=1)))
        self.humidity_sensor_box.add(self.humidity_sensor_bar)
        self.humidity_sensor_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the humidity sensor content & box
        self.humidity_sensor_label = toga.Label(
            text=("Humidity: " + str(self.humidity_sensor_bar.value) + "%")
        )
        self.humidity_sensor_label_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.humidity_sensor_label_box.add(toga.Label("", style=Pack(flex=1)))
        self.humidity_sensor_label_box.add(self.humidity_sensor_label)
        self.humidity_sensor_label_box.add(toga.Label("", style=Pack(flex=1)))


        self.light_sensor_bar = toga.ProgressBar(
            max=25000, 
            value=0,
            style=(Pack(flex=0, width=350))
        )
        self.light_sensor_bar.start()
        self.light_sensor_bar.value = 0
        self.light_sensor_bar.stop()
        self.light_sensor_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.light_sensor_box.add(toga.Label("", style=Pack(flex=1)))
        self.light_sensor_box.add(self.light_sensor_bar)
        self.light_sensor_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the light sensor content & box
        self.light_sensor_label = toga.Label(
            text=("Sunlight: " + str(self.light_sensor_bar.value))
        )
        self.light_sensor_label_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.light_sensor_label_box.add(toga.Label("", style=Pack(flex=1)))
        self.light_sensor_label_box.add(self.light_sensor_label)
        self.light_sensor_label_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the quiz button content & box
        self.plant_view_quiz_button = toga.Button(
            text="Take the quiz!",
            style=Pack(padding=10),
            on_press=self.show_quiz
        )
        self.plant_view_quiz_button_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_view_quiz_button_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_view_quiz_button_box.add(self.plant_view_quiz_button)
        self.plant_view_quiz_button_box.add(toga.Label("", style=Pack(flex=1)))


        #Add the different images to show plant health based on data
        self.image_thriving_plant = toga.Image('resources/thriving_plant.png')
        self.image_healthy_plant = toga.Image('resources/healthy_plant.png')
        self.image_dying_plant = toga.Image('resources/dying_plant.png')

        self.image_view_plant_health = toga.ImageView(
            image=self.image_thriving_plant,
            style=Pack(padding=10, height=225)
        )



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
        self.main_box_plant_data.add(self.refresh_button_box)
        self.main_box_plant_data.add(self.moisture_sensor_label_box)
        self.main_box_plant_data.add(self.moisture_sensor_box)
        self.main_box_plant_data.add(self.temp_sensor_label_box)
        self.main_box_plant_data.add(self.temp_sensor_box)
        self.main_box_plant_data.add(self.humidity_sensor_label_box)
        self.main_box_plant_data.add(self.humidity_sensor_box)
        self.main_box_plant_data.add(self.light_sensor_label_box)
        self.main_box_plant_data.add(self.light_sensor_box)
        self.main_box_plant_data.add(self.plant_view_quiz_button_box)
        self.main_box_plant_data.add(self.image_view_plant_health)
        self.main_box_plant_data.add(self.back_button_box_1)

        self.scroll_box.content = self.main_box_plant_data



    #########################################################
    #            CREATE THE PLANT CREATION VIEW             #
    #########################################################

    def show_plant_creation(self, widget):


        #Call the database query to grab the different plants to choose from
        plants = dbutils.grab_plants()
        list_plants= []
        for i in plants:
            list_plants.append(i[0])


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
            items=list_plants,
            style=Pack(padding=10)
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
        

        #Create the images
        self.flf_image = toga.Image('resources/flf_plant.jpg')
        self.snakeplant_image = toga.Image('resources/snakeplant.jpg')
        self.spiderplant_image = toga.Image('resources/spiderplant.jpg')
        self.plant_image_view = toga.ImageView(
            style=Pack(padding=10, height=225)
        )

        if self.plant_creation_selection.value == 'Fiddle Leaf Fig':
            self.plant_image_view.image = self.flf_image
        if self.plant_creation_selection.value == 'Snake Plant':
            self.plant_image_view.image = self.snakeplant_image
        if self.plant_creation_selection.value == 'Spider Plant':
            self.plant_image_view.image = self.spiderplant_image

        self.watering_image_view = toga.ImageView(
            image='resources/watering_plant.jpg',
            style=Pack(padding=10, height=225)
        )
        self.sunlight_image_view = toga.ImageView(
            image='resources/sunlight_plant.jpg',
            style=Pack(padding=10, height=225)
        )

        #Call the SQL query to create a new plant profile
        dbutils.create_plant_profile(self.plant_creation_name.value, self.plant_creation_selection.value)

        #Call the SQL query to show the correct tutorial based on the chosen plant
        tutorial_content = dbutils.grab_plant_tutorial(self.plant_creation_selection.value)


        #Create the main box for the tutorial content
        self.main_box_plant_tutorial = toga.Box(
            style=Pack(direction=COLUMN)
        )


        #Create the title content & box
        self.plant_tutorial_title = toga.Label(
            text="You've successfully created your new " + str(self.plant_creation_selection.value).lower() + "!",
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



        #Create the tutorial content content & boxes
        self.plant_tutorial_general_info_header = toga.Label(
            text="General Info",
            style=Pack(font_size=15)
        )
        self.plant_tutorial_general_info_header_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_general_info_header_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_general_info_header_box.add(self.plant_tutorial_general_info_header)
        self.plant_tutorial_general_info_header_box.add(toga.Label("", style=Pack(flex=1)))

        self.plant_tutorial_general_info = toga.Label(
            text=tutorial_content[0][0],
            style=Pack(font_size=12)
        )
        self.plant_tutorial_general_info_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_general_info_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_general_info_box.add(self.plant_tutorial_general_info)
        self.plant_tutorial_general_info_box.add(toga.Label("", style=Pack(flex=1)))

        self.plant_tutorial_watering_header = toga.Label(
            text="Watering",
            style=Pack(font_size=15)
        )
        self.plant_tutorial_watering_header_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_watering_header_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_watering_header_box.add(self.plant_tutorial_watering_header)
        self.plant_tutorial_watering_header_box.add(toga.Label("", style=Pack(flex=1)))

        self.plant_tutorial_watering = toga.Label(
            text=tutorial_content[0][1],
            style=Pack(font_size=12)
        )
        self.plant_tutorial_watering_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_watering_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_watering_box.add(self.plant_tutorial_watering)
        self.plant_tutorial_watering_box.add(toga.Label("", style=Pack(flex=1)))

        self.plant_tutorial_sunlight_header = toga.Label(
            text="Sunlight",
            style=Pack(font_size=15)
        )
        self.plant_tutorial_sunlight_header_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_sunlight_header_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_sunlight_header_box.add(self.plant_tutorial_sunlight_header)
        self.plant_tutorial_sunlight_header_box.add(toga.Label("", style=Pack(flex=1)))

        self.plant_tutorial_sunlight = toga.Label(
            text=tutorial_content[0][2],
            style=Pack(font_size=12)
        )
        self.plant_tutorial_sunlight_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_sunlight_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_sunlight_box.add(self.plant_tutorial_sunlight)
        self.plant_tutorial_sunlight_box.add(toga.Label("", style=Pack(flex=1)))

        self.plant_tutorial_climate_header = toga.Label(
            text="Climate",
            style=Pack(font_size=15)
        )
        self.plant_tutorial_climate_header_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_climate_header_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_climate_header_box.add(self.plant_tutorial_climate_header)
        self.plant_tutorial_climate_header_box.add(toga.Label("", style=Pack(flex=1)))

        self.plant_tutorial_climate = toga.Label(
            text=tutorial_content[0][3],
            style=Pack(font_size=12)
        )
        self.plant_tutorial_climate_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_climate_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_climate_box.add(self.plant_tutorial_climate)
        self.plant_tutorial_climate_box.add(toga.Label("", style=Pack(flex=1)))

        self.plant_tutorial_summary_header = toga.Label(
            text="Summary",
            style=Pack(font_size=15)
        )
        self.plant_tutorial_summary_header_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_summary_header_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_summary_header_box.add(self.plant_tutorial_summary_header)
        self.plant_tutorial_summary_header_box.add(toga.Label("", style=Pack(flex=1)))

        self.plant_tutorial_summary = toga.Label(
            text=tutorial_content[0][4],
            style=Pack(font_size=12)
        )
        self.plant_tutorial_summary_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_tutorial_summary_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_tutorial_summary_box.add(self.plant_tutorial_summary)
        self.plant_tutorial_summary_box.add(toga.Label("", style=Pack(flex=1)))



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
        self.main_box_plant_tutorial.add(self.plant_tutorial_general_info_header_box)
        self.main_box_plant_tutorial.add(self.plant_image_view)
        self.main_box_plant_tutorial.add(self.plant_tutorial_general_info_box)
        self.main_box_plant_tutorial.add(self.plant_tutorial_watering_header_box)
        self.main_box_plant_tutorial.add(self.watering_image_view)
        self.main_box_plant_tutorial.add(self.plant_tutorial_watering_box)
        self.main_box_plant_tutorial.add(self.plant_tutorial_sunlight_header_box)
        self.main_box_plant_tutorial.add(self.sunlight_image_view)
        self.main_box_plant_tutorial.add(self.plant_tutorial_sunlight_box)
        self.main_box_plant_tutorial.add(self.plant_tutorial_climate_header_box)
        self.main_box_plant_tutorial.add(self.plant_tutorial_climate_box)
        self.main_box_plant_tutorial.add(self.plant_tutorial_summary_header_box)
        self.main_box_plant_tutorial.add(self.plant_tutorial_summary_box)
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


        plant_name = dbutils.grab_plant_from_profile_name(self.plant_view_selection.value)[0]
        #Create the subheading content & box
        self.plant_quiz_subheading = toga.Label(
            text="Take the following quiz on the " + plant_name.lower() + "!",
            style=Pack(font_size=15)
        )
        self.plant_quiz_subheading_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_subheading_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_subheading_box.add(self.plant_quiz_subheading)
        self.plant_quiz_subheading_box.add(toga.Label("", style=Pack(flex=1)))
        
        



        #Get the questions and answer choices for the quiz
        full_questions = dbutils.get_question(self.plant_view_selection.value)

        questions = []
        option1 = []
        option2 = []
        option3 = []
        self.choice = []
        self.questions_box = []
        self.option_box = []

        self.quiz_box = toga.Box(
            style=Pack(direction=COLUMN, padding=5, flex=1)
        )

        self.answers = [x[-2] for x in full_questions]
        self.user_ans = [''] * len(full_questions)

        for idx, question in enumerate(full_questions):
            questions.append(toga.Label(
                question[1],
                style=Pack(padding=0)
            )
            )
            option1.append(toga.Button(
                question[2],
                on_press=partial(self.change_answer, idx, question[2]),
                style=Pack(padding=5),
            )
            )
            option2.append(toga.Button(
                question[3],
                on_press=partial(self.change_answer, idx, question[3]),
                style=Pack(padding=5),
            )
            )
            option3.append(toga.Button(
                question[4],
                on_press=partial(self.change_answer, idx, question[4]),
                style=Pack(padding=5),
            )
            )
            self.choice.append(toga.Label(
                'Your answer: ',
                style=Pack(padding=5, padding_bottom=25),
            )
            )



        #Create the question content & box
        self.plant_quiz_question1 = toga.Label(
            text="Question 1: ",
            style=Pack(font_size=15)
        )
        self.plant_quiz_question1_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_question1_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_question1_box.add(self.plant_quiz_question1)
        self.plant_quiz_question1_box.add(questions[0])
        self.plant_quiz_question1_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the answer choices content & box
        self.plant_quiz_options1_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_options1_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_options1_box.add(option1[0])
        self.plant_quiz_options1_box.add(option2[0])
        self.plant_quiz_options1_box.add(option3[0])
        self.plant_quiz_options1_box.add(toga.Label("", style=Pack(flex=1)))

        
        #Create the answer selection content & box
        self.plant_quiz_choice1_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_choice1_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_choice1_box.add(self.choice[0])
        self.plant_quiz_choice1_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the question content & box
        self.plant_quiz_question2 = toga.Label(
            text="Question 2: ",
            style=Pack(font_size=15)
        )
        self.plant_quiz_question2_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_question2_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_question2_box.add(self.plant_quiz_question2)
        self.plant_quiz_question2_box.add(questions[1])
        self.plant_quiz_question2_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the answer choices content & box
        self.plant_quiz_options2_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_options2_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_options2_box.add(option1[1])
        self.plant_quiz_options2_box.add(option2[1])
        self.plant_quiz_options2_box.add(option3[1])
        self.plant_quiz_options2_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the answer selection content & box
        self.plant_quiz_choice2_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_choice2_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_choice2_box.add(self.choice[1])
        self.plant_quiz_choice2_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the question content & box
        self.plant_quiz_question3 = toga.Label(
            text="Question 3: ",
            style=Pack(font_size=15)
        )
        self.plant_quiz_question3_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_question3_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_question3_box.add(self.plant_quiz_question3)
        self.plant_quiz_question3_box.add(questions[2])
        self.plant_quiz_question3_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the answer choices content & box
        self.plant_quiz_options3_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_options3_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_options3_box.add(option1[2])
        self.plant_quiz_options3_box.add(option2[2])
        self.plant_quiz_options3_box.add(option3[2])
        self.plant_quiz_options3_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the answer selection content & box
        self.plant_quiz_options3_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_options3_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_options3_box.add(option1[2])
        self.plant_quiz_options3_box.add(option2[2])
        self.plant_quiz_options3_box.add(option3[2])
        self.plant_quiz_options3_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the answer selection content & box
        self.plant_quiz_choice3_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.plant_quiz_choice3_box.add(toga.Label("", style=Pack(flex=1)))
        self.plant_quiz_choice3_box.add(self.choice[2])
        self.plant_quiz_choice3_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the submit button
        self.return_button = toga.Button(
            text="Submit",
            on_press=self.return_main,
            style=Pack(padding=5, padding_top=20)
        )
        self.return_button_box = toga.Box(
            style=Pack(direction=ROW, padding=10, alignment="center")
        )
        #Add the content into the box, and center it
        self.return_button_box.add(toga.Label("", style=Pack(flex=1)))
        self.return_button_box.add(self.return_button)
        self.return_button_box.add(toga.Label("", style=Pack(flex=1)))


        #Create the back button content & box
        self.back_button_4 = toga.Button(
            text="<-- Go Back",
            style=Pack(padding=10),
            on_press=self.show_plant_data
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
        self.main_box_plant_quiz.add(self.plant_quiz_question1_box)
        self.main_box_plant_quiz.add(self.plant_quiz_options1_box)
        self.main_box_plant_quiz.add(self.plant_quiz_choice1_box)
        self.main_box_plant_quiz.add(self.plant_quiz_question2_box)
        self.main_box_plant_quiz.add(self.plant_quiz_options2_box)
        self.main_box_plant_quiz.add(self.plant_quiz_choice2_box)
        self.main_box_plant_quiz.add(self.plant_quiz_question3_box)
        self.main_box_plant_quiz.add(self.plant_quiz_options3_box)
        self.main_box_plant_quiz.add(self.plant_quiz_choice3_box)
        self.main_box_plant_quiz.add(self.return_button_box)
        self.main_box_plant_quiz.add(self.back_button_box_4)

        self.scroll_box.content = self.main_box_plant_quiz



    #########################################################
    #      UPDATE THE USERS ANSWER FOR A QUIZ QUESTION      #
    #########################################################
        
    def change_answer(self, id, value, widget=None):
        
        
        assert isinstance(id, int)
        self.choice[id].text = 'Your answer: {}'.format(value)
        self.user_ans[id] = value



    #########################################################
    #     UPDATE PLANT DATA VIEW BASED ON PLANT PROFILE     #
    #########################################################


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
        


    #########################################################
    #     UPDATE PLANT DATA VIEW BASED ON PLANT PROFILE     #
    #########################################################

    def update_data(self, widget):

        #Call the database query to grab the plant profiles & their data
        data = dbutils.grab_plant_data(self.plant_view_selection.value)
        moisture = data[0][1]
        temp = data[0][2]
        humidity = data[0][3]
        light = data[0][4]


        self.moisture_sensor_label.text = "Moisture: " + str(moisture)
        self.temp_sensor_label.text =  "Temperature: " + str(temp) + " Celsius"
        self.humidity_sensor_label.text =  "Humidity: " + str(humidity) + "%"
        self.light_sensor_label.text = "Sunlight: " + str(light)

        if light > 18000:
            self.image_view_plant_health.image = self.image_dying_plant
        elif light < 9000:
            self.image_view_plant_health.image = self.image_healthy_plant
        else:
            self.image_view_plant_health.image = self.image_thriving_plant
        yield 0.1


        #self.moisture_sensor_bar.value = 0
        self.moisture_sensor_bar.start()
        self.moisture_sensor_bar.value = moisture
        self.moisture_sensor_bar.stop()

        #self.temp_sensor_bar.value = 0
        self.temp_sensor_bar.start()
        self.temp_sensor_bar.value = temp
        self.temp_sensor_bar.stop()

        #self.humidity_sensor_bar.value = 0
        self.humidity_sensor_bar.start()
        self.humidity_sensor_bar.value = humidity
        self.humidity_sensor_bar.stop()

        #self.light_sensor_bar.value = 0
        self.light_sensor_bar.start()
        self.light_sensor_bar.value = light
        self.light_sensor_bar.stop()




def main():
    return IndoorBotany()
