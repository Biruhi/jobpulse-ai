import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
import pandas as pd
import plotly.express as px

from app.scraper import (
    get_jobs
)

from app.analytics import (
    generate_analytics
)

from app.exporter import (
    export_to_excel
)

from app.skill_extractor import (
    extract_skills
)

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="JobPulse AI",
    layout="wide"
)

st.title(
    "💼 JobPulse AI"
)

st.markdown(
    """
    Search remote jobs, analyze hiring trends,
    extract skills, and export reports.
    """
)

# ==================================
# SEARCH
# ==================================

keyword = st.text_input(
    "Job Keyword",
    "Python"
)

search_btn = st.button(
    "🔍 Search Jobs"
)

# ==================================
# PROCESS
# ==================================

if search_btn:

    with st.spinner(
        "Searching jobs..."
    ):

        df = get_jobs(
            keyword
        )

    # ==========================
    # EMPTY RESULT
    # ==========================

    if len(df) == 0:

        st.warning(
            "No jobs found for this keyword."
        )

        st.stop()

    # ==========================
    # ANALYTICS
    # ==========================

    analytics = (
        generate_analytics(
            df
        )
    )

    # ==========================
    # KPI CARDS
    # ==========================

    st.subheader(
        "📊 Dashboard"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Jobs Found",
        analytics["Jobs Found"]
    )

    col2.metric(
        "Companies",
        analytics["Companies"]
    )

    col3.metric(
        "Locations",
        analytics["Locations"]
    )

    # ==========================
    # JOB TABLE
    # ==========================

    st.subheader(
        "📋 Job Listings"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    # ==========================
    # SKILL ANALYSIS
    # ==========================

    st.subheader(
        "🛠 Skill Analysis"
    )

    skills = extract_skills(
        df
    )

    if len(skills) > 0:

        skill_df = pd.DataFrame(
            skills,
            columns=[
                "Skill",
                "Count"
            ]
        )

        skill_chart = px.bar(
            skill_df,
            x="Skill",
            y="Count",
            title="Most Requested Skills"
        )

        st.plotly_chart(
            skill_chart,
            use_container_width=True
        )

        st.dataframe(
            skill_df,
            use_container_width=True
        )

    else:

        st.info(
            "No skill data available."
        )

    # ==========================
    # LOCATION ANALYSIS
    # ==========================

    if "Location" in df.columns:

        location_df = (
            df["Location"]
            .value_counts()
            .reset_index()
        )

        location_df.columns = [
            "Location",
            "Count"
        ]

        location_chart = px.bar(
            location_df,
            x="Location",
            y="Count",
            title="Jobs by Location"
        )

        st.plotly_chart(
            location_chart,
            use_container_width=True
        )

    # ==========================
    # EXPORT
    # ==========================

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    output_file = (
        "outputs/job_report.xlsx"
    )

    export_to_excel(
        df,
        output_file
    )

    with open(
        output_file,
        "rb"
    ) as file:

        st.download_button(
            label=
            "⬇ Download Excel Report",
            data=file,
            file_name=
            "job_report.xlsx",
            mime=
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )