import json
from datetime import datetime
import os   # For saving the username and password
import openai   # For the AI
from kivy.animation import Animation    
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.uix.card import Card
from kivymd.app import MDApp
from kivy.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton

openai.api_key = "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"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username_input = MDTextField(hint_text="Enter your username", size_hint=(.8, None), height=50)
        self.password_input = MDTextField(hint_text="Enter your password", size_hint=(.8, None), height=50, password=True)
        self.login_button = MDRaisedButton(text="Log in", size_hint=(.8, None), height=50)
        self.login_button.bind(on_release=self.login_submit)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.login_button)
        self.add_widget(layout)

    def login_submit(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        with open("users.json", "r") as f:
            users = json.load(f)
        if username in users and users[username]['password'] == password:
            user_info = {"username": username, "last_login": datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
            app = MDApp.get_running_app()
            app.user_info = user_info
            app.home_screen.update_info()
            app.switch_screen('home', direction='left')
            with open("user_info.json", "r") as f:  # Save the username and password in user_info.json
                json.dump(user_info, f)
        else:
            Snackbar(text="Invalid username or password").open()
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username_label = Label(text="", size_hint=(.8, None), height=50)
        self.last_login_label = Label(text="", size_hint=(.8, None), height=50)
        self.logout_button = MDRaisedButton(text="Logout", size_hint=(.8, None), height=50)
        self.logout_button.bind(on_release=self.logout_submit)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.username_label)
        layout.add_widget(self.last_login_label)
        layout.add_widget(self.logout_button)
        self.add_widget(layout)

    def update_info(self):
        app = MDApp.get_running_app()
        self.username_label.text = "Username: " + app.user_info["username"]
        self.last_login_label.text = "Last login: " + app.user_info["last_login"]

    def logout_submit(self, instance):
        app = MDApp.get_running_app()
        app.user_info = {}
        app.switch_screen('login', direction='right')


class HomeScreen(Screen):
    def __init__(self, user_info, **kwargs):
        super().__init__(**kwargs)
        self.user_info = user_info

        card = MDCard(
            padding=20,
            size_hint=(.8, .6),
            pos_hint={'center_x': .5, 'center_y': .5},
            orientation="vertical"
        )

        box_layout = BoxLayout(orientation='vertical')
        label = Label(
            text="SystemEnhance™ | Make your work easier and faster with SystemEnhance™",
            halign="center",
            font_size='20sp',
            size_hint_y=None,
            height=50,
        )

        box_layout.add_widget(label)

        profile_button = Button(
            text="View Profile",
            size_hint=(.8, None),
            height=50
        )
        profile_button.bind(on_release=lambda x: self.switch_screen('profile'))
        box_layout.add_widget(profile_button)

        info_button = Button(
            text="Info",
            size_hint=(.8, None),
            height=50
        )
        info_button.bind(on_release=lambda x: self.switch_screen('info'))
        box_layout.add_widget(info_button)

        search_button = Button(
            text="Search",
            size_hint=(.8, None),
            height=50
        )
        search_button.bind(on_release=lambda x: self.switch_screen('search'))
        box_layout.add_widget(search_button)

        card.add_widget(box_layout)
        self.add_widget(card)

class ProfileScreen(Screen):
    user_info = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.user_info_data = kwargs.get('user_info', {})
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        title_label = Label(
            text="User Profile",
            font_size='30sp',
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(title_label)

        name_label = Label(
            text=f"Name: {self.user_info_data.get('name', '')}",
            font_size='20sp',
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(name_label)

        email_label = Label(
            text=f"Email: {self.user_info_data.get('email', '')}",
            font_size='20sp',
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(email_label)

        logout_button = Button(
            text="Logout",
            size_hint=(.8, None),
            height=50
        )

        logout_button.bind(on_release=lambda x: self.switch_screen('login'))

        self.layout.add_widget(logout_button)

    def update_info(self):
        self.clear_widgets()
        card = MDCard(
            padding=20,
            size_hint=(.8, .6),
            pos_hint={'center_x': .5, 'center_y': .5},
            orientation="vertical"
        )

        box_layout = BoxLayout(orientation='vertical')
        label = Label(
            text="Profile",
            halign="center",
            font_size='20sp',
            size_hint_y=None,
            height=50,
        )

        box_layout.add_widget(label)

        label = Label(
            text=f"Username: {self.user_info['username']}",
            halign="center",
            font_size='20sp',
            size_hint_y=None,
            height=50,
        )

        box_layout.add_widget(label)

        label = Label(
            text=f"Last login: {self.user_info['last_login']}",
            halign="center",
            font_size='20sp',
            size_hint_y=None,
            height=50,
        )

        box_layout.add_widget(label)

        card.add_widget(box_layout)
        self.add_widget(card)

class BoostApp(App):
    def switch_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    def show_error(self):
        Snackbar(text="Incorrect username or password").open()

    def show_answer(self, answer):
        dialog = MDDialog(
            title="AI Answer",
            text=answer,
            buttons=[
                MDFlatButton(
                    text="Close",
                    on_release=lambda dialog: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def login(self, username, password):
        if username == "admin" and password == "admin":
            self.switch_screen('home')
        else:
            self.show_error()

    def build(self):
        screen_manager = ScreenManager()

        login_screen = LoginScreen(name='login')
        login_screen.login_callback = self.login
        screen_manager.add_widget(login_screen)

        # switch to login screen
        screen_manager.current = 'login'

        home_screen = HomeScreen(name='home')
        home_screen.answer_callback = self.show_answer
        screen_manager.add_widget(home_screen)

        profile_screen = ProfileScreen(name='profile')
        screen_manager.add_widget(profile_screen)

        return screen_manager


class InfoScreen(Screen):
    def init(self, **kwargs):
        super().init(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.info_label = Label(
        text="SystemEnhance™ is a software platform that helps individuals\
             and organizations to automate and streamline various tasks.\
                 The platform uses the latest AI technologies to enhance productivity and efficiency.\
                     With SystemEnhance™, you can automate tasks such as data entry, content creation,\
                         customer support, and much more. Whether you're a small business owner or a large enterprise,\
                             SystemEnhance™ can help you save time and money, while improving the quality of your work.",
        font_size='20sp',
        halign='center',
        size_hint_y=None,
        height=600,
        text_size=(600, None)
        )
        self.layout.add_widget(self.info_label)

class SearchScreen(Screen):
    def init(self, **kwargs):
        super().init(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.search_bar = MDTextField(hint_text="Enter your query", size_hint=(.8, None), height=50)
        self.search_button = MDRaisedButton(text="Search", size_hint=(.8, None), height=50)
        self.search_button.bind(on_release=self.search)
        self.layout.add_widget(self.search_bar)
        self.layout.add_widget(self.search_button)

    def search(self, instance):
        query = self.search_bar.text.strip()    # get the query from the search bar
        if not query:   # check if the query is empty
            Snackbar(text="Please enter a query").open()        # show a snackbar if the query is empty
            return  # exit the function if the query is empty
        try:
            result = openai.Completion.create(engine="davinci", prompt=query, max_tokens=100, n=1, stop=None, temperature=0.5)
            if not result or not result.choices or not result.choices[0] or not result.choices[0].text:
                raise ValueError()
            answer = result.choices[0].text.strip()
            self.show_answer(answer)
        except:
            Snackbar(text="Error occurred while searching").open()

def show_answer(self, answer):
    dialog = MDDialog(
        title="AI Answer",
        text=answer,
        buttons=[
            MDFlatButton(
                text="Close",
                on_release=lambda dialog: dialog.dismiss()
            )
        ]
    )
    dialog.open()


class BoostEnhanceApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        self.screen_manager = ScreenManager()
        self.user_info = {}
        self.login_screen = LoginScreen(name='login')
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.current = 'login'
        bottom_nav = MDBottomNavigation()
        home_item = MDBottomNavigationItem(text='Home', icon='home', on_release=lambda x: self.switch_screen('home'))
        contact_item = MDBottomNavigationItem(text='Contact', icon='email', on_release=lambda x: self.switch_screen('contact'))
        content_item = MDBottomNavigationItem(text='Content', icon='file-document-outline', on_release=lambda x: self.switch_screen('content'))
        profile_item = MDBottomNavigationItem(text='Profile', icon='account', on_release=lambda x: self.switch_screen('profile'))
        search_item = MDBottomNavigationItem(text='Search', icon='magnify', on_release=lambda x: self.switch_screen('search'))
        bottom_nav.add_widget(home_item)
        bottom_nav.add_widget(contact_item)
        bottom_nav.add_widget(content_item)
        bottom_nav.add_widget(profile_item)
        bottom_nav.add_widget(search_item)
        layout = RelativeLayout()
        layout.add_widget(self.screen_manager)
        layout.add_widget(bottom_nav)
        return layout


    def switch_screen(self, screen_name):
        screen = next((s for s in self.screen_manager.children if s.name == screen_name), None)
        if screen:
            self.screen_manager.transition.direction = 'left' if self.screen_manager.current_screen.pos_hint['center_x'] < screen.pos_hint['center_x'] else 'right'
            self.screen_manager.current = screen.name

    def on_stop(self):
        with open('user_info.json', 'w') as file:
            json.dump(self.user_info, file)

    def on_start(self):
        if not os.path.isfile('user_info.json'):
            with open('user_info.json', 'w') as file:
                json.dump({}, file)

        with open('user_info.json', 'r') as file:
            self.user_info = json.load(file)

if __name__ == '__main__':
    BoostEnhanceApp().run()