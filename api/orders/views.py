from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from orders.models import Order
import base.views as base_views


@csrf_exempt
@require_POST
def new_order(request):
    # Check if there is a destination and color
    if ("destination" not in request.POST) or ("color" not in request.POST):
        return base_views.create_json_response(
            success=False,
            message="Missing destination or color",
            status=400,
        )

    destination = request.POST["destination"]
    color = request.POST["color"]

    if not color.isdigit():
        return base_views.create_json_response(
            success=False,
            message="The color is not a non-negative integer",
            status=400,
        )

    order = Order.objects.create(
        destination=destination, color=color,
        status=Order.STATUS_NOT_ACTIVE)

    return base_views.create_json_response(
        data={"id": order.pk}
    )
