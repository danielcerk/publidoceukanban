from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta

from api.board.models import Board
from ..models import Card, Feedback

from django.contrib.auth import get_user_model

User = get_user_model()

class CardModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(

            name='daniel', email='daniel@gmail.com',
            password='1234'

        )

        self.board = Board.objects.create(customer=self.user)

    def test_create_valid_card(self):

        card = Card.objects.create(
            board=self.board,
            title='Card Teste',
            description='Descrição do card',
        )
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(str(card), 'Card Teste')
        self.assertTrue(card.is_active)
        self.assertEqual(card.status, 'todo')

    def test_card_invalid_due_date_before_start_date(self):

        start = date.today()
        due = start - timedelta(days=1)

        card = Card(
            board=self.board,
            title='Card com erro de data',
            start_date=start,
            due_date=due
        )

        with self.assertRaises(ValidationError) as context:
            card.full_clean()

        self.assertIn('A data de entrega não pode ser anterior à data de início.', str(context.exception))

    def test_card_default_image(self):

        card = Card.objects.create(
            board=self.board,
            title='Card sem imagem'
        )
        self.assertEqual(
            card.image,
            'https://storage.googleapis.com/star-lab/blog/OGs/image-not-found.png'
        )

    def test_card_status_choices(self):

        card = Card.objects.create(
            board=self.board,
            title='Card status válido',
            status='done'
        )
        self.assertEqual(card.status, 'done')

        card_invalid = Card(
            board=self.board,
            title='Card inválido',
            status='invalido'
        )
        with self.assertRaises(ValidationError):
            card_invalid.full_clean()


class FeedbackModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(

            name='daniel', email='daniel@gmail.com',
            password='1234'

        )

        self.board = Board.objects.create(customer=self.user)
        self.card = Card.objects.create(board=self.board, title='Card Teste')

    def test_create_feedback(self):

        feedback = Feedback.objects.create(
            card=self.card,
            text='Esse card precisa de ajustes'
        )
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertEqual(feedback.card, self.card)
        self.assertEqual(str(feedback), f'Feedback ref. {self.card.title}')
