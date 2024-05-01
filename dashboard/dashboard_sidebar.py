import reflex as rx
from dashboard.components.sidebar.sidebar import sidebar
from dashboard.components.sidebar.sidebar_link import sidebar_link

dashboard_sidebar = sidebar(
    sidebar_link(text="Dashboard", href="/", icon="bar_chart_3"),
    logo_src="/logo.png",
    heading="Irrigation System",
)