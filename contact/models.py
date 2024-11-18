from django.db import models


class ContactMessage(models.Model):
    """
    Model to store messages submitted via the contact form.
    """

    # Name of the person submitting the message
    name = models.CharField(
        max_length=100
    )

    # Email address of the person submitting the message
    email = models.EmailField()

    # Subject of the message
    subject = models.CharField(
        max_length=200
    )

    # The message content
    message = models.TextField()

    # Timestamp for when the message was created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        """
        String representation of the ContactMessage model.
        """
        return f"Message from {self.name} - {self.subject}"
