import pandas as pd

df = pd.read_csv("clean_predictive_maintenance.csv")


def get_dataset_overview():
    return {
        "dataset_name": "clean_predictive_maintenance.csv",
        "rows": int(df.shape[0]),
        "columns": list(df.columns)
    }


def highest_torque_machine():
    row = df.loc[df["Torque [Nm]"].idxmax()]
    return row.to_dict()


def lowest_rpm_machine():
    row = df.loc[df["Rotational speed [rpm]"].idxmin()]
    return row.to_dict()


def highest_failure_machine():
    failed = df[df["Machine failure"] == 1]
    if failed.empty:
        return {"message": "No failed machines found in dataset."}
    row = failed.loc[failed["Torque [Nm]"].idxmax()]
    return row.to_dict()


def lowest_failure_machine():
    safe = df[df["Machine failure"] == 0]
    if safe.empty:
        return {"message": "No safe machines found in dataset."}
    row = safe.loc[safe["Torque [Nm]"].idxmin()]
    return row.to_dict()