from django.apps import AppConfig


class DatingConfig(AppConfig):
    name = 'dating'

    def ready(self):
    	import dating.signals
