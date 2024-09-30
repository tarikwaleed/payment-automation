from abc import ABC, abstractmethod
class PaymentManager(ABC):
    def __init__(self, payment_link, payment_method, personal_info=None):
        self.payment_link = payment_link
        self.personal_info = personal_info
        self.payment_method = payment_method
        self.driver = None  # WebDriver instance
    @abstractmethod
    def initialize_driver(self):
        """Initialize the web driver."""
        pass

    @abstractmethod
    def automate_payment(self):
        """Automate the payment process."""
        pass

    @abstractmethod
    def close_driver(self):
        """Close the web driver and clean up resources."""
        pass
