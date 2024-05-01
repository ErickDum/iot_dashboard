import reflex as rx
from dashboard.components.cards.card import card

class Line(rx.Base):
    data_key: str
    type_= "linear"
    stroke: str
    #isAnimationActive={false}

def line_chart(data: list[dict], data_key: str, lines: list[Line]) -> rx.Component:
    return card(
        rx.recharts.line_chart(
            *[
                rx.recharts.line(data_key=line.data_key, type_=line.type_, stroke=line.stroke)
                for line in lines
            ],
            rx.recharts.x_axis(data_key=data_key),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            rx.recharts.cartesian_grid(),
            data=data,
            height=300,
        )
    )