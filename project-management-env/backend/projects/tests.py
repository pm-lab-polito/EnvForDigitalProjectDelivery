from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from projects.models import Project
from accounts import views as account_views
from projects import views as project_views
from guardian.shortcuts import get_user_perms


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


    def test_post_create_project(self):
        """
            Ensure we can create a project as Project Management Office
        """
        user = self.generate_pmo_user_data()
        reg_response = self.post_user_registration(user)
        self.define_user_role(reg_response, 'PMO')
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
            Ensure we can update a project name with permission of 'hasChangeProjectPermission'
        """
        user_pmo = self.generate_pmo_user_data()
        reg = self.post_user_registration(user_pmo)
        self.define_user_role(reg, 'PMO')
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
        assert response.status_code == status.HTTP_200_OK

        db_project = Project.objects.get(id=project_id)
        assert db_project.project_name == 'edited project'


    def delete_project(self, project_id, token=None):
        url = reverse(project_views.DeleteProjectAPI.name, None, {project_id})
        auth_token = f'Token {token}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_delete_project(self):
        """
            Ensure we can delete a project with permission of 'hasDeleteProjectPermission' 
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.define_user_role(reg, 'PMO')
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
            Ensure we can get details of a single project with permission of 'hasViewProjectPermission'
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.define_user_role(reg, 'PMO')
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


    def patch_add_stakeholder_to_project(self, project_id, stakeholders, token):
        url = reverse(project_views.AddStakeholdersToProjectAPI.name, None, {project_id})
        auth_token = 'Token '+token
        stakeholders = { "stakeholders": stakeholders}
        response = self.client.patch(url, data=stakeholders, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_patch_add_stakeholder_to_project(self):
        """
            Ensure a project author can add stakeholders to a project.
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.define_user_role(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data['project']['id']

        # register a new user
        user = self.generate_ps_user_data()
        reg = self.post_user_registration(user)
        assert reg.status_code == status.HTTP_201_CREATED
        self.define_user_role(reg, 'PS')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        stakeholders = [response.data.get('user').get('id')]
        
        # add a new stakeholder to project
        response = self.patch_add_stakeholder_to_project(project_id=project_id, stakeholders=stakeholders, 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('detail') == "Stakeholders added successfully"
        # count = author + new stakeholder
        assert Project.objects.get(id=project_id).stakeholders.count() == 2


    def patch_remove_stakeholder_from_project(self, project_id, stakeholders, token):
        url = reverse(project_views.RemoveStakeholdersFromProjectAPI.name, None, {project_id})
        auth_token = 'Token '+token
        stakeholders = { "stakeholders": stakeholders}
        response = self.client.patch(url, data=stakeholders, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_patch_remove_stakeholder_from_project(self):
        """
            Ensure a project author can remove stakeholders from a project.
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.define_user_role(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data['project']['id']

        # register a new user
        user = self.generate_ps_user_data()
        reg = self.post_user_registration(user)
        assert reg.status_code == status.HTTP_201_CREATED
        self.define_user_role(reg, 'PS')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        stakeholders = [response.data.get('user').get('id')]
        
        # add a new stakeholder to project
        response = self.patch_add_stakeholder_to_project(project_id=project_id, stakeholders=stakeholders, 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        # count = author + new stakeholder
        assert Project.objects.get(id=project_id).stakeholders.count() == 2

        # remove a stakeholder from project
        response = self.patch_remove_stakeholder_from_project(project_id=project_id, stakeholders=stakeholders, 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('detail') == "Stakeholders removed successfully"
        # count = author + new stakeholder
        assert Project.objects.get(id=project_id).stakeholders.count() == 1


    def get_stakeholders_of_project(self, project_id, token):
        url = reverse(project_views.GetStakeholdersOfProjectAPI.name, None, {project_id})
        auth_token = 'Token '+token
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_get_stakeholders_of_project(self):
        """
            Ensure we can get stakeholders of a project with permission of 'hasViewProjectPermission'.
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.define_user_role(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        stakeholder_1 = response.data.get('user')
        del stakeholder_1['is_active']

        # create a new project
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data['project']['id']

        # register a new user
        user = self.generate_ps_user_data()
        reg = self.post_user_registration(user)
        assert reg.status_code == status.HTTP_201_CREATED
        self.define_user_role(reg, 'PS')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        stakeholder_2 = response.data.get('user')
        del stakeholder_2['is_active']
        stakeholders = [response.data.get('user').get('id')]
        
        # add a new stakeholder to project
        response = self.patch_add_stakeholder_to_project(project_id=project_id, stakeholders=stakeholders, 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK

        # get stakeholders
        response = self.get_stakeholders_of_project(project_id=project_id, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['stakeholders']) == 2
        self.assertEqual([stakeholder_1, stakeholder_2], response.data['stakeholders'])


    def get_projects_of_stakeholder(self, token):
        url = reverse(project_views.GetProjectsOfStakeholderAPI.name)
        auth_token = 'Token '+token
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def test_get_projects_of_stakeholder(self):
        """
            Ensure a stakeholder can get a project list where he is a stakeholder as Account owner.
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.define_user_role(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project_id = response.data['project']['id']

        # register a new user
        user = self.generate_ps_user_data()
        reg = self.post_user_registration(user)
        assert reg.status_code == status.HTTP_201_CREATED
        self.define_user_role(reg, 'PS')
        login_res = self.post_user_login(user)
        assert login_res.status_code == status.HTTP_200_OK

        stakeholders = [login_res.data.get('user').get('id')]
        
        # add a new stakeholder to project
        response = self.patch_add_stakeholder_to_project(project_id=project_id, stakeholders=stakeholders, 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK

        # get projects of stakeholder
        auth_token = login_res.data['auth_token']
        response = self.get_projects_of_stakeholder(token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    
    def post_assign_project_permissions(self, user_id, project_id, perms, token):
        url = reverse(project_views.AddProjectPermissionsOfUserAPI.name)
        auth_token = 'Token '+token
        permissions = { 
            "user_id": user_id,
            "project_id": project_id,
            "permissions": perms
        }
        response = self.client.post(url, data=permissions, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def get_project_permissions_of_stakeholder(self, user_id, project_id, token):
        url = reverse(project_views.GetProjectPermissionsOfUserAPI.name, None, [user_id, project_id])
        auth_token = 'Token '+token
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def post_delete_project_permissions(self, user_id, project_id, perms, token):
        url = reverse(project_views.DeleteProjectPermissionsOfUserAPI.name)
        auth_token = 'Token '+token
        permissions = { 
            "user_id": user_id,
            "project_id": project_id,
            "permissions": perms
        }
        response = self.client.post(url, data=permissions, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def post_assign_all_project_permissions(self, user_id, project_id, token):
        url = reverse(project_views.AssignAllProjectPermissionsToStakeholderAPI.name)
        auth_token = 'Token '+token
        data = { 
            "user_id": user_id,
            "project_id": project_id
        }
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_project_permissions(self):
        """
            Ensure a project author can assign and delete main project permissions of stakeholders of the project.
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.define_user_role(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project = Project.objects.get(id=response.data['project']['id'])

        # register a new user
        user = self.generate_ps_user_data()
        reg = self.post_user_registration(user)
        assert reg.status_code == status.HTTP_201_CREATED
        
        self.define_user_role(reg, 'PS')
        user = User.objects.get(pk=reg.data.get('user').get('id'))

        # add a new stakeholder to project
        response = self.patch_add_stakeholder_to_project(project_id=project.id, stakeholders=[user.id], 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK

        # assign main project permissions to a stakeholder
        assert not get_user_perms(user, project)
        permissions = ["change_project", "add_project", "delete_project", "view_project"]
        response = self.post_assign_project_permissions(user_id=user.id, project_id=project.id, 
            perms=permissions, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        # get project permissions of a stakeholder
        response = self.get_project_permissions_of_stakeholder(user_id=user.id, project_id=project.id, 
            token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        perms = response.data.get('permissions')
        self.assertEqual(list(perms).sort(), permissions.sort())

        # delete main project permissions of a stakehodler
        response = self.post_delete_project_permissions(user_id=user.id, project_id=project.id, 
            perms=permissions, token=auth_token)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not get_user_perms(user, project)

        # assign all permissions
        response = self.post_assign_all_project_permissions(user_id=user.id, project_id=project.id, 
            token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(get_user_perms(user, project)) == 20
    


    def get_actual_cost_of_project(self, project_id, token):
        url = reverse(project_views.GetActualCostOfProjectAPI.name, None, [project_id])
        auth_token = 'Token '+token
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_get_actual_cost_of_project(self):
        """
            Ensure we can get actual cost of project with permission of 'hasViewProjectPermission'.
        """
        user = self.generate_pmo_user_data()
        reg = self.post_user_registration(user)
        self.define_user_role(reg, 'PMO')
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK

        # create a new project
        author = response.data['user']['id']
        auth_token = response.data['auth_token']
        project = self.generate_project_data(author=author)
        response = self.post_create_project(project=project, token=auth_token)
        assert response.status_code == status.HTTP_201_CREATED

        project = response.data['project']['id']

        # get actual cost
        response = self.get_actual_cost_of_project(project_id=project, token=auth_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('actual_cost') == 0.00
        assert response.data.get('resource_spendings') == 0.00
        assert response.data.get('contract_spendings') == 0.00
    