
import http.server, http, pathlib, sys, argparse, ssl, os, builtins, tempfile
import base64, binascii, functools, contextlib

# Does not seem to do be used, but leaving this import out causes uploadserver
# to not receive IPv4 requests when started with default options under Windows
import socket

# The cgi module was deprecated in Python 3.13, so I saved a copy in this
# project
if sys.version_info.major == 3 and sys.version_info.minor < 13:
    import cgi
else:
    import uploadserver.cgi

COLOR_SCHEME = {
    'light': 'light',
    'auto': 'light dark',
    'dark': 'dark',
}
def send_upload_page(handler: http.server.BaseHTTPRequestHandler):
    handler.send_response(http.HTTPStatus.OK)
    handler.send_header('Content-Type', 'text/html; charset=utf-8')
    handler.send_header('Content-Length', len(get_upload_page()))
    handler.end_headers()
    handler.wfile.write(get_upload_page())


def get_upload_page() -> bytes:
    return bytes('''<!DOCTYPE html>
<html>
<head>
<title>File Upload</title>
<meta name="viewport" content="width=device-width, user-scalable=no" />
<meta name="color-scheme" content="''' + '''">
</head>
<body>
<h1>File Upload</h1>
<form action="upload" method="POST" enctype="multipart/form-data">
<input name="files" type="file" multiple />
<br />
<br />
<input type="submit" />
</form>
<p id="task"></p>
<p id="status"></p>
</body>
<script>
document.getElementsByTagName('form')[0].addEventListener('submit', async e => {
  e.preventDefault()

  const uploadFormData = new FormData(e.target)
  const filenames = uploadFormData.getAll('files').map(v => v.name).join(', ')
  const uploadRequest = new XMLHttpRequest()
  uploadRequest.open(e.target.method, e.target.action)
  uploadRequest.timeout = 3600000

  uploadRequest.onreadystatechange = () => {
    if (uploadRequest.readyState === XMLHttpRequest.DONE) {
      let message = `${uploadRequest.status}: ${uploadRequest.statusText}`
      if (uploadRequest.status === 0) message = 'Connection failed'
      if (uploadRequest.status === 204) {
        message = `Success: ${uploadRequest.statusText}`
      }
      document.getElementById('status').textContent = message
    }
  }

  uploadRequest.upload.onprogress = e => {
    document.getElementById('status').textContent = (e.loaded === e.total ?
      'Saving…' :
      `${Math.floor(100*e.loaded/e.total)}% ` +
      `[${Math.floor(e.loaded/1024)} / ${Math.floor(e.total/1024)}KiB]`
    )
  }

  uploadRequest.send(uploadFormData)

  document.getElementById('task').textContent = `Uploading ${filenames}:`
  document.getElementById('status').textContent = '0%'
})
</script>
</html>''', 'utf-8')


class CGIHTTPRequestHandler(ListDirectoryInterception,
                            http.server.CGIHTTPRequestHandler):
    def do_GET(self):
        if not check_http_authentication(self): return

        if self.path == '/upload':
            send_upload_page(self)
        else:
            super().do_GET()

    def do_POST(self):
        if not check_http_authentication(self): return

        if self.path == '/upload':
            result = receive_upload(self)

            if result[0] < http.HTTPStatus.BAD_REQUEST:
                self.send_response(result[0], result[1])
                self.end_headers()
            else:
                self.send_error(result[0], result[1])
        else:
            super().do_POST()

    def do_PUT(self):
        self.do_POST()
