from server.serializers import ProductSerializer
from .models import Product
# from fractions import Fraction

class ProductService:
    @staticmethod
    def create_products(prices_list):
        # products = []
        

        for item in prices_list:
            price_text, title_text, link_href = item
            words = title_text.split()
            value='NA'
            power='NA'
            current='NA'
            value1=0
            n1=price_text.split()
            value2=float(n1[1])
            if len(words) > 0:
                for i in words:
                    n = len(i)
                    if n>=2 and  (i[n-2:n].lower()=='uh' or  i[n-2:n].lower()=='mh'):
                        unit = i[n-2:n].lower()  # Convert to lowercase for consistency
                        try:
                            value1 = float(i[0:n-2])
                            if unit == 'uh':
                                value1 /= 1000000
                            elif unit == 'mh':
                                value1 /= 1000
                            else:
                                value1 = float(i[0:n-2])

                            print(f"Value1 assigned: {value1}")  # Debugging print
                        except ValueError:
                            print("Error converting to float:", i[0:n-2])
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
                # 'image_url': image_url,
                'current_rating': current,
                'power_rating': power,
                'value': value,
                'value1':value1,
                'value2':value2,
                'core':'NA',

            }
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                product = serializer.save()  # This returns the created or updated product instance

        # Make additional updates to the product
                product.title = title_text
                product.price = price_text
                product.link = link_href
                # product.image_url = image_url
                product.value=value
                product.power_rating=power
                product.current_rating=current
                product.value1=value1
                product.value2=value2
                product.core='NA'

                product.save()
                print(f"Created product: {serializer.instance}")
            else:
                print(f"Error creating product: {serializer.errors}")
            # products.append(product)
        all_objects = Product.objects.all()
        print(all_objects)
        return


    def create_products2(prices_list):
        # products = []
        

        for item in prices_list:
            title, price, value, current,core,link_href = item
            # words = title_text.split()
            
            power='NA'
            n1=len(value)
            unit = value[n1-2:n1].lower()  # Convert to lowercase for consistency
            
            value1 = float(value[0:n1-3])
            if unit == 'uh':
                value1 /= 1000000
            elif unit == 'mh':
                value1 /= 1000

            n1=price.split()
            plen=len(n1[2])
            value2=float(n1[2][1:plen])
            
            
                
            data = {
                'title': title,
                'price': price,
                'link': link_href,
                # 'image_url': image_url,
                'current_rating': current,
                'power_rating': power,
                'value': value,
                'value1':value1,
                'value2':value2,
                'core':core,

            }
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                product = serializer.save()  # This returns the created or updated product instance

        # Make additional updates to the product
                product.title = title
                product.price = price
                product.link = link_href
                # product.image_url = image_url
                product.value=value
                product.power_rating=power
                product.current_rating=current
                product.value1=value1
                product.value2=value2
                product.core=core

                product.save()
                print(f"Created product: {serializer.instance}")
            else:
                print(f"Error creating product: {serializer.errors}")
            # products.append(product)
        all_objects = Product.objects.all()
        print(all_objects)
        return
