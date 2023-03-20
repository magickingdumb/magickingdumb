import openai
from kivy.utils import escape_markup
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivy.properties import ObjectProperty
from datetime import datetime
import re
import json
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel

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
