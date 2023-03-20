from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class ArticleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.scroll_view = ScrollView()
        self.scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)

    def load_article(self, url):
        UrlRequest(url, on_success=self.parse_article)
        
    def parse_article(self, request, response):
        content = response['content']
        content = re.sub(r'<.*?>', '', content)
        content = content.replace('\n', '')

        content_label = Label(text=content, size_hint_y=None,height=300, font_size='18sp', halign='justify')
        self.scroll_layout.add_widget(content_label)
