"""
Util functions for the app.
"""

import os
from collections import OrderedDict
from datetime import datetime
import shutil
import pandas as pd
from pandas import DataFrame
from babylab.src import api


def format_percentage(x: float | int) -> str:
    """Format number into percentage.

    Args:
        x (float | int): Number to format. Must be higher than or equal to zero, and lower than or equal to one.

    Raises:
        ValueError: If number is not higher than or equal to zero, and lower than or equal to one.

    Returns:
        str: Formatted percentage
    """  # pylint: disable=line-too-long
    if x > 100 or x < 0:
        raise ValueError(
            "`x` higher than or equal to zero, and lower than or equal to one"
        )
    return str(int(float(x))) if x else ""


def format_taxi_isbooked(address: str, isbooked: str) -> str:
    """Format ``taxi_isbooked`` variable to HTML.

    Args:
        address (str): ``taxi_address`` value.
        isbooked (str): ``taxi_isbooked`` value.

    Returns:
        str: Formatted HTML string.
    """  # pylint: disable=line-too-long
    if isbooked not in ["0", "1"]:
        raise ValueError("`is_booked` must be one of '0' or '1'")
    if not address:
        return ""
    if int(isbooked):
        return "<p style='color: green;'>Yes</p>"
    return "<p style='color: red;'>No</p>"


def format_df(
    x: DataFrame,
    data_dict: dict,
    prefixes: list[str] = None,
) -> DataFrame:
    """Reformat dataframe.

    Args:
        x (DataFrame): Dataframe to reformat.
        data_dict (dict): Data dictionary to labels to use, as returned by ``models.get_data_dict``.
        prefixes (list[str]): List of `refixes to look for in variable names.

    Returns:
        DataFrame: A reformated Dataframe.
    """
    if prefixes is None:
        prefixes = ["participant", "appointment", "language"]
    for col_name, col_values in x.items():
        kdict = [x + "_" + col_name for x in prefixes]
        for k in kdict:
            if k in data_dict:
                x[col_name] = [data_dict[k][v] if v else "" for v in col_values]
        if "lang" in col_name:
            x[col_name] = ["" if v == "None" else v for v in x[col_name]]
        if "exp" in col_name:
            x[col_name] = [format_percentage(v) for v in col_values]
        if "taxi_isbooked" in col_name:
            pairs = zip(x["taxi_address"], x[col_name])
            x[col_name] = [format_taxi_isbooked(a, i) for a, i in pairs]
    return x


def format_dict(x: dict, data_dict=dict) -> dict:
    """Reformat dictionary.

    Args:
        x (dict): dictionary to reformat.
        data_dict (dict): Data dictionary to labels to use, as returned by ``models.get_data_dict``.

    Returns:
        dict: A reformatted dictionary.
    """
    fields = ["participant_", "appointment_", "language_"]
    for f in fields:
        for k, v in x.items():
            kdict = f + k
            if kdict in data_dict and v:
                x[k] = data_dict[kdict][v]
            if "exp" in k:
                x[k] = round(float(v), None) if v else ""
    return x


def replace_labels(x: DataFrame | dict, data_dict: dict) -> DataFrame:
    """Replace field values with labels.

    Args:
        x (pd.DataFrame): Pandas DataFrame in which to replace values with labels.
        data_dict (dict, optional): Data dictionary as returned by ``get_data_dictionary``. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """  # pylint: disable=line-too-long
    if isinstance(x, DataFrame):
        return format_df(x, data_dict)
    if isinstance(x, dict):
        return format_dict(x, data_dict)
    return None


def get_participants_table(records: api.Records, data_dict: dict = None) -> DataFrame:
    """Get participants table

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.

    Returns:
        pd.DataFrame: Table of partcicipants.
    """
    cols = [
        "name",
        "age_now_months",
        "age_now_days",
        "sex",
        "date_created",
        "date_updated",
    ]
    if not records.participants.records:
        return DataFrame([], columns=cols)

    new_age_months = []
    new_age_days = []
    for _, v in records.participants.records.items():
        age = api.get_age(
            birth_date=api.get_birth_date(
                age=f"{v.data['age_now_months']}:{v.data['age_now_days']}"
            )
        )
        new_age_months.append(int(age[0]))
        new_age_days.append(int(age[1]))

    df = records.participants.to_df()
    df["age_now_months"] = new_age_months
    df["age_now_days"] = new_age_days
    return replace_labels(df, data_dict)


