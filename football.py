from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import requests
import smtplib
import random
import string

API_KEY = "YOUR_FOOTBALL_DATA_ORG_API_KEY"  # Replace with your API key from football-data.org

class LiveFootballScoresApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.header = Label(text="Live Football Scores", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.header)

        self.logged_in = False
        self.username = None

        self.signup_button = Button(text="Sign Up", size_hint=(0.5, None), height=50)
        self.signup_button.bind(on_press=self.show_signup_popup)
        self.layout.add_widget(self.signup_button)

        self.login_button = Button(text="Login", size_hint=(0.5, None), height=50)
        self.login_button.bind(on_press=self.show_login_popup)
        self.layout.add_widget(self.login_button)

        self.table_layout = GridLayout(cols=4, size_hint=(1, 0.7))
        self.table_layout.add_widget(Label(text="Home Team"))
        self.table_layout.add_widget(Label(text="Away Team"))
        self.table_layout.add_widget(Label(text="Score"))
        self.table_layout.add_widget(Label(text="Status"))
        self.layout.add_widget(ScrollView(size_hint=(1, 0.7), do_scroll_x=False, do_scroll_y=True, bar_color=(0, 0, 0, 1)))
        self.layout.children[-1].add_widget(self.table_layout)

        self.error_label = Label(text="", color=(1, 0, 0, 1), size_hint=(1, None), height=50)
        self.layout.add_widget(self.error_label)

        return self.layout

    def show_signup_popup(self, _=None):
        popup_layout = BoxLayout(orientation='vertical')

        username_input = TextInput(hint_text="Username", multiline=False)
        email_input = TextInput(hint_text="Email", multiline=False)
        password_input = TextInput(hint_text="Password", multiline=False, password=True)

        signup_button = Button(text="Sign Up", size_hint=(1, None), height=50)
        signup_button.bind(on_press=lambda _: self.signup(username_input.text, email_input.text, password_input.text))

        popup_layout.add_widget(Label(text="Signup"))
        popup_layout.add_widget(username_input)
        popup_layout.add_widget(email_input)
        popup_layout.add_widget(password_input)
        popup_layout.add_widget(signup_button)

        popup = Popup(title="Signup", content=popup_layout, size_hint=(None, None), size=(400, 300))
        popup.open()

    def signup(self, username, email, password):
        # Replace this with a secure database and proper email verification mechanism
        if not username or not email or not password:
            self.show_error_popup("Please fill in all fields.")
            return

        # Simulate email verification by generating a random verification code
        verification_code = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        self.send_verification_email(email, verification_code)

        self.show_error_popup(f"Verification email sent to {email}. Use code {verification_code} to verify.")
        # Save user details in a secure database and set logged_in to False until verification is complete
        self.username = username
        self.logged_in = False

    def send_verification_email(self, email, verification_code):
        # Replace this with actual email sending code using smtplib or a dedicated email service
        print(f"Email sent to {email}. Verification code: {verification_code}")

    def show_login_popup(self, _=None):
        popup_layout = BoxLayout(orientation='vertical')

        username_input = TextInput(hint_text="Username", multiline=False)
        password_input = TextInput(hint_text="Password", multiline=False, password=True)

        login_button = Button(text="Login", size_hint=(1, None), height=50)
        login_button.bind(on_press=lambda _: self.login(username_input.text, password_input.text))

        popup_layout.add_widget(Label(text="Login"))
        popup_layout.add_widget(username_input)
        popup_layout.add_widget(password_input)
        popup_layout.add_widget(login_button)

        popup = Popup(title="Login", content=popup_layout, size_hint=(None, None), size=(400, 200))
        popup.open()

    def login(self, username, password):
        # Replace this with actual authentication code against a secure database
        if not username or not password:
            self.show_error_popup("Please enter your username and password.")
            return

        # Simulate successful login with a valid username and password
        if username == "demo" and password == "password":
            self.logged_in = True
            self.username = username
            self.error_label.text = ""
            self.update_scores()
        else:
            self.logged_in = False
            self.error_label.text = "Invalid credentials. Please try again."

    def show_error_popup(self, error_message):
        popup = Popup(title="Error", content=Label(text=error_message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def update_scores(self, _=None):
        if not self.logged_in:
            self.show_error_popup("Please log in to view live scores.")
            return

        headers = {
            "X-Auth-Token": API_KEY
        }
        try:
            response = requests.get("http://api.football-data.org/v2/matches?status=LIVE", headers=headers)
            response.raise_for_status()
            data = response.json()
            
            matches = data.get("matches", [])
            if not matches:
                self.clear_table()
                self.table_layout.add_widget(Label(text="No live matches at the moment.", font_size=20, col_span=4))
            else:
                self.clear_table()
                for match in matches:
                    home_team = match["homeTeam"]["name"]
                    away_team = match["awayTeam"]["name"]
                    score = f"{match['score']['fullTime']['homeTeam']} - {match['score']['fullTime']['awayTeam']}"
                    status = match["status"]
                    
                    self.table_layout.add_widget(Label(text=home_team))
                    self.table_layout.add_widget(Label(text=away_team))
                    self.table_layout.add_widget(Label(text=score))
                    self.table_layout.add_widget(Label(text=status))
        except requests.exceptions.RequestException as e:
            self.show_error_popup(f"Error fetching live scores: {e}")

    def clear_table(self):
        # Clear all widgets from the table layout except the header row
        for widget in self.table_layout.children[:]:
            if widget != self.header:
                self.table_layout.remove_widget(widget)

if __name__ == "__main__":
    LiveFootballScoresApp().run()
