from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.board.models import Board 

from ..models import Card, Feedback
from ..serializers import CardSerializer

User = get_user_model()


class CardSerializerSingleFeedbackTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='tester', email='test@example.com', password='123456'
        )
        self.board = Board.objects.create(customer=self.user)

    def test_create_card_without_feedback(self):
        data = {'title': 'Card simples', 'description': 'Sem feedback'}
        serializer = CardSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        card = serializer.save(board=self.board)

        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(card.title, 'Card simples')
        self.assertEqual(Feedback.objects.count(), 0)

    def test_create_card_with_feedback(self):
        data = {
            'title': 'Card com feedback',
            'description': 'Teste nested',
            'feedback': {'text': 'Primeiro feedback'},
        }
        serializer = CardSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        card = serializer.save(board=self.board)

        self.assertEqual(Card.objects.count(), 1)

    def test_update_card_add_feedback(self):
        card = Card.objects.create(title='Card update', board=self.board)

        data = {'feedback': {'text': 'Novo feedback'}}
        serializer = CardSerializer(instance=card, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        card.refresh_from_db()

    def test_serializer_output_contains_feedback(self):
        card = Card.objects.create(title='Card output', board=self.board)
        Feedback.objects.create(card=card, text='Feedback teste')

        serializer = CardSerializer(card)
        data = serializer.data

        self.assertIn('feedback', data)
        self.assertEqual(data['feedback']['text'], 'Feedback teste')
