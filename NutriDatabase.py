import requests
import argparse
import socket
import ipaddress
import json
import re
from netaddr import IPNetwork

# class GreyNoiseInvalidDate(Exception):
# 	pass

class NDB(object):

	def __init__(self, api_key, user_agent=None, base_url=None, session=None, headers=None, timeout=60, validate_ssl=True):
		assert isinstance(api_key,str)
		self.api_key = api_key
		self.user_agent = user_agent or 'NDB API Client'
		self.base_url = base_url
		self.timeout = timeout
		self.validate_ssl = validate_ssl
		self.session = session or requests.session()
		self.default_headers = headers or {'User-Agent': self.user_agent, 'key': self.api_key}
		self.default_request_args = {'timeout':self.timeout,'verify':self.validate_ssl}

	def _request(self, method, url, params=None, data=None, headers=None, args=None):
		headers = headers or self.default_headers
		args = args or self.default_request_args
		session = self.session
		resp = session.request(method, url, data=data, headers=headers, params=params, **args)
		resp.raise_for_status()
		return json.loads(resp.text)

	def list_standard(self, item):
		url = 'https://api.nal.usda.gov/ndb/search/?format=json&q={}&ds=Standard%20Reference&api_key={}&type=b&offset=0&max=50'.format(item, self.api_key)
		return self._request('get', url)

	def list_branded(self, item):
		url = 'https://api.nal.usda.gov/ndb/search/?format=json&q={}&ds=Branded%20Food%20Products&api_key={}&type=b&offset=0&max=50'.format(item, self.api_key)
		return self._request('get', url)




	# def get_noise_bulk(self, date=None, url='/v2/noise/bulk'):
	# 	url = self.base_url+url
	# 	if date:
	# 		if not re.match('',date):
	# 			raise GreyNoiseInvalidDate('Date %s does not match YYYY-MM-DD' % (date))
	# 		url = url+'/'+date

	# 	resp = self._request('get',url)
	# 	noise_ips = resp['noise_ips']
	# 	complete = resp['complete']
	# 	offset = resp['offset']
	# 	while not complete:
	# 		resp = self._request('get',url,params={'offset':offset})
	# 		complete = resp['complete']
	# 		if not complete:
	# 			noise_ips.extend(resp['noise_ips'])
	# 			offset = resp['offset']
	# 	return noise_ips

	# def get_noise_quick(self, ip, url='/v2/noise/quick/{}'):
	# 	ipaddress.ip_address(ip)
	# 	url = self.base_url+url
	# 	url = url.format(ip)
	# 	return self._request('get',url)

	# def get_noise_multi_quick(self, ips, url='/v2/noise/multi/quick'):
	# 	url = self.base_url+url
	# 	req_ips = set()
	# 	for ip in ips:
	# 		try:
	# 			ipaddress.ip_address(ip)
	# 			req_ips.add(ip)
	# 		except:
	# 			print('IP address %s is not valid, skipping')
	# 	req_ips = list(req_ips)
	# 	data = json.dumps({"ips":req_ips})
	# 	return self._request('get',url,data=data)

	# def get_context(self, ip, url='/v2/noise/context/{}'):
	# 	ipaddress.ip_address(ip)
	# 	url = self.base_url+url
	# 	url = url.format(ip)
	# 	return self._request('get',url)

	# def translate_code(self, code):
	# 	return self.noise_codes.get(code,'Unknown')