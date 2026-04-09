import pandas as pd

df = pd.read_csv("clean_predictive_maintenance.csv")


def run_dataframe_code(code: str):
    """
    Execute pandas analysis code against the dataframe `df`.

    Rules for the generated code:
    - Final answer must be stored in a variable named `result`
    - Code may use pandas operations on `df`
    - No file operations
    - No imports
    - No network calls
    """

    blocked_terms = [
        "import",
        "__",
        "open(",
        "exec(",
        "eval(",
        "os.",
        "sys.",
        "subprocess",
        "write(",
        "read(",
    ]

    lowered = code.lower()
    for term in blocked_terms:
        if term in lowered:
            return {
                "error": f"Blocked unsafe code pattern: {term}"
            }

    local_vars = {"df": df.copy(), "result": None}

    try:
        exec(code, {"__builtins__": {}}, local_vars)
        return {"result": local_vars.get("result")}
    except Exception as e:
        return {"error": str(e)}