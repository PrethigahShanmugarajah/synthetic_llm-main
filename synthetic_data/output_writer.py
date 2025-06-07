import pandas as pd
import json
import pyarrow as pa
import pyarrow.parquet as pq

def write_data_to_file(data, output_path, output_format):
    """Writes the data to a file in the specified format."""
    if output_format == "csv":
        data.to_csv(output_path, index=False)
    elif output_format == "parquet":
        table = pa.Table.from_pandas(data)
        pq.write_table(table, output_path)
    elif output_format == "json":
        with open(output_path, "w") as f:
            if isinstance(data, list):
                json.dump(data, f, indent=2)
            elif isinstance(data, pd.DataFrame):
                data.to_json(f, orient="records", indent=2)
            else:
                print("Warning: Data is neither a list nor a DataFrame. Saving as is.")
                json.dump(data, f, indent=2)
    else:
        raise ValueError("Invalid output format.")