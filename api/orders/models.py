from django.db import models


class Order(models.Model):
    # A train location, e.g. Bishan
    destination = models.TextField()
    # PositiveSmallIntegerField accepts [0, 32767]
    color = models.PositiveSmallIntegerField()
    # SmallIntegerField accepts [-32768, 32767]
    status = models.SmallIntegerField()

    # The status values should be the same order as the flow and starting
    # from 0
    STATUS_NOT_ACTIVE = 0
    STATUS_ACTIVE = 1
    STATUS_COMPLETED = 2
    STATUS_FLOW = [STATUS_NOT_ACTIVE, STATUS_ACTIVE, STATUS_COMPLETED]

    def as_json(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "color": self.color,
            "status": self.status,
        }
