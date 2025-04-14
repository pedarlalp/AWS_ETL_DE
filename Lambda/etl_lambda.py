import boto3
import pandas as pd
import requests
from io import StringIO

def lambda_handler(event, context):
    url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
    response = requests.get(url)
    df = pd.read_csv(StringIO(response.text))
    df.columns = [c.lower() for c in df.columns]

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3 = boto3.client('s3')
    s3.put_object(Bucket='your-s3-bucket', Key='transformed/airtravel.csv', Body=csv_buffer.getvalue())
    return {'statusCode': 200, 'body': 'Upload complete'}
