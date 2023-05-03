"""
weather api
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pyowm import OWM
# import csv
from pathlib import Path


def f2c(f):
    assert isinstance(f, float)
    return round((f-32)/1.8, 1)


def get_weather(city, state='', country=''):
    assert isinstance(city, str)
    assert isinstance(state, str)
    owm = OWM('5ef03d7d9d895585fed49cd96a19c984').weather_manager()
    try:
        if state == '':
            if city == '':
                return 'Please enter a city name'
            else:
                if country == '':
                    weather = owm.weather_at_place('{}'.format(city)).weather
                    now_temp = f2c(float(weather.temperature('fahrenheit')['temp']))
                    return '{}, {}C'.format(str(weather.detailed_status), now_temp)
                else:
                    weather = owm.weather_at_place('{},{}'.format(city, country)).weather
                    now_temp = f2c(float(weather.temperature('fahrenheit')['temp']))
                    return '{}, {}C'.format(str(weather.detailed_status), now_temp)
        else:
            if city == '':
                return 'Please enter a city name'
            else:
                if country == '':
                    weather = owm.weather_at_place('{},{}, US'.format(city, state)).weather
                    now_temp = f2c(float(weather.temperature('fahrenheit')['temp']))
                    return '{}, {}C'.format(str(weather.detailed_status), now_temp)
                else:
                    weather = owm.weather_at_place('{},{},{}'.format(city, state, country)).weather
                    now_temp = f2c(float(weather.temperature('fahrenheit')['temp']))
                    return '{}, {}C'.format(str(weather.detailed_status), now_temp)
    except:
        return 'Wrong info :('

class Weatherapi(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.favorite_cities = []
        self.resources_folder = Path(__file__).joinpath("../resources").resolve()
        self.db_filepath = self.resources_folder.joinpath("fc.txt")
        with open(self.db_filepath, 'r') as fc:
            self.favorite_cities.extend(fc.read().split(','))

        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        city_label = toga.Label(
            "Enter city: ",
            style=Pack(padding=(0, 5))
        )
        self.city_input = toga.TextInput(style=Pack(flex=1))

        city_box = toga.Box(style=Pack(direction=ROW, padding=5))
        city_box.add(city_label)
        city_box.add(self.city_input)

        state_label = toga.Label(
            "Enter state: ",
            style=Pack(padding=(0, 5))
        )
        self.state_input = toga.TextInput(style=Pack(flex=1))

        state_box = toga.Box(style=Pack(direction=ROW, padding=5))
        state_box.add(state_label)
        state_box.add(self.state_input)

        country_label = toga.Label(
            "Enter country: ",
            style=Pack(padding=(0, 5))
        )
        self.country_input = toga.TextInput(style=Pack(flex=1))

        country_box = toga.Box(style=Pack(direction=ROW, padding=5))
        country_box.add(country_label)
        country_box.add(self.country_input)

        button = toga.Button(
            'Weather today',
            on_press=self.show_weather,
            style=Pack(padding=5)
        )

        img = toga.Image('resources/power.png')
        imgview = toga.ImageView(img, style=Pack(padding=5))
        imgview.style.update(height=256)

        add_button = toga.Button(
            'Add to my favorites',
            on_press=self.add_favorites,
            style=Pack(padding=5)
        )

        self.button2 = toga.Button(
            'Weather at the selected city',
            on_press=self.show_weather2,
            style=Pack(padding=5)
        )

        self.delete_button = toga.Button(
            'Delete in my favorites',
            on_press=self.delete_favorite,
            style=Pack(padding=5)
        )

        self.selection = toga.Selection(items=self.favorite_cities, style=Pack(padding=5, padding_right=50))

        self.main_box.add(city_box)
        self.main_box.add(state_box)
        self.main_box.add(country_box)
        self.main_box.add(button)
        self.main_box.add(add_button)
        self.main_box.add(imgview)
        self.main_box.add(self.selection)
        self.main_box.add(self.button2)
        self.main_box.add(self.delete_button)

        self.scroll = toga.ScrollContainer(content=self.main_box, horizontal=False)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.scroll
        self.main_window.show()

    def show_weather(self, widget):
        self.main_window.info_dialog(
            'Weather in {}, {}'.format(self.city_input.value, self.state_input.value, self.country_input.value),
            get_weather(self.city_input.value, self.state_input.value, self.country_input.value),
        )

    def show_weather2(self, widget):
        self.main_window.info_dialog(
            'Weather in {}'.format(self.selection.value),
            get_weather(self.selection.value),
        )

    def add_favorites(self, widget):
        if self.city_input.value:
            if self.city_input.value in self.favorite_cities:
                self.main_window.info_dialog(
                    'xD',
                    'Already in my favorites',
                )
            else:
                self.selection.items.append(self.city_input.value)
                with open(self.db_filepath, 'w') as fc:
                    # writer = csv.writer(fc)
                    # writer.writerow(self.favorite_cities)
                    for idx, i in enumerate(self.favorite_cities):
                        if idx != len(self.favorite_cities) - 1:
                            fc.write(i + ',')
                        else:
                            fc.write(i)

                self.main_box.remove(self.selection)
                self.main_box.remove(self.button2)
                self.main_box.remove(self.delete_button)

                self.selection = toga.Selection(items=self.favorite_cities, style=Pack(padding=5, padding_right=50))

                self.main_box.add(self.selection)
                self.main_box.add(self.button2)
                self.main_box.add(self.delete_button)

                self.main_window.info_dialog(
                    ':)',
                    'Successfully added to my favorites',
                )
                print(self.favorite_cities)
        else:
            self.main_window.info_dialog(
                ':(',
                'Please enter a city name',
            )

    def delete_favorite(self, widget):
        city_name = self.selection.value
        self.favorite_cities.remove(self.selection.value)
        with open(self.db_filepath, 'w') as fc:
            for idx, i in enumerate(self.favorite_cities):
                if idx != len(self.favorite_cities) - 1:
                    fc.write(i + ',')
                else:
                    fc.write(i)

        self.main_box.remove(self.selection)
        self.main_box.remove(self.button2)
        self.main_box.remove(self.delete_button)

        self.selection = toga.Selection(items=self.favorite_cities, style=Pack(padding=5))

        self.main_box.add(self.selection)
        self.main_box.add(self.button2)
        self.main_box.add(self.delete_button)

        self.main_window.info_dialog(
            ':)',
            'Deleted {}'.format(city_name),
        )

def main():
    return Weatherapi(icon='./resources/weatherapi.ico')
