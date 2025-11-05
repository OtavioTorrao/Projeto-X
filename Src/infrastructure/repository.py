from abc import ABC, abstractmethod
from typing import Dict, List
from Src.domain.models import CreditCard, Purchase, Installment
from decimal import Decimal

# Interface do Repositorio (Porta DDD) [9]
class CreditCardRepository(ABC):
    @abstractmethod
    def get_card(self, card_id: int) -> CreditCard:
        pass

    @abstractmethod
    def save_card(self, card: CreditCard):
        pass

    @abstractmethod
    def save_purchase(self, purchase: Purchase):
        pass

    @abstractmethod
    def get_installments_for_invoice(self, card_id: int, due_month: int, due_year: int) -> List[Installment]:
        pass
        
    @abstractmethod
    def mark_installments_as_posted(self, installments_ids: List[int]):
        pass


# Implementacao simples do Repositorio (Adaptador)
class InMemoryRepository(CreditCardRepository):
    # Base de dados simulada (JSON/local)
    cards: Dict[int, CreditCard] = {
        1: CreditCard(id=1, limit_total=Decimal('10000.00'), limit_available=Decimal('10000.00'))
    }
    purchases: Dict[int, Purchase] = {}
    installments: List[Installment] = []
    
    # Auto-increment
    next_purchase_id = 1
    next_installment_id = 1

    def get_card(self, card_id: int) -> CreditCard:
        if card_id not in self.cards:
            raise LookupError("Cartão não encontrado")
        return self.cards[card_id]

    def save_card(self, card: CreditCard):
        self.cards[card.id] = card

    def save_purchase(self, purchase: Purchase):
        purchase.id = self.next_purchase_id
        self.purchases[purchase.id] = purchase
        self.next_purchase_id += 1
        
        # Salvar as parcelas
        for inst in purchase.installments:
            inst.id = self.next_installment_id
            inst.purchase_id = purchase.id  # Corrigido: associar ao ID da compra
            self.installments.append(inst)
            self.next_installment_id += 1


    def get_installments_for_invoice(self, card_id: int, due_month: int, due_year: int) -> List[Installment]:
        """Consulta as parcelas que vencem no mes e ainda nao foram lancadas."""
        return [
            inst for inst in self.installments 
            if inst.purchase_id in self.purchases and 
               self.purchases[inst.purchase_id].card_id == card_id and
               inst.due_date.month == due_month and 
               inst.due_date.year == due_year and 
               not inst.is_posted_to_invoice
        ]
        
    def mark_installments_as_posted(self, installments_ids: List[int]):
        """Atualiza a flag para evitar contagem dupla."""
        for inst in self.installments:
            if inst.id in installments_ids:
                inst.is_posted_to_invoice = True
