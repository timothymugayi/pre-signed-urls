#  Copyright (c) 2019 tiptapcode or its affiliates. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
#
#  https://www.apache.org/licenses/LICENSE-2.0
#
#  or in the "license" file accompanying this file. This file is
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
#  language governing permissions and limitations under the License.

import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner

# python > 3 should be installed
# pip install cryptography
# pip install boto3
# cloudfront distribution association with s3 bucket should be configured and key pairs generated
# The difference between s3 and cloudfront is that cloudfront caches the content of s3 in edge locations
# to reduce the latency with which objects are fetched. The reason signed urls are used is because you
# do not want to provide the users direct links to s3 at any time. So you create a cloudfront distribution
# pointing to s3 bucket, create a signed ur

def rsa_signer(message):
    """
    A signer to create a signed CloudFront URL.
    First you create a cloudfront signer based on a normalized RSA signer
    key.pem is the private keyfile downloaded from CloudFront keypair
    :param message:  the message to be signed
    :type message:
    :return: Signed content as a binary string
    :rtype: binary string
    """
    with open('/Users/{YOUR_PATH}/Downloads/pk-{KEY_ID_FOUND_ATTACHED_PEM_FILE}.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    signer = private_key.signer(padding.PKCS1v15(), hashes.SHA1())
    signer.update(message)
    return signer.finalize()

key_id = '{KEY_ID_FOUND_ATTACHED_PEM_FILE}'
url = 'https://d1i5zfj88u6j2z.cloudfront.net/downloads/whitepaper.pdf'
expire_date = datetime.datetime(2020, 1, 1)

cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)

# Create a signed url that will be valid until the specfic expiry date
# provided using a canned policy.
signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
print(signed_url)