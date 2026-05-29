from collections import Counter


def extract_skills(df):

    if len(df) == 0:

        return []

    if "Tags" not in df.columns:

        return []

    skills = []

    for tags in df["Tags"]:

        if tags is None:

            continue

        for skill in str(tags).split(","):

            skill = skill.strip()

            if skill:

                skills.append(skill)

    return Counter(
        skills
    ).most_common(10)