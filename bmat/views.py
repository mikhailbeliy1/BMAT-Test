from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.reverse import reverse

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView

from .models import MusicalWork
from .serializers import MusicalWorkSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions

from rest_framework.response import Response

import csv, io
from django.shortcuts import render
from django.contrib import messages

import json

# Create your views here.


def index(request):
    return HttpResponse('Hello, Welcome to BMAT!')


class MusicalWorkListView(ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = MusicalWork.objects.all()
    serializer_class = MusicalWorkSerializer


class upload_works_csv(APIView):
	def get(self, request, format=None):
		return render(request, 'upload_works_csv.html', {})
	def post(self, request, format=None):
		try:
			csv_file = request.FILES['upload_works_csv']
			if not csv_file.name.endswith('.csv'):
				print('===mikhail===', 'not csv file.')
				return HttpResponseRedirect(reverse('upload_works_csv'))
			# if file is too large, return
			if csv_file.multiple_chunks():
				messages.error(request, 'Uploaded file is too big (%.2f MB).' % (csv_file.size/(1000*1000),))
				return HttpResponseRedirect(reverse("upload_works_csv"))

			file_data = csv_file.read().decode("utf-8")

			lines = file_data.split('\n')
			#loop over the lines and save them in db. If error , store as string and then display
			for line in lines:
				if line == '':
					continue

				fields = line.split(',')

				data_dict = {}
				data_dict['title'] = fields[0]
				data_dict['contributors'] = fields[1].split('|')
				data_dict['iswc'] = fields[2]

				if data_dict['iswc'] == 'iswc':
					continue

				musicalWork = MusicalWork.objects.filter(iswc=data_dict['iswc']).first()
				if (musicalWork == None):
					musicalWork = MusicalWork.objects.filter(title=data_dict['title']).first()


				if checkMusicalWorkDeuplicate(musicalWork, data_dict):
					if unionMusicalWork(musicalWork, data_dict):
						# Update Musical Work
						musicalWork.save()

				else:
					# Create New Musical Work
					musicalWorkSerializer = MusicalWorkSerializer(musicalWork)
					musicalWorkSerializer.create(data_dict)


		except Exception as e:
			messages.error(request, 'Unable to upload file. '+repr(e))

		return HttpResponseRedirect(reverse('upload_works_csv'))


class search_iswc(APIView):
	def get(self, request, format=None):
		return render(request, 'search.html', {})
	def post(self, request, format=None):
		iswc = request.data['iswc']
		musicalWork = MusicalWork.objects.filter(iswc=iswc).all()
		musicalWorkSerializer = MusicalWorkSerializer(musicalWork, many=True)

		response = musicalWorkSerializer.data
		response = json.loads(json.dumps(response))
		return Response(response)


def checkMusicalWorkDeuplicate(musicalWork, data_dict):

	if musicalWork == None:
		return False

	if musicalWork.iswc == data_dict['iswc']:
		return True
	if musicalWork.title == data_dict['title']:
		for contributor in data_dict['contributors']:
			if contributor in musicalWork.contributors:
				return True
	return False

def unionMusicalWork(musicalWork, data_dict):

	is_update = False

	if musicalWork.iswc == '' and data_dict['iswc'] != '':
		musicalWork.iswc = data_dict['iswc']
		is_update = True

	org_length = len(musicalWork.contributors)
	musicalWork.contributors = musicalWork.contributors + list(set(data_dict['contributors']) - set(musicalWork.contributors))
	new_length = len(musicalWork.contributors)

	is_update |= (org_length != new_length)


	return is_update
