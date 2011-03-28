'''
Created on Feb 21th, 2011

@author: Dmytro Korsakov
'''
import os

from ConfigParser import ConfigParser, NoSectionError, NoOptionError


class ScalrCfgError(BaseException):
	pass


class ScalrEnvError(ScalrCfgError):
	pass

	
class ConfigSection(object):
	config_name = None
	options = {}
	
	def __init__(self, **kwargs):
		for arg in kwargs:
			if hasattr(self, arg):
				setattr(self, arg, kwargs[arg])

	def write(self, base_path, section):
		config = ConfigParser()
		
		path = os.path.join(base_path, self.config_name)
		if os.path.exists(path):
			config.read(path)
		else:
			os.makedirs(os.path.dirname(path))
			
		if not config.has_section(section):
			config.add_section(section)
		
		for option in self.options:
			config.set(section, self.options[option], getattr(self, option))
			
		file = open(path, 'w')
		config.write(file)
		file.close()
			
	@classmethod
	def from_ini(cls, base_path, section):
		path = os.path.join(base_path, cls.config_name)
		
		if not os.path.exists(path):
			raise ScalrCfgError('%s: Config file not found.' % path)
		
		config = ConfigParser()	
		config.read(path)
		obj = cls()
		setattr(obj, 'name', section)
		
		for option in cls.options:
			try:
				setattr(obj, option, config.get(section, cls.options[option]))
			except (NoSectionError, NoOptionError), e:
				raise ScalrCfgError('%s in %s'%(e, path))
		return obj


class Scripts(ConfigSection):
	svn=None
	git=None
	
	config_name = 'config.ini'
	options = {'svn':'svn', 'git':'git'}

	def write(self, base_path, section='scripts'):
		super(Scripts, self).write(base_path, section)
			
	@classmethod
	def from_ini(cls, base_path, section='scripts'):
		return super(Scripts, cls).from_ini(base_path, section)
				
class Environment(ConfigSection):
	url=None
	key_id=None
	key=None
	api_version = None	
	
	config_name = 'config.ini'
	
	options = dict(
			url = 'scalr_url',
			key_id = 'scalr_key_id',
			key = 'scalr_api_key',
			api_version = 'version')
	
	def write(self, base_path, section='api'):
		super(Environment, self).write(base_path, section)
			
	@classmethod
	def from_ini(cls, base_path, section='api'):
		return super(Environment, cls).from_ini(base_path, section)
	
			
class Application(ConfigSection):
	
	name = None
	repo_name = None
	farm_id = None
	farm_role_id = None
	remote_path = None 
	
	config_name = 'apps.ini'
	
	options = dict(
		repo_name = 'repo_name',
		farm_id = 'farm_id',
		farm_role_id = 'farm_role_id',
		remote_path = 'remote_path')


class Repository(ConfigSection):		
	name = None
	type = None
	url = None
	login = None
	password = None 

	config_name = 'repos.ini'
	
	options = dict(
		type = 'type',
		url = 'url',
		login = 'login',
		password = 'password')


class Configuration:
	logger = None
	base_path = None
	
	environment = None
	application = None
	repository = None
	scripts = None
	
	def __init__(self, base_path=None, logger=None):
		self.base_path = base_path or os.path.expanduser("~/.scalr/")
		self.logger = logger

	def set_logger(self, logger):
		self.logger = logger
				
	def set_environment(self, key, key_id, url):
		if key and key_id and url:
			self.environment = Environment(key=key, key_id=key_id, url=url)
	
		try:
			self.environment = Environment.from_ini(self.base_path)
		except ScalrCfgError:
			raise ScalrEnvError('Environment not set.')
		
		if not self.environment or not self.environment.key or not self.environment.key_id or not self.environment.url:
			raise ScalrEnvError('Environment not set.')
		
	def set_application(self, name):
		try:
			self.application = Application.from_ini(self.base_path, name)
		except ScalrCfgError:
			raise ScalrEnvError('Application settings are not set.')
	
	def set_repository(self, name):
		try:
			self.repository = Repository.from_ini(self.base_path, name)
		except ScalrCfgError:
			raise ScalrEnvError('Repository settings are not set.')
		
	def set_scripts(self):
		try:
			self.scripts = Scripts.from_ini(self.base_path)
		except ScalrCfgError:
			raise ScalrEnvError('Script settings are not set.')