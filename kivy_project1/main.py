from kivymd.app import MDApp

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRectangleFlatButton

from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

from settings import Settings
from user import User

import bcrypt


LabelBase.register(name="Roboto", fn_regular="assets/font/Roboto-Thin.ttf", fn_bold="assets/font/Roboto-Medium.ttf")
Window.clearcolor = get_color_from_hex("#101216")


class MyApp(MDApp):
    dialog = None
    dialog1 = None

    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.current_user = None
        self.dialog_box = None
        self.title = "My first MD App "
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Builder.load_file("pages/splash.kv"))
        self.screen_manager.add_widget(Builder.load_file("pages/login.kv"))
        self.screen_manager.add_widget(Builder.load_file("pages/dashboard.kv"))
        self.screen_manager.add_widget(Builder.load_file("pages/signup.kv"))
        self.screen_manager.add_widget(Builder.load_file("pages/food.kv"))
        self.screen_manager.add_widget(Builder.load_file("pages/drink.kv"))
        self.screen_manager.add_widget(Builder.load_file("pages/dessert.kv"))




    def build(self):
        self.screen_manager.current = "splash"
        return self.screen_manager

    def on_start(self):
        Clock.schedule_once(self.to_login_page, 1)

    def to_login_page(self, *args):
        self.screen_manager.current = "login"

    def return_to_menu(self, *args):
        self.screen_manager.current = "dashboard"

    def to_sign_up(self, *args):
        self.screen_manager.current = "signup"

    def to_food(self, *args):
        self.screen_manager.current = "food"
    def to_drink(self, *args):
        self.screen_manager.current = "drink"
    def to_dessert(self, *args):
        self.screen_manager.current = "dessert"


    def error_same_username(self):
        if not self.dialog1:
            self.dialog1 = MDDialog(
                title="Warning!",
                text="This username have been used!",
                buttons=[
                    MDRectangleFlatButton(
                        text="Close", text_color=self.theme_cls.primary_color, on_release=self.close_dialog1
                    ),
                ],
            )
        self.dialog1.open()

    def close_dialog1(self, obj):
        self.dialog1.dismiss()

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Warning!",
                text="Wrong Input !",
                buttons=[
                    MDRectangleFlatButton(
                        text="Close", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()


    def find_user_by_username(self, username):
        with self.settings.conn:
            self.settings.cur.execute("""
    				SELECT * FROM users WHERE username=:username
    				""",
                                      {"username": username})
        return self.settings.cur.fetchone()

    def logger(self):
        username_entry = self.root.screens[1].ids['username_entry'].text
        password_entry = self.root.screens[1].ids['password_entry'].text

        user = self.find_user_by_username(username_entry)

        if user:
            # print(bcrypt.checkpw(password_entry.encode("utf-8"), user[2]))
            if bcrypt.checkpw(password_entry.encode("utf-8"), user[1]):
                self.root.screens[1].ids['username_entry'].text = ""
                self.root.screens[1].ids['password_entry'].text = ""

                self.current_user = User(user[0], user[2], user[3])
                self.current_user.bio = user[4]
                self.current_user.pic = user[5]


                self.to_dashboard()
                self.root.screens[1].ids['username_entry'].text = ""
                self.root.screens[1].ids['password_entry'].text = ""
                return True
            else:
                self.show_alert_dialog()
                self.root.screens[1].ids['username_entry'].text = ""
                self.root.screens[1].ids['password_entry'].text = ""
        else:
            self.show_alert_dialog()
            self.root.screens[1].ids["username_entry"].text = ""
            self.root.screens[1].ids["password_entry"].text = ""

    def to_dashboard(self):
        fullname = self.current_user.first.title() + " " + self.current_user.last.title()

        self.root.screens[2].ids['full_name'].text = fullname
        self.root.screens[2].ids['bio'].text = self.current_user.bio
        self.root.screens[2].ids['user_image'].source = self.current_user.pic
        self.root.current = "dashboard"



    def close_dialog2(self, *args):
        self.dialog_box.dismiss()
        self.root.screens[2].ids['nav_drawer'].set_state("close")

    def exit(self, *args):
        self.dialog_box.dismiss()
        self.current_user = None
        self.root.current = "login"

    def sign_out(self, *args):
        if not self.dialog_box:
            self.dialog_box = MDDialog(
                title = "Confirmation",
                text = "Are you sure to log out?",
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=self.close_dialog2
                    ),
                    MDFlatButton(
                        text="Yes",
                        on_release=self.exit
                    )

                ]

            )
        self.dialog_box.open()


    def insert_usr(self, usr):
        with self.settings.conn:
            self.settings.cur.execute("INSERT INTO users VALUES (:username,:password, :first, :last, :bio, :pic)", {"first":usr.first, "last":usr.last, "username":usr.username,"password":usr.password, "bio":usr.bio, "pic":usr.pic})

    def sign_up(self):
        new_username = self.root.screens[3].ids['username_entry'].text
        new_password = self.root.screens[3].ids['password_entry'].text
        new_first = self.root.screens[3].ids["first_entry"].text
        new_last = self.root.screens[3].ids["last_entry"].text
        new_bio = self.root.screens[3].ids["birth_entry"].text
        new_pic = self.root.screens[3].ids["user_pic"].text
        user = self.find_user_by_username(new_username)
        if new_username != "":
            if new_password != "":
                if new_first != "":
                    if new_last != "":
                        if new_bio != "":
                            if new_pic != "":
                                if user:
                                    self.error_same_username()
                                    self.root.screens[3].ids['username_entry'] = ""
                                    self.root.screens[3].ids['password_entry'] = ""
                                    self.root.screens[3].ids['first_entry'] = ""
                                    self.root.screens[3].ids['last_entry'] = ""
                                    self.root.screens[3].ids['birth_entry'] = ""
                                    self.root.screens[3].ids['user_pic'] = ""
                                else:
                                    usr = User(new_username, new_first, new_last)
                                    usr.bio = new_bio
                                    usr.pic = "assets/img/" + new_pic
                                    repassword = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                                    usr.password = repassword
                                    self.insert_usr(usr)
                                    self.root.current = "login"
                                    self.root.screens[3].ids['username_entry'] = ""
                                    self.root.screens[3].ids['password_entry'] = ""
                                    self.root.screens[3].ids['first_entry'] = ""
                                    self.root.screens[3].ids['last_entry'] = ""
                                    self.root.screens[3].ids['birth_entry'] = ""
                                    self.root.screens[3].ids['user_pic'] = ""
                            else:
                                self.show_alert_dialog()
                                self.root.screens[3].ids['username_entry'] = ""
                                self.root.screens[3].ids['password_entry'] = ""
                                self.root.screens[3].ids['first_entry'] = ""
                                self.root.screens[3].ids['last_entry'] = ""
                                self.root.screens[3].ids['birth_entry'] = ""
                                self.root.screens[3].ids['user_pic'] = ""
                        else:
                            self.show_alert_dialog()
                            self.root.screens[3].ids['username_entry'] = ""
                            self.root.screens[3].ids['password_entry'] = ""
                            self.root.screens[3].ids['first_entry'] = ""
                            self.root.screens[3].ids['last_entry'] = ""
                            self.root.screens[3].ids['birth_entry'] = ""
                            self.root.screens[3].ids['user_pic'] = ""
                    else:
                        self.show_alert_dialog()
                        self.root.screens[3].ids['username_entry'] = ""
                        self.root.screens[3].ids['password_entry'] = ""
                        self.root.screens[3].ids['first_entry'] = ""
                        self.root.screens[3].ids['last_entry'] = ""
                        self.root.screens[3].ids['birth_entry'] = ""
                        self.root.screens[3].ids['user_pic'] = ""
                else:
                    self.show_alert_dialog()
                    self.root.screens[3].ids['username_entry'] = ""
                    self.root.screens[3].ids['password_entry'] = ""
                    self.root.screens[3].ids['first_entry'] = ""
                    self.root.screens[3].ids['last_entry'] = ""
                    self.root.screens[3].ids['birth_entry'] = ""
                    self.root.screens[3].ids['user_pic'] = ""
            else:
                self.show_alert_dialog()
                self.root.screens[3].ids['username_entry'] = ""
                self.root.screens[3].ids['password_entry'] = ""
                self.root.screens[3].ids['first_entry'] = ""
                self.root.screens[3].ids['last_entry'] = ""
                self.root.screens[3].ids['birth_entry'] = ""
                self.root.screens[3].ids['user_pic'] = ""
        else:
            self.show_alert_dialog()
            self.root.screens[3].ids['username_entry'] = ""
            self.root.screens[3].ids['password_entry'] = ""
            self.root.screens[3].ids['first_entry'] = ""
            self.root.screens[3].ids['last_entry'] = ""
            self.root.screens[3].ids['birth_entry'] = ""
            self.root.screens[3].ids['user_pic'] = ""



if __name__ == "__main__":
    app = MyApp()
    app.run()
