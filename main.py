import sqlite3
import os
import shutil

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.popup import Popup


DATABASE = "ti_eho.db"


# =========================================================
# DATABASE
# =========================================================

def create_database():

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            location TEXT
        )
    """)

    db.commit()
    db.close()


def add_object(name, category, location):

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO objects
        (name, category, location)
        VALUES (?, ?, ?)
    """, (
        name,
        category,
        location
    ))

    db.commit()
    db.close()


def update_object(
    object_id,
    name,
    category,
    location
):

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        UPDATE objects
        SET name = ?,
            category = ?,
            location = ?
        WHERE id = ?
    """, (
        name,
        category,
        location,
        object_id
    ))

    db.commit()
    db.close()


def get_object(object_id):

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name, category, location
        FROM objects
        WHERE id = ?
    """, (object_id,))

    result = cursor.fetchone()

    db.close()

    return result


def get_objects(
    search="",
    category="",
    location=""
):

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    query = """
        SELECT id, name, category, location
        FROM objects
        WHERE 1=1
    """

    params = []

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if search.strip() != "":

        query += """
            AND (
                name LIKE ?
                OR category LIKE ?
                OR location LIKE ?
            )
        """

        text = "%" + search.strip() + "%"

        params.extend([
            text,
            text,
            text
        ])

    # -----------------------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------------------

    if category.strip() != "":

        query += """
            AND category = ?
        """

        params.append(
            category.strip()
        )

    # -----------------------------------------------------
    # LOCATION FILTER
    # -----------------------------------------------------

    if location.strip() != "":

        query += """
            AND location = ?
        """

        params.append(
            location.strip()
        )

    query += """
        ORDER BY id DESC
    """

    cursor.execute(
        query,
        params
    )

    results = cursor.fetchall()

    db.close()

    return results


def delete_object(object_id):

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM objects WHERE id = ?",
        (object_id,)
    )

    db.commit()
    db.close()


# =========================================================
# STATISTICS
# =========================================================

def get_total_objects():

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM objects"
    )

    result = cursor.fetchone()[0]

    db.close()

    return result


def get_total_categories():

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT category)
        FROM objects
        WHERE category IS NOT NULL
        AND TRIM(category) != ''
    """)

    result = cursor.fetchone()[0]

    db.close()

    return result


def get_total_locations():

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT location)
        FROM objects
        WHERE location IS NOT NULL
        AND TRIM(location) != ''
    """)

    result = cursor.fetchone()[0]

    db.close()

    return result


# =========================================================
# FILTER DATA
# =========================================================

def get_categories():

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        SELECT DISTINCT category
        FROM objects
        WHERE category IS NOT NULL
        AND TRIM(category) != ''
        ORDER BY category COLLATE NOCASE
    """)

    results = [
        row[0]
        for row in cursor.fetchall()
    ]

    db.close()

    return results


def get_locations():

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        SELECT DISTINCT location
        FROM objects
        WHERE location IS NOT NULL
        AND TRIM(location) != ''
        ORDER BY location COLLATE NOCASE
    """)

    results = [
        row[0]
        for row in cursor.fetchall()
    ]

    db.close()

    return results


# =========================================================
# BACKUP
# =========================================================

def create_backup():

    if not os.path.exists(DATABASE):
        return None

    backup_path = "ti_eho_backup.db"

    shutil.copy2(
        DATABASE,
        backup_path
    )

    return backup_path


def restore_backup():

    backup_path = "ti_eho_backup.db"

    if not os.path.exists(
        backup_path
    ):
        return False

    shutil.copy2(
        backup_path,
        DATABASE
    )

    return True


# =========================================================
# TEXT INPUT
# =========================================================

def make_text_input(hint):

    field = TextInput(

        hint_text=hint,

        font_size=dp(19),

        multiline=False,

        # -------------------------------------------------
        # ΣΗΜΑΝΤΙΚΟ
        # -------------------------------------------------
        # Το κρατάμε έτσι επειδή αυτή είναι η έκδοση
        # που σταμάτησε το μπέρδεμα των ελληνικών λέξεων.
        # -------------------------------------------------

        input_type="null",

        keyboard_suggestions=False,

        padding=[
            dp(12),
            dp(10)
        ],

        background_normal="",

        background_active="",

        background_color=(
            0.96,
            0.97,
            0.99,
            1
        ),

        foreground_color=(
            0.05,
            0.08,
            0.12,
            1
        ),

        hint_text_color=(
            0.40,
            0.45,
            0.50,
            1
        ),

        cursor_color=(
            0.03,
            0.32,
            0.78,
            1
        )
    )

    return field


# =========================================================
# BUTTON
# =========================================================

def make_button(
    text,
    font_size=18,
    color=(1, 1, 1, 1),
    background=(0.02, 0.20, 0.55, 1)
):

    button = Button(

        text=text,

        font_size=dp(font_size),

        bold=True,

        color=color,

        background_normal="",

        background_down="",

        background_color=background
    )

    return button
    # =========================================================
# HOME SCREEN
# =========================================================

class HomeScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        root = FloatLayout()

        # -------------------------------------------------
        # BACKGROUND
        # -------------------------------------------------

        with root.canvas.before:

            Color(
                0.025,
                0.055,
                0.10,
                1
            )

            self.bg = RoundedRectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = Label(

            text="ΤΙ ΕΧΩ;",

            font_size=dp(42),

            bold=True,

            color=(
                1,
                1,
                1,
                1
            ),

            size_hint=(1, 0.12),

            pos_hint={
                "center_x": 0.5,
                "top": 0.96
            }
        )

        root.add_widget(
            title
        )

        # -------------------------------------------------
        # SUBTITLE
        # -------------------------------------------------

        subtitle = Label(

            text=
            "Οργάνωσε και βρες όλα τα αντικείμενά σου",

            font_size=dp(16),

            color=(
                0.65,
                0.72,
                0.82,
                1
            ),

            size_hint=(1, 0.07),

            pos_hint={
                "center_x": 0.5,
                "top": 0.86
            }
        )

        root.add_widget(
            subtitle
        )

        # -------------------------------------------------
        # STATISTICS PANEL
        # -------------------------------------------------

        stats_panel = BoxLayout(

            orientation="horizontal",

            spacing=dp(8),

            padding=[
                dp(5),
                dp(5)
            ],

            size_hint=(0.92, 0.17),

            pos_hint={
                "center_x": 0.5,
                "top": 0.78
            }
        )

        # -------------------------------------------------
        # TOTAL OBJECTS
        # -------------------------------------------------

        self.objects_stat = self.create_stat_box(
            "0",
            "ΑΝΤΙΚΕΙΜΕΝΑ"
        )

        stats_panel.add_widget(
            self.objects_stat
        )

        # -------------------------------------------------
        # CATEGORIES
        # -------------------------------------------------

        self.categories_stat = self.create_stat_box(
            "0",
            "ΕΙΔΗ"
        )

        stats_panel.add_widget(
            self.categories_stat
        )

        # -------------------------------------------------
        # LOCATIONS
        # -------------------------------------------------

        self.locations_stat = self.create_stat_box(
            "0",
            "ΣΗΜΕΙΑ"
        )

        stats_panel.add_widget(
            self.locations_stat
        )

        root.add_widget(
            stats_panel
        )

        # -------------------------------------------------
        # MAIN PANEL
        # -------------------------------------------------

        panel = FloatLayout(

            size_hint=(0.90, 0.47),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.40
            }
        )

        with panel.canvas.before:

            Color(
                0.025,
                0.31,
                0.76,
                0.98
            )

            self.panel_bg = RoundedRectangle(

                pos=panel.pos,

                size=panel.size,

                radius=[dp(20)]
            )

        panel.bind(
            pos=self.update_panel,
            size=self.update_panel
        )

        # -------------------------------------------------
        # ADD BUTTON
        # -------------------------------------------------

        add_button = make_button(

            "ΠΡΟΣΘΗΚΗ ΑΝΤΙΚΕΙΜΕΝΟΥ",

            17,

            (
                0.03,
                0.18,
                0.40,
                1
            ),

            (
                1,
                1,
                1,
                1
            )
        )

        add_button.size_hint = (
            0.82,
            0.20
        )

        add_button.pos_hint = {

            "center_x": 0.5,

            "top": 0.83
        }

        add_button.bind(
            on_press=self.open_add
        )

        panel.add_widget(
            add_button
        )

        # -------------------------------------------------
        # SEARCH BUTTON
        # -------------------------------------------------

        search_button = make_button(

            "ΑΝΑΖΗΤΗΣΗ ΑΝΤΙΚΕΙΜΕΝΟΥ",

            17,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.02,
                0.20,
                0.55,
                1
            )
        )

        search_button.size_hint = (
            0.82,
            0.20
        )

        search_button.pos_hint = {

            "center_x": 0.5,

            "top": 0.56
        }

        search_button.bind(
            on_press=self.open_search
        )

        panel.add_widget(
            search_button
        )

        # -------------------------------------------------
        # FILTER BUTTON
        # -------------------------------------------------

        filter_button = make_button(

            "ΚΑΤΗΓΟΡΙΕΣ ΚΑΙ ΣΗΜΕΙΑ",

            17,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.05,
                0.10,
                0.18,
                1
            )
        )

        filter_button.size_hint = (
            0.82,
            0.20
        )

        filter_button.pos_hint = {

            "center_x": 0.5,

            "top": 0.29
        }

        filter_button.bind(
            on_press=self.open_filters
        )

        panel.add_widget(
            filter_button
        )

        root.add_widget(
            panel
        )

        # -------------------------------------------------
        # BACKUP BUTTON
        # -------------------------------------------------

        backup_button = make_button(

            "ΑΝΤΙΓΡΑΦΟ ΑΣΦΑΛΕΙΑΣ",

            14,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.12,
                0.38,
                0.25,
                1
            )
        )

        backup_button.size_hint = (
            0.42,
            0.08
        )

        backup_button.pos_hint = {

            "center_x": 0.28,

            "y": 0.055
        }

        backup_button.bind(
            on_press=self.make_backup
        )

        root.add_widget(
            backup_button
        )

        # -------------------------------------------------
        # RESTORE BUTTON
        # -------------------------------------------------

        restore_button = make_button(

            "ΕΠΑΝΑΦΟΡΑ",

            14,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.35,
                0.18,
                0.10,
                1
            )
        )

        restore_button.size_hint = (
            0.42,
            0.08
        )

        restore_button.pos_hint = {

            "center_x": 0.72,

            "y": 0.055
        }

        restore_button.bind(
            on_press=self.ask_restore
        )

        root.add_widget(
            restore_button
        )

        self.add_widget(
            root
        )

        # -------------------------------------------------
        # INITIAL STATISTICS
        # -------------------------------------------------

        self.update_statistics()

    # =====================================================
    # STAT BOX
    # =====================================================

    def create_stat_box(
        self,
        number,
        title
    ):

        box = FloatLayout()

        with box.canvas.before:

            Color(
                0.055,
                0.085,
                0.14,
                1
            )

            box.background = RoundedRectangle(

                pos=box.pos,

                size=box.size,

                radius=[dp(12)]
            )

        box.bind(
            pos=lambda instance, value:
            self.update_stat_background(
                instance,
                value
            ),

            size=lambda instance, value:
            self.update_stat_background(
                instance,
                value
            )
        )

        number_label = Label(

            text=number,

            font_size=dp(25),

            bold=True,

            color=(
                1,
                1,
                1,
                1
            ),

            size_hint=(1, 0.58),

            pos_hint={
                "center_x": 0.5,
                "top": 0.93
            }
        )

        box.add_widget(
            number_label
        )

        title_label = Label(

            text=title,

            font_size=dp(10),

            bold=True,

            color=(
                0.55,
                0.72,
                0.90,
                1
            ),

            size_hint=(1, 0.30),

            pos_hint={
                "center_x": 0.5,
                "y": 0.08
            }
        )

        box.add_widget(
            title_label
        )

        box.number_label = number_label

        return box

    # =====================================================
    # STATISTICS
    # =====================================================

    def update_statistics(self):

        total = get_total_objects()

        categories = get_total_categories()

        locations = get_total_locations()

        self.objects_stat.number_label.text = str(
            total
        )

        self.categories_stat.number_label.text = str(
            categories
        )

        self.locations_stat.number_label.text = str(
            locations
        )

    # =====================================================
    # STAT BACKGROUND
    # =====================================================

    def update_stat_background(
        self,
        instance,
        value
    ):

        instance.background.pos = instance.pos

        instance.background.size = instance.size

    # =====================================================
    # NAVIGATION
    # =====================================================

    def open_add(
        self,
        instance
    ):

        self.manager.current = "add"

    def open_search(
        self,
        instance
    ):

        search = self.manager.get_screen(
            "search"
        )

        search.search_input.text = ""

        search.load_objects()

        self.manager.current = "search"

    def open_filters(
        self,
        instance
    ):

        filters = self.manager.get_screen(
            "filters"
        )

        filters.refresh_filters()

        self.manager.current = "filters"

    # =====================================================
    # BACKUP
    # =====================================================

    def make_backup(
        self,
        instance
    ):

        result = create_backup()

        if result:

            self.show_message(
                "ΑΝΤΙΓΡΑΦΟ ΑΣΦΑΛΕΙΑΣ",
                "Το αντίγραφο ασφαλείας "
                "δημιουργήθηκε επιτυχώς."
            )

        else:

            self.show_message(
                "ΣΦΑΛΜΑ",
                "Δεν ήταν δυνατή η δημιουργία "
                "του αντιγράφου."
            )

    # =====================================================
    # RESTORE CONFIRMATION
    # =====================================================

    def ask_restore(
        self,
        instance
    ):

        content = FloatLayout()

        message = Label(

            text=
            "Η επαναφορά θα αντικαταστήσει\n"
            "τα τωρινά δεδομένα με το backup.\n\n"
            "Θέλεις να συνεχίσεις;",

            font_size=dp(16),

            color=(
                0.08,
                0.10,
                0.14,
                1
            ),

            halign="center",

            valign="middle",

            size_hint=(0.90, 0.60),

            pos_hint={
                "center_x": 0.5,
                "top": 0.90
            }
        )

        content.add_widget(
            message
        )

        yes = make_button(

            "ΕΠΑΝΑΦΟΡΑ",

            13,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.65,
                0.08,
                0.08,
                1
            )
        )

        yes.size_hint = (
            0.40,
            0.22
        )

        yes.pos_hint = {
            "x": 0.08,
            "y": 0.08
        }

        content.add_widget(
            yes
        )

        no = make_button(

            "ΑΚΥΡΩΣΗ",

            13,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.02,
                0.20,
                0.55,
                1
            )
        )

        no.size_hint = (
            0.40,
            0.22
        )

        no.pos_hint = {
            "right": 0.92,
            "y": 0.08
        }

        content.add_widget(
            no
        )

        popup = Popup(

            title="ΕΠΙΒΕΒΑΙΩΣΗ",

            content=content,

            size_hint=(0.86, 0.38),

            auto_dismiss=False
        )

        no.bind(
            on_press=popup.dismiss
        )

        yes.bind(
            on_press=lambda x:
            self.restore_data(
                popup
            )
        )

        popup.open()

    # =====================================================
    # RESTORE
    # =====================================================

    def restore_data(
        self,
        popup
    ):

        result = restore_backup()

        popup.dismiss()

        if result:

            self.update_statistics()

            self.show_message(
                "ΕΠΑΝΑΦΟΡΑ",
                "Τα δεδομένα επαναφέρθηκαν "
                "επιτυχώς."
            )

        else:

            self.show_message(
                "ΔΕΝ ΒΡΕΘΗΚΕ BACKUP",
                "Δεν υπάρχει διαθέσιμο "
                "αντίγραφο ασφαλείας."
            )

    # =====================================================
    # MESSAGE
    # =====================================================

    def show_message(
        self,
        title,
        message
    ):

        content = FloatLayout()

        text = Label(

            text=message,

            font_size=dp(17),

            color=(
                0.08,
                0.10,
                0.14,
                1
            ),

            halign="center",

            valign="middle",

            size_hint=(0.90, 0.55),

            pos_hint={
                "center_x": 0.5,
                "top": 0.88
            }
        )

        content.add_widget(
            text
        )

        ok = make_button(

            "OK",

            15,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.02,
                0.20,
                0.55,
                1
            )
        )

        ok.size_hint = (
            0.42,
            0.24
        )

        ok.pos_hint = {
            "center_x": 0.5,
            "y": 0.08
        }

        content.add_widget(
            ok
        )

        popup = Popup(

            title=title,

            content=content,

            size_hint=(0.82, 0.32),

            auto_dismiss=False
        )

        ok.bind(
            on_press=popup.dismiss
        )

        popup.open()

    # =====================================================
    # BACKGROUND
    # =====================================================

    def update_bg(
        self,
        instance,
        value
    ):

        self.bg.pos = instance.pos

        self.bg.size = instance.size

    def update_panel(
        self,
        instance,
        value
    ):

        self.panel_bg.pos = instance.pos

        self.panel_bg.size = instance.size
        # =========================================================
