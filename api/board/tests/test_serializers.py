from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from ..serializers import BoardSerializer
from ..models import Board

User = get_user_model()


class BoardSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            name="testuser",
            email="test@test.com",
            password="testpass123"
        )
        self.board = Board.objects.create(customer=self.user)

    def test_serializer_valid_data(self):
        
        data = {"customer": self.user.id}
        serializer = BoardSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_output(self):
        
        serializer = BoardSerializer(instance=self.board)
        data = serializer.data

        self.assertEqual(data["customer"], self.user.id)
        
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)
