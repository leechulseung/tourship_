from django.shortcuts import render

def tourship(request):
	return render(request, 'group/tour_list.html')