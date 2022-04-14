from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from accounts import views
from knox.models import AuthToken


class AccountsTest(APITestCase):
    def generate_pmo_user_data(self):
        return {
            "first_name": "Luca",
            "last_name": "Verdi",
            "email": "pmo@email.com",
            "password": "pmo12345",
            "confirm_password": "pmo12345",
            "user_type": "PMO"
        }

    def generate_ps_user_data(self):
        return {
            "first_name": "Giovanni",
            "last_name": "Valdieri",
            "email": "ps@email.com",
            "password": "ps123456",
            "confirm_password": "ps123456",
            "user_type": "PS"
        }


    def post_user_resgistration(self, user):
        url = reverse(views.RegisterAPI.name)
        response = self.client.post(url, data=user, format='json')
        return response


    def test_post_and_get_registration(self):
        """
            Ensure we can create a new user account and then retrieve it
        """
        user = self.generate_pmo_user_data()
        response = self.post_user_resgistration(user)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        saved_user = User.objects.get()
        assert saved_user.email == user['email']
        assert saved_user.first_name == user['first_name']
        assert saved_user.last_name == user['last_name']
        assert saved_user.is_active == True


    def test_existing_user_email(self):
        """
            Ensure we cannot create a user account with an existing email
        """
        user = self.generate_ps_user_data()
        response1 = self.post_user_resgistration(user)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_user_resgistration(user)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST


    def post_user_login(self, user):
        url = reverse(views.LoginAPI.name)
        response = self.client.post(url, data=user, format='json')
        return response
        

    def test_user_login(self):
        """
            Ensure we can login with registered user account
        """
        user = self.generate_ps_user_data()
        self.post_user_resgistration(user)
        response = self.post_user_login(user)
        assert response.status_code == status.HTTP_200_OK
        tokens = AuthToken.objects.all()
        assert tokens.count() == 1


    def test_user_login_failure(self):
        """
            Ensure we cannot login with unregistered user account
        """
        fake_user = {
            "email": "fake@email.com",
            "password": "fake123456"
        }
        response = self.post_user_login(fake_user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def get_user_details(self, user_id, token):
        url = reverse(views.UserDetailsAPI.name, None, {user_id})
        auth_token = 'Token '+token
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response


    def test_get_user_details(self):
        """
            Ensure we can get details of a single user as PMO OR as an account owner 
                AND only with authenticated account
        """
        # Authorized user can get his data
        ps_user = self.generate_ps_user_data()
        reg_response1 = self.post_user_resgistration(ps_user)
        login_response1 = self.post_user_login(ps_user)
        response1 = self.get_user_details(reg_response1.data['user']['id'], 
                login_response1.data['auth_token'])
        assert response1.status_code == status.HTTP_200_OK

        # PMO account can get data of another user
        pmo_user = self.generate_pmo_user_data()
        reg_response2 = self.post_user_resgistration(pmo_user)
        login_response2 = self.post_user_login(pmo_user)
        response2 = self.get_user_details(reg_response1.data['user']['id'], 
                login_response2.data['auth_token'])
        assert response2.status_code == status.HTTP_200_OK


    def test_get_user_details_permissions(self):
        """
            Ensure we cann't get details of a single user if not an account owner 
                ANd authenticated account
        """
        # UnAuthorized user can not get data
        pmo_user = self.generate_pmo_user_data()
        reg_response1 = self.post_user_resgistration(pmo_user)
        response1 = self.get_user_details(reg_response1.data['user']['id'], 'withoutAUTH')
        assert response1.status_code == status.HTTP_401_UNAUTHORIZED

        # If not account owner can not get data
        ps_user = self.generate_ps_user_data()
        reg_response2 = self.post_user_resgistration(ps_user)
        login_response = self.post_user_login(ps_user)
        response2 = self.get_user_details(reg_response1.data['user']['id'], 
                login_response.data['auth_token'])
        assert response2.status_code == status.HTTP_403_FORBIDDEN


    def get_user_list(self, token):
        url = reverse(views.UserListAPI.name)
        auth_token = 'Token '+token
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_token, format='json')
        return response
    

    def test_get_user_list(self):
        """
            Ensure we can get a list of users as PMO user
        """
        # UnAuthorized user can not retrieve data
        ps_user = self.generate_ps_user_data()
        reg_response = self.post_user_resgistration(ps_user)
        response = self.get_user_list('withoutAUTH')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # not pmo_user
        login_response = self.post_user_login(ps_user)
        response = self.get_user_list(login_response.data['auth_token'])
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Authorized PMO user can retrieve data
        pmo_user = self.generate_pmo_user_data()
        reg_response = self.post_user_resgistration(pmo_user)
        login_response = self.post_user_login(pmo_user)
        response = self.get_user_list(login_response.data['auth_token'])
        assert response.status_code == status.HTTP_200_OK


    def test_patch_deactivate_and_activate_user(self):
        """
            Ensure, as PMO we can deactivate and activate user to prevent accessing system
        """

        # UnAuthorized user can not deactivate/activate a user
        ps_user = self.generate_ps_user_data()
        reg_response = self.post_user_resgistration(ps_user)
        user_id = reg_response.data['user']['id']
        url_activate = reverse(views.ActivateUserAPI.name, None, {user_id})
        url_deactivate = reverse(views.DeactivateUserAPI.name, None, {user_id})
        response1 = self.client.patch(url_deactivate, format='json')
        response2 = self.client.patch(url_activate, format='json')
        assert response1.status_code == status.HTTP_401_UNAUTHORIZED
        assert response2.status_code == status.HTTP_401_UNAUTHORIZED

        # not pmo_user
        login_response = self.post_user_login(ps_user)
        token = 'Token ' + login_response.data['auth_token']
        response1 = self.client.patch(url_deactivate, HTTP_AUTHORIZATION = token, format='json')
        response2 = self.client.patch(url_activate, HTTP_AUTHORIZATION = token, format='json')
        assert response1.status_code == status.HTTP_403_FORBIDDEN
        assert response2.status_code == status.HTTP_403_FORBIDDEN

        # Authorized PMO user can deactivate/activate a user 
        pmo_user = self.generate_pmo_user_data()
        reg_response = self.post_user_resgistration(pmo_user)
        login_response = self.post_user_login(pmo_user)
        token = 'Token ' + login_response.data['auth_token']
        saved_user = User.objects.get(id=user_id)
        assert saved_user.is_active == True

        response1 = self.client.patch(url_deactivate, HTTP_AUTHORIZATION = token, format='json')
        deactivated_user = User.objects.get(id=user_id)
        assert response1.status_code == status.HTTP_204_NO_CONTENT
        assert deactivated_user.is_active== False

        response2 = self.client.patch(url_activate, HTTP_AUTHORIZATION = token, format='json')
        activated_user = User.objects.get(id=user_id)
        assert response2.status_code == status.HTTP_204_NO_CONTENT
        assert activated_user.is_active == True


    def test_post_logout(self):
        """
            Ensure we can logout
        """
        # logout one user
        user = self.generate_ps_user_data()
        self.post_user_resgistration(user)
        login = self.post_user_login(user)
        auth_tokens = AuthToken.objects.all()
        assert auth_tokens.count() == 1

        token = 'Token ' + login.data['auth_token']
        url = reverse('knox-logout')
        response = self.client.post(url, HTTP_AUTHORIZATION=token, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        auth_tokens = AuthToken.objects.all()
        assert auth_tokens.count() == 0