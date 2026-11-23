from datetime import datetime, timezone
import glob
import os
import shutil
import pandas as pd

os.environ["KAGGLE_USERNAME"] = os.getenv("KAGGLE_USERNAME", "")
os.environ["KAGGLE_KEY"] = os.getenv("KAGGLE_KEY", "")

import kaggle

dataset_slug = "bwandowando/tomtom-traffic-data-55-countries-387-cities"
download_dir = "temp_kaggle"
os.makedirs(download_dir, exist_ok=True)

print("Mengunduh dataset TomTom dari Kaggle...")
kaggle.api.authenticate()
kaggle.api.dataset_download_files(dataset_slug, path=download_dir, unzip=True)

matches = glob.glob(
    os.path.join(download_dir, "**", "*NewApi*"), recursive=True
)
selected_path = matches[0]
if os.path.isdir(selected_path):
  csv_file = [
      os.path.join(selected_path, f)
      for f in os.listdir(selected_path)
      if os.path.isfile(os.path.join(selected_path, f))
  ][0]
else:
  csv_file = selected_path

df = pd.read_csv(csv_file)
df_latest = df.sort_values("UpdateTimeUTC", ascending=False).head(5000)

os.makedirs("data_output", exist_ok=True)
timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
output_file = f"data_output/tomtom_traffic_{timestamp_str}.csv"
df_latest.to_csv(output_file, index=False)

shutil.rmtree(download_dir, ignore_errors=True)
print(f"Ingestion selesai: {output_file} ({len(df_latest)} baris)")