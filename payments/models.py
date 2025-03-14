from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser


class PaymentHistory(models.Model):
    class PaymentMethod(models.TextChoices):
        KHALTI = "khalti", _("Khalti")
        ESEWA = "esewa", _("Esewa")
        BANK = "bank", _("Bank Transfer")
        CARD = "card", _("Credit Card")
        CASH = "cash", _("Cash Payment")

    transaction_id = models.CharField(
        _("transaction ID"),
        max_length=500,
        unique=True,
        db_index=True,
        help_text=_("Unique identifier for the payment transaction"),
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="payment_histories",
        verbose_name=_("User"),
    )
    total_payment = models.DecimalField(
        _("total amount"),
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Total amount paid in the transaction"),
    )
    payment_via = models.CharField(
        _("payment method"),
        max_length=20,
        choices=PaymentMethod.choices,
        help_text=_("Method used for the payment"),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Timestamp when the payment was recorded"),
    )
    is_successful = models.BooleanField(
        _("successful"),
        default=True,
        help_text=_("Indicates if the payment was successful"),
    )
    metadata = models.JSONField(
        _("metadata"),
        default=dict,
        blank=True,
        help_text=_("Additional payment details in JSON format"),
    )

    class Meta:
        verbose_name = _("Payment History")
        verbose_name_plural = _("Payment Histories")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["transaction_id"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.user.email} ({self.total_payment})"
