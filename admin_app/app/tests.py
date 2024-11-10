from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from .models import User, Items
from .utilities import JWT


class AdminDashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.add_new_user(
            name="adminuser",
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        self.token = JWT.generate_token(self.admin_user)

        self.client.cookies['jwt'] = self.token

        self.item = Items.objects.create(
            name="Test Item",
            type="Test Type",
            description="Test Description",
            price=100,
            amount=10,
            image=None,
            image_name="test_image.jpg"
        )

    def test_admin_dashboard_view(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'admin_dashboard.html')

    def test_admin_inventory_view(self):
        print(f"Token: {self.token}")
        response = self.client.get(reverse('admin_inventory'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.item.name)

    def test_admin_inventory_add_item(self):
        new_item_data = {
            'name': 'New Item',
            'category': 'New Category',
            'description': 'New Description',
            'price': 150,
            'amount': 20,
            'image_name': 'new_image.jpg',
            'action': 'add'
        }
        response = self.client.post(reverse('admin_inventory'), data=new_item_data)
        self.assertEqual(response.status_code,  status.HTTP_302_FOUND)
        self.assertTrue(Items.objects.filter(name='New Item').exists())

    def test_admin_inventory_edit_item(self):

        update_data = {
            'name': 'Updated Item',
            'category': 'Updated Category',
            'description': 'Updated Description',
            'price': 200,
            'amount': 30,
            'action': 'edit',
            'item_id': self.item.id
        }
        response = self.client.post(reverse('admin_inventory'), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        updated_item = Items.objects.get(id=self.item.id)
        self.assertEqual(updated_item.name, 'Updated Item')
        self.assertEqual(updated_item.price, 200)

    def test_admin_inventory_delete_item(self):
        delete_data = {
            'action': 'delete',
            'item_id': self.item.id
        }
        response = self.client.post(reverse('admin_inventory'), data=delete_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse(Items.objects.filter(id=self.item.id).exists())