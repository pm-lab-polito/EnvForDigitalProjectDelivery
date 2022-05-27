from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from project_charter.models import ProjectCharter, BusinessCaseSWOT
from accounts import views as account_views
from projects import views as project_views
from project_charter import views as project_charter_views


class ProjectTest(APITestCase):
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


    def activate_user(self, user, role=None):
        db_user = User.objects.get(pk=user.data['user']['id'])
        db_user.user_role = role
        db_user.is_active = True
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
        response = self.client.post(url, data=project_charter,
             HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_post_create_project_charter(self):
        """
            Ensure we can create a project charter as registered PM stakeholder
        """
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.activate_user(reg_response, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # Authorized Project Management can create a new project charter
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.activate_user(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # create existing project charter
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def patch_edit_project_charter(self, project_charter_id, data, token=None):
        url = reverse(project_charter_views.EditProjectCharterAPI.name, None, {project_charter_id})
        auth_token = f'Token {token}'
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def test_patch_edit_project_charter(self):
        """
            Ensure we can update a project charter as Project Manager
        """
        user_pmo = self.generate_pmo_user_data()
        reg = self.post_user_registration(user_pmo)
        self.activate_user(reg, 'PMO')
        response = self.post_user_login(user_pmo)
        assert response.status_code == status.HTTP_200_OK

        author = response.data.get('user').get('id')
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.activate_user(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        author = response.data.get('user').get('id')
        auth_token = response.data['auth_token']
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_charter['sow'] = 'new sow'
        id = response.data.get('project_charter').get('id')
        response = self.patch_edit_project_charter(project_charter_id=id, data=project_charter)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.patch_edit_project_charter(project_charter_id=id, data=project_charter, 
            token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        db_project = ProjectCharter.objects.get(id=id)
        assert db_project.sow == 'new sow'


    def delete_project_charter(self, project_charter_id, token=None):
        url = reverse(project_charter_views.DeleteProjectCharterAPI.name, None, {project_charter_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
       

    def test_delete_project_charter(self):
        """
            Ensure we can delete a project charter as registered Project Manager
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.activate_user(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # Authorized Project Manager can delete a project charter
        author = response.data.get('user').get('id')
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.activate_user(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        author = response.data.get('user').get('id')
        auth_token = response.data.get('auth_token')
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_charter_id = response.data.get('project_charter').get('id')
        response = self.delete_project_charter(project_charter_id=project_charter_id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        response = self.delete_project_charter(project_charter_id=project_charter_id, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert ProjectCharter.objects.count() == 0

        # delete non existing project charter
        response = self.delete_project_charter(project_charter_id=project_charter_id, token=auth_token)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def get_project_charter_details(self, project_charter_id, token=None):
        url = reverse(project_charter_views.ProjectCharterDetailsAPI.name, None, {project_charter_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_get_project_charter_details(self):
        """
            Ensure we can get details of a project charter as an authenticated stakeholder
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.activate_user(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        author = response.data.get('user').get('id')
        auth_token = response.data.get('auth_token')
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED


        id = response.data.get('project_charter').get('id')
        response = self.get_project_charter_details(project_charter_id=id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == id

        # none existing project charter
        id = 3
        response = self.get_project_charter_details(project_charter_id=id, token=auth_token)
        assert response.status_code == status.HTTP_404_NOT_FOUND






    ############# Business Case SWOT ######

    def post_add_bus_case_swot(self, swot, token=None):
        url = reverse(project_charter_views.BusinessCaseSWOTAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=swot, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_post_add_bus_case_swot(self):
        """
            Ensure we can add a new bus_case swot as registered PM stakeholder
        """
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.activate_user(reg_response, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        author = response.data.get('user').get('id')
        auth_token = response.data.get('auth_token')
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.activate_user(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        author = response.data.get('user').get('id')
        auth_token = response.data.get('auth_token')
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        id = response.data.get('project_charter').get('id')
        swot = {
            "project_charter": id,
            "swot_type": "opportunity",
            "content": "Very small legacy in PIMS"
        }
        response = self.post_add_bus_case_swot(swot=swot)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.post_add_bus_case_swot(swot=swot, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED
        assert BusinessCaseSWOT.objects.count() == 1

        db_swot = BusinessCaseSWOT.objects.get(id=response.data.get('swot').get('id'))
        assert db_swot.swot_type == "opportunity"
        assert db_swot.content == "Very small legacy in PIMS"


    def delete_bus_case_swot(self, swot_id, token=None):
        url = reverse(project_charter_views.DeleteBusinessCaseSWOTAPI.name, None, {swot_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
       

    def test_delete_bus_case_swot(self):
        """
            Ensure we can delete a bus_case swot as registered Project Manager
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.activate_user(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # Authorized Project Manager can delete a bus_case swot
        author = response.data.get('user').get('id')
        auth_token = response.data.get('auth_token')
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')

        user = self.generate_pm_user_data()
        reg_response = self.post_user_registration(user)
        self.activate_user(reg_response, 'PM')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        author = response.data.get('user').get('id')
        auth_token = response.data.get('auth_token')
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        id = response.data.get('project_charter').get('id')
        swot = {
            "project_charter": id,
            "swot_type": "opportunity",
            "content": "Very small legacy in PIMS"
        }
        response = self.post_add_bus_case_swot(swot=swot, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        swot_id = response.data.get('swot').get('id')
        response = self.delete_bus_case_swot(swot_id=swot_id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        response = self.delete_bus_case_swot(swot_id=swot_id, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert BusinessCaseSWOT.objects.count() == 0

        # delete non existing bus case swot
        response = self.delete_bus_case_swot(swot_id=swot_id, token=auth_token)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def get_bus_case_swot_details(self, swot_id, token=None):
        url = reverse(project_charter_views.SWOTDetailsAPI.name, None, {swot_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_get_bus_case_swot_details(self):
        """
            Ensure we can get details of a swot as an authenticated stakeholder
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.activate_user(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        author = response.data.get('user').get('id')
        auth_token = response.data.get('auth_token')
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        id = response.data.get('project_charter').get('id')
        swot = {
            "project_charter": id,
            "swot_type": "opportunity",
            "content": "Very small legacy in PIMS"
        }
        response = self.post_add_bus_case_swot(swot=swot, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        swot_id = response.data.get('swot').get('id')
        response = self.get_bus_case_swot_details(swot_id=swot_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('id') == swot_id
        assert response.data.get('swot_type') == "opportunity"
        assert response.data.get('content') == "Very small legacy in PIMS"

        # none existing project charter
        id = 3
        response = self.get_bus_case_swot_details(swot_id=id, token=auth_token)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def get_swot_list(self, project_charter_id, token):
        url = reverse(project_charter_views.SWOTListOfProjectCharterAPI.name, None, {project_charter_id})
        auth_token = 'Token '+token
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def test_get_swot_list(self):
        """
            Ensure we can get a list of bus_case swot as an authenticated stakeholder
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.activate_user(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data.get('project').get('id')
        project_charter = self.generate_project_charter_data(author=author, project_id=project_id)
        response = self.post_create_project_charter(project_charter=project_charter, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        id = response.data.get('project_charter').get('id')
        swot = {
            "project_charter": id,
            "swot_type": "opportunity",
            "content": "Very small legacy in PIMS"
        }
        response = self.post_add_bus_case_swot(swot=swot, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        response = self.get_swot_list(project_charter_id=id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get("swot-list")) == 1


    