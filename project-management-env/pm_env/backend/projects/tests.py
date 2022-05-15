from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from projects.models import Project
from accounts import views as account_views
from projects import views as project_views
from knox.models import AuthToken


class ProjectTest(APITestCase):
    def generate_pmo_user_data(self):
        return {
            "first_name": "Luca",
            "last_name": "Verdi",
            "email": "pmo@email.com",
            "password": "pmo12345",
            "confirm_password": "pmo12345"
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


    def test_post_create_project(self):
        """
            Ensure we can create a project as registered PMO stakeholder
        """
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.activate_user(reg_response, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # Authorized Project Management Office can create a new project
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('project').get('project_name') == project.get('project_name')


    def patch_edit_project_name(self, project_id, new_name, token=None):
        url = reverse(project_views.EditProjectAPI.name, None, {project_id})
        auth_token = f'Token {token}'
        project = {'project_name': new_name}
        response = self.client.patch(url, data=project, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def test_patch_edit_project_name(self):
        """
            Ensure we can update a project name as Project Management Office
        """
        user_pmo = self.generate_pmo_user_data()
        reg = self.post_user_registration(user_pmo)
        self.activate_user(reg, 'PMO')
        response = self.post_user_login(user_pmo)
        assert response.status_code == status.HTTP_200_OK

        # Authorized Project Management Office can edit a project name
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data['project']['id']
        response = self.patch_edit_project_name(project_id=project_id, new_name='edited project')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.patch_edit_project_name(project_id=project_id, 
            new_name='edited project', token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        db_project = Project.objects.get(id=project_id)
        assert db_project.project_name == 'edited project'


    def delete_project(self, project_id, token=None):
        url = reverse(project_views.DeleteProjectAPI.name, None, {project_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_delete_project(self):
        """
            Ensure we can delete a project as registered Project Management Office
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.activate_user(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # Authorized Project Management Office can delete a project 
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data['project']['id']
        response = self.delete_project(project_id=project_id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        response = self.delete_project(project_id=project_id, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        project_ids = Project.objects.all().values_list('id', flat=True)
        assert  project_id not in project_ids

        # delete non existing project
        response = self.delete_project(project_id=project_id, token=auth_token)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def get_project_details(self, project_id, token=None):
        url = reverse(project_views.ProjectDetailsAPI.name, None, {project_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_get_project_details(self):
        """
            Ensure we can get details of a single project as an authenticated stakeholder
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

        project_id = response.data['project']['id']
        response = self.get_project_details(project_id=project_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == project_id
        assert response.data['project_name'] == project['project_name']

        # none existing project
        project_id = 3
        response = self.get_project_details(project_id=project_id, token=auth_token)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def get_project_list(self, token):
        url = reverse(project_views.ProjectListAPI.name)
        auth_token = 'Token '+token
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def test_get_project_list(self):
        """
            Ensure we can get a list of projects as PMO stakeholder
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

        
        response = self.get_project_list(token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        user = self.generate_ps_user_data()
        reg = self.post_user_registration(user)
        self.activate_user(reg, 'PS')
        response = self.post_user_login(user)
        auth_token = response.data['auth_token']
        response = self.get_project_list(token=auth_token)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    