def get_appointments_table(
    records: api.Records,
    data_dict: dict = None,
    ppt_id: str = None,
    study: str = None,
) -> DataFrame:
    """Get appointments table.

    Args:
        records (api.Records): _description_

    Returns:
        pd.DataFrame: Table of appointments.
    """
    apts = (
        records.participants.records[ppt_id].appointments
        if ppt_id
        else records.appointments
    )

    if study:
        apts.records = {
            k: v for k, v in apts.records.items() if v.data["study"] == study
        }

    if not apts.records:
        return DataFrame(
            [],
            columns=[
                "appointment_id",
                "record_id",
                "study",
                "status",
                "date",
                "date_created",
                "date_updated",
                "taxi_address",
                "taxi_isbooked",
            ],
        )

    new_age_now_months = []
    new_age_now_days = []
    new_age_apt_months = []
    new_age_apt_days = []
    for v in apts.records.values():
        age_now_months = records.participants.records[v.record_id].data[
            "age_now_months"
        ]
        age_now_days = records.participants.records[v.record_id].data["age_now_days"]
        age_now = api.get_age(
            birth_date=api.get_birth_date(age=f"{age_now_months}:{age_now_days}"),
            timestamp=datetime.strptime(
                records.participants.records[v.record_id].data["date_created"],
                "%Y-%m-%d %H:%M:%S",
            ),
        )
        age_apt = api.get_age(
            birth_date=api.get_birth_date(
                age=f"{age_now_months}:{age_now_days}",
                timestamp=datetime.strptime(
                    v.data["date"],
                    "%Y-%m-%d %H:%M",
                ),
            )
        )
        new_age_now_months.append(int(age_now[0]))
        new_age_now_days.append(int(age_now[1]))
        new_age_apt_months.append(int(age_apt[0]))
        new_age_apt_days.append(int(age_apt[1]))
    df = apts.to_df()
    df["appointment_id"] = df["id"]
    df["age_now_months"] = new_age_now_months
    df["age_now_days"] = new_age_now_days
    df["age_apt_months"] = new_age_apt_months
    df["age_apt_days"] = new_age_apt_days

    return replace_labels(df, data_dict)


def get_questionnaires_table(
    records: api.Records,
    data_dict: dict = None,
    ppt_id: str = None,
) -> DataFrame:
    """Get questionnaires table."""
    if ppt_id is None:
        quest = records.questionnaires
    else:
        quest = records.participants.records[ppt_id].questionnaires
    if not quest.records:
        return DataFrame(
            [],
            columns=[
                "record_id",
                "questionnaire_id",
                "isestimated",
                "date_created",
                "date_updated",
                "lang1",
                "lang1_exp",
                "lang2",
                "lang2_exp",
                "lang3",
                "lang3_exp",
                "lang4",
                "lang4_exp",
            ],
        )
    df = quest.to_df()
    df["questionnaire_id"] = [
        str(r) + ":" + str(q) for r, q in zip(df.index, df["redcap_repeat_instance"])
    ]
    df = replace_labels(df, data_dict)
    df["isestimated"] = [
        (
            "<p style='color: red;'>Estimated</p>"
            if i == "1"
            else "<p style='color: green;'>Calculated</p>"
        )
        for i in df["isestimated"]
    ]
    return df


