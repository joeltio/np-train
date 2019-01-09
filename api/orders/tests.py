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