# ADD / EDIT OBJECT SCREEN
# =========================================================

class AddObjectScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.editing_id = None

        root = FloatLayout()

        # -------------------------------------------------
        # BACKGROUND
        # -------------------------------------------------

        with root.canvas.before:

            Color(
                0.025,
                0.055,
                0.10,
                1
            )

            self.bg = RoundedRectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        self.header = Label(
            text="ΠΡΟΣΘΗΚΗ ΑΝΤΙΚΕΙΜΕΝΟΥ",

            font_size=dp(28),

            bold=True,

            color=(
                1,
                1,
                1,
                1
            ),

            size_hint=(1, 0.12),

            pos_hint={
                "center_x": 0.5,
                "top": 0.97
            }
        )

        root.add_widget(
            self.header
        )

        # -------------------------------------------------
        # PANEL
        # -------------------------------------------------

        panel = FloatLayout(

            size_hint=(0.90, 0.70),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.48
            }
        )

        with panel.canvas.before:

            Color(
                0.025,
                0.31,
                0.76,
                0.98
            )

            self.panel_bg = RoundedRectangle(

                pos=panel.pos,

                size=panel.size,

                radius=[dp(20)]
            )

        panel.bind(
            pos=self.update_panel,
            size=self.update_panel
        )

        # -------------------------------------------------
        # OBJECT NAME
        # -------------------------------------------------

        name_label = Label(

            text="ΟΝΟΜΑ ΑΝΤΙΚΕΙΜΕΝΟΥ",

            font_size=dp(15),

            bold=True,

            color=(
                1,
                1,
                1,
                1
            ),

            size_hint=(0.82, 0.08),

            pos_hint={
                "center_x": 0.5,
                "top": 0.90
            },

            halign="left"
        )

        panel.add_widget(
            name_label
        )

        self.name_input = make_text_input(
            "π.χ. Βίδα"
        )

        self.name_input.size_hint = (
            0.82,
            0.13
        )

        self.name_input.pos_hint = {
            "center_x": 0.5,
            "top": 0.82
        }

        panel.add_widget(
            self.name_input
        )

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        category_label = Label(

            text="ΕΙΔΟΣ",

            font_size=dp(15),

            bold=True,

            color=(
                1,
                1,
                1,
                1
            ),

            size_hint=(0.82, 0.08),

            pos_hint={
                "center_x": 0.5,
                "top": 0.67
            },

            halign="left"
        )

        panel.add_widget(
            category_label
        )

        self.category_input = make_text_input(
            "π.χ. Εργαλεία"
        )

        self.category_input.size_hint = (
            0.82,
            0.13
        )

        self.category_input.pos_hint = {
            "center_x": 0.5,
            "top": 0.59
        }

        panel.add_widget(
            self.category_input
        )

        # -------------------------------------------------
        # LOCATION
        # -------------------------------------------------

        location_label = Label(

            text="ΣΗΜΕΙΟ",

            font_size=dp(15),

            bold=True,

            color=(
                1,
                1,
                1,
                1
            ),

            size_hint=(0.82, 0.08),

            pos_hint={
                "center_x": 0.5,
                "top": 0.44
            },

            halign="left"
        )

        panel.add_widget(
            location_label
        )

        self.location_input = make_text_input(
            "π.χ. Αποθήκη - Ράφι 3"
        )

        self.location_input.size_hint = (
            0.82,
            0.13
        )

        self.location_input.pos_hint = {
            "center_x": 0.5,
            "top": 0.36
        }

        panel.add_widget(
            self.location_input
        )

        # -------------------------------------------------
        # SAVE BUTTON
        # -------------------------------------------------

        self.save_button = make_button(

            "ΑΠΟΘΗΚΕΥΣΗ",

            17,

            (
                0.03,
                0.18,
                0.40,
                1
            ),

            (
                1,
                1,
                1,
                1
            )
        )

        self.save_button.size_hint = (
            0.82,
            0.13
        )

        self.save_button.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.16
        }

        self.save_button.bind(
            on_press=self.save_object
        )

        panel.add_widget(
            self.save_button
        )

        root.add_widget(
            panel
        )

        # -------------------------------------------------
        # BACK BUTTON
        # -------------------------------------------------

        back_button = make_button(

            "ΠΙΣΩ",

            16,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.05,
                0.10,
                0.18,
                1
            )
        )

        back_button.size_hint = (
            0.40,
            0.09
        )

        back_button.pos_hint = {
            "center_x": 0.5,
            "y": 0.035
        }

        back_button.bind(
            on_press=self.go_back
        )

        root.add_widget(
            back_button
        )

        self.add_widget(
            root
        )

    # =====================================================
    # NEW OBJECT
    # =====================================================

    def prepare_new(self):

        self.editing_id = None

        self.header.text = (
            "ΠΡΟΣΘΗΚΗ ΑΝΤΙΚΕΙΜΕΝΟΥ"
        )

        self.save_button.text = (
            "ΑΠΟΘΗΚΕΥΣΗ"
        )

        self.name_input.text = ""

        self.category_input.text = ""

        self.location_input.text = ""

    # =====================================================
    # EDIT OBJECT
    # =====================================================

    def prepare_edit(
        self,
        object_id
    ):

        data = get_object(
            object_id
        )

        if not data:
            return

        self.editing_id = object_id

        self.header.text = (
            "ΕΠΕΞΕΡΓΑΣΙΑ ΑΝΤΙΚΕΙΜΕΝΟΥ"
        )

        self.save_button.text = (
            "ΑΠΟΘΗΚΕΥΣΗ ΑΛΛΑΓΩΝ"
        )

        self.name_input.text = (
            data[1] or ""
        )

        self.category_input.text = (
            data[2] or ""
        )

        self.location_input.text = (
            data[3] or ""
        )

    # =====================================================
    # SAVE
    # =====================================================

    def save_object(
        self,
        instance
    ):

        name = self.name_input.text.strip()

        category = (
            self.category_input.text.strip()
        )

        location = (
            self.location_input.text.strip()
        )

        # -------------------------------------------------
        # NAME REQUIRED
        # -------------------------------------------------

        if name == "":

            self.show_message(

                "ΛΕΙΠΕΙ ΤΟ ΟΝΟΜΑ",

                "Πρέπει να γράψεις το όνομα "
                "του αντικειμένου."
            )

            return

        # -------------------------------------------------
        # EDIT EXISTING
        # -------------------------------------------------

        if self.editing_id is not None:

            update_object(

                self.editing_id,

                name,

                category,

                location
            )

            self.prepare_new()

            self.manager.current = "search"

            search = self.manager.get_screen(
                "search"
            )

            search.load_objects()

            search.show_message(

                "ΑΠΟΘΗΚΕΥΤΗΚΕ",

                "Οι αλλαγές αποθηκεύτηκαν "
                "με επιτυχία."
            )

            return

        # -------------------------------------------------
        # ADD NEW
        # -------------------------------------------------

        add_object(

            name,

            category,

            location
        )

        self.prepare_new()

        self.show_message(

            "ΑΠΟΘΗΚΕΥΤΗΚΕ",

            "Το αντικείμενο προστέθηκε "
            "με επιτυχία."
        )

    # =====================================================
    # MESSAGE
    # =====================================================

    def show_message(
        self,
        title,
        message
    ):

        content = FloatLayout()

        text = Label(

            text=message,

            font_size=dp(17),

            color=(
                0.08,
                0.10,
                0.14,
                1
            ),

            halign="center",

            valign="middle",

            size_hint=(0.90, 0.55),

            pos_hint={
                "center_x": 0.5,
                "top": 0.88
            }
        )

        content.add_widget(
            text
        )

        ok = make_button(

            "OK",

            15,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.02,
                0.20,
                0.55,
                1
            )
        )

        ok.size_hint = (
            0.42,
            0.24
        )

        ok.pos_hint = {
            "center_x": 0.5,
            "y": 0.08
        }

        content.add_widget(
            ok
        )

        popup = Popup(

            title=title,

            content=content,

            size_hint=(0.82, 0.32),

            auto_dismiss=False
        )

        ok.bind(
            on_press=popup.dismiss
        )

        popup.open()

    # =====================================================
    # BACK
    # =====================================================

    def go_back(
        self,
        instance
    ):

        self.prepare_new()

        self.manager.current = "home"

    # =====================================================
    # BACKGROUND
    # =====================================================

    def update_bg(
        self,
        instance,
        value
    ):

        self.bg.pos = instance.pos

        self.bg.size = instance.size

    def update_panel(
        self,
        instance,
        value
    ):

        self.panel_bg.pos = instance.pos

        self.panel_bg.size = instance.size
        # =========================================================
