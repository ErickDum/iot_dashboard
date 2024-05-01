import reflex as rx
import asyncio
import paho.mqtt.client as mqtt
import datetime

from dashboard.styles import BACKGROUND_COLOR, FONT_FAMILY
from dashboard.dashboard_sidebar import dashboard_sidebar
from dashboard.components.navbar import navbar

from dashboard.components.cards.stat_card import stat_card
from dashboard.components.cards.card import card
from dashboard.components.line_chart import line_chart
from dashboard.components.line_chart import Line

lines = [
    Line(data_key="soil_moisture", stroke="#006400"), 
    Line(data_key="goal_humidity", stroke="#FF0000"),  
]

class IndexState(rx.State):
    chart_data: list[dict]
    temperature: int = 0
    ambiental_humidity: int = 0
    goal_humidity: int = 0
    pump_activations: int = 0

    def on_connect(self, client, userdata, flags, reason_code, properties):
        client.subscribe("Salida/#")

    def on_message(self, client, userdata, msg):
        client.publish("Entrada", self.goal_humidity)
        data = str(msg.payload)[2:-1].split(",")
        soil = data[0]
        self.ambiental_humidity = data[1]
        self.temperature = data[2]

        if int(self.goal_humidity) > int(soil):
            self.pump_activations +=1

        if len(self.chart_data) >= 40:
            self.chart_data.pop(0)
        self.chart_data.append({"time": datetime.datetime.now().strftime("%H:%M:%S"), "soil_moisture": soil, "goal_humidity": self.goal_humidity })
    
    
    def set_goal_humidity(self, form_data: dict[str, str]):
        self.goal_humidity = form_data["humedad"]

    @rx.background
    async def refresh_data(self):
        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.on_connect = self.on_connect   
        mqttc.on_message = self.on_message
        mqttc.connect("192.168.213.150", 1883, 60)

        while True:
            async with self:
                mqttc.loop()
            await asyncio.sleep(0.8)

def content_grid():
    return rx.chakra.grid(
        rx.chakra.grid_item(
            stat_card(title="Temperatura Actual", stat=[IndexState.temperature, "°C"]), 
            col_span=1, row_span=1
        ),
        rx.chakra.grid_item(
            stat_card(title="Humedad Ambiental", stat=[IndexState.ambiental_humidity, "%"]), 
            col_span=1, row_span=1
        ),
        rx.chakra.grid_item(
            stat_card(title="Activaciones de la bomba", stat=[IndexState.pump_activations, "veces"]), 
            col_span=1, row_span=1
        ),
        rx.chakra.grid_item(
            card(
                rx.form(
                    rx.vstack(
                        rx.text("Setear humedad"),
                        rx.hstack(
                            rx.input(placeholder="Ingrese un valor", id="humedad"),
                            rx.button("Submit"),
                        ),
                    ),
                    reset_on_submit=True,
                    on_submit=IndexState.set_goal_humidity,
                )
            ),
            col_span=1, row_span=1
        ),
        rx.chakra.grid_item(rx.heading("Humedad del suelo", padding_top="1em"), col_span=4, row_span=1),
        rx.chakra.grid_item(line_chart(IndexState.chart_data, "time", lines), col_span=4, row_span=1),
        template_rows="repeat(1, 1fr)",
        template_columns="repeat(4, 1fr)",
    )

@rx.page(on_load=IndexState.refresh_data)
def index() -> rx.Component:
    return rx.box(
        dashboard_sidebar,
        rx.box(
            navbar(heading = "Dashboard"),
            rx.box(
                content_grid(),
                margin_top="calc(50px + 2em)",
                padding="2em",
            ),
            padding_left="250px",
        ),
        #rx.logo(),
        background_color=BACKGROUND_COLOR,
        font_family=FONT_FAMILY,
        padding_bottom="4em",
    )