from shiny import App, ui, reactive
from shiny_calendar import shiny_calendar, render_shiny_calendar
from shiny_calendar import shiny_calendar_call_js_func

app_ui = ui.page_fluid(
    ui.layout_columns(
        [
            ui.h2("shiny-calendar demo"),
            ui.markdown("""
            - **FullCalendar:** easy init and loading of events, navigation using built-in buttons
            - **Interactivity**: select a date or an event to see the data sent back to the server
            - **Custom JS calls**: change event color on click, select a date and click on "Add Event"
            """),
        ],
        [
            ui.br(),
            ui.input_action_button("button_add_event", "Add Event"),
            ui.input_checkbox("msg_checkbox", "Show data sent to server", False),
        ],
        col_widths=(7, -1, 3),
    ),
    ui.card(shiny_calendar("my_calendar")),
)


def server(input, output, session):
    event_counter = 0
    selected_date = None

    @reactive.effect
    @reactive.event(input.button_add_event)
    async def _():
        nonlocal selected_date
        if not selected_date:
            ui.notification_show(
                "You must select a date in the calendar before adding an event",
                type="warning",
                duration=2,
            )
            return
        nonlocal event_counter
        event_counter = event_counter + 1
        js_func = (
            "calendar.addEvent({id: 'id_%d', title: 'some event %d', start: '%s', end: '%s'});"
            % (event_counter, event_counter, selected_date[0], selected_date[1])
        )
        await shiny_calendar_call_js_func(session, "my_calendar", js_func)

    @reactive.effect
    async def _():
        nonlocal selected_date
        msg = input.my_calendar()
        if msg["type"] == "eventClick":
            # if eventClick, set the border and background of then event to red
            # the proper way would be to use eventClassNames, this is just an example
            event_id = msg["data"]["event"]["id"]
            js_func = f"""
                const calEvent = calendar.getEventById("{event_id}");
                calEvent.setProp("backgroundColor", "red");
                calEvent.setProp("borderColor", "red");
                """
            await shiny_calendar_call_js_func(session, "my_calendar", js_func)
        elif msg["type"] == "select":
            selected_date = (msg["data"]["start"], msg["data"]["end"])

    @reactive.effect
    @reactive.event(input.my_calendar)
    def _():
        if input.msg_checkbox():
            m = ui.modal(
                f"{input.my_calendar()}",
                title="Data sent to server:",
                size="l",
                easy_close=True,
            )
            ui.modal_show(m)

    @render_shiny_calendar
    def my_calendar():
        return [
            {
                # react on event click
                "eventClick": "",
                # react on date click
                # "dateClick" : "",
                # react on date/time selection
                "select": "",
                # react on date/time de-selection
                # "unselect" : "",
                # react on event add
                # "eventAdd": "",
                # react on event change
                # "eventChange": "",
                # react on event remove
                # "eventRemove": "",
                # react on events set
                # "eventsSet": "",
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "timeGridDay,timeGridWeek listDay,listWeek dayGridDay,dayGridWeek,dayGridMonth",
                },
                "views": {
                    "timeGridDay": {"buttonText": "time D"},
                    "timeGridWeek": {"buttonText": "time W"},
                    "listDay": {"buttonText": "list D"},
                    "listWeek": {"buttonText": "list W"},
                    "dayGridDay": {"buttonText": "day D"},
                    "dayGridWeek": {"buttonText": "day W"},
                    "dayGridMonth": {"buttonText": "day M"},
                },
                "initialDate": "2024-07-01",
                "firstDay": 1,
                "allDaySlot": False,
                "editable": True,
                "selectable": True,
                "dayMaxEvents": True,
                "initialView": "timeGridWeek",
                "events": [
                    {
                        "id": "id1",
                        "title": "Event 1",
                        "start": "2024-07-03",
                        "end": "2024-07-05",
                    },
                    {
                        "id": "id2",
                        "title": "Event 2",
                        "start": "2024-07-01",
                        "end": "2024-07-10",
                    },
                    {
                        "id": "id3",
                        "title": "Event 3",
                        "start": "2024-07-20",
                        "end": "2024-07-20",
                    },
                    {
                        "id": "id4",
                        "title": "Event 4",
                        "start": "2024-07-23",
                        "end": "2024-07-25",
                    },
                    {
                        "id": "id5",
                        "title": "Event 5",
                        "start": "2024-07-29",
                        "end": "2024-07-30",
                    },
                    {
                        "id": "id6",
                        "title": "Event 6",
                        "start": "2024-07-28",
                        "end": "2024-07-20",
                    },
                    {
                        "id": "id7",
                        "title": "Event 7",
                        "start": "2024-07-01T08:30:00",
                        "end": "2024-07-01T10:30:00",
                    },
                    {
                        "id": "id8",
                        "title": "Event 8",
                        "start": "2024-07-01T07:30:00",
                        "end": "2024-07-01T10:30:00",
                    },
                    {
                        "id": "id9",
                        "title": "Event 9",
                        "start": "2024-07-02T10:40:00",
                        "end": "2024-07-02T12:30:00",
                    },
                ],
            }
        ]


app = App(app_ui, server)
