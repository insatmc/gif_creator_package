import os
import imageio

def handler(event,context):
  files = event["files"]
  testresult = event["testresult"]
  i = 0
  filenames = []
  for file in files:
    filename = "/tmp/im-"+str(testresult)+"-"+str(i)+".png"
    fh = open(filename, "wb")
    filenames.append(filename)
    i = i + 1
    fh.write(file.decode('base64'))
    fh.close
  images = []
  for filename in filenames:
    images.append(imageio.imread(filename))

  hashGif = hashlib.sha224(event["id"]+"/"+event["user"]+'/'+event["testrun"]+"/"+event["testcase"]).hexdigest()
  imageio.mimsave(hashGif+'.gif', images)
  fh = open(hashGif+'.gif', "rb")
  s3.Object('run-records', hashGif+'.gif').put(
    Body=fh,
    ACL='public-read',
    Metadata={
      'Content-Type': 'image/gif'
    }
  )
  for filename in filenames:
      os.remove(filename)
  return "https://s3.eu-west-2.amazonaws.com/run-records/"+hashGif+".gif"

