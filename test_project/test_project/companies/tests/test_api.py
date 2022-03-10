# Register Django Settings to run the file
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adjust_test.settings")
django.setup()

import json

import pytest

from django.urls import reverse

from test_project.companies.models import Company

companies_url = reverse('companies-list')
pytestmark = pytest.mark.django_db


def test_zero_companies_should_return_empty_list(client)->None:
    response = client.get(companies_url)
    assert response.status_code== 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_return_succeed(client)->None:
    test_company = Company.objects.create(name = "Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get('name') == test_company.name
    assert response_content.get('status') == "Hiring"
    assert response_content.get('application_link') == ""
    assert response_content.get('notes') == ""

   
def test_create_company_without_arguments_should_fail(client)->None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name":["This field is required."]}

def test_create_existing_company_should_fail(client)->None:
    test_company = Company.objects.create(name = "Amazon")
    response = client.post(path=companies_url, data={"name":"Amazon"})
    assert response.status_code == 400
    assert json.loads(response.content) == {"name":["company with this name already exists."]}

def test_create_company_with_only_name_all_fields_should_be_default(client)->None:
    response = client.post(path=companies_url, data={"name":"Amazon"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get('name') == "Amazon"
    assert response_content.get('status') == "Hiring"
    assert response_content.get('application_link') == ""
    assert response_content.get('notes') == ""

def test_create_company_with_name_and_layoffs_status(client)->None:
    response = client.post(path=companies_url, data={"name":"Amazon", "status": "Layoffs"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get('name') == "Amazon"
    assert response_content.get('status') == "Layoffs"
    assert response_content.get('application_link') == ""
    assert response_content.get('notes') == ""

def test_create_company_with_wrong_status_should_fail(client)->None:
    response = client.post(path=companies_url, data={"name":"Amazon", "status": "wrongStatus"})
    assert response.status_code == 400
    assert "wrongStatus" in str(response.content)
    assert "is not a valid choice" in str(response.content)

# Example of test which can fail but the sets should complete
@pytest.mark.xfail
def test_can_fail()->None:
    assert 1==2

# Example of test which should be skipped
@pytest.mark.skip
def test_should_be_skipped()->None:
    assert 1==2

# Example of test which will raise an Exception with a specific string
def raise_covid19_exception()->None:
    raise ValueError("CoronaVirus Exception")

def test_raise_covid19_exception_should_pass()->None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)