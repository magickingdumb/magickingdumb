from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import button
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.label import MDLabel
from kivy.utils import escape_markup
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from datetime import datetime
import re
import json
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.scrollview import ScrollView

from user_database import create_users_table, add_user, check_user_credentials, get_all_usernames
from article_screen import ArticleScreen
from market_analysis_screen import MarketAnalysisScreen

class LoginScreen(Screen):
    def __init__(self, main_app=None, on_login=None, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.main_app = main_app
        self.on_login = on_login
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        self.username_input = MDTextField(hint_text="Username", size_hint=(0.8, None), height=50, pos_hint={"x": 0.1, "y": 0.55})
        self.password_input = MDTextField(hint_text="Password", size_hint=(0.8, None), height=50, password=True, pos_hint={"x": 0.1, "y": 0.45})

        self.login_button = MDRaisedButton(text="Login", on_release=self.login, pos_hint={"x": 0.1, "y": 0.35})
        self.register_button = MDRaisedButton(text="Register", on_release=self.register, pos_hint={"x": 0.1, "y": 0.25})
        self.profile_button = MDRaisedButton(text="Profile", on_release=self.go_to_profile_screen, pos_hint={"x": 0.1, "y": 0.15})
        self.news_feed_button = MDRaisedButton(text="Go to News Feed", on_release=self.go_to_news_feed_screen, pos_hint={"x": 0.3, "y": 0.4})
        self.market_analysis_button = MDRaisedButton(text="Market Analysis", on_release=self.go_to_market_analysis_screen, pos_hint={"x": 0.1, "y": 0.05})
        self.logout_button = MDRaisedButton(text="Logout", on_release=self.logout, pos_hint={"x": 0.1, "y": 0.05})
        self.search_button = MDRaisedButton(text="Search", on_release=self.search, pos_hint={"x": 0.1, "y": 0.05})

        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.login_button)
        self.layout.add_widget(self.register_button)
        self.layout.add_widgit(self.logout_button)
        self.layout.add_widget(self.profile_button)
        self.layout.add_widget(self.news_feed_button)
        self.layout.add_widget(self.market_analysis_button)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        user_info = check_user_credentials(username, password)
        if user_info:
            self.on_login(user_info)
            self.manager.current = "profile"
        else:
            Snackbar(text="Invalid username or password").open()

    def go_to_news_feed_screen(self, instance):
        self.manager.current = "news_feed"
        NewsFeedScreen = NewsFeedScreen()

    def go_to_market_analysis_screen(self, instance):
        self.manager.current = "market_analysis"
        MarketAnalysisScreen = MarketAnalysisScreen()

    def register(self, instance):
        self.manager.current = "register"
        RegisterScreen = RegisterScreen()

    def logout(self, instance):
        self.manager.current = "login"
        LoginScreen = LoginScreen()

    def search(self, instance):
        self.manager.current = "search"
        SearchScreen = SearchScreen()

    def go_to_profile_screen(self, instance):
        self.manager.current = "profile_screen"
        ProfileScreen = ProfileScreen()