def count_col(
    x: DataFrame,
    col: str,
    values_sort: bool = False,
    cumulative: bool = False,
    missing_label: str = "Missing",
) -> dict:
    """Count frequencies of column in DataFrame.

    Args:
        x (DataFrame): DataFrame containing the target column.
        col (str): Name of the column.
        values_sort (str, optional): Should the resulting dict be ordered by values? Defaults to False.
        cumulative (bool, optional): Should the counts be cumulative? Defaults to False.
        missing_label (str, optional): Label to associate with missing values. Defaults to "Missing".

    Returns:
        dict: Counts of each category, sorted in descending order.
    """  # pylint: disable=line-too-long
    counts = x[col].value_counts().to_dict()
    counts = {missing_label if not k else k: v for k, v in counts.items()}
    counts = dict(sorted(counts.items()))
    if values_sort:
        counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    if cumulative:
        for idx, (k, v) in enumerate(counts.items()):
            if idx > 0:
                counts[k] = v + list(counts.values())[idx - 1]
    return counts


def prepare_dashboard(records: api.Records = None, data_dict: dict = None):
    """Prepare data for dashboard"""
    ppts = get_participants_table(records, data_dict=data_dict)
    apts = get_appointments_table(records, data_dict=data_dict)
    quest = get_questionnaires_table(records, data_dict=data_dict)
    ppts["age_days"] = round(
        ppts["age_now_days"] + (ppts["age_now_months"] * 30.437), None
    ).astype(int)
    age_bins = list(range(0, max(ppts["age_days"]), 15))
    labels = [f"{int(a // 30)}:{int(a % 30)}" for a in age_bins]
    ppts["age_days_binned"] = pd.cut(
        ppts["age_days"], bins=age_bins, labels=labels[:-1]
    )

    age_dist = count_col(ppts, "age_days_binned")
    sex_dist = count_col(ppts, "sex", values_sort=True)
    ppts_date_created = count_col(ppts, "date_created", cumulative=True)
    apts_date_created = count_col(apts, "date_created", cumulative=True)
    status_dist = count_col(apts, "status", values_sort=True)
    lang1_dist = count_col(quest, "lang1", values_sort=True, missing_label="None")
    lang2_dist = count_col(quest, "lang2", values_sort=True, missing_label="None")
    return {
        "n_ppts": ppts.shape[0],
        "n_apts": apts.shape[0],
        "age_dist_labels": list(age_dist.keys()),
        "age_dist_values": list(age_dist.values()),
        "sex_dist_labels": list(sex_dist.keys()),
        "sex_dist_values": list(sex_dist.values()),
        "ppts_date_created_labels": list(ppts_date_created.keys()),
        "ppts_date_created_values": list(ppts_date_created.values()),
        "apts_date_created_labels": list(apts_date_created.keys()),
        "apts_date_created_values": list(apts_date_created.values()),
        "status_dist_labels": list(status_dist.keys()),
        "status_dist_values": list(status_dist.values()),
        "lang1_dist_labels": list(lang1_dist.keys()),
        "lang1_dist_values": list(lang1_dist.values()),
        "lang2_dist_labels": list(lang2_dist.keys()),
        "lang2_dist_values": list(lang2_dist.values()),
    }


def prepare_participants(records: api.Records = None, data_dict: dict = None):
    """Prepare data for participants page"""
    df = get_participants_table(records, data_dict=data_dict)
    classes = "table table-hover table-responsive"
    df["record_id"] = [f"<a href=/participants/{str(i)}>{str(i)}</a>" for i in df.index]
    df.index = df.index.astype(int)
    df = df.sort_index(ascending=False)
    df["modify_button"] = [
        f'<a href="/participants/{p}/participant_modify"><button type="button" class="btn btn-warning">Modify</button></a>'  # pylint: disable=line-too-long
        for p in df.index
    ]
    df = df[
        [
            "record_id",
            "name",
            "age_now_months",
            "age_now_days",
            "sex",
            "date_created",
            "date_updated",
            "modify_button",
        ]
    ]
    df = df.rename(
        columns={
            "record_id": "Participant",
            "name": "Name",
            "age_now_months": "Age (months)",
            "age_now_days": "Age (days)",
            "sex": "Sex",
            "date_created": "Added on",
            "date_updated": "Last updated",
            "modify_button": "",
        }
    )
    return {
        "table": df.to_html(
            classes=classes, escape=False, justify="left", index=False, bold_rows=True
        )
    }


