from server.serializers import ProductSerializer
from .models import Product
# from fractions import Fraction

class ProductService:
    @staticmethod
    def create_products(prices_list):
        # products = []
        

        for item in prices_list:
            price_text, title_text, link_href, image_url = item
            words = title_text.split()
            value='NA'
            power='NA'
            current='NA'
            if len(words) > 0:
                for i in words:
                    n = len(i)
                    if n>=2 and (i[n-2:n] == 'uH' or i[n-2:n] == 'mH'):
                        # value = float(i[0:n-2])
                
                        value = i
                    if i[n-1] == 'W':
                        # fraction_str = i[0:n-1].strip()
                        # power = float(Fraction(fraction_str))
                        power=i
                    if i[n-1] == 'A':
                        current=i
            
                
            data = {
                'title': title_text,
                'price': price_text,
                'link': link_href,
                'image_url': image_url,
                'current_rating': current,
                'power_rating': power,
                'value': value,

            }
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                product = serializer.save()  # This returns the created or updated product instance

        # Make additional updates to the product
                product.title = title_text
                product.price = price_text
                product.link = link_href
                product.image_url = image_url
                product.value=value
                product.power_rating=power
                product.current_rating=current

                product.save()
                print(f"Created product: {serializer.instance}")
            else:
                print(f"Error creating product: {serializer.errors}")
            # products.append(product)
        all_objects = Product.objects.all()
        print(all_objects)
        return
