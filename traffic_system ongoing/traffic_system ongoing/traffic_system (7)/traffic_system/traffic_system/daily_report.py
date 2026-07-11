import pandas as pd
import os
from datetime import datetime

LOG_DIR = "logs"


def generate_daily_excel_report(date=None):
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    csv_file = os.path.join(LOG_DIR, f"traffic_2026-01-30.csv")
    excel_file = os.path.join(LOG_DIR, f"daily_report.xlsx")

    if not os.path.exists(csv_file):
        print(f"[REPORT] No CSV log found for {date}")
        return

    # ✅ ROBUST CSV READ
    df = pd.read_csv(
        csv_file,
        engine="python",
        on_bad_lines="skip"
    )

    total = len(df)
    success = len(df[df["Status"] == "SUCCESS"])
    fail = len(df[df["Status"] == "FAIL"])
    success_rate = round((success / total) * 100, 2) if total else 0

    summary_df = pd.DataFrame({
        "Metric": ["Total Sessions", "SUCCESS", "FAIL", "SUCCESS %"],
        "Value": [total, success, fail, success_rate]
    })

    if fail > 0:
        fail_breakdown = (
            df[df["Status"] == "FAIL"]["Error Reason"]
            .value_counts()
            .reset_index()
        )
        fail_breakdown.columns = ["Error Reason", "Count"]
    else:
        fail_breakdown = pd.DataFrame(columns=["Error Reason", "Count"])

    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        fail_breakdown.to_excel(writer, sheet_name="Failure Breakdown", index=False)
        df.to_excel(writer, sheet_name="Raw Logs", index=False)

    print("=" * 60)
    print(f"📊 DAILY SUCCESS REPORT GENERATED")
    print(f"Date          : {date}")
    print(f"Total         : {total}")
    print(f"SUCCESS       : {success}")
    print(f"FAIL          : {fail}")
    print(f"SUCCESS RATE  : {success_rate}%")
    print(f"Excel File    : {excel_file}")
    print("=" * 60)


if __name__ == "__main__":
    generate_daily_excel_report()
