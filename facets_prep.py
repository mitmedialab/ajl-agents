from utils.storage.managers import storage_for_path
from utils.fingerprint import compact_fingerprint_path


# Objective: go from a dataset or a formatted csv to facets url
#content = '/Users/debraji/work/clarifai/conf/dst/ppb_upload.json'
content = '/Users/debraji/work/clarifai/conf/dst/PPB_upload_reformat.json'
#past_s3_url = 'https://s3.amazonaws.com/clarifai-img/data_strategists/31/e3/33/6f1e6abe1b745395e10a5cda17.json'
past_s3_url = 'https://s3.amazonaws.com/clarifai-img/data_strategists/ab/9d/af/97cc5c40977074f88516fd3829'
s3_past_path = past_s3_url.strip('https://s3.amazonaws.com')
s3_past_path = s3_past_path.strip('.json')
content2 = '/Users/debraji/play/mosaic_ppb_1270.jpg'
image_rehost = True

if image_rehost:
  s3_path = 's3://clarifai-img/data_strategists/c2/e8/f4/b4c98240ebf6f151f54289f8c1.png'
  content = content2
else:
  s3_bucket = 's3://clarifai-img'
  s3_base = 'data_strategists'
  file_loc = compact_fingerprint_path(content)
  s3_path = "%s/%s/%s" % (s3_bucket, s3_base, file_loc)


with open(content, 'rb') as bytes_file:
  bytes_io = bytes_file.read()

storage = storage_for_path(s3_path)

print content
#if not storage.exists(content):  # here is how we check indirectly if the content is already rehosted
if True:
  print 'Rehosting...'
  storage.open(s3_path, 'wb').write(bytes_io)
  storage.make_public(s3_path)

  upload_url = s3_path.replace('s3://', 'https://s3.amazonaws.com/')
  s3_url  = upload_url.partition('?')[0]
  print s3_url

