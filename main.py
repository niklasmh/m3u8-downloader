import urllib.request as request
from sys import argv, stdout

try:
  url = argv[1]
  base_url = "/".join(url.split(".m3u8")[0].split("/")[:-1])
except:
  print("You need to pass a URL (schema://.../file.m3u8)")
  exit(2)
print(base_url)

try:
  [*name, ext] = argv[2].split(".")
  if not len(name):
    name = [ext]
    ext = "mp4"
  name = ".".join(name)
except:
  print("The next argument should be the name of the file (name|name.ext)")
  exit(3)

fake_useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

segments = [line for line in request.urlopen(url).read().decode('utf-8').split("\n") if line and line[0] != "#"]
segment_count = len(segments)

with open(f"{name}.{ext}", "w+b") as f:
  for i, seg_url in enumerate(segments):
    r = request.Request(f"{base_url}/{seg_url}", headers={"User-Agent": fake_useragent})
    f.write(request.urlopen(r).read())
    progress = i / segment_count * 100
    progress_bar = "█"*int(progress)
    no_progress_bar = " "*int(100 - progress)
    print(f"\r[{progress_bar}{no_progress_bar}] {progress:.2f}%", end="")
  print("Done!")
