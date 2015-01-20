''' Views not associated with an app '''
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def home(request):
	return HttpResponseRedirect(reverse('competition:home'))