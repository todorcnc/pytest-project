from urllib import response
from django.test import TestCase


import json

from unittest import TestCase
import pytest

from django.urls import reverse
from django.test import Client

from test_project.companies.models import Company

@pytest.mark.django_db
class TestGetCompanies(TestCase):

    def setUp(self)->None:
        self.client = Client()
        self.companies_url = reverse('companies-list')
    
    def tearDown(self) -> None:
        pass

    def test_zero_companies_should_return_empty_list(self)->None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_return_succeed(self)->None:
        test_company = Company.objects.create(name = "Amazon")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get('name'), test_company.name)
        self.assertEqual(response_content.get('status'), "Hiring")
        self.assertEqual(response_content.get('application_link'), "")
        self.assertEqual(response_content.get('notes'), "")

        test_company.delete()
