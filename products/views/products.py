import json

from django.views import View
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404

from ..models import Product, ProductImage, Category


class ProductListView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        products = []

        for p in Product.objects.all().prefetch_related("images", "category"):
            products.append({
                "id": p.pk,
                "name": p.name,
                "description": p.description,
                "price": str(p.price),
                "stock": p.stock,
                "is_active": p.is_active,
                "category": p.category.name if p.category else None,
                "category_id": p.category_id,
                "images": [
                    {
                        "id": img.pk,
                        "url": img.image.url,
                        "alt_text": img.alt_text
                    }
                    for img in p.images.all()
                ],
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat(),
            })

        return JsonResponse({"products": products})


    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body)

        name = data.get("name")
        if not name:
            return JsonResponse({"name": "Required."}, status=400)
        if len(name) > 256:
            return JsonResponse({"name": "Max 256 characters."}, status=400)

        if data.get("price") is None:
            return JsonResponse({"price": "Required."}, status=400)

        stock = data.get("stock")
        if stock is None:
            return JsonResponse({"stock": "Required."}, status=400)
        if stock < 0:
            return JsonResponse({"stock": "Must be positive."}, status=400)

        category = None
        category_id = data.get("category_id")
        if category_id:
            category = get_object_or_404(Category, pk=category_id)

        product = Product.objects.create(
            name=data["name"],
            description=data.get("description"),
            price=data["price"],
            stock=data["stock"],
            category=category,
            is_active=data.get("is_active", True)
        )

        return JsonResponse(
            {
                "id": product.pk,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock": product.stock,
                "is_active": product.is_active,
                "category": product.category.name if product.category else None,
                "category_id": product.category_id,
                "created_at": product.created_at.isoformat(),
                "updated_at": product.updated_at.isoformat(),
            },
            status=201
        )


class ProductDetailView(View):

    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        product = get_object_or_404(Product, pk=pk)

        return JsonResponse({
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
                    "url": img.image.url,
                    "alt_text": img.alt_text
                }
                for img in product.images.all()
            ],
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat(),
        })


    def put(self, request: HttpRequest, pk: int) -> JsonResponse:
        product = get_object_or_404(Product, pk=pk)

        data = json.loads(request.body)

        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)

        product.save()

        return JsonResponse(
            {
                "id": product.pk,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock": product.stock,
                "is_active": product.is_active,
                "category": product.category.name if product.category else None,
                "category_id": product.category_id,
                "created_at": product.created_at.isoformat(),
                "updated_at": product.updated_at.isoformat()
            },
            status=204
        )
    def delete(self, request: HttpRequest, pk:int) -> JsonResponse:
        product = get_object_or_404(Product, pk=pk)

        product.delete()

        return JsonResponse({'product': 'Deleted.'}, status=204)