def prepare_record_id(ppt_id: str, records: api.Records = None, data_dict: dict = None):
    """Prepare record ID page"""
    data = records.participants.records[ppt_id].data
    for k, v in data.items():
        kdict = "participant_" + k
        if kdict in data_dict:
            data[k] = data_dict[kdict][v] if v else ""
    data["age_now_months"] = (
        str(data["age_now_months"]) if data["age_now_months"] else ""
    )
    data["age_now_days"] = str(data["age_now_days"]) if data["age_now_days"] else ""
    data["parent1"] = data["parent1_name"] + " " + data["parent1_surname"]
    data["parent2"] = data["parent2_name"] + " " + data["parent2_surname"]

    classes = "table table-hover table-responsive"

    # prepare participants table
    df_appt = get_appointments_table(records, data_dict=data_dict, ppt_id=ppt_id)
    df_appt["record_id"] = [f"<a href=/participants/{i}>{i}</a>" for i in df_appt.index]
    df_appt["appointment_id"] = [
        f"<a href=/appointments/{i}>{i}</a>" for i in df_appt["appointment_id"]
    ]
    df_appt = df_appt.sort_values(by="date", ascending=False)
    df_appt = df_appt[
        [
            "record_id",
            "appointment_id",
            "study",
            "date",
            "date_created",
            "date_updated",
            "taxi_address",
            "taxi_isbooked",
            "status",
        ]
    ]
    df_appt = df_appt.rename(
        columns={
            "record_id": "Participant",
            "appointment_id": "Appointment",
            "study": "Study",
            "date": "Date",
            "date_created": "Made on the",
            "date_updated": "Last update",
            "taxi_address": "Taxi address",
            "taxi_isbooked": "Taxi booked",
            "status": "Status",
        }
    )
    table_appt = df_appt.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    # prepare language questionnaires table
    df_quest = get_questionnaires_table(records, data_dict=data_dict, ppt_id=ppt_id)
    df_quest["questionnaire_id"] = [
        f"<a href=/participants/{index}/questionnaires/{i}>{i}</a>"
        for index, i in zip(df_quest.index, df_quest["questionnaire_id"])
    ]
    df_quest["record_id"] = [
        f"<a href=/participants/{i}>{i}</a>" for i in df_quest.index
    ]
    df_quest = df_quest[
        [
            "questionnaire_id",
            "record_id",
            "lang1",
            "lang1_exp",
            "lang2",
            "lang2_exp",
            "lang3",
            "lang3_exp",
            "lang4",
            "lang4_exp",
            "date_created",
            "date_updated",
        ]
    ]
    df_quest = df_quest.sort_values("date_created", ascending=False)
    df_quest = df_quest.rename(
        columns={
            "record_id": "ID",
            "questionnaire_id": "Questionnaire",
            "date_updated": "Last updated",
            "date_created": "Created on the:",
            "lang1": "L1",
            "lang1_exp": "%",
            "lang2": "L2",
            "lang2_exp": "%",
            "lang3": "L3",
            "lang3_exp": "%",
            "lang4": "L4",
            "lang4_exp": "%",
        }
    )

    table_quest = df_quest.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    return {
        "data": data,
        "table_appointments": table_appt,
        "table_questionnaires": table_quest,
    }


def prepare_appointments(
    records: api.Records, data_dict: dict = None, study: str = None
):
    """Prepare appointments page"""
    df = get_appointments_table(records, data_dict=data_dict, study=study)
    classes = "table table-hover table-responsive"
    df["record_id"] = [f"<a href=/participants/{i}>{i}</a>" for i in df.index]
    df["modify_button"] = [
        f'<a href="/participants/{p}/{a}/appointment_modify"><button type="button" class="btn btn-warning">Modify</button></a>'  # pylint: disable=line-too-long
        for p, a in zip(df.index, df["appointment_id"])
    ]
    df["appointment_id"] = [
        f"<a href=/appointments/{i}>{i}</a>" for i in df["appointment_id"]
    ]
    status_color_map = {
        "Scheduled": "black",
        "Confirmed": "orange",
        "Successful": "green",
        "Cancelled - Drop": "grey",
        "Cancelled - Reschedule": "red",
        "No show": "red",
    }
    df["status"] = [
        f"<p style='color: {status_color_map[s]};'>{s}</p>" for s in df["status"]
    ]

    df = df[
        [
            "appointment_id",
            "record_id",
            "study",
            "status",
            "date",
            "date_created",
            "date_updated",
            "taxi_address",
            "taxi_isbooked",
            "modify_button",
        ]
    ]
    df = df.sort_values("date_updated", ascending=False)

    df = df.rename(
        columns={
            "appointment_id": "Appointment",
            "record_id": "Participant",
            "study": "Study",
            "status": "Appointment status",
            "date": "Date",
            "date_created": "Made on the",
            "date_updated": "Last updated",
            "taxi_address": "Taxi address",
            "taxi_isbooked": "Taxi booked",
            "modify_button": "",
        }
    )

    table = df.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    return {"table": table}


