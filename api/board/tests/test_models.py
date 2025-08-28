from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Board
from django.utils.timezone import now
import time

User = get_user_model()

class BoardModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            name="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.board = Board.objects.create(customer=self.user)

    def test_board_creation(self):

        self.assertEqual(Board.objects.count(), 2)
        self.assertEqual(self.board.customer, self.user)

    def test_str_representation(self):
        
        self.assertEqual(str(self.board), f"Quadro de {self.user}")

    def test_created_at_auto_field(self):

        self.assertIsNotNone(self.board.created_at)

    def test_updated_at_auto_field(self):

        old_updated_at = self.board.updated_at
        time.sleep(0.1)
        self.board.customer = self.user
        self.board.save()
        self.board.refresh_from_db()
        self.assertGreater(self.board.updated_at, old_updated_at)
