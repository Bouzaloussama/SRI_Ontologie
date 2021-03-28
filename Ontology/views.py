from time import sleep
from django.shortcuts import render, get_object_or_404, redirect

from . Onto_methods import Methods

# Create your views here.


def Ontology(request):

	requet = ""
	if request.method == 'POST':
			requet = request.POST.get('requet')
	if requet == "":
		requet = "Sports"
	onto = Methods.main(requet)

	Termes = onto[1]
	Concepts = onto[0]
	

	ontcon_term = []
	for m in onto[0]:
		ontcon_term.append(m)
	for m in onto[1]:
		ontcon_term.append(m)
	
	requet_after=  '+'.join(ontcon_term)

	
	context = {
		'concepts' : Concepts,
		'termes'   : Termes,
		'requet_befor_reformulation': requet,
		'requet_after_reformulation': requet_after
	}

	return render(request, 'bas1.html', context)


def All_class(request):

	classes = Methods.All_class()
	print(classes)

	context = {

		'all_class' : classes,

	}

	return render(request, 'All_class.html', context)
