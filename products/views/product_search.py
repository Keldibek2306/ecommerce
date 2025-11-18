from django.views import View
from django.http import JsonResponse, HttpRequest
from django.db.models import Q
from ..models import Product


class ProductSearchView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.all()
        search_query = request.GET.get("search")
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        category_id = request.GET.get("category")
        if category_id:
            products = products.filter(category_id=category_id)

        is_active = request.GET.get("is_active")
        if is_active is not None:
            if is_active.lower() == "true":
                products = products.filter(is_active=True)
            elif is_active.lower() == "false":
                products = products.filter(is_active=False)

        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        in_stock = request.GET.get("in_stock")
        if in_stock and in_stock.lower() == "true":
            products = products.filter(stock__gt=0)

        order_by = request.GET.get("order_by", "-created_at")
        valid_orders = [
            "name", "-name", 
            "price", "-price", 
            "created_at", "-created_at",
            "stock", "-stock"
        ]

        if order_by not in valid_orders:
            return JsonResponse(
                {"error": "Invalid order_by value."},
                status=400
            )

        products = products.order_by(order_by)

        product_list = []
        for product in products:
            product_list.append({
                "id": product.pk,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock": product.stock,
                "is_active": product.is_active,
                "category": product.category.name if product.category else None,
                "category_id": product.category_id,
                "images": [
                    {
                        "id": img.pk,
                        "url": f"{request.build_absolute_uri()}{img.image.url}",
                        "alt_text": img.alt_text
                    }
                    for img in product.images.all()
                ],
                "created_at": product.created_at.isoformat(),
                "updated_at": product.updated_at.isoformat()
            })

        return JsonResponse(
            {
                "products": product_list,
                "count": len(product_list)
            },
            status=200
        )
