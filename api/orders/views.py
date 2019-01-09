from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from orders.models import Order
import base.helpers as base_helpers


@require_GET
def uncompleted_order(request):
    # Get the latest uncompleted order
    order = Order.objects.filter(
        status=Order.STATUS_NOT_COMPLETED).order_by("-id").first()

    if order is not None:
        return base_helpers.create_json_response(
            data=order.as_json()
        )
    else:
        return base_helpers.create_json_response(
            message="There are no uncompleted orders",
            empty_data=True,
        )


@csrf_exempt
@require_POST
def new_order(request):
    # Check if there is a destination and color
    if not base_helpers.has_keys({"destination", "color"}, request.POST):
        return base_helpers.create_json_response(
            success=False,
            message="Missing destination or color",
            status=400,
        )

    destination = request.POST["destination"]
    color = request.POST["color"]

    if not base_helpers.validate_positive_int(color, include_zero=True):
        return base_helpers.create_json_response(
            success=False,
            message="The color is not a non-negative integer",
            status=400,
        )

    order = Order.objects.create(
        destination=destination, color=color,
        status=Order.STATUS_NOT_ACTIVE)

    return base_helpers.create_json_response(
        data={"id": order.pk}
    )


@csrf_exempt
@require_POST
def update_order(request):
    if not base_helpers.has_keys({"id", "new_status"}):
        return base_helpers.create_json_response(
            success=False,
            message="Missing id or new_status",
            status=400,
        )

    if not base_helpers.validate_positive_int(
            request.POST["id"], include_zero=True):
        return base_helpers.create_json_response(
            success=False,
            message="Bad id",
            status=400,
        )
    elif not request.POST["new_status"] in Order.STATUS_FLOW:
        return base_helpers.create_json_response(
            success=False,
            message="Bad new_status",
            status=400,
        )

    new_status = request.POST["new_status"]

    # Find the order
    order = Order.objects.filter(pk=int(request.POST["id"]))

    if not order.exists():
        return base_helpers.create_json_response(
            success=False,
            message="There is no order with that id",
            status=400,
        )

    # Only allow changes in this order:
    # NOT_ACTIVE > ACTIVE > COMPLETED
    if order.status == Order.STATUS_FLOW[-1]:
        return base_helpers.create_json_response(
            success=False,
            message="The order is already complete",
            status=400,
        )
    elif new_status - order.status != 1:
        return base_helpers.create_json_response(
            success=False,
            message="Cannot update status beyond 1 step",
            status=400,
        )

    order.status = new_status
    order.save()
