def generate_analytics(df):

    return {

        "Jobs Found":
        len(df),

        "Companies":
        df["Company"].nunique()
        if len(df) > 0
        else 0,

        "Locations":
        df["Location"].nunique()
        if len(df) > 0
        else 0
    }