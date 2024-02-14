import stripe
from homework import settings


class StripeHelpers:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    @staticmethod
    def create_customer(email):
        try:
            stripe_customer = stripe.Customer.create(email=email)
            return stripe_customer.id
        except stripe.error.AuthenticationError as e:
            raise e

    @staticmethod
    def create_payment_intent(amount, currency, customer):
        try:
            payment_intent = stripe.PaymentIntent.create(amount=amount, currency=currency,
                                                         payment_method_types=["card"], customer=customer)
            return payment_intent.id, payment_intent.status
        except stripe.error.AuthenticationError as e:
            raise e
        except stripe.error.SignatureVerificationError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def confirm_payment_intent(payment_id):
        try:
            payment_intent = stripe.PaymentIntent.confirm(payment_id, payment_method="pm_card_visa",
                                                          return_url="http://127.0.0.1:8000/chats/payment/success/")
            return payment_intent.next_action.redirect_to_url.url, payment_intent.status
        except stripe.error.AuthenticationError as e:
            raise e
        except stripe.error.SignatureVerificationError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def retrieve_payment_intent(payment_id):
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_id)
            return payment_intent.status
        except stripe.error.AuthenticationError as e:
            raise e
        except stripe.error.SignatureVerificationError as e:
            raise e
        except Exception as e:
            raise e
