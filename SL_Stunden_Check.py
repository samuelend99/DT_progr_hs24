import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from main import get_projects, get_time_entries, get_services, convert_seconds_to_hours, load_all_project_budgets

def set_sidebar_style():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #d0d0d0; /* RAL 7045 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Stundenformatierung für Stunden und Minuten
def format_hours_and_minutes(hours):
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m}m"

# Funktion für die Farbgebung
# Funktion für die Farbgebung
def color_remaining_hours(val):
    if isinstance(val, str) and 'h' in val:  # Umrechnung von "Xh Ym" zurück in float
        h, m = map(int, val.replace('h', '').replace('m', '').split())
        val = h + m / 60

    if val == 0:  # Bedingung für "0h 0m"
        return 'background-color: white'  # Weißer Hintergrund
    elif val > 15:
        return 'background-color: green'  # Grüner Hintergrund
    elif 0 < val <= 15:
        return 'background-color: orange'  # Oranger Hintergrund
    else:
        return 'background-color: red'  # Roter Hintergrund


# Funktion für die Hauptseite
def main_page():
    set_sidebar_style()
    with st.sidebar:
        st.header("Menu")
        if st.button("Projekt wählen"):
            st.session_state["page"] = "main"
        if st.button("Übersicht"):
            st.session_state["page"] = "chart"

    col1, col2 = st.columns([9, 5])
    with col1:
        pass
    with col2:
        st.image("Logo_MH.jpg", use_column_width=True)

    st.title("Stunden-Check")

    projects = get_projects()
    if not projects:
        st.error("Keine Projekte gefunden oder Fehler beim Abruf der Projekte.")
        st.stop()

    project_options = {proj['name']: proj['id'] for proj in projects}
    selected_project_name = st.selectbox("Wähle ein Projekt:", list(project_options.keys()))
    project_id = project_options[selected_project_name]

    time_range_option = st.radio(
        "Zeitraum auswählen:",
        ("Benutzerdefinierter Zeitraum", "Gesamter Zeitraum bis heute")
    )

    if time_range_option == "Benutzerdefinierter Zeitraum":
        time_since = st.date_input("Von:", value=None)
        time_until = st.date_input("Bis:", value=None)
    else:
        time_since = datetime.date(2000, 1, 1)
        time_until = datetime.date.today()

    if st.button("Check"):
        st.session_state.update({
            "project_id": project_id,
            "project_name": selected_project_name,
            "time_since": time_since,
            "time_until": time_until,
            "page": "results"
        })
        st.session_state['trigger_update'] = not st.session_state.get('trigger_update', False)

# Funktion für die Ergebnisseite (Tabelle)
def results_page():
    set_sidebar_style()
    with st.sidebar:
        st.header("Menu")
        if st.button("Projekt wählen"):
            st.session_state["page"] = "main"
        if st.button("Übersicht"):
            st.session_state["page"] = "chart"

    project_id = st.session_state.get("project_id")
    selected_project_name = st.session_state.get("project_name")
    time_since = st.session_state.get("time_since")
    time_until = st.session_state.get("time_until")

    entries = get_time_entries(time_since, time_until, project_id)
    entries_df = pd.DataFrame(entries)

    if entries_df.empty:
        st.warning("Keine Zeiteinträge für dieses Projekt in diesem Zeitraum gefunden.")
        st.stop()

    if 'projects_id' in entries_df.columns:
        entries_df.rename(columns={'projects_id': 'project_id'}, inplace=True)

    entries_df["used_hours"] = entries_df["duration"] / 3600.0

    services = get_services()
    services_df = pd.DataFrame(services)
    service_mapping = dict(zip(services_df["id"], services_df["name"]))
    entries_df["service_name"] = entries_df["services_id"].map(service_mapping)

    used_hours_df = entries_df.groupby(["project_id", "service_name"], as_index=False)["used_hours"].sum()

    all_budgets_df = load_all_project_budgets()
    project_budget_df = all_budgets_df[all_budgets_df["project_id"] == project_id]

    if project_budget_df.empty:
        st.warning("Keine Budgetdaten für dieses Projekt gefunden.")
        st.stop()

    merged_df = pd.merge(project_budget_df, used_hours_df, left_on=["project_id", "phase_name"],
                         right_on=["project_id", "service_name"], how="left")

    merged_df["used_hours"] = merged_df["used_hours"].fillna(0)
    merged_df["remaining_hours"] = merged_df["budget_hours"] - merged_df["used_hours"]

    display_df = merged_df[["phase_name", "budget_hours", "used_hours", "remaining_hours"]]
    display_df_for_display = display_df.rename(columns={
        "phase_name": "Leistung",
        "budget_hours": "Geplante Stunden",
        "used_hours": "Verbrauchte Stunden",
        "remaining_hours": "Verbleibende Stunden"
    })

    columns_to_format = ["Geplante Stunden", "Verbrauchte Stunden", "Verbleibende Stunden"]
    for col in columns_to_format:
        display_df_for_display[col] = display_df_for_display[col].apply(format_hours_and_minutes)

    # Tabelle anzeigen ohne Nummerierung
    row_height = 38
    max_height = 800
    calculated_height = min(len(display_df_for_display) * row_height, max_height)

