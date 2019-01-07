from django.db import models


class Order(models.Model):
    # A train location, e.g. Bishan
    destination = models.TextField()
    # PositiveSmallIntegerField accepts [0, 32767]
    color = models.PositiveSmallIntegerField()
    # SmallIntegerField accepts [-32768, 32767]
    status = models.SmallIntegerField()

    STATUS_NOT_ACTIVE = 0
    STATUS_ACTIVE = 1
    STATUS_COMPLETED = 2

    def as_json(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "color": self.color,
            "status": self.status,
        }