# OBJECT CARD
# =========================================================

class ObjectCard(BoxLayout):

    def __init__(
        self,
        object_data,
        search_screen,
        **kwargs
    ):

        super().__init__(
            orientation="horizontal",
            spacing=dp(8),
            padding=[
                dp(12),
                dp(10),
                dp(8),
                dp(10)
            ],
            size_hint_y=None,
            height=dp(118),
            **kwargs
        )

        self.object_id = object_data[0]

        self.search_screen = search_screen

        name = object_data[1] or ""

        category = (
            object_data[2]
            or
            "Χωρίς είδος"
        )

        location = (
            object_data[3]
            or
            "Χωρίς σημείο"
        )

        # -------------------------------------------------
        # CARD BACKGROUND
        # -------------------------------------------------

        with self.canvas.before:

            Color(
                0.055,
                0.085,
                0.14,
                1
            )

            self.card_bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

            Color(
                0.10,
                0.25,
                0.42,
                1
            )

            self.card_line = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(14)
                ),
                width=1
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # -------------------------------------------------
        # INFORMATION
        # -------------------------------------------------

        info = BoxLayout(
            orientation="vertical",
            spacing=dp(1),
            size_hint_x=0.70
        )

        name_label = Label(
            text=name,
            font_size=dp(19),
            bold=True,
            color=(
                1,
                1,
                1,
                1
            ),
            halign="left",
            valign="middle"
        )

        name_label.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                instance.size
            )
        )

        info.add_widget(
            name_label
        )

        category_label = Label(
            text="Είδος: " + category,
            font_size=dp(14),
            color=(
                0.55,
                0.72,
                0.90,
                1
            ),
            halign="left",
            valign="middle"
        )

        category_label.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                instance.size
            )
        )

        info.add_widget(
            category_label
        )

        location_label = Label(
            text="Σημείο: " + location,
            font_size=dp(14),
            color=(
                0.72,
                0.76,
                0.82,
                1
            ),
            halign="left",
            valign="middle"
        )

        location_label.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                instance.size
            )
        )

        info.add_widget(
            location_label
        )

        self.add_widget(
            info
        )

        # -------------------------------------------------
        # ACTIONS
        # -------------------------------------------------

        actions = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_x=0.30
        )

        # -------------------------------------------------
        # EDIT
        # -------------------------------------------------

        edit_button = make_button(
            "ΕΠΕΞΕΡΓΑΣΙΑ",
            11,
            (
                1,
                1,
                1,
                1
            ),
            (
                0.02,
                0.20,
                0.55,
                1
            )
        )

        edit_button.size_hint_y = 0.5

        edit_button.bind(
            on_press=self.edit_object
        )

        actions.add_widget(
            edit_button
        )

        # -------------------------------------------------
        # DELETE
        # -------------------------------------------------

        delete_button = make_button(
            "ΔΙΑΓΡΑΦΗ",
            11,
            (
                1,
                1,
                1,
                1
            ),
            (
                0.65,
                0.08,
                0.08,
                1
            )
        )

        delete_button.size_hint_y = 0.5

        delete_button.bind(
            on_press=self.ask_delete
        )

        actions.add_widget(
            delete_button
        )

        self.add_widget(
            actions
        )

    # =====================================================
    # BACKGROUND
    # =====================================================

    def update_background(
        self,
        instance,
        value
    ):

        self.card_bg.pos = instance.pos

        self.card_bg.size = instance.size

        self.card_line.rounded_rectangle = (
            instance.x,
            instance.y,
            instance.width,
            instance.height,
            dp(14)
        )

    # =====================================================
    # EDIT
    # =====================================================

    def edit_object(
        self,
        instance
    ):

        add_screen = self.search_screen.manager.get_screen(
            "add"
        )

        add_screen.prepare_edit(
            self.object_id
        )

        self.search_screen.manager.current = "add"

    # =====================================================
    # DELETE CONFIRMATION
    # =====================================================

    def ask_delete(
        self,
        instance
    ):

        content = FloatLayout()

        message = Label(
            text=
            "Θέλεις σίγουρα να διαγράψεις\n"
            "αυτό το αντικείμενο;",

            font_size=dp(17),

            color=(
                0.08,
                0.10,
                0.14,
                1
            ),

            halign="center",

            valign="middle",

            size_hint=(0.90, 0.55),

            pos_hint={
                "center_x": 0.5,
                "top": 0.88
            }
        )

        content.add_widget(
            message
        )

        yes_button = make_button(
            "ΔΙΑΓΡΑΦΗ",
            13,
            (
                1,
                1,
                1,
                1
            ),
            (
                0.65,
                0.08,
                0.08,
                1
            )
        )

        yes_button.size_hint = (
            0.40,
            0.24
        )

        yes_button.pos_hint = {
            "x": 0.08,
            "y": 0.08
        }

        content.add_widget(
            yes_button
        )

        no_button = make_button(
            "ΑΚΥΡΩΣΗ",
            13,
            (
                1,
                1,
                1,
                1
            ),
            (
                0.02,
                0.20,
                0.55,
                1
            )
        )

        no_button.size_hint = (
            0.40,
            0.24
        )

        no_button.pos_hint = {
            "right": 0.92,
            "y": 0.08
        }

        content.add_widget(
            no_button
        )

        popup = Popup(
            title="ΕΠΙΒΕΒΑΙΩΣΗ",
            content=content,
            size_hint=(0.84, 0.34),
            auto_dismiss=False
        )

        no_button.bind(
            on_press=popup.dismiss
        )

        yes_button.bind(
            on_press=lambda x:
            self.confirm_delete(
                popup
            )
        )

        popup.open()

    # =====================================================
    # DELETE
    # =====================================================

    def confirm_delete(
        self,
        popup
    ):

        delete_object(
            self.object_id
        )

        popup.dismiss()

        self.search_screen.load_objects()

        self.search_screen.update_home_statistics()