def prepare_questionnaires(records: api.Records = None, data_dict: dict = None):
    """Prepare appointments page"""
    df = get_questionnaires_table(records, data_dict=data_dict)
    classes = "table table-hover"
    df["modify_button"] = [
        f'<a href="/participants/{p}/questionnaires/{q}/questionnaire_modify"><button type="button" class="btn btn-warning">Modify</button></a>'  # pylint: disable=line-too-long
        for p, q in zip(df.index, df["questionnaire_id"])
    ]
    df["questionnaire_id"] = [
        f"<a href=/participants/{index}/questionnaires/{i}>{i}</a>"
        for index, i in zip(df.index, df["questionnaire_id"])
    ]
    df["record_id"] = [f"<a href=/participants/{i}>{i}</a>" for i in df.index]
    df = df[
        [
            "questionnaire_id",
            "record_id",
            "isestimated",
            "lang1",
            "lang1_exp",
            "lang2",
            "lang2_exp",
            "lang3",
            "lang3_exp",
            "lang4",
            "lang4_exp",
            "date_updated",
            "date_created",
            "modify_button",
        ]
    ]
    df = df.sort_values("date_created", ascending=False)
    df = df.rename(
        columns={
            "record_id": "Participant",
            "questionnaire_id": "Questionnaire",
            "isestimated": "Status",
            "date_updated": "Last updated",
            "date_created": "Added on the:",
            "lang1": "L1",
            "lang1_exp": "%",
            "lang2": "L2",
            "lang2_exp": "%",
            "lang3": "L3",
            "lang3_exp": "%",
            "lang4": "L4",
            "lang4_exp": "%",
            "modify_button": "",
        }
    )

    table = df.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    return {"table": table}


def prepare_studies(
    records: api.Records = None, data_dict: dict = None, study: str = None
):
    """Prepare appointments page"""
    df = get_appointments_table(records, data_dict=data_dict, study=study)
    classes = "table table-hover table-responsives"
    df["appointment_id"] = [
        f"<a href=/appointments/{i}>{i}</a>" for i in df["appointment_id"]
    ]
    df["record_id"] = [f"<a href=/participants/{i}>{i}</a>" for i in df.index]
    df = df[
        [
            "appointment_id",
            "record_id",
            "study",
            "date",
            "date_created",
            "date_updated",
            "taxi_address",
            "taxi_isbooked",
            "status",
        ]
    ]
    df = df.sort_values("date", ascending=False)

    df = df.rename(
        columns={
            "appointment_id": "Appointment",
            "record_id": "Participant",
            "study": "Study",
            "date": "Date",
            "date_created": "Made on the",
            "date_updated": "Last updated",
            "taxi_address": "Taxi address",
            "taxi_isbooked": "Taxi booked",
            "status": "Appointment status",
        }
    )

    table = df.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    date = df["Date"].value_counts().to_dict()
    date = OrderedDict(sorted(date.items()))
    for idx, (k, v) in enumerate(date.items()):
        if idx > 0:
            date[k] = v + list(date.values())[idx - 1]

    return {
        "n_apts": df.shape[0],
        "date_labels": list(date.keys()),
        "date_values": list(date.values()),
        "table": table,
    }


def clean_tmp(path: str = "tmp"):
    """Clean temporal directory"""
    if os.path.exists(path):
        shutil.rmtree(path)
