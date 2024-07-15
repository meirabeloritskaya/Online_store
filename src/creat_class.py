import json
import os
from abc import ABC, abstractmethod


class ProductAbstract(ABC):
    @abstractmethod
    def __str__(self):
        pass


class MixinLog:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_creation()

    def log_creation(self):
        class_name = self.__class__.__name__
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        print("-------------------------------")
        print(f"Создан объект: {class_name} с атрибутами: {attributes}")


class Product(ProductAbstract, MixinLog):
    """Представляет продукт с названием, описанием, ценой и количеством."""

    def __init__(self, name: str, description: str, price: float, quantity: int, color: str = ""):
        """Инициализирует продукт с заданными параметрами."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.color = color
        super().__init__()

    def __str__(self):
        """Возвращает строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Складывает цены продуктов, умноженные на их количество."""
        if isinstance(other, type(self)):
            return (self.price * self.quantity) + (other.price * other.quantity)
        else:
            return "Можно складывать товары только из одинаковых классов продуктов"

    @classmethod
    def create_product(cls, name, description, price, quantity, color=""):
        """Создает новый экземпляр продукта через метод класса."""
        return cls(name, description, price, quantity, color)

    @property
    def price(self):
        """Получает цену продукта."""
        return self._price

    @price.setter
    def price(self, price):
        """Устанавливает цену продукта, если она положительная."""
        if price > 0:
            self._price = price
        else:
            print("цена введена некорректная")


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        color: str,
        performance: float,
        model: str,
        memory: int,
    ):
        super().__init__(name, description, price, quantity, color)
        self.performance = performance
        self.model = model
        self.memory = memory

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт., Производительность: {self.performance}, Модель: {self.model}, Память: {self.memory} ГБ"


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        color: str,
        country: str,
        germination_period: int,
    ):
        super().__init__(name, description, price, quantity, color)
        self.country = country
        self.germination_period = germination_period

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт., Страна: {self.country}, Срок прорастания: {self.germination_period} дней"


class Category:
    """Представляет категорию продуктов с их уникальными наименованиями."""

    total_categories = 0
    categories_list = []
    unique_products = set()

    def __init__(self, name: str, description: str, products=None):
        """Инициализирует категорию с заданным названием, описанием и продуктами."""
        self.name = name
        self.description = description
        self.__products = products if products is not None else []
        Category.total_categories += 1
        Category.categories_list.append(self)
        for product in self.__products:
            Category.unique_products.add(product.name)

    def add_product(self, value: object):
        """Добавляет продукт в категорию."""
        if isinstance(value, Product):
            self.__products.append(value)
            Category.unique_products.add(value.name)
        else:
            raise ValueError("Можно добавлять только объекты классов Product и его наследников")

    @property
    def products(self):
        """Возвращает список строковых представлений продуктов в категории."""
        return [str(product) for product in self.__products]

    def get_unique_products(self):
        """Возвращает уникальные продукты в категории."""
        unique_products = {}
        for product in self.__products:
            if product.name not in unique_products:
                unique_products[product.name] = product
            else:
                unique_products[product.name]["quantity"] += product.quantity
        return unique_products.values()

    def __len__(self):
        """Возвращает общее количество продуктов в категории."""
        return sum(product.quantity for product in self.__products)

    def __str__(self):
        """Возвращает строковое представление категории."""
        return f"{self.name}, количество продуктов: {len(self)} шт."


def load_data_from_json(file_path):
    """Загружает данные о продуктах из JSON-файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for category_data in data:
            products = []
            for product_data in category_data["products"]:
                if category_data["name"] == "Smartphone":
                    products.append(
                        Smartphone(
                            name=product_data["name"],
                            description=product_data["description"],
                            price=product_data["price"],
                            quantity=product_data["quantity"],
                            color=product_data.get("color", ""),
                            performance=product_data.get("performance", 0.0),
                            model=product_data.get("model", ""),
                            memory=product_data.get("memory", 0),
                        )
                    )
                elif category_data["name"] == "LawnGrass":
                    products.append(
                        LawnGrass(
                            name=product_data["name"],
                            description=product_data["description"],
                            price=product_data["price"],
                            quantity=product_data["quantity"],
                            color=product_data.get("color", ""),
                            country=product_data["country"],
                            germination_period=product_data["germination_period"],
                        )
                    )
                else:
                    products.append(
                        Product.create_product(
                            name=product_data["name"],
                            description=product_data["description"],
                            price=product_data["price"],
                            quantity=product_data["quantity"],
                        )
                    )
            Category(name=category_data["name"], description=category_data["description"], products=products)
            # products = [Product.create_product(**product_data) for product_data in category_data["products"]]
            # Category(name=category_data["name"], description=category_data["description"], products=products)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "products.json")

    load_data_from_json(file_path)

    def print_categories_description():
        """Печатает описание всех категорий."""
        print("-----------------")
        print("Список категорий:")
        print("-----------------")
        for category in Category.categories_list:
            print(f"{category.name}: {category.description}")

    def print_categories():
        """Печатает все категории."""
        print("-------------------------------")
        for category in Category.categories_list:
            print(category)

    def print_unique_products():
        """Печатает список уникальных продуктов."""
        print("-------------------------------")
        print("Список уникальных продуктов:")
        print("-------------------------------")
        unique_products = {}
        for category in Category.categories_list:
            for product in category.get_unique_products():
                if product.name not in unique_products:
                    unique_products[product.name] = product
                else:
                    unique_products[product.name].quantity += product.quantity
        for product in unique_products.values():
            print(product)

    def total_price_by_category():
        """Выводит общую стоимость продуктов по категориям."""
        print("-------------------------------")
        print("Результаты сложения цен продуктов по категориям:\n")
        for category in Category.categories_list:
            total_sum = 0.0
            print(f"Категория: {category.name}")
            for product in category.get_unique_products():
                total_sum += product.price * product.quantity
            print(f"Общая сумма для категории {category.name}: {total_sum} руб.")
            print()

    print_categories_description()
    print_categories()
    print_unique_products()
    total_price_by_category()

    print("-------------------------------")
    print("\nОбщее количество категорий:", Category.total_categories)
    print("Общее количество уникальных продуктов:", len(Category.unique_products))
