from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ModelMeta(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SSLCommerzPaymentSettings(models.Model):
    store_id = models.CharField(max_length=200, blank=True, null=True)
    store_pass = models.CharField(max_length=200, blank=True, null=True)
    is_sandbox = models.BooleanField(
        default=False, null=True, blank=True, help_text="Please Select No"
    )
    redirect_url = models.URLField(_("Redirect URL"), blank=True, null=True)

    def get_credentials(self):
        return {
            "store_id": self.store_id,
            "store_pass": self.store_pass,
            "is_sandbox": self.is_sandbox,
        }

    def get_redirect_url(self):
        return self.redirect_url

    class Meta:
        verbose_name = "SSLCommerz Settings"


class Order(ModelMeta):
    # transaction = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name="transactions",
    # )
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # payment_steam = models.ForeignKey(
    #     verbose_name="Payment Stream",
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    # )
    name = models.CharField(max_length=50)
    email = models.EmailField()
    reminder = models.BooleanField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("paid", "PAID"),
            ("unpaid", "UNPAID"),
        ],
        default="unpaid",
    )

    @property
    def store_amount(self):
        return self.transaction.store_amount

    def __str__(self):
        return f"{self.name} - {self.email}"


class Transaction(ModelMeta):
    channel = models.CharField(
        max_length=20, choices=[("sslcommerz", ("SSLcommerz"))], default="sslcommerz"
    )
    tran_id = models.CharField(
        _("Transaction ID"), max_length=20, blank=True, null=True
    )
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    store_amount = models.DecimalField(
        _("Store Amount"), max_digits=20, decimal_places=2, blank=True, null=True
    )
    tran_status = models.CharField(
        _("Transaction Status"),
        max_length=20,
        choices=[
            ("init", "Init"),
            ("cancel", "Cancel"),
            ("success", "Success"),
            ("failed", "Failed"),
        ],
        default="init",
    )
    tran_type = models.CharField(
        _("Transacton Type"),
        max_length=10,
        choices=[
            ("payment", "PAYMENT"),
            ("refund", "REFUND"),
        ],
        default="payment",
    )
    api_response = models.JSONField(_("API Response"), blank=True, null=True)

    def __str__(self):
        return f"{self.tran_id} - {self.tran_status}"


class PaymentStream(ModelMeta):
    # project = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )
    steam_name = models.TextField(_("Stream Name"))
    description = models.TextField(blank=True, null=True)
    goal_amount = models.DecimalField(
        _("Goal Amount"), max_digits=20, decimal_places=2, blank=True, null=True
    )
    package_amount = models.DecimalField(
        _("Package Amount"), max_digits=20, decimal_places=2, blank=True, null=True
    )
    is_package = models.BooleanField(
        _("Is Package"), default=False, blank=True, null=True
    )
    is_active = models.BooleanField(_("Is Active"), default=True, blank=True, null=True)

    def __str__(self):
        return self.steam_name

    @property
    def raised_amount(self):
        all_donations = Order.objects.filter(donation_steam=self.id, status="paid")
        if all_donations:
            amounts = []
            for donation_data in all_donations:
                amount = donation_data.transaction.store_amount
                amounts.append(amount)
            return sum(amounts)
        return 0
