from payment import RazorpayFactory, StripeFactory

class Aggregator:
    def __init__(self):
        self.name = "Base"
        self.processing_fee = 0.0
        self.factory = None

    def call_get_payment_object(self, method_type, amount, **args):
        # get the object from the factory
        payment_obj = self.factory.get_payment_object(method_type, **args)
        
        if payment_obj is None:
            return False

        # calculate total with fee
        total = amount + (amount * self.processing_fee / 100)
        
        print("Processing:", payment_obj.get_details())
        print("Total to pay:", total)
        
        return payment_obj.pay(total)

class RazorpayAggregator(Aggregator):
    def __init__(self):
        self.name = "Razorpay"
        self.processing_fee = 2.0
        self.factory = RazorpayFactory

class StripeAggregator(Aggregator):
    def __init__(self):
        self.name = "Stripe"
        self.processing_fee = 2.9
        self.factory = StripeFactory

#Aggregator Factory

class AggregatorFactory:
    factory = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator
    }

    @classmethod
    def get_aggregator_object(cls, aggregator_name):
        if aggregator_name not in cls.factory:
            print("Unknown aggregator")
            return None
        return cls.factory[aggregator_name]()

# CLI

if __name__ == "__main__":
    print("Select Aggregator (stripe/razorpay): ")
    agg_name = input().lower()

    agg = AggregatorFactory.get_aggregator_object(agg_name)
    
    if agg:
        print("Select Method (card/upi): ")
        method = input().lower()

        # store details in a dictionary
        args = {}
        
        if method == "card":
            args["card_number"] = input("Enter card number: ")
        elif method == "upi":
            args["upi_id"] = input("Enter UPI ID: ")
            if agg_name == "stripe":
                # stripe needs this extra token
                args["token"] = input("Enter token: ")
        else:
            print("Invalid method")
            exit()

        try:
            amt = float(input("Enter amount: "))
            agg.call_get_payment_object(method, amt, **args)
        except ValueError:
            print("Invalid amount")
