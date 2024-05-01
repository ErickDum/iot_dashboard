import reflex as rx

from dashboard.styles import BACKGROUND_COLOR, THEME, STYLESHEETS

from dashboard.pages.index import index

app = rx.App(
    theme=THEME,
    stylesheets=STYLESHEETS,
    background_color=BACKGROUND_COLOR,
)

app.add_page(index, route="/")