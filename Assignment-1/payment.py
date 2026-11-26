from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def get_details(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass

class RazorpayCardPayment(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number

    def get_details(self):
        return "Razorpay Card ending in " + self.card_number[-4:]

    def pay(self, amount):
        print("Charged Rs", amount, "to Razorpay Card")
        return True

class RazorpayUPIPayment(PaymentMethod):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def get_details(self):
        return "Razorpay UPI: " + self.upi_id

    def pay(self, amount):
        print("Charged Rs", amount, "to Razorpay UPI")
        return True

class StripeCardPayment(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number

    def get_details(self):
        return "Stripe Card ending in " + self.card_number[-4:]

    def pay(self, amount):
        print("Charged Rs", amount, "to Stripe Card")
        return True

class StripeUPIPayment(PaymentMethod):
    def __init__(self, upi_id, token=""):
        self.upi_id = upi_id
        self.token = token

    def get_details(self):
        return "Stripe UPI: " + self.upi_id

    def pay(self, amount):
        print("Charged Rs", amount, "to Stripe UPI")
        return True

#Factories
class FactoryPaymentMethod:
    factory = {}

    @classmethod
    def get_payment_object(cls, method_type, **kwargs):
        if method_type not in cls.factory:
            print("Method not supported")
            return None
        return cls.factory[method_type](**kwargs)

class RazorpayFactory(FactoryPaymentMethod):
    factory = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment
    }

class StripeFactory(FactoryPaymentMethod):
    factory = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment
    }
