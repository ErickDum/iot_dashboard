import reflex as rx

from dashboard.components.cards.card import card

def stat_card(title: str, stat:list) -> rx.Component:
    return card(
        rx.hstack(
            rx.vstack(
                rx.text(title),
                rx.hstack(
                    rx.chakra.stat(
                    rx.chakra.stat_number(stat[0], color="var(--green-9)"),
                    ),
                    rx.text(stat[1], color="var(--green-9)"),
                )
            ),
        ),
        width="90%",
    )