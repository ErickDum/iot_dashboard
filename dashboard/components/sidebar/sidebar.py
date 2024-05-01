import reflex as rx
from dashboard.styles import FONT_FAMILY

def sidebar(
    *sidebar_links,
    **props,
) -> rx.Component:
    logo_src = props.get("logo_src", "/logo.png")
    heading = props.get("heading", "NOT SET")
    return rx.vstack(
        rx.hstack(
            rx.image(src=logo_src, height="72px", border_radius="8px"),
            rx.heading(
                heading, 
                font_family=FONT_FAMILY, 
                size="7"
            ),
            width="100%",
        ),
        rx.divider(margin_y="3"),
        rx.vstack(
            *sidebar_links,
            padding_y="1em",
        ),
        # Properties for make a sidebar
        width="250px",
        position="fixed",
        height="100%",
        left="0px",
        top="0px",
        align_items="left",
        z_index="10",
        backdrop_filter="blur(10px)",
        padding="2em",
    )