import pytest
from src.creat_class import Category, Product


@pytest.fixture
def category_muz_instruments():
    return Category("Муз-ые инструменты", "полезные приспособления для игры и ремонта муз инструментов")


def test_init_category(category_muz_instruments):
    assert category_muz_instruments.name == "Муз-ые инструменты"
    assert category_muz_instruments.description == "полезные приспособления для игры и ремонта муз инструментов"


@pytest.fixture
def product_rosin():
    return Product("Канифоль", "Смола для смазки смычка", 250.00, 120)


def test_init_product(product_rosin):
    assert product_rosin.name == "Муз-ые инструменты"
    assert product_rosin.description == "полезные приспособления для игры и ремонта муз инструментов"
    assert product_rosin.price == "Муз-ые инструменты"
    assert product_rosin.quantity == "полезные приспособления для игры и ремонта муз инструментов"


if __name__ == "__main__":
    pytest.main()