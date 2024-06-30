import json
import os


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @classmethod
    def create_product(cls, name, description, price, quantity):
        return cls(name, description, price, quantity)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if price > 0:
            self._price = price
        else:
            print("цена введена некорректная")


class Category:
    total_categories = 0
    categories_list = []
    unique_products = set()

    def __init__(self, name: str, description: str, products=None):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []
        Category.total_categories += 1
        Category.categories_list.append(self)
        for product in self.__products:
            Category.unique_products.add(product.name)

    def add_product(self, product: Product):
        self.__products.append(product)
        Category.unique_products.add(product.name)

    @property
    def products(self):
        return [f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products]

    def get_unique_products(self):
        unique_products = {}
        for product in self.__products:
            if product.name not in unique_products:
                unique_products[product.name] = {
                    "price": product.price,
                    "quantity": product.quantity,
                }
            else:
                unique_products[product.name]["quantity"] += product.quantity
        return unique_products


def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for category_data in data:
            products = [Product.create_product(**product_data) for product_data in category_data["products"]]
            Category(name=category_data["name"], description=category_data["description"], products=products)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "products.json")

    load_data_from_json(file_path)

    def print_categories():
        print("Список категорий:")
        for category in Category.categories_list:
            print(f"{category.name}: {category.description}")

    def print_unique_products():
        print("\nСписок уникальных продуктов:")
        for category in Category.categories_list:
            unique_products = category.get_unique_products()
            for product_name, info in unique_products.items():
                print(f"{product_name}: {info['price']} руб, Остаток: {info['quantity']} шт")

    print_categories()
    print_unique_products()

    print("\nОбщее количество категорий:", Category.total_categories)
    print("Общее количество уникальных продуктов:", len(Category.unique_products))
