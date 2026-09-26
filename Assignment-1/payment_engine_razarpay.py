import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Type

@dataclass
class Item:
    name: str
    price: float
    quantity: int

class Order:
    @classmethod
    def from_dict(cls, data: Dict) -> "Order":
        items = [Item(**item) for item in data["items"]]
        return cls(data.get("order_id", "N/A"), items)

    def __init__(self, order_id, items: List[Item]):
        self.order_id = order_id
        self.items = items

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def grand_total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)

# Task 1: Payment Method 
class PaymentMethod(ABC):
    "Abstract base for every concrete payment method of every gateway."

    @abstractmethod
    def get_details(self) -> str:
        "Human-readable summary of the payment instrument."
        raise NotImplementedError

    @abstractmethod
    def pay(self, amount: float) -> bool:
        "Attempt to charge `amount`. Returns True on success."
        raise NotImplementedError


class RazorpayCardPayment(PaymentMethod):
    def __init__(self, card_number: str, card_holder: str = "", **kwargs):
        self.card_number = card_number
        self.card_holder = card_holder

    def get_details(self) -> str:
        return f"Razorpay Card ending in {self.card_number[-4:]}"

    def pay(self, amount: float) -> bool:
        print("Paying:", amount, "using Razorpay Card.")
        return True


class RazorpayUPIPayment(PaymentMethod):
    def __init__(self, upi_id: str, **kwargs):
        self.upi_id = upi_id

    def get_details(self) -> str:
        return f"Razorpay UPI ({self.upi_id})"

    def pay(self, amount: float) -> bool:
        print("Paying:", amount, "using Razorpay UPI.")
        return True


class StripeCardPayment(PaymentMethod):
    def __init__(self, card_number: str, token: str = "", **kwargs):
        self.card_number = card_number
        self.token = token

    def get_details(self) -> str:
        return f"Stripe Card ending in {self.card_number[-4:]}"

    def pay(self, amount: float) -> bool:
        print("Paying:", amount, "using Stripe Card.")
        return True

class StripeUPIPayment(PaymentMethod):
    def __init__(self, upi_id: str, token: str = "", **kwargs):
        self.upi_id = upi_id
        self.token = token

    def get_details(self) -> str:
        return f"Stripe UPI ({self.upi_id})"

    def pay(self, amount: float) -> bool:
        print("Paying:", amount, "using Stripe UPI.")
        return True
    
# Task 2: Payment Method Factory (Abstract Factory)

class FactoryPaymentMethod(ABC):
    "Every gateway-specific factory must expose a `factory` mapping."
    factory: Dict[str, Type[PaymentMethod]] = {}

    @classmethod
    def get_payment_object(cls, method_type: str, **kwargs) -> PaymentMethod:
        if method_type not in cls.factory:
            raise ValueError(
                f"Unsupported payment method '{method_type}' for {cls.__name__}. "
                f"Available: {list(cls.factory.keys())}"
            )
        return cls.factory[method_type](**kwargs)

class RazorpayFactory(FactoryPaymentMethod):
    factory = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment,
    }

class StripeFactory(FactoryPaymentMethod):
    factory = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment,
    }
# Task 3: Aggregator 
class Aggregator(ABC):
    name: str
    payment_factory: Type[FactoryPaymentMethod]

    def call_get_payment_object(self, method_type: str, amount: float, **kwargs) -> bool:
        "Delegates instantiation to the gateway's payment factory, then pays."
        try:
            payment_method = self.payment_factory.get_payment_object(method_type, **kwargs)
        except ValueError as exc:
            print("Error:", exc)
            return False
        return payment_method.pay(amount)
    
class RazorpayAggregator(Aggregator):
    def __init__(self):
        self.name = "Razorpay"
        self.processing_fee = 2.0  # percent
        self.payment_factory = RazorpayFactory


class StripeAggregator(Aggregator):
    def __init__(self):
        self.name = "Stripe"
        self.processing_fee = 2.9  # percent
        self.payment_factory = StripeFactory

# Task 4: Aggregator Factory

class AggregatorFactory:
    factory: Dict[str, Type[Aggregator]] = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator,
    }

    @classmethod
    def get_aggregator_object(cls, aggregator_name: str) -> Aggregator:
        if aggregator_name not in cls.factory:
            raise ValueError(
                f"Unsupported aggregator '{aggregator_name}'. "
                f"Available: {list(cls.factory.keys())}"
            )
        return cls.factory[aggregator_name]()

def process_order() -> List[Item]:
    items: List[Item] = []
    while True:
        name = input("Enter item name (or 'done' to finish): ")
        if name.lower() == "done":
            if not items:
                print("At least one item is required to place an order.")
                continue
            break
        try:
            price = float(input("Enter item price: "))
            quantity = int(input("Enter item quantity: "))
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue
        if price < 0 or quantity < 0:
            print("Price and quantity must be non-negative. Please try again.")
            continue
        items.append(Item(name, price, quantity))
    return items

# Task 5: CLI Client Workflow

def collect_payment_kwargs(method_type: str) -> Dict[str, str]:
    "Gathers the raw credential fields the chosen method needs."
    kwargs = {}
    if method_type == "card":
        kwargs["card_number"] = input("Enter card number: ").strip()
        kwargs["card_holder"] = input("Enter card holder name: ").strip()
    elif method_type == "upi":
        kwargs["upi_id"] = input("Enter UPI ID: ").strip()
    return kwargs


def main():
    print("=== Multi-Gateway Payment Processing Engine ===")

    order_id = input("Enter order ID: ")
    items = process_order()
    order = Order(order_id, items)
    print()
    print("Total items:", order.total_items)
    print("Grand total:", order.grand_total)
    print()

    # 1. Select Aggregator
    aggregator_name = input("Select Aggregator (stripe / razorpay): ").strip().lower()
    try:
        aggregator = AggregatorFactory.get_aggregator_object(aggregator_name)
    except ValueError as exc:
        print("Error:", exc)
        sys.exit(1)

    # 2. Select Method
    method_type = input("Select Method (card / upi): ").strip().lower()

    # 3. Enter Payment Details
    payment_kwargs = collect_payment_kwargs(method_type)

    # 4. Route execution dynamically (aggregator -> factory -> payment method -> pay)
    fee = order.grand_total * (aggregator.processing_fee / 100)
    total_with_fee = order.grand_total + fee
    print("Processing fee:", fee)
    print("Amount to charge:", total_with_fee)

    success = aggregator.call_get_payment_object(method_type, total_with_fee, **payment_kwargs)

    if success:
        print("Payment of", total_with_fee, "processed successfully.")
    else:
        print("Payment of", total_with_fee, "failed.")
if __name__ == "__main__":
    main()
