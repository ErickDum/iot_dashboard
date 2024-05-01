import reflex as rx
from dashboard.styles import FONT_FAMILY

def navbar(heading: str) -> rx.Component:
    return rx.hstack(
        rx.heading(heading, font_family=FONT_FAMILY, size="6"),
        # Properties for create a navbar
        position="fixed",
        width="calc(100% - 250px)",
        top="0px",
        padding_x="2em",
        padding_top="2em",
        padding_bottom="1em",
        backdrop_filter="blur(10px)",
        z_index="1000",
    )