class RegisterScreen(Screen):
    def __init__(self, main_app, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.main_app = main_app
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        self.username_input = MDTextField(hint_text="Username", size_hint=(0.8, None), height=50, pos_hint={"x": 0.1, "y": 0.55})
        self.password_input = MDTextField(hint_text="Password", size_hint=(0.8, None), height=50, password=True, pos_hint={"x": 0.1, "y": 0.45})
        self.email_input = MDTextField(hint_text="Email", size_hint=(0.8, None), height=50, pos_hint={"x": 0.1, "y": 0.35})
        register_button = MDRaisedButton(text="Register", on_release=self.register, pos_hint={"x": 0.1, "y": 0.25})

        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(register_button)

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        email = self.email_input.text

        if add_user(username, password, email):
            Snackbar(text="Registration successful!").open()
            self.main_app.screen_manager.current = "login"
        else:
            Snackbar(text="Registration failed. Username or email already exists.").open()

class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(CustomScreenManager, self).__init__(**kwargs)
        self.transition = SlideTransition()
        self.transition.direction = 'left'
        self.transition.duration = 0.5

class BoostEnhanceScreen(Screen):
    def __init__(self, app, **kwargs):
        super(BoostEnhanceScreen, self).__init__(**kwargs)
        self.app = app
        self.layout = BoxLayout(orientation='vertical')
        
        self.anchor_layout = AnchorLayout(anchor_x='right', anchor_y='center')
        self.search_field = MDTextField(hint_text='Enter your search query', size_hint=(0.8, None), height=30)
        self.anchor_layout.add_widget(self.search_field)
        self.layout.add_widget(self.anchor_layout)
        
        search_button = MDRaisedButton(text='Search', on_release=self.search_query)
        self.layout.add_widget(search_button)
        
        back_button = Button(text='Back', size_hint=(1, 0.1), on_release=self.go_back)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

    def search_query(self, *args):
        query = self.search_field.text.strip()
        if query:
            # Perform the search and display the result in SearchResultsScreen
            answer = self.app.perform_search(query)
            self.manager.get_screen('search_results').update_answer(answer)
            self.manager.current = 'search_results'
        else:
            Snackbar(text="Please enter a search query").show()

    def go_back(self, *args):
        self.manager.current = self.manager.history.pop()

class SearchResultsScreen(Screen):
    def __init__(self, app, **kwargs):
        super(SearchResultsScreen, self).__init__(**kwargs)
        self.app = app
        self.layout = BoxLayout(orientation='vertical')
        
        self.anchor_layout = AnchorLayout(anchor_x='right', anchor_y='center')
        self.search_field = MDTextField(hint_text='Enter your search query', size_hint=(0.8, None), height=30)
        self.anchor_layout.add_widget(self.search_field)
        self.layout.add_widget(self.anchor_layout)
        
        search_button = MDRaisedButton(text='Search', on_release=self.search_query)
        self.layout.add_widget(search_button)
        
        back_button = Button(text='Back', size_hint=(1, 0.1), on_release=self.go_back)
        
class ProfileScreen(Screen):
    display_name = StringProperty()
    description = StringProperty()

    def __init__(self, app, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.app = app

    def update_display_name(self, display_name):
        self.display_name = display_name
        self.description = self.app.get_profile_description(self.display_name)
        self.description_label.text = self.description
        self.description_label.size_hint_y = None
        self.description_label.height = self.description_label.texture_size[1]
        self.description_label.pos_hint_y = None
        self.name_label.text = self.display_name
        self.name_label.size_hint_y = None
        self.name_label.height = self.name_label.texture_size[1]
        self.name_label.pos_hint_y = None
        self.image_label.source = self.app.get_profile_image(self.display_name)

    def update_description(self, description):
        self.description = description
        self.description_label.text = self.description
        self.description_label.size_hint_y = None
        self.description_label.height = self.description_label.texture_size[1]
        self.name_label.text = self.display_name
        self.name_label.size_hint_y = None
        self.name_label.height = self.name_label.texture_size[1]
        self.name_label.pos_hint_y = None
        self.image_label.source = self.app.get_profile_image(self.display_name)
    
    def update_image(self, image):
        self.image_label.source = image
        self.name_label.text = self.display_name
        self.name_label.size_hint_y = None
        self.name_label.height = self.name_label.texture_size[1]
        self.name_label.pos_hint_y = None
        self.description_label.text = self.description
        self.description_label.size_hint_y = None
        self.description_label.height = self.description_label.texture_size[1]
        self.name_label.text = self.display_name
        self.name_label.size_hint_y = None
        self.name_label.height = self.name_label.texture_size[1]
        self.name_label.pos_hint_y = None

class MainScreen(Screen):
    def __init__(self, app, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.app = app

        self.layout = BoxLayout(orientation="vertical")

        self.search_bar = MDTextField(
            hint_text="Enter your query", size_hint=(0.8, None), height=50
        )
        self.search_button = MDFloatingActionButton(
            icon="search", pos_hint={"center_x": 0.5, "center_y": 0.1}
        )
        self.search_button.bind(on_release=self.search)

        self.layout.add_widget(self.search_bar)
        self.layout.add_widget(self.search_button)

        self.answer_label = MDLabel(
            text="", halign="center", theme_text_color="Secondary", size_hint_y=None
        )
        self.layout.add_widget(self.answer_label)

        self.add_widget(self.layout)

    def search(self, instance):
        query = self.search_bar.text
        response = openai.Completion.create(
            engine="davinci-instruct-beta",
            prompt=f"Find information about {query}",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        if response and response.choices and response.choices[0]:
            answer = response.choices[0].text.strip()
        else:
            answer = f"No results found for '{query}'"

        search_results_screen = self.app.screen_manager.get_screen("search_results")
        search_results_screen.update_answer(answer)
        self.app.screen_manager.current = "search_results"
    
    def go_back(self, *args):
        self.app.go_back()

class NewsFeedScreen(Screen):
    sources = ['abc-news', 'bbc-news', 'cnn', 'fox-news','google-news', 'nbc-news', 'the-washington-post', 'usa-today']
    def __init__(self, app, **kwargs):
        super(NewsFeedScreen, self).__init__(**kwargs)
        self.app = app
        self.fetch_articles()
        self.name = "news_feed"

        self.layout = BoxLayout(orientation='vertical')
        self.news_label = MDLabel(text="News", font_style="H2")
        self.layout.add_widget(self.news_label)

        self.add_widget(self.layout)

        self.news_label = MDLabel(text="News", font_style="H2", pos_hint={"center_x": 0.5, "top": 0.95})
        self.layout.add_widget(self.news_label)

        back_button = Button(text="Back to Login", pos_hint={"x": 0.1, "y": 0.1})
        back_button.bind(on_release=self.go_to_login)
        self.layout.add_widget(back_button)

    def go_to_login(self, instance):
        self.app.screen_manager.current = "login"
        self.news_source_input = MDTextField(hint_text="Enter your favorite news source (e.g. 'CNN')", size_hint=(.8, None), height=50)
        self.add_source_button = MDRaisedButton(text="Add", size_hint=(.2, None), height=50, pos_hint={'center_x': .5})
        self.add_source_button.bind(on_release=self.add_source)
        self.source_list = MDList()
        self.card = MDCard(padding=20, size_hint=(.8, .6), pos_hint={'center_x': .5, 'center_y': .5})
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.news_source_input)
        self.layout.add_widget(self.add_source_button)
        self.layout.add_widget(self.source_list)
        self.card.add_widget(self.layout)
        self.add_widget(self.card)
        self.news_articles_label = Label(
            text="Select a news source above to view articles.",
            halign="center",
            font_size='20sp',
            size_hint_y=None,
            height=50,
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.add_widget(self.news_articles_label)

        self.load_news()

    def fetch_articles(self):
        api_key = "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"
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        UrlRequest(url, on_success=self.display_articles)

    def display_articles(self, request, response):
        articles = response['articles']
        for article in articles:
            # Code to display articles

            title = article['title']
            description = article['description']
            url = article['url']

            item_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=150)
            title_label = Label(text=title, font_size='20sp', size_hint_y=None, height=50)
            item_layout.add_widget(title_label)

            description_label = Label(text=description, size_hint_y=None, height=50)
            item_layout.add_widget(description_label)
            read_more_button = Button(text="Read More", size_hint_y=None, height=50)
            read_more_button.bind(on_release=lambda x: self.show_article(url))
            item_layout.add_widget(read_more_button)
           
            self.scroll_layout.add_widget(item_layout)

    def show_article(self, url):
        app = App.get_running_app()
        app.root.current = 'article'
        article_screen = app.root.get_screen('article')
        article_screen.load_article(url)

    def on_enter(self, *args):
        self.card.pos_hint = {'center_x': .5, 'center_y': .5}
        self.news_articles_label.pos_hint = {'center_x': .5, 'center_y': .2}

    def add_source(self, instance):
        source = self.news_source_input.text.lower().replace(" ", "-")
        if source in NewsScreen.sources:
            Snackbar(text="This source has already been added.").open()
        else:
            NewsScreen.sources.append(source)
            self.source_list.add_widget(OneLineListItem(text=source.upper()))
            self.news_source_input.text = ""

    def update_news(self, instance):
        source = instance.text.lower()
        url = f'https://newsapi.org/v2/top-headlines?sources={source}&apiKey={openai.api_key}'
        UrlRequest(url, on_success=self.show_news, on_error=self.show_error)

    def show_news(self, urlrequest, data):
        articles = data['articles']
        if len(articles) == 0:
            self.news_articles_label.text = "No articles found for this source."
        else:
            self.source_list.clear_selection()
            self.news_articles_label.text = f"Top articles from {urlrequest.url.split('=')[1].upper()}"
            self.card.pos_hint = {'center_x': .5, 'center_y': .8}
            self.news_articles_label.pos_hint = {'center_x': .5, 'center_y': .95}
            self.card.remove_widget(self.layout)
            scroll_view = ScrollView()
            news_layout = BoxLayout(orientation='vertical',spacing=10, padding=20, size_hint_y=None)
            news_layout.bind(minimum_height=news_layout.setter('height'))
            for article in articles:
                title = escape_markup(article['title'])
                description = escape_markup(article['description'])
                published_date = datetime.strptime(
                article['publishedAt'][:19], '%Y-%m-%dT%H:%M:%S')
                published_date_string = published_date.strftime('%m/%d/%Y %I:%M %p')
                content = escape_markup(article['content']) if article['content'] is not None else ""
                news_item = MDCard(orientation='vertical',size_hint_y=None, height=350, padding=10)
                news_item.add_widget(Label(text=title, font_size='16sp',size_hint_y=None, height=40))
                news_item.add_widget(Label(text=published_date_string,font_size='12sp', size_hint_y=None, height=30))
                news_item.add_widget(Label(text=description, font_size='14sp', size_hint_y=None, height=120))
                news_item.add_widget(Label(text=content, font_size='12sp',size_hint_y=None, height=140))
                news_layout.add_widget(news_item)
                scroll_view.add_widget(news_layout)
                self.card.add_widget(scroll_view)

    def show_error(self, urlrequest, error):
        self.news_articles_label.text = f"Error: {error}"
    
    def load_news(self):
        self.fetch_articles()

class TestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = SlideTransition()

        # Add the login_screen to the screen_manager
        self.login_screen = LoginScreen(main_app=self, on_login=self.on_login_successful)
        self.login_screen.market_analysis_button.bind(on_press=self.login_screen.go_to_market_analysis_screen)
        self.login_screen.news_feed_button.bind(on_press=self.login_screen.go_to_news_feed_screen)
        self.login_screen.register_button.bind(on_press=self.login_screen.register)
        self.login_screen.profile_button.bind(on_press=self.login_screen.go_to_profile_screen)
        self.login_screen.search_button.bind(on_press=self.login_screen.go_to_search_results_screen)
        self.screen_manager.add_widget(self.login_screen)

        # Add the other screens to the screen_manager
        self.screen_manager.add_widget(MarketAnalysisScreen(self))
        self.screen_manager.add_widget(NewsFeedScreen(self))
        self.screen_manager.add_widget(SearchScreen(self))
        self.screen_manager.add_widget(SearchResultsScreen(self))
        self.screen_manager.add_widget(ProfileScreen(self))
        self.screen_manager.add_widget(MainScreen(self))

        # Set the current screen to login_screen
        self.screen_manager.current = "login_screen"
        return self.screen_manager

    def on_login_successful(self, user_info):
        self.user_info = user_info
        self.root.current = "main"

if __name__ == "__main__":
    TestApp().run()

