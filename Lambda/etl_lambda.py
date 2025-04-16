import boto3
import pandas as pd
import requests
from io import StringIO


def lambda_handler(event, context):
    url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text))
        df.columns = [c.lower() for c in df.columns]

        # Convert the DataFrame to CSV in memory
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Set up the S3 client
        s3 = boto3.client('s3')

        # Upload to S3
        try:
            print(f"Uploading file to S3 with Key: transformed/airtravel.csv")
            s3.put_object(Bucket='transformedetldatafile', Key='transformed/airtravel.csv', Body=csv_buffer.getvalue())
            print("File uploaded successfully.")
        except Exception as e:
            print("S3 Upload Failed:", e)
            return {'statusCode': 500, 'body': str(e)}

        return {'statusCode': 200, 'body': 'File uploaded successfully'}

    else:
        print(f"Failed to retrieve file, status code: {response.status_code}")
        return {'statusCode': 500, 'body': 'Failed to retrieve file from URL'}
