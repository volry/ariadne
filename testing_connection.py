#%%
from google.cloud import storage
#%%
# Explicitly create a storage client with your service account JSON key file
storage_client = storage.Client.from_service_account_json('/home/vova/Downloads/bionic-run-419111-4b5d62a9fac3.json')
# List buckets to test the client
bucket = storage_client.bucket('assets-monitoring-1')
blobs = list(bucket.list_blobs())
print(blobs)
# %%