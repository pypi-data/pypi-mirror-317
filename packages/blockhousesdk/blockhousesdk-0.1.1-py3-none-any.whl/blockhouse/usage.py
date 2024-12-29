
from blockhouse.client import BlockhouseClient

client = BlockhouseClient()

bucket_name = 'blockhouse-bucket'
file_name = 'file_name'

client.transfer_file(file_name, bucket_name)
