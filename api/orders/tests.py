import json

from django.test import TransactionTestCase
from django.test.client import RequestFactory

from orders import views
from orders import models


class NewOrderViewTestCase(TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.new_orders_url = "/orders/new"

    def assertBadRequest(self, data):
        request = self.factory.post(self.new_orders_url, data=data)
        response = views.new_order(request)

        self.assertEqual(response.status_code, 400)

    def test_create_with_missing_data(self):
        # Only destination
        payload = {
            "destination": "Bishan"
        }

        self.assertBadRequest(payload)

        # Only color
        payload = {
            "color": 5
        }

        self.assertBadRequest(payload)

    def test_invalid_data(self):
        # Invalid destination
        payload = {
            "destination": 5,
            "color": 5,
        }

        self.assertBadRequest(payload)

        # Invalid color
        payload = {
            "destination": "Bishan",
            "color": "asdf",
        }

        self.assertBadRequest(payload)

    def test_create(self):
        payload = {
            "destination": "Bishan",
            "color": 5,
        }

        request = self.factory.post(self.new_orders_url, data=payload)
        response = views.new_order(request)

        self.assertEqual(response.status_code, 200)

        # Check if there is a new record in the DB
        json_response = json.loads(response.content)
        order_id = json_response["data"]["id"]

        query = models.Order.objects.filter(id=order_id)
        self.assertTrue(query.exists())

        # Check the contents of the new record
        db_order = query.first()
        self.assertEqual(db_order.destination, "Bishan")
        self.assertEqual(db_order.color, 5)


class UpdateOrderViewTestCase(TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.update_orders_url = "/orders/update"

        # Create some orders
        self.not_active = models.Order.objects.create(
            destination="Bishan",
            color=5,
            status=models.Order.STATUS_NOT_ACTIVE,
        )

        self.active = models.Order.objects.create(
            destination="Bishan",
            color=5,
            status=models.Order.STATUS_ACTIVE,
        )

        self.completed = models.Order.objects.create(
            destination="Bishan",
            color=5,
            status=models.Order.STATUS_COMPLETED,
        )

        self.orders = [self.not_active, self.active, self.completed]

    def send_request(self, data):
        request = self.factory.post(self.update_orders_url, data=data)
        response = views.update_order(request)

        return response

    def assertBadRequest(self, data):
        response = self.send_request(data)
        self.assertEqual(response.status_code, 400)

    def test_reject_invalid_update_status(self):
        def test_disallow(from_status, to_status):
            order = self.orders[from_status]

            payload = {
                "id": order.pk,
                "new_status": to_status
            }

            self.assertBadRequest(data=payload)

        # Disallow NOT_ACTIVE -> COMPLETED
        test_disallow(from_status=models.Order.STATUS_NOT_ACTIVE,
                      to_status=models.Order.STATUS_COMPLETED)

        # Disallow ACTIVE -> NOT_ACTIVE
        test_disallow(from_status=models.Order.STATUS_ACTIVE,
                      to_status=models.Order.STATUS_NOT_ACTIVE)

        # Disallow COMPLETED -> NOT_ACTIVE
        test_disallow(from_status=models.Order.STATUS_COMPLETED,
                      to_status=models.Order.STATUS_NOT_ACTIVE)

        # Disallow COMPLETED -> ACTIVE
        test_disallow(from_status=models.Order.STATUS_COMPLETED,
                      to_status=models.Order.STATUS_ACTIVE)

    def test_normal_update_status(self):
        # NOT_ACTIVE -> ACTIVE
        payload = {
            "id": self.not_active.pk,
            "new_status": models.Order.STATUS_ACTIVE
        }
        response = self.send_request(payload)
        self.assertEqual(response.status_code, 200)

        # Check that the order has been updated
        self.assertEqual(self.not_active.status, models.Order.STATUS_ACTIVE)

        # ACTIVE -> COMPLETED
        payload["new_status"] = models.Order.STATUS_COMPLETED
        response = self.send_request(payload)
        self.assertEqual(response.status_code, 200)

        # Check that the order has been updated
        self.assertEqual(self.not_active.status, models.Order.COMPLETED)
