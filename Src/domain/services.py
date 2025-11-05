from Src.domain.models import CreditCard, Purchase, Installment
from Src.infrastructure.repository import CreditCardRepository
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from typing import List

class CreditCardService:
    def __init__(self, repository: CreditCardRepository):
        self.repo = repository

    def register_installment_purchase(self, card_id: int, total_value: Decimal, num_installments: int, 
                                      description: str, category: str, transaction_date: date) -> Purchase:
        
        card = self.repo.get_card(card_id)
        
        # 1. Aplicar a regra do limite primeiro (valor total)
        card.debit_limit(total_value)
        self.repo.save_card(card)
        
        # 2. Calcular parcelas (garantindo precisao e distribuicao)
        base_value = (total_value * 100 // num_installments) / 100
        remainder = total_value - (base_value * num_installments)
        
        installments: List[Installment] = []
        
        for i in range(1, num_installments + 1):
            installment_value = base_value
            if i == 1:
                installment_value += remainder
                
            due_date = transaction_date + relativedelta(months=i)
            
            # ID é None, será preenchido pelo repositorio
            installment = Installment(
                id=None,
                purchase_id=-1, # Será ajustado na persistência
                installment_number=i,
                value=installment_value,
                due_date=due_date
            )
            installments.append(installment)

        # 3. Criar a entidade Purchase e persistir o agregado
        purchase = Purchase(
            id=-1, 
            card_id=card_id, 
            total_value=total_value, 
            num_installments=num_installments, 
            description=description,
            category=category,
            transaction_date=transaction_date,
            installments=installments
        )
        self.repo.save_purchase(purchase)
        
        return purchase

    def close_invoice(self, card_id: int, closing_month: int, closing_year: int) -> Decimal:
        """Agrega apenas as parcelas nao lançadas para a fatura do mes."""
        card = self.repo.get_card(card_id)
        
        installments_to_post = self.repo.get_installments_for_invoice(
            card_id, closing_month, closing_year
        )
        
        total_posted = Decimal('0.00')
        posted_ids = []

        for inst in installments_to_post:
            total_posted += inst.value
            posted_ids.append(inst.id)
            
        # Marca as parcelas como lançadas (Prevenção de Duplicidade)
        if posted_ids:
            self.repo.mark_installments_as_posted(posted_ids)
            
        card.current_invoice_balance = total_posted
        self.repo.save_card(card)
        
        return total_posted