# Index entfernen
    display_df_for_display.reset_index(drop=True, inplace=True)

# Tabelle mit st.table anzeigen (ohne sichtbaren Index)
    st.markdown("### Stundenübersicht")
    st.table(display_df_for_display.style.applymap(color_remaining_hours, subset=["Verbleibende Stunden"]))



    total_budget = merged_df["budget_hours"].sum()
    total_used = merged_df["used_hours"].sum()
    total_remaining = merged_df["remaining_hours"].sum()

    st.markdown("**Gesamtübersicht:**")
    st.write(f"**Budget insgesamt:** {format_hours_and_minutes(total_budget)}")
    st.write(f"**Verbraucht:** {format_hours_and_minutes(total_used)}")
    st.markdown(f"<h3 style='font-size:24px; font-weight:bold;'>Verbleibend: {format_hours_and_minutes(total_remaining)}</h3>", unsafe_allow_html=True)

def chart_page():
    set_sidebar_style()
    with st.sidebar:
        st.header("Menu")
        if st.button("Projekt wählen"):
            st.session_state["page"] = "main"
        if st.button("Tabelle anzeigen"):
            st.session_state["page"] = "results"

    project_id = st.session_state.get("project_id")
    time_since = st.session_state.get("time_since")
    time_until = st.session_state.get("time_until")

    # Zeiteinträge abrufen
    entries = get_time_entries(time_since, time_until, project_id)
    entries_df = pd.DataFrame(entries)

    if entries_df.empty:
        st.warning("Keine Zeiteinträge für dieses Projekt in diesem Zeitraum gefunden.")
        st.stop()

    entries_df["used_hours"] = entries_df["duration"] / 3600.0

    # Leistungen abrufen und Mapping erstellen
    services = get_services()
    services_df = pd.DataFrame(services)
    service_mapping = dict(zip(services_df["id"], services_df["name"]))
    entries_df["service_name"] = entries_df["services_id"].map(service_mapping)

    # Verbrauchte Stunden pro Leistung aggregieren
    used_hours_df = entries_df.groupby("service_name", as_index=False)["used_hours"].sum()

    # Budget abrufen und filtern
    all_budgets_df = load_all_project_budgets()
    project_budget_df = all_budgets_df[all_budgets_df["project_id"] == project_id]

    if project_budget_df.empty:
        st.warning("Keine Budgetdaten für dieses Projekt gefunden.")
        st.stop()

    # Nur Leistungen im Budget und in den Zeiteinträgen behalten
    budget_services = project_budget_df["phase_name"].unique()
    used_hours_df = used_hours_df[used_hours_df["service_name"].isin(budget_services)]

    # Kreisdiagramm für Stunden pro Leistung
    st.title("Übersicht")
    fig1 = px.pie(used_hours_df, values="used_hours", names="service_name", title="Stunden pro Leistung")
    st.plotly_chart(fig1)

    # Kreisdiagramm: Gebrauchte Stunden vs. Gesamtbudget
    total_used_hours = entries_df["used_hours"].sum()
    total_budget_hours = project_budget_df["budget_hours"].sum()
    remaining_budget_hours = total_budget_hours - total_used_hours

    if remaining_budget_hours < 0:
        remaining_budget_hours = 0  # Verhindern, dass negative Werte auftreten

    budget_data = pd.DataFrame({
        "Kategorie": ["Verbraucht", "Übrig"],
        "Stunden": [total_used_hours, remaining_budget_hours]
    })

    fig2 = px.pie(budget_data, values="Stunden", names="Kategorie", 
                  title="Gebrauchte Stunden vs. Gesamtbudget")
    st.plotly_chart(fig2)



# Seitenwechsel-Logik
if "page" not in st.session_state:
    st.session_state["page"] = "main"

if st.session_state["page"] == "main":
    main_page()
elif st.session_state["page"] == "results":
    results_page()
elif st.session_state["page"] == "chart":
    chart_page()
