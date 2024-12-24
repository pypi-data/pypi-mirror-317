import json
import time
from dataclasses import dataclass
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import SnowparkSQLException
import snowflake.permissions as permission
from snowflake.snowpark.functions import lit, call_udf

PRIVILEGES = ["BIND SERVICE ENDPOINT", "CREATE COMPUTE POOL", "CREATE WAREHOUSE"]


session = get_active_session()

title = "<<TITLE>>"
models_hub_url = "<<MODELS_HUB_URL>>"
example_text = "<<EXAMPLE_TEXT>>"


@dataclass
class Reference:
    name: str
    label: str
    type: str
    description: str
    bound_alias: str


st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto",
)


css = """
    /* Sidebar styles */
    section[data-testid="stSidebar"] {
        background: #ecf9ff;
        color: grey;
    }
    section[data-testid="stSidebar"] h1 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        font-size: 18px;
        line-height: 22px;
        color: #1E77B7;
    }
    section[data-testid="stSidebar"] .element-container .stMarkdown p {
        color: rgb(49, 51, 63) !important;
    }
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3 {
        color: #1E77B7;
    }
    /* Padding and spacing for the layout */
    .custom-padding {
        padding: 10px 0px; /* Vertical padding */
    }
"""
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


st.title(title)

st.sidebar.markdown(
    """
<h2 style="font-size: 27px; margin-bottom: 0; font-weight: 600; line-height: 1.2;">
  <a href="https://www.johnsnowlabs.com/" style="color: #3399FF; text-decoration: none; font-size: 28px;">John Snow</a>
  <span style="color: #6666CC; font-size: 26px;">LABS</span>
</h2>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="custom-padding"></div>', unsafe_allow_html=True)

if models_hub_url:
    st.sidebar.markdown(
        f"🔗 [View Model Card]({models_hub_url})", unsafe_allow_html=True
    )


def start_service(min_instances=1, max_instances=1):
    """Start the service with the specified parameters and display a message."""
    session.call("app_public.start_app", min_instances, max_instances)
    st.toast("Service starting...")


def stop_service():
    """Stop the running service and display a message."""
    session.call("app_public.stop_app")
    st.toast("Service stopped.")


def wait_for_service(max_attempts=180, delay=5):
    """Wait for the service to become 'READY' or 'FAILED', retrying every 'delay' seconds."""

    if st.button("Stop Service", type="primary"):
        stop_service()
        st.experimental_rerun()
    with st.spinner("The service is starting, please wait..."):
        for _ in range(max_attempts):
            time.sleep(delay)
            service_status = get_service_status()

            if service_status in ("READY", "FAILED"):
                return

    st.error("Service failed to start within the expected time. Stopping the service.")
    stop_service()


def run_via_ui():

    st.markdown('<div class="custom-padding"></div>', unsafe_allow_html=True)
    with st.form(key="prediction_form"):
        textTyped = st.text_area(
            "**Please type the text for which you want to see the predictions, in the text area below:**",
            value=example_text,
            height=200,
        )

        submit_button = st.form_submit_button(label="Apply")

    if submit_button:
        with st.status("Predicting...", expanded=True) as status:
            response = invoke_endpoint(textTyped)
            with st.container(height=500, border=True):
                st.json(response, expanded=True)
            status.update(label="Prediction complete!", state="complete")


def sql_examples():
    st.write(
        "If you prefer to run the prediction using Snowflake SQL, use the following example to call the UDF that runs the prediction. This can be helpful if you want to integrate the prediction into your existing SQL workflows."
    )
    app = session.get_current_database()
    schema = "app_public"

    st.code(
        f"""USE DATABASE {app};
USE SCHEMA {schema};
SELECT PREDICTION_UDF('{example_text}')
""",
        language="sql",
        line_numbers=True,
    )

    st.write(
        "The app also gives you access to the following procedures that manage the state of the endpoint service"
    )

    st.code(
        """# Used to start the endpoint service.
CALL app_public.start_app();
# Used to stop the endpoint service
CALL app_public.stop_app();
# Used to get the status of the endpoint service
CALL app_public.service_status()""",
        language="sql",
        line_numbers=True,
    )


def run_streamlit():
    service_status = get_service_status()
    if service_status == "NOT READY":
        st.warning(
            "Service is not running. Configure the parameters and click on the button below to start the service."
        )
        with st.form(key="start_service_form"):
            col1, col2 = st.columns(2)
            with col1:
                min_instances = st.number_input(
                    "Min Instances",
                    min_value=1,
                    value=1,
                    step=1,
                    help="Adding multiple instances will enhance overall performance but will also lead to higher infrastructure costs and quicker consumption of credits.",
                )
            with col2:
                max_instances = st.number_input(
                    "Max Instances",
                    min_value=1,
                    value=1,
                    step=1,
                )
            start_button = st.form_submit_button("Start Service", type="primary")

        if start_button:
            if max_instances < min_instances:
                st.error("Max Nodes cannot be less than Min Nodes")
            else:
                start_service(int(min_instances), int(max_instances))
                st.experimental_rerun()

    if service_status == "PENDING":
        wait_for_service(delay=5, max_attempts=240)
        st.experimental_rerun()

    if service_status == "READY":
        st.warning(
            "Service is running. Please remember to stop the service after you are done!"
        )
        if st.button("Stop Service", type="primary"):
            stop_service()
            st.experimental_rerun()

        st.header("Running the endpoint", divider=True)

        ui_tab, example_tab = st.tabs(["UI", "SQL"])

        with ui_tab:
            run_via_ui()

        with example_tab:
            sql_examples()

    elif service_status == "FAILED":
        st.error("Service failed to start.")
        stop_service()


def invoke_endpoint(text):
    result = session.sql("select app_public.prediction_udf(?)", params=[text]).collect()
    return result[0][0]


def get_service_status():
    """Get the status of the service.
    Returns one of the following: 'NOT READY', 'PENDING', 'READY', 'FAILED'."""

    try:
        result = session.call("app_public.service_status")
    except SnowparkSQLException:
        result = "NOT READY"
    return result


def setup():
    st.header("First-time setup")
    st.caption(
        """\
        Follow the instructions below to set up your application.
        Once you have completed the steps, you will be able to continue to the main example.
    """
    )

    refs = get_references()
    for ref in refs:
        name = ref.name
        label = ref.label

        if not ref.bound_alias:
            st.button(
                f"{label} ↗",
                on_click=permission.request_reference,
                args=[name],
                key=name,
            )
        else:
            st.caption(f"*{label}* binding exists ✅")

        if not ref.bound_alias:
            return

    st.divider()
    res = permission.get_missing_account_privileges(PRIVILEGES)

    if res and len(res) > 0:
        st.caption(f"The following privileges are needed")
        st.code(",".join(PRIVILEGES), language="markdown")
        st.button(
            "Request Privileges",
            on_click=permission.request_account_privileges,
            args=[PRIVILEGES],
        )
        return
    else:
        st.session_state.privileges_granted = True
        st.experimental_rerun()


def get_references():
    app_name = session.get_current_database()
    data_frame = session.create_dataframe([""])
    refs = data_frame.select(
        call_udf("system$get_reference_definitions", lit(app_name))
    ).collect()[0][0]
    references = []
    for row in json.loads(refs):
        bound_alias = row["bindings"][0]["alias"] if row["bindings"] else None
        references.append(
            Reference(
                row["name"],
                row["label"],
                row["object_type"],
                row["description"],
                bound_alias,
            )
        )
    return references


if __name__ == "__main__":
    try:
        if "privileges_granted" not in st.session_state:
            setup()
        else:
            run_streamlit()
    except Exception as e:
        st.write(e)
