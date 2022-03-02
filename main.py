from models import *
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton, MDRectangleFlatButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBody, ThreeLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar


class MainWindow(MDBoxLayout):
    pass


class RightButton(IRightBody, MDIconButton):
    pass


class SearchResulItem(ThreeLineAvatarIconListItem):
    last_name = ''
    last_barcode = ''
    last_departament = ''

    def __init__(self, produs_id, **kwargs):
        super(SearchResulItem, self).__init__(**kwargs)
        self.produs_id = produs_id

    def delete_product(self, obj):
        delete_by_id(self.produs_id)
        self.close_dialog(obj)
        self.parent.remove_widget(self)

    def get_one(self):
        elm = get_one_row(self.produs_id)
        elm = elm.val()
        self.last_name = elm["name"]
        self.last_barcode = elm["barcode"]
        self.last_departament = elm["departament"]

    def show_confirm_dialog(self):
        self.dialog = MDDialog(title='Ștergeți înregistrarea?',
                               text="Informația ștearsă nu poate fi restabilită",
                               size_hint=(0.6, 1),
                               buttons=[MDFlatButton(text='Închide', on_release=self.close_dialog),
                                        MDFlatButton(text='Șterge', on_release=self.delete_product, )]
                               )
        self.dialog.open()

    def show_udate_diaalog(self):
        content_layout = MDBoxLayout(
            orientation="vertical",
            height="130dp"
        )
        lsn = MDTextField(
            hint_text="Denumirea produsului",
        )
        lsb = MDTextField(
            hint_text="Barcodul produsului",
        )
        lsd = MDTextField(
            hint_text="Departamentul produsului",
        )
        lsn.text = str(self.last_name)
        lsb.text = str(self.last_barcode)
        lsd.text = str(self.last_departament)

        def exchange(obj):
            self.last_name = lsn.text
            self.last_departament = lsd.text
            self.last_barcode = lsb.text
            self.update(obj)

        content_layout.add_widget(lsn)
        content_layout.add_widget(lsb)
        content_layout.add_widget(lsd)
        self.update_dialog = MDDialog(title='Editarea înregistrării:',
                                      type="custom",
                                      size_hint=(.7, 8),
                                      content_cls=content_layout,
                                      buttons=[MDFlatButton(text='Închide', on_release=self.close_update_dialog),
                                               MDFlatButton(text='Reînoiește', on_release=exchange)]
                                      )
        self.update_dialog.open()

    def update(self, obj):
        update_row(self.last_name, self.last_departament, self.last_barcode, self.produs_id)
        self.close_update_dialog(obj)
        LogisticApp.get_all(self)

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def close_update_dialog(self, obj):
        self.update_dialog.dismiss()


class LogisticApp(MDApp):

    def clearWidgets(self):
        app = MDApp.get_running_app()
        result_list_widget = app.root.ids.search_results
        result_list_widget.clear_widgets()
        return result_list_widget

    def get_all(self):
        app = MDApp.get_running_app()
        result_list_widget = app.root.ids.search_results
        result_list_widget.clear_widgets()
        reponse = all()
        for product in reponse.each():
            value = product.val()
            value["key"] = product.key()
            result_list_widget.add_widget(
                SearchResulItem(text=value["name"], secondary_text=value["departament"], tertiary_text=value["barcode"],
                                produs_id=value["key"])
            )

    def name_search_and_fill(self, query):
        result_list_widget = self.clearWidgets()
        response = all()
        for product in response.each():
            value = product.val()
            value["key"] = product.key()
            if query in value["name"] or query in value["departament"] or query in value["barcode"]:
                result_list_widget.add_widget(
                    SearchResulItem(text=value["name"], secondary_text=value["departament"],
                                    tertiary_text=value["barcode"], produs_id=value["key"])
                )

    def build(self):
        return MainWindow()

    def save_product(self, name, departament, barcode):
        if produs_saver(name, departament, barcode):
            app = MDApp.get_running_app()
            screen_manager = app.root.ids.bottom_navigation
            screen_manager.switch_tab("screen search")
            self.get_all()
            app.root.ids.add_name.text = ""
            app.root.ids.add_departament.text = ""
            app.root.ids.add_barcode.text = ""

    def on_start(self, **kwargs):
        self.get_all()


if __name__ == "__main__":
    LogisticApp().run()
