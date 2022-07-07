from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from projects.models import Project
from project_budget.models import ResourceSpending
from project_budget.models import ContractSpending
from accounts import views as account_views
from projects import views as project_views
from project_charter import views as project_charter_views
from project_resources import views as project_resources_views
from project_procurements import views as project_procurements_views
from project_budget import views as project_budget_views
from guardian.shortcuts import assign_perm


class ProjectBudgetTest(APITestCase):
    def generate_pmo_user_data(self):
        return {
            "first_name": "Luca",
            "last_name": "Verdi",
            "email": "pmo@email.com",
            "password": "pmo12345",
            "confirm_password": "pmo12345"
        }


    def generate_pm_user_data(self):
        return {
            "first_name": "Antonio",
            "last_name": "Bruno",
            "email": "pm@email.com",
            "password": "pm123456",
            "confirm_password": "pm123456"
        }


    def generate_ps_user_data(self):
        return {
            "first_name": "Giovanni",
            "last_name": "Valdieri",
            "email": "ps@email.com",
            "password": "ps123456",
            "confirm_password": "ps123456"
        }


    def generate_project_data(self, author):
        return {
            "project_name": "test project",
            "author": author
        }


    def generate_project_charter_data(self, author, project_id):
        return {
            "project": project_id,
            "author": author,
            "sow": "standard thesis outline",
            "contract": "Guida Studente DIGEP per la tesi",
            "business_case": "Research Case Digital PM"
        }


    def generate_project_budget_data(self):
        return [
            {
                "year": 2022,
                "budget": 23000.00
            },
            {
                "year": 2023,
                "budget": 20000.00
            }
        ]


    def generate_additional_budget_data(self, project, budget):
        return{
            "project": project,
            "budget": budget,
            "amount": 2000.00
        }


    def generate_project_resource_data(self, project_id):
        return {
            "project": project_id,
            "name": "engineer",
            "description": "price in eur/hour",
            "cost": 12.00,
            "category": "human"
        }


    def generate_resource_spending_data(self, project, resource, budget):
        return {
            "project": project,
            "resource": resource,
            "budget": budget,
            "assignment": 10,
            "description": "some information about spending",
            "date": "2022-05-12"
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


    def generate_contract_spending_data(self, project, contract, budget):
        return {
            "project": project,
            "contract": contract,
            "budget": budget,
            "description": "details of spending",
            "date": "2022-06-12"
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

    def post_create_project_charter(self, project_charter, token=None):
        url = reverse(project_charter_views.ProjectCharterAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=project_charter, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def post_set_project_budget(self, project_charter_id, budget, token=None):
        url = reverse(project_budget_views.ProjectBudgetAPI.name, None, {project_charter_id})
        auth_token = f'Token {token}'
        response = self.client.post(url, data=budget, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def patch_update_project_budget(self, project_budget_id, data, token=None):
        url = reverse(project_budget_views.EditProjectBudgetAPI.name, None, {project_budget_id})
        auth_token = f'Token {token}'
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def get_project_budget_details(self, budget_id, token=None):
        url = reverse(project_budget_views.ProjectBudgetDetailsAPI.name, None, {budget_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def get_actual_cost_of_project_by_budget(self, budget_id, token=None):
        url = reverse(project_budget_views.GetActualCostOfProjectByBudgetAPI.name, None, {budget_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def get_total_project_budget(self, project_charter_id, token=None):
        url = reverse(project_budget_views.TotalProjectBudgetAPI.name, None, {project_charter_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def delete_project_budget(self, budget_id, token=None):
        url = reverse(project_budget_views.DeleteProjectBudgetAPI.name, None, {budget_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def delete_total_project_budget(self, project_charter_id, token=None):
        url = reverse(project_budget_views.DeleteTotalProjectBudgetAPI.name, None, {project_charter_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_project_budget(self):
        """
            Ensure we can set and manage project budget with certain permissions
        """
        # register user
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        # register user pm
        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK
        
        # assign project charter permissions to a stakeholder
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        user = User.objects.get(pk=author)
        project = Project.objects.get(pk=project_id)
        assign_perm('project_charter.add_project_charter', user, project)

        # add a new project charter
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # set project budget
        project_charter_id = response.data.get('project_charter').get('id')
        budget = self.generate_project_budget_data()
        response = self.post_set_project_budget(project_charter_id=project_charter_id, budget=budget, 
            token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # edit budget
        assign_perm('project_charter.change_project_charter', user, project)
        budget_id = response.data[0].get('id')
        budget_data = budget[0]
        budget_data['budget'] = 30000.00
        response = self.patch_update_project_budget(project_budget_id=budget_id, data=budget_data, token=auth_token)
        assert response.status_code == status.HTTP_200_OK

        # get project budget details
        assign_perm('project_charter.view_project_charter', user, project)
        response = self.get_project_budget_details(budget_id=budget_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('budget') == 30000.00

        # get actual cost of project according to budget
        response = self.get_actual_cost_of_project_by_budget(budget_id=budget_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('year') == 2022
        assert response.data.get('budget') == 30000.00
        assert response.data.get('actual_cost') == 0.00
        assert response.data.get('resource_spending') == 0.00
        assert response.data.get('contract_spending') == 0.00

        # delete project budget instance 
        assign_perm('project_charter.delete_project_charter', user, project)
        response = self.delete_project_budget(budget_id=budget_id, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # get again to check deleted budget
        response = self.get_project_budget_details(budget_id=budget_id, token=auth_token)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # get total project budget
        response = self.get_total_project_budget(project_charter_id=project_charter_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        # delete total project budget
        response = self.delete_total_project_budget(project_charter_id=project_charter_id, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT
    

    ###### Test Additional Budget

    def post_request_additional_budget(self, budget, token=None):
        url = reverse(project_budget_views.RequestAdditionalBudgetAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=budget, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def patch_update_additional_budget_status(self, additional_budget_id, data, token=None):
        url = reverse(project_budget_views.UpdateAdditionalFundRequestStatusAPI.name, None, 
            {additional_budget_id})
        auth_token = f'Token {token}'
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def get_additional_budget_details(self, budget_id, token=None):
        url = reverse(project_budget_views.GetAdditionalBudgetDetailsAPI.name, None, {budget_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def get_additional_budget_requests(self, project_id, token=None):
        url = reverse(project_budget_views.GetAdditionalBudgetRequestsAPI.name, None, {project_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_additional_project_budget(self):
        """
            Ensure we can request and manage additional project budget with certain permissions
        """
        # register user
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project 
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        # register user pm
        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK
        
        # assign project charter permissions to a stakeholder
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        user = User.objects.get(pk=author)
        project = Project.objects.get(pk=project_id)
        assign_perm('project_charter.add_project_charter', user, project)

        # add a new project charter
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # set project budget
        project_charter_id = response.data.get('project_charter').get('id')
        budget = self.generate_project_budget_data()
        response = self.post_set_project_budget(project_charter_id=project_charter_id, budget=budget, 
            token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # request additional project budget as a project manager
        assign_perm('project_budget.add_additional_budget', user, project)
        budget_id = response.data[0].get('id')
        additional_budget = self.generate_additional_budget_data(project=project_id, budget=budget_id)
        response = self.post_request_additional_budget(budget=additional_budget, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        additional_budget_id = response.data.get('additional-budget').get('id')

        # register user project sponsor
        user = self.generate_ps_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PS')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # update additional budget status as project sponsor
        user_id = response.data['user']['id']
        auth_token = response.data['auth_token']
        user = User.objects.get(pk=user_id)
        assign_perm('project_budget.change_additional_budget', user, project)
        confirm_data = {"status": "approved"}
        response = self.patch_update_additional_budget_status(additional_budget_id=additional_budget_id,
            data=confirm_data, token=auth_token)
        assert response.status_code == status.HTTP_200_OK

        # get additional budget details
        assign_perm('project_budget.view_additional_budget', user, project)
        response = self.get_additional_budget_details(budget_id=budget_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('status') == 'approved'

        # get additional budget requests
        response = self.get_additional_budget_requests(project_id=project_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1



###### Test Resource Spending

    def post_add_project_resource(self, project_resource, token=None):
        url = reverse(project_resources_views.AddResourceAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=project_resource, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def post_add_resource_spending(self, spending, token=None):
        url = reverse(project_budget_views.AddResourceSpendingAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=spending, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def patch_update_resource_spending(self, spending_id, data, token=None):
        url = reverse(project_budget_views.UpdateResourceSpendingAPI.name, None, {spending_id})
        auth_token = f'Token {token}'
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def get_resource_spending_details(self, spending_id, token=None):
        url = reverse(project_budget_views.GetResourceSpendingDetailsAPI.name, None, {spending_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def get_resource_spendings_by_budget(self, budget_id, token=None):
        url = reverse(project_budget_views.GetResourceSpendingsByBudgetAPI.name, None, {budget_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def delete_resource_spending(self, spending_id, token=None):
        url = reverse(project_budget_views.DeleteResourceSpendingAPI.name, None, {spending_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_resource_spending(self):
        """
            Ensure we can manage resource spending with certain permissions
        """
        # register user
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project 
        author = response.data['user']['id']
        auth_token_pmo = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token_pmo)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        # register user pm
        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK
        
        # assign project charter permissions to a stakeholder
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        user = User.objects.get(pk=author)
        project = Project.objects.get(pk=project_id)
        assign_perm('project_charter.add_project_charter', user, project)

        # add a new project charter
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # set project budget
        project_charter_id = response.data.get('project_charter').get('id')
        budget = self.generate_project_budget_data()
        response = self.post_set_project_budget(project_charter_id=project_charter_id, budget=budget, 
            token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        budget_id = response.data[0].get('id')

        # add a new resource
        resource = self.generate_project_resource_data(project_id=project_id)
        response = self.post_add_project_resource(project_resource=resource, token=auth_token_pmo)
        assert response.status_code == status.HTTP_201_CREATED
        
        # add a resource spending
        assign_perm('project_budget.add_project_spending', user, project)
        resource_id = response.data.get('resource').get('id')
        spending_data = self.generate_resource_spending_data(project=project_id, resource=resource_id, 
            budget=budget_id)
        response = self.post_add_resource_spending(spending=spending_data, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # update resource spending
        assign_perm('project_budget.change_project_spending', user, project)
        resource_spending_id = response.data.get('resource-spending').get('id')
        spending_data['assignment'] = 25
        response = self.patch_update_resource_spending(spending_id=resource_spending_id, data=spending_data, 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK

        # get details of spending
        assign_perm('project_budget.view_project_spending', user, project)
        response = self.get_resource_spending_details(spending_id=resource_spending_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('assignment') == 25

        # get resource spending list by budget
        response = self.get_resource_spendings_by_budget(budget_id=budget_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        # delete resource spending
        assign_perm('project_budget.delete_project_spending', user, project)
        response = self.delete_resource_spending(spending_id=resource_spending_id, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        resource_spendings = ResourceSpending.objects.count()
        assert resource_spendings == 0




###### Test Contract Spending

    def post_add_project_contract(self, contract, token=None):
        url = reverse(project_procurements_views.AddContractAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=contract, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def post_add_contract_spending(self, spending, token=None):
        url = reverse(project_budget_views.AddContractSpendingAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=spending, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def patch_update_contract_spending(self, spending_id, data, token=None):
        url = reverse(project_budget_views.UpdateContractSpendingAPI.name, None, {spending_id})
        auth_token = f'Token {token}'
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def get_contract_spending_details(self, spending_id, token=None):
        url = reverse(project_budget_views.GetContractSpendingDetailsAPI.name, None, {spending_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def get_contract_spendings_by_budget(self, budget_id, token=None):
        url = reverse(project_budget_views.GetContractSpendingsByBudgetAPI.name, None, {budget_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def delete_contract_spending(self, spending_id, token=None):
        url = reverse(project_budget_views.DeleteContractSpendingAPI.name, None, {spending_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_contract_spending(self):
        """
            Ensure we can manage contract spending with certain permissions
        """
        # register user
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project 
        author = response.data['user']['id']
        auth_token_pmo = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token_pmo)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        # register user pm
        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK
        
        # assign project charter permissions to a stakeholder
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        user = User.objects.get(pk=author)
        project = Project.objects.get(pk=project_id)
        assign_perm('project_charter.add_project_charter', user, project)

        # add a new project charter
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # set project budget
        project_charter_id = response.data.get('project_charter').get('id')
        budget = self.generate_project_budget_data()
        response = self.post_set_project_budget(project_charter_id=project_charter_id, budget=budget, 
            token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        budget_id = response.data[0].get('id')

        # add a new contract
        contract = self.generate_project_contract_data(project_id=project_id)
        response = self.post_add_project_contract(contract=contract, token=auth_token_pmo)
        assert response.status_code == status.HTTP_201_CREATED
        
        # add a contract spending
        assign_perm('project_budget.add_project_spending', user, project)
        contract_id = response.data.get('contract').get('id')
        spending_data = self.generate_contract_spending_data(project=project_id, contract=contract_id, 
            budget=budget_id)
        response = self.post_add_contract_spending(spending=spending_data, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # update contract spending
        assign_perm('project_budget.change_project_spending', user, project)
        contract_spending_id = response.data.get('contract-spending').get('id')
        spending_data['description'] = "some information here"
        response = self.patch_update_contract_spending(spending_id=contract_spending_id, data=spending_data, 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK

        # get details of spending
        assign_perm('project_budget.view_project_spending', user, project)
        response = self.get_contract_spending_details(spending_id=contract_spending_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('description') == "some information here"

        # get contract spending list by budget
        response = self.get_contract_spendings_by_budget(budget_id=budget_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        # delete contract spending
        assign_perm('project_budget.delete_project_spending', user, project)
        response = self.delete_contract_spending(spending_id=contract_spending_id, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        contract_spendings = ContractSpending.objects.count()
        assert contract_spendings == 0




###### Test Forecasting

    def post_forecast_balance(self, budget_id, data, token=None):
        url = reverse(project_budget_views.ForecastBalanceAPI.name, None, {budget_id})
        auth_token = f'Token {token}'
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def post_forecast_future_spending(self, budget_id, data, token=None):
        url = reverse(project_budget_views.ForecastFutureSpendingAPI.name, None, {budget_id})
        auth_token = f'Token {token}'
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_forecasting(self):
        """
            Ensure we can forecast future spending with 'ViewProjectSpending' permission
        """
        # register user
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project 
        author = response.data['user']['id']
        auth_token_pmo = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token_pmo)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        # register user pm
        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK
        
        # assign project charter permissions to a stakeholder
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        user = User.objects.get(pk=author)
        project = Project.objects.get(pk=project_id)
        assign_perm('project_charter.add_project_charter', user, project)

        # add a new project charter
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # set project budget
        project_charter_id = response.data.get('project_charter').get('id')
        budget = self.generate_project_budget_data()
        response = self.post_set_project_budget(project_charter_id=project_charter_id, budget=budget, 
            token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        budget_id = response.data[0].get('id')
        forecast_data = {
            "total_scheduled_tasks": 64,
            "task_duration": 8,
            "employee_cost_day": 800,
            "actual_activity": [4, 5, 3, 4, 5, 7, 6, 3]
        }
        assign_perm('project_budget.view_project_spending', user, project)

        # forecast balance 
        response = self.post_forecast_balance(budget_id=budget_id, data=forecast_data, token=auth_token)
        assert response.status_code == status.HTTP_200_OK

        # forecast future spending
        response = self.post_forecast_future_spending(budget_id=budget_id, data=forecast_data, token=auth_token)
        assert response.status_code == status.HTTP_200_OK