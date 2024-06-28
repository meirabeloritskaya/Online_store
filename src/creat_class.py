class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    total_categories = 0
    categories_list = []
    unique_products = set()

    def __init__(self, name: str, description: str, products=None):
        self.name = name
        self.description = description
        self.products = products if products is not None else []
        Category.total_categories += 1
        Category.categories_list.append(self)
        for product in self.products:
            Category.unique_products.add(product.name)

    def add_product(self, product: Product):
        self.products.append(product)

    def get_unique_products(self):
        unique_products = {}
        for product in self.products:
            if product.name not in unique_products:
                unique_products[product.name] = {
                    "price": product.price,
                    "quantity": product.quantity,
                }
            else:
                unique_products[product.name]["quantity"] += product.quantity
        return unique_products


product_1 = Product(
    name="Тюнер",
    description="Устройство для настройки инструментов",
    price=700.00,
    quantity=55,
)
product_2 = Product(name="Канифоль", description="Смола для смазки смычка", price=250.00, quantity=120)
product_3 = Product(
    name="Скрипка",
    description="сидячий/стоячий инструмент",
    price=40000.00,
    quantity=14,
)
product_4 = Product(name="Виолончель", description="сидячий инструмент", price=55000.00, quantity=13)

category_1 = Category(
    name="Муз-ые аксессуары",
    description="полезные приспособления для игры и ремонта муз инструментов",
    products=[product_1, product_2],
)
category_2 = Category(
    name="Муз-ые инструменты",
    description="инструменты для игры в оркестре",
    products=[product_3, product_4],
)


def print_categories():
    print("Список категорий:")
    for category in Category.categories_list:
        print(f"{category.name}: {category.description}")


def print_unique_products():
    print("\nСписок уникальных продуктов:")
    for category in Category.categories_list:
        unique_products = category.get_unique_products()
        for product_name, info in unique_products.items():
            print(f"{product_name}: {info['price']} руб, {info['quantity']} шт")


print_categories()
print_unique_products()


print("\nОбщее количество категорий:", Category.total_categories)
print("Общее количество уникальных продуктов:", len(Category.unique_products))
