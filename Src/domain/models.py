from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List, Optional

@dataclass
class CreditCard:
    id: int
    limit_total: Decimal
    limit_available: Decimal  # Afetado pelo valor total da compra
    current_invoice_balance: Decimal = Decimal('0.00') # Afetado pelas parcelas do mês
    
    def debit_limit(self, amount: Decimal):
        """Regra de negocio: Debita o limite disponivel (valor total da compra)."""
        if amount > self.limit_available:
            raise ValueError("Limite insuficiente.")
        self.limit_available -= amount

@dataclass
class Installment:
    id: Optional[int]
    purchase_id: int
    installment_number: int
    value: Decimal
    due_date: date
    is_posted_to_invoice: bool = False # Evita dupla contagem no fechamento

@dataclass
class Purchase:
    id: int
    card_id: int
    total_value: Decimal
    num_installments: int
    description: str
    category: str
    transaction_date: date
    installments: List[Installment]