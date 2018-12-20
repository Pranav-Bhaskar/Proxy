import socket
import _thread

def reciver(connection):
	data = b''
	while True:
		k = connection.recv(1024)
		if k == b'':
			break
		data += k
	return data
		
def connector(data):
	details = data.split(' ')
	hostname = details[1].split('://')[-1]
	port = 80
	if len(hostname.split(':')) > 1:
		port = int(hostname.split(':')[-1].split('/')[0])
	hostname = data.split('Host: ')[-1].split('\r\n')[0].split(':')[0]
	com = socket.socket()
	com.connect((hostname, port))
	return com

def comunicator(con, data):
	flag = True
	try:
		while True:
			data = con.recv(1024).decode('utf-8')
			if data == '':
				break
			com = connector(data)
			com.send(data.encode('utf-8'))
			data = reciver(com)
			if data == b'':
				break
			con.send(data)
	except:
		print('A thread closed ')

if __name__ == '__main__':
	try:
		s = socket.socket()
		s.bind(('127.0.0.1', 8080))
		s.listen(20)
	except:
		print('ERROR : Could\'t create socket')
		exit()
	try:
		while(True):
			c, md = s.accept()
			_thread.start_new_thread(comunicator, (c, md))
		
	except:
		s.close()
		print('Server closed.')
		exit()