# =========================================================
# SEARCH SCREEN
# =========================================================

class SearchScreen(Screen):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(**kwargs)

        root = FloatLayout()

        # -------------------------------------------------
        # BACKGROUND
        # -------------------------------------------------

        with root.canvas.before:

            Color(
                0.025,
                0.055,
                0.10,
                1
            )

            self.bg = RoundedRectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = Label(
            text="ΑΝΑΖΗΤΗΣΗ",
            font_size=dp(30),
            bold=True,
            color=(
                1,
                1,
                1,
                1
            ),
            size_hint=(1, 0.10),
            pos_hint={
                "center_x": 0.5,
                "top": 0.97
            }
        )

        root.add_widget(
            title
        )

        # -------------------------------------------------
        # SEARCH INPUT
        # -------------------------------------------------

        self.search_input = make_text_input(
            "Γράψε τι ψάχνεις..."
        )

        self.search_input.size_hint = (
            0.82,
            0.09
        )

        self.search_input.pos_hint = {
            "center_x": 0.5,
            "top": 0.85
        }

        root.add_widget(
            self.search_input
        )

        self.search_input.bind(
            text=self.on_search_text
        )

        # -------------------------------------------------
        # RESULTS COUNT
        # -------------------------------------------------

        self.results_label = Label(
            text="0 αντικείμενα",
            font_size=dp(14),
            color=(
                0.60,
                0.70,
                0.82,
                1
            ),
            size_hint=(0.82, 0.05),
            pos_hint={
                "center_x": 0.5,
                "top": 0.745
            },
            halign="left"
        )

        root.add_widget(
            self.results_label
        )

        # -------------------------------------------------
        # SCROLL VIEW
        # -------------------------------------------------

        self.scroll = ScrollView(
            size_hint=(0.92, 0.58),
            pos_hint={
                "center_x": 0.5,
                "top": 0.72
            },
            do_scroll_x=False,
            bar_width=dp(4)
        )

        self.list_box = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=[
                dp(2),
                dp(2),
                dp(2),
                dp(15)
            ],
            size_hint_y=None
        )

        self.list_box.bind(
            minimum_height=self.list_box.setter(
                "height"
            )
        )

        self.scroll.add_widget(
            self.list_box
        )

        root.add_widget(
            self.scroll
        )

        # -------------------------------------------------
        # BACK BUTTON
        # -------------------------------------------------

        back_button = make_button(
            "ΠΙΣΩ",
            15,
            (
                1,
                1,
                1,
                1
            ),
            (
                0.05,
                0.10,
                0.18,
                1
            )
        )

        back_button.size_hint = (
            0.40,
            0.09
        )

        back_button.pos_hint = {
            "center_x": 0.5,
            "y": 0.035
        }

        back_button.bind(
            on_press=self.go_back
        )

        root.add_widget(
            back_button
        )

        self.add_widget(
            root
        )

    # =====================================================
    # LOAD OBJECTS
    # =====================================================

    def load_objects(
        self,
        search=None
    ):

        if search is None:
            search = self.search_input.text

        results = get_objects(
            search=search
        )

        self.list_box.clear_widgets()

        for item in results:

            card = ObjectCard(
                item,
                self
            )

            self.list_box.add_widget(
                card
            )

        count = len(results)

        if count == 1:
            self.results_label.text = (
                "1 αντικείμενο"
            )

        else:
            self.results_label.text = (
                str(count)
                + " αντικείμενα"
            )

    # =====================================================
    # LIVE SEARCH
    # =====================================================

    def on_search_text(
        self,
        instance,
        value
    ):

        self.load_objects(
            value
        )

    # =====================================================
    # HOME STATISTICS
    # =====================================================

    def update_home_statistics(self):

        home = self.manager.get_screen(
            "home"
        )

        home.update_statistics()

    # =====================================================
    # MESSAGE
    # =====================================================

    def show_message(
        self,
        title,
        message
    ):

        content = FloatLayout()

        label = Label(
            text=message,
            font_size=dp(17),
            color=(
                0.08,
                0.10,
                0.14,
                1
            ),
            halign="center",
            valign="middle",
            size_hint=(0.90, 0.55),
            pos_hint={
                "center_x": 0.5,
                "top": 0.88
            }
        )

        content.add_widget(
            label
        )

        ok = make_button(
            "OK",
            15,
            (
                1,
                1,
                1,
                1
            ),
            (
                0.02,
                0.20,
                0.55,
                1
            )
        )

        ok.size_hint = (
            0.42,
            0.24
        )

        ok.pos_hint = {
            "center_x": 0.5,
            "y": 0.08
        }

        content.add_widget(
            ok
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.82, 0.32),
            auto_dismiss=False
        )

        ok.bind(
            on_press=popup.dismiss
        )

        popup.open()

    # =====================================================
    # BACK
    # =====================================================

    def go_back(
        self,
        instance
    ):

        self.search_input.text = ""

        self.list_box.clear_widgets()

        self.manager.current = "home"

    # =====================================================
    # BACKGROUND
    # =====================================================

    def update_bg(
        self,
        instance,
        value
    ):

        self.bg.pos = instance.pos

        self.bg.size = instance.size
        # =========================================================
