import requests
import pandas as pd


def get_jobs(keyword):

    url = "https://remoteok.com/api"

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

    except Exception:

        return pd.DataFrame()

    jobs = []

    for item in data:

        if not isinstance(
            item,
            dict
        ):
            continue

        title = (
            item.get("position")
            or item.get("title")
            or ""
        )

        company = (
            item.get("company")
            or ""
        )

        location = (
            item.get("location")
            or "Remote"
        )

        tags = item.get(
            "tags",
            []
        )

        description = (
            item.get("description")
            or ""
        )

        date_posted = (
            item.get("date")
            or ""
        )

        apply_link = (
            item.get("url")
            or ""
        )

        searchable_text = (

            f"{title} "
            f"{description} "
            f"{' '.join(tags)}"

        ).lower()

        if keyword.lower() in searchable_text:

            jobs.append({

                "Title":
                title,

                "Company":
                company,

                "Location":
                location,

                "Date Posted":
                date_posted,

                "Tags":
                ", ".join(tags),

                "Apply Link":
                apply_link
            })

    return pd.DataFrame(
        jobs
    )