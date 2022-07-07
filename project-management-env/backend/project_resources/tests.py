from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from project_resources.models import Resource
from accounts import views as account_views
from projects import views as project_views
from project_resources import views as project_resources_views


class ProjectResourcesTest(APITestCase):
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


    def generate_project_resource_data(self, project_id):
        return {
            "project": project_id,
            "name": "engineer",
            "description": "price in eur/hour",
            "cost": 12.00,
            "category": "human"
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


    def post_add_project_resource(self, project_resource, token=None):
        url = reverse(project_resources_views.AddResourceAPI.name)
        auth_token = f'Token {token}'
        response = self.client.post(url, data=project_resource,
             HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def patch_update_project_resource(self, project_resource_id, data, token=None):
        url = reverse(project_resources_views.UpdateResourceAPI.name, None, {project_resource_id})
        auth_token = f'Token {token}'
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def get_project_resource(self, resource_id, token=None):
        url = reverse(project_resources_views.GetResourceAPI.name, None, {resource_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    
    def get_list_of_project_resource(self, project_id, token=None):
        url = reverse(project_resources_views.GetResourceListOfProjectAPI.name, None, {project_id})
        auth_token = f'Token {token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def delete_project_resource(self, project_resource_id, token=None):
        url = reverse(project_resources_views.RemoveResourceAPI.name, None, {project_resource_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response

    def test_project_resource(self):
        """
            Ensure we can add and manage a project resource with certain permissions
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

        # add a new project resource
        resource = self.generate_project_resource_data(project_id=project_id)
        response = self.post_add_project_resource(project_resource=resource, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED
        
        resource_id = response.data.get('resource').get('id')

        # get list of resources
        response = self.get_list_of_project_resource(project_id=project_id, token=auth_token)
        assert len(response.data) == 1

        # update project resource
        resource["cost"] = 11.00
        response = self.patch_update_project_resource(project_resource_id=resource_id, 
            data=resource, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        resources = Resource.objects.all()
        assert resources[0].cost == 11.00

        # get a resource 
        response = self.get_project_resource(resource_id=resource_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('project') == project_id
        assert response.data.get('name') == 'engineer'

        # remove project resource
        response = self.delete_project_resource(project_resource_id=resource_id, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        resources = Resource.objects.all()
        assert resources.count() == 0
        


    
    
