# coding=utf-8
# __version__ = '0.0.12'
import os, sys, codecs
from http.server import HTTPServer, SimpleHTTPRequestHandler
from outdated import check_outdated
from socketserver import ThreadingMixIn
import ssl
from OpenSSL import crypto
import site

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

class HTTPS:

    def __init__(self,host,port,keyfile,certfile):
        print('keyfile =',keyfile)
        print('certfile =',certfile)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        httpd = ThreadingSimpleServer((host, port), SimpleHTTPRequestHandler)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print("server started at https://%s:%s" % (host, port))
        httpd.serve_forever()
        pass

class HTTP:

    def __init__(self,host,port):
        httpd = ThreadingSimpleServer((host, port), SimpleHTTPRequestHandler)
        print("server started at http://%s:%s" % (host, port))
        httpd.serve_forever()
        pass

class GenCert:

    def __init__(self):
        sitepackages_dir = self.get_sitepackages_dir()
        self.certdir = os.path.join(sitepackages_dir, 'cert')
        self.KEY_FILE = os.path.join(self.certdir, 'key.pem')
        self.CERT_FILE = os.path.join(self.certdir, 'cert.pem')
        self.CERT_FILE = os.path.join(self.certdir, 'cert.pem')
        self.mkdir(self.certdir)
        pass

    def cert_gen(self,
             emailAddress="emailAddress",
             commonName="commonName",
             countryName="US",
             localityName="localityName",
             stateOrProvinceName="stateOrProvinceName",
             organizationName="organizationName",
             organizationUnitName="organizationUnitName",
             serialNumber=0,
             validityStartInSeconds=0,
             validityEndInSeconds=10 * 365 * 24 * 60 * 60,):

        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = countryName
        cert.get_subject().ST = stateOrProvinceName
        cert.get_subject().L = localityName
        cert.get_subject().O = organizationName
        cert.get_subject().OU = organizationUnitName
        cert.get_subject().CN = commonName
        cert.get_subject().emailAddress = emailAddress
        cert.set_serial_number(serialNumber)
        cert.gmtime_adj_notBefore(validityStartInSeconds)
        cert.gmtime_adj_notAfter(validityEndInSeconds)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')
        with open(self.CERT_FILE, "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
        with open(self.KEY_FILE, "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))


    def mkdir(self, dir, force=False):
        if not os.path.isdir(dir):
            if force == True:
                os.makedirs(dir)
            else:
                os.mkdir(dir)

    def get_sitepackages_dir(self):
        getsitepackages = site.getsitepackages()
        for i in getsitepackages:
            # print(os.path.join(i, 'myhttps'))
            # print(os.path.isdir(os.path.join(i, 'myhttps')))
            if os.path.isdir(os.path.join(i, 'myhttps')):
                return os.path.join(i, 'myhttps')


class Functions:
    def __init__(self):
        pass

    def getVersion(self):
        firstline = self.read("__init__.py").splitlines()[0]
        ver = firstline.split("'")[1]
        return ver

    def getUsage(self):
        st = False
        usage = ""
        for line in self.read("__init__.py").splitlines():
            if st and not line.startswith('"""'):
                usage += line + "\n"
            if line.startswith('__usage__'):
                st = True
            if st and line.startswith('"""'):
                break
        if not st:
            raise RuntimeError("Unable to find usage string.")
        else:
            return usage

    def read(self,rel_path):
        here = os.path.abspath(os.path.dirname(__file__))
        with codecs.open(os.path.join(here, rel_path), 'r') as fp:
            return fp.read()

def main():
    ver = Functions().getVersion()
    print('current version:',ver)
    is_outdated, latest = check_outdated("myhttps", ver)
    if is_outdated:
        print("The package myhttps is out of date. Your version is %s, the latest is %s." % (ver, latest))
    host = '0.0.0.0'
    port = 11443

    mode='HTTPS'
    # print(os.path.exists(certfile));exit()

    usage = Functions().getUsage()
    version = Functions().getVersion()
    if "--help" in sys.argv:
        print(usage)
        exit()
    if "--v" in sys.argv:
        print("myhttps version: ", version)
        exit()
    if "-p" in sys.argv:
        port = sys.argv[sys.argv.index("-p") + 1]
        port = int(port)
    if "-h" in sys.argv:
        host = sys.argv[sys.argv.index("-h") + 1]
    if "-c" in sys.argv:
        certfile = sys.argv[sys.argv.index("-c") + 1]
    if "-k" in sys.argv:
        keyfile = sys.argv[sys.argv.index("-k") + 1]
    if "-mode" in sys.argv:
        mode = sys.argv[sys.argv.index("-mode") + 1]
    pwd = os.path.dirname(os.path.realpath(__file__))
    print('current shared dir:',pwd)
    if mode == 'HTTPS':
        _GenCert = GenCert()
        keyfile = _GenCert.KEY_FILE
        certfile = _GenCert.CERT_FILE
        if not "-c" in sys.argv:

            if not os.path.exists(certfile):
                _GenCert.cert_gen()
        HTTPS(host,port,keyfile,certfile)
    elif mode == 'HTTP':
        HTTP(host,port)
    else:
        raise Exception("mode must be HTTPS or HTTP")

if __name__ == "__main__":
    main()
    # GenCert()
    # Functions().getVersion()
    pass
