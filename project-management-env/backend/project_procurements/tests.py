from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from project_procurements.models import Contract
from accounts import views as account_views
from projects import views as project_views
from project_procurements import views as project_procurements_views


class ProjectProcurementsTest(APITestCase):
    def generate_pmo_user_data(self):
        return {
            "first_name": "Luca",
            "last_name": "Verdi",
            "email": "pmo@email.com",
            "password": "pmo12345",
            "confirm_password": "pmo12345"
        }


    def generate_project_data(self, author):
        return {
            "project_name": "test project",
            "author": author
        }


    def generate_project_contract_data(self, project_id):
        return {
            "project": project_id,
            "product": "wood",
            "description": "wood with good quality",
            "unit_price": 2.50,
            "assignment": 100,
            "supplier": "New Wood MMC",
            "date": "2022-06-09"
        }


    def define_user_role(self, user, role=None):
        db_user = User.objects.get(pk=user.data['user']['id'])
        db_user.user_role = role
        db_user.save()


    def post_user_registration(self, user):
        url = reverse(account_views.RegisterAPI.name)
        response = self.client.post(url, data=user, format='json')
        return response


    def post_user_login(self, user):
        url = reverse(account_views.LoginAPI.name)
        response = self.client.post(url, data=user, format='json')
        return response
        

    def post_create_project(self, project, token=None):
        url = reverse(project_views.ProjectAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=project, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def post_add_project_contract(self, contract, token=None):
        url = reverse(project_procurements_views.AddContractAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=contract, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def patch_update_project_contract(self, contract_id, data, token=None):
        url = reverse(project_procurements_views.UpdateContractAPI.name, None, {contract_id})
        auth_token = f'Token {token}'
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def get_project_contract(self, contract_id, token=None):
        url = reverse(project_procurements_views.GetContractDetailsAPI.name, None, {contract_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def get_list_of_project_contract(self, project_id, token=None):
        url = reverse(project_procurements_views.GetContractsOfProjectAPI.name, None, {project_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def delete_project_contract(self, contract_id, token=None):
        url = reverse(project_procurements_views.DeleteContractAPI.name, None, {contract_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    def test_project_contract(self):
        """
            Ensure we can add and manage a project contract with certain permissions
        """
        # register user
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # Create a new project
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        # add a new project contract
        contract = self.generate_project_contract_data(project_id=project_id)
        response = self.post_add_project_contract(contract=contract, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED
        
        contract_id = response.data.get('contract').get('id')

        # get list of contracts
        response = self.get_list_of_project_contract(project_id=project_id, token=auth_token)
        assert len(response.data) == 1

        # update project contract
        contract["assignment"] = 150
        response = self.patch_update_project_contract(contract_id=contract_id, data=contract, 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        contracts = Contract.objects.all()
        assert contracts[0].assignment == 150

        # get a contract
        response = self.get_project_contract(contract_id=contract_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('project') == project_id
        assert response.data.get('product') == 'wood'
        assert response.data.get('unit_price') == 2.50

        # remove project contract
        response = self.delete_project_contract(contract_id=contract_id, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        contracts = Contract.objects.all()
        assert contracts.count() == 0
        


    
    
