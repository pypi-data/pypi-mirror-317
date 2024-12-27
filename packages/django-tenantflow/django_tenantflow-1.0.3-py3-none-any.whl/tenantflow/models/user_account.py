from django.db import models

class AbstractUserAccount(models.Model):
    """
    Abstract model to represent the relationship between a user and an account in the project.
    """
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name="user_accounts",
        help_text="User associated with the account"
    )
    account = models.ForeignKey(
        'tenantflow.AbstractAccount',
        on_delete=models.CASCADE,
        related_name="user_accounts",
        help_text="Account associated with the user"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation date")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update date")

    def __str__(self):
        return f"{self.user.username} - {self.account.name}"

    class Meta:
        abstract = True
        unique_together = ('user', 'account')
        verbose_name = "User-Account Relationship"
        verbose_name_plural = "User-Account Relationships"
