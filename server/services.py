from server.serializers import ProductSerializer
from .models import Product

class ProductService:
    @staticmethod
    def create_products(prices_list):
        # products = []
        for item in prices_list:
            price_text, title_text, link_href, image_url = item
            data = {
            'title': title_text,
            'price': price_text,
            'link': link_href,
            'image_url': image_url
        }
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                product = serializer.save()  # This returns the created or updated product instance

        # Make additional updates to the product
                product.title=title_text
                product.price = price_text
                product.link = link_href
                product.image_url = image_url
                product.save()
                print(f"Created product: {serializer.instance}")
            else:
                print(f"Error creating product: {serializer.errors}")
            # products.append(product)
        all_objects = Product.objects.all()
        print(all_objects)
        return 