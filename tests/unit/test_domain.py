
import unittest
from datetime import date
from decimal import Decimal
from Src.domain.models import CreditCard
from Src.domain.services import CreditCardService
from Src.infrastructure.repository import InMemoryRepository

class TestCreditCardService(unittest.TestCase):

    def setUp(self):
        """Configura um novo repositório em memória para cada teste."""
        self.repository = InMemoryRepository()
        self.service = CreditCardService(self.repository)
        
        # Reinicia os dados do repositório antes de cada teste
        self.repository.cards = {
            1: CreditCard(id=1, limit_total=Decimal('10000.00'), limit_available=Decimal('10000.00'))
        }
        self.repository.purchases = {}
        self.repository.installments = []
        self.repository.next_purchase_id = 1
        self.repository.next_installment_id = 1

    def test_register_installment_purchase_success(self):
        """Testa o registro de uma compra parcelada com sucesso."""
        card_id = 1
        total_value = Decimal('1200.00')
        num_installments = 12
        
        purchase = self.service.register_installment_purchase(
            card_id=card_id,
            total_value=total_value,
            num_installments=num_installments,
            description="Notebook",
            category="Electronics",
            transaction_date=date(2023, 1, 10)
        )
        
        # 1. Verifica se o limite do cartão foi debitado corretamente
        updated_card = self.repository.get_card(card_id)
        self.assertEqual(updated_card.limit_available, Decimal('8800.00'))
        
        # 2. Verifica se a compra foi salva
        self.assertIn(purchase.id, self.repository.purchases)
        
        # 3. Verifica se as parcelas foram criadas corretamente
        self.assertEqual(len(purchase.installments), num_installments)
        
        # 4. Verifica o valor das parcelas (1200 / 12 = 100)
        for installment in purchase.installments:
            self.assertEqual(installment.value, Decimal('100.00'))

    def test_register_purchase_insufficient_limit(self):
        """Testa a falha no registro de compra por limite insuficiente."""
        with self.assertRaises(ValueError):
            self.service.register_installment_purchase(
                card_id=1,
                total_value=Decimal('15000.00'), # Maior que o limite
                num_installments=10,
                description="Viagem",
                category="Lazer",
                transaction_date=date(2023, 2, 5)
            )

    def test_close_invoice_with_installments(self):
        """Testa o fechamento da fatura com parcelas a serem lançadas."""
        # Cenário: Duas compras com parcelas que vencem em Março de 2023
        self.service.register_installment_purchase(
            card_id=1, total_value=Decimal('300.00'), num_installments=3, 
            description="Livro", category="Educação", transaction_date=date(2023, 2, 15)
        ) # Parcela 1 vence em Mar/2023 (R$100)
        
        self.service.register_installment_purchase(
            card_id=1, total_value=Decimal('500.00'), num_installments=5, 
            description="Jantar", category="Alimentação", transaction_date=date(2023, 1, 20)
        ) # Parcela 2 vence em Mar/2023 (R$100)

        # Fechar a fatura de Março de 2023
        total_closed = self.service.close_invoice(card_id=1, closing_month=3, closing_year=2023)
        
        # Verifica se o total da fatura está correto (100 + 100)
        self.assertEqual(total_closed, Decimal('200.00'))
        
        # Verifica se o saldo da fatura no cartão foi atualizado
        updated_card = self.repository.get_card(1)
        self.assertEqual(updated_card.current_invoice_balance, Decimal('200.00'))

    def test_close_invoice_no_installments(self):
        """Testa o fechamento da fatura sem parcelas para o mês."""
        total_closed = self.service.close_invoice(card_id=1, closing_month=5, closing_year=2023)
        
        self.assertEqual(total_closed, Decimal('0.00'))

if __name__ == '__main__':
    unittest.main()