# FILTER SCREEN
# =========================================================

class FilterScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        root = FloatLayout()

        # -------------------------------------------------
        # BACKGROUND
        # -------------------------------------------------

        with root.canvas.before:

            Color(
                0.025,
                0.055,
                0.10,
                1
            )

            self.bg = RoundedRectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = Label(
            text="ΚΑΤΗΓΟΡΙΕΣ ΚΑΙ ΣΗΜΕΙΑ",

            font_size=dp(27),

            bold=True,

            color=(
                1,
                1,
                1,
                1
            ),

            size_hint=(1, 0.10),

            pos_hint={
                "center_x": 0.5,
                "top": 0.96
            }
        )

        root.add_widget(title)

        # -------------------------------------------------
        # CATEGORY TITLE
        # -------------------------------------------------

        category_title = Label(
            text="ΕΙΔΗ",

            font_size=dp(18),

            bold=True,

            color=(
                0.55,
                0.72,
                0.90,
                1
            ),

            size_hint=(0.82, 0.07),

            pos_hint={
                "center_x": 0.5,
                "top": 0.86
            },

            halign="left"
        )

        root.add_widget(category_title)

        # -------------------------------------------------
        # CATEGORY SCROLL
        # -------------------------------------------------

        self.category_scroll = ScrollView(
            size_hint=(0.82, 0.26),

            pos_hint={
                "center_x": 0.5,
                "top": 0.79
            },

            do_scroll_x=False
        )

        self.category_box = BoxLayout(
            orientation="vertical",

            spacing=dp(6),

            size_hint_y=None,

            padding=[
                0,
                dp(2)
            ]
        )

        self.category_box.bind(
            minimum_height=self.category_box.setter(
                "height"
            )
        )

        self.category_scroll.add_widget(
            self.category_box
        )

        root.add_widget(
            self.category_scroll
        )

        # -------------------------------------------------
        # LOCATION TITLE
        # -------------------------------------------------

        location_title = Label(
            text="ΣΗΜΕΙΑ",

            font_size=dp(18),

            bold=True,

            color=(
                0.55,
                0.72,
                0.90,
                1
            ),

            size_hint=(0.82, 0.07),

            pos_hint={
                "center_x": 0.5,
                "top": 0.48
            },

            halign="left"
        )

        root.add_widget(location_title)

        # -------------------------------------------------
        # LOCATION SCROLL
        # -------------------------------------------------

        self.location_scroll = ScrollView(
            size_hint=(0.82, 0.26),

            pos_hint={
                "center_x": 0.5,
                "top": 0.41
            },

            do_scroll_x=False
        )

        self.location_box = BoxLayout(
            orientation="vertical",

            spacing=dp(6),

            size_hint_y=None,

            padding=[
                0,
                dp(2)
            ]
        )

        self.location_box.bind(
            minimum_height=self.location_box.setter(
                "height"
            )
        )

        self.location_scroll.add_widget(
            self.location_box
        )

        root.add_widget(
            self.location_scroll
        )

        # -------------------------------------------------
        # BACK
        # -------------------------------------------------

        back_button = make_button(
            "ΠΙΣΩ",

            15,

            (
                1,
                1,
                1,
                1
            ),

            (
                0.05,
                0.10,
                0.18,
                1
            )
        )

        back_button.size_hint = (
            0.40,
            0.09
        )

        back_button.pos_hint = {
            "center_x": 0.5,
            "y": 0.035
        }

        back_button.bind(
            on_press=self.go_back
        )

        root.add_widget(
            back_button
        )

        self.add_widget(root)

    # =====================================================
    # REFRESH FILTERS
    # =====================================================

    def refresh_filters(self):

        self.category_box.clear_widgets()

        self.location_box.clear_widgets()

        categories = get_categories()

        locations = get_locations()

        # -------------------------------------------------
        # CATEGORIES
        # -------------------------------------------------

        if not categories:

            label = Label(
                text="Δεν υπάρχουν καταχωρημένα είδη.",

                font_size=dp(14),

                color=(
                    0.60,
                    0.65,
                    0.72,
                    1
                ),

                size_hint_y=None,

                height=dp(38)
            )

            self.category_box.add_widget(
                label
            )

        else:

            for category in categories:

                button = make_button(
                    category,

                    14,

                    (
                        1,
                        1,
                        1,
                        1
                    ),

                    (
                        0.02,
                        0.20,
                        0.55,
                        1
                    )
                )

                button.size_hint_y = None

                button.height = dp(42)

                button.bind(
                    on_press=lambda instance,
                    value=category:
                    self.open_category(
                        value
                    )
                )

                self.category_box.add_widget(
                    button
                )

        # -------------------------------------------------
        # LOCATIONS
        # -------------------------------------------------

        if not locations:

            label = Label(
                text="Δεν υπάρχουν καταχωρημένα σημεία.",

                font_size=dp(14),

                color=(
                    0.60,
                    0.65,
                    0.72,
                    1
                ),

                size_hint_y=None,

                height=dp(38)
            )

            self.location_box.add_widget(
                label
            )

        else:

            for location in locations:

                button = make_button(
                    location,

                    14,

                    (
                        1,
                        1,
                        1,
                        1
                    ),

                    (
                        0.05,
                        0.10,
                        0.18,
                        1
                    )
                )

                button.size_hint_y = None

                button.height = dp(42)

                button.bind(
                    on_press=lambda instance,
                    value=location:
                    self.open_location(
                        value
                    )
                )

                self.location_box.add_widget(
                    button
                )

    # =====================================================
    # OPEN CATEGORY
    # =====================================================

    def open_category(
        self,
        category
    ):

        search = self.manager.get_screen(
            "search"
        )

        search.search_input.text = ""

        results = get_objects(
            category=category
        )

        search.list_box.clear_widgets()

        for item in results:

            card = ObjectCard(
                item,
                search
            )

            search.list_box.add_widget(
                card
            )

        search.results_label.text = (
            str(len(results))
            + " αντικείμενα"
        )

        self.manager.current = "search"

    # =====================================================
    # OPEN LOCATION
    # =====================================================

    def open_location(
        self,
        location
    ):

        search = self.manager.get_screen(
            "search"
        )

        search.search_input.text = ""

        results = get_objects(
            location=location
        )

        search.list_box.clear_widgets()

        for item in results:

            card = ObjectCard(
                item,
                search
            )

            search.list_box.add_widget(
                card
            )

        search.results_label.text = (
            str(len(results))
            + " αντικείμενα"
        )

        self.manager.current = "search"

    # =====================================================
    # BACK
    # =====================================================

    def go_back(
        self,
        instance
    ):

        self.manager.current = "home"

    # =====================================================
    # BACKGROUND
    # =====================================================

    def update_bg(
        self,
        instance,
        value
    ):

        self.bg.pos = instance.pos

        self.bg.size = instance.size


# =========================================================
# SCREEN MANAGER
# =========================================================

class MainScreenManager(
    ScreenManager
):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(**kwargs)

        # -------------------------------------------------
        # HOME
        # -------------------------------------------------

        self.add_widget(
            HomeScreen(
                name="home"
            )
        )

        # -------------------------------------------------
        # ADD / EDIT
        # -------------------------------------------------

        self.add_widget(
            AddObjectScreen(
                name="add"
            )
        )

        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        self.add_widget(
            SearchScreen(
                name="search"
            )
        )

        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        self.add_widget(
            FilterScreen(
                name="filters"
            )
        )

        self.current = "home"


# =========================================================
# APP
# =========================================================

class TiEhoApp(App):

    def build(self):

        self.title = "ΤΙ ΕΧΩ;"

        create_database()

        return MainScreenManager()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    TiEhoApp().run()