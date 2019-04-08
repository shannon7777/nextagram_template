import os
import boto3, botocore
from app import app
from flask_login import current_user
from models.user import User
import braintree

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg', 'gif'])

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    user = User.get_by_id(current_user.id)
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            str(user.username) + "/" + file.filename,
            # file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    
    return f"{file.filename}"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=app.config.get('BT_MERCHANT_KEY'),
        public_key=app.config.get('BT_PUBLIC_KEY'),
        private_key=app.config.get('BT_PRIVATE_KEY')
    )
)

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)
