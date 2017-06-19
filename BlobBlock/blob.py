from azure.storage.blob import BlockBlobService
import ConfigParser

#retrieving config from config file
cfg = ConfigParser.ConfigParser()
cfg.read("azureBlob.cfg")
azureAccountName = cfg.get("ConfigBlob","account")
azureAccountKey = cfg.get("ConfigBlob","key")

#connecting blob service
block_blob_service = BlockBlobService(account_name=azureAccountName, account_key=azureAccountKey)

#creating the container
block_blob_service.create_container('pythoncontainer2')

#sending some blob
block_blob_service.create_blob_from_path(
    'pythoncontainer',
    'config2',
    'azureBlob.cfg'
    )

#download a blockblob
block_blob_service.get_blob_to_path('pythoncontainer', 'myblockblob', 'out-sunset.cfg')

#list all blobs
generator = block_blob_service.list_blobs('pythoncontainer')
for blob in generator:
    print(blob.name)

#delete a blob
block_blob_service.delete_blob('pythoncontainer', 'myblockblob')
