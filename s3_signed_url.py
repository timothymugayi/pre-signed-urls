
#  Copyright (c) 2019 tiptapcode or its affiliates. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
#
#  https://www.apache.org/licenses/LICENSE-2.0
#
#  or in the "license" file accompanying this file. This file is
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
#  language governing permissions and limitations under the License.

import os
import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

# python > 3 should be installed
# pip install boto3
# s3v4
# (Default) Signature Version 4
# v4 algorithm starts with X-Amz-Algorithm
#
# s3
# (Deprecated) Signature Version 2,  this only works in some regions new regions not supported
# if you have to generate signed url that has > 7 days expiry then use version 2 if your region supports it

s3_signature ={
    'v4':'s3v4',
    'v2':'s3'
}

# Below is optional you do not need these additional variables as boto3 supports
# reading values from env variables. This is for illustration purpose
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

def create_presigned_url(bucket_name, bucket_key, expiration=3600, signature_version=s3_signature['v4']):
    """Generate a presigned URL for the S3 object
    :param bucket_name: string
    :param bucket_key: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param signature_version: string
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             config=Config(signature_version=signature_version),
                             region_name=AWS_DEFAULT_REGION
                             )
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': bucket_key},
                                                    ExpiresIn=expiration)
        print(s3_client.list_buckets()['Owner'])
        for key in s3_client.list_objects(Bucket=bucket_name, Prefix=bucket_key)['Contents']:
            print(key['Key'])
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response

weeks = 8
seven_days_as_seconds = 604800
generated_signed_url = create_presigned_url('djangosimplified', 'downloads/whitepaper.pdf', seven_days_as_seconds, s3_signature['v4'])
print(generated_signed_url)