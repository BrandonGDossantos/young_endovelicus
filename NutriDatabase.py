import requests
import argparse
import socket
import ipaddress
import json
import re

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

	def ndbno_lookup(self, ndbno):
		url = 'https://api.nal.usda.gov/ndb/V2/reports?ndbno={}&type=b&format=json&api_key={}'.format(ndbno, self.api_key)
		return self._request('get', url)