# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, db, DataValidationError
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)

        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.category, product.category)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.price, product.price)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch it back
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)

    def test_update_a_product(self):
        """It should Update a product"""
        product = ProductFactory()
        product.id = None
        self.assertEqual(str(product), f"<Product {product.name} id=[None]>")
        product.create()
        self.assertIsNotNone(product.id)
        product.description = "Product description updated"
        product_id = product.id
        product.update()
        self.assertEqual(product.id, product_id)
        self.assertEqual(product.description, "Product description updated")
        products = Product.all()
        self.assertEqual(len(products), 1)
        found_product = products[0]
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.description, product.description)

    def test_update_a_product_without_id(self):
        """It should not Update a product without id"""
        product = ProductFactory()
        product.id = None
        self.assertEqual(str(product), f"<Product {product.name} id=[None]>")
        product.description = "Product description updated"
        with self.assertRaises(DataValidationError):
            product.update()

    def test_delete_a_product(self):
        """It should Delete a product"""
        product = ProductFactory()
        product.id = None
        self.assertEqual(str(product), f"<Product {product.name} id=[None]>")
        product.create()
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        product.delete()
        products = Product.all()
        self.assertEqual(len(products), 0)

    def test_find_by_name_a_product(self):
        """It sould find a product by name"""

        products = []
        for _ in range(0, 5):
            product = ProductFactory()
            product.id = None
            self.assertEqual(str(product), f"<Product {product.name} id=[None]>")
            product.create()
            self.assertIsNotNone(product.id)
            products.append(product)

        first_product = products[0]
        counter = 0
        for element in products:
            if element.name == first_product.name:
                counter += 1

        products_founded = Product.find_by_name(first_product.name)
        self.assertEqual(products_founded.count(), counter)
        for element in products_founded:
            self.assertEqual(element.name, first_product.name)

    def test_find_by_availability_a_product(self):
        """It sould find a product by availability """

        products = []
        for _ in range(0, 10):
            product = ProductFactory()
            product.id = None
            self.assertEqual(str(product), f"<Product {product.name} id=[None]>")
            product.create()
            self.assertIsNotNone(product.id)
            products.append(product)

        first_product = products[0]
        counter = 0
        for element in products:
            if element.available == first_product.available:
                counter += 1

        products_founded = Product.find_by_availability(first_product.available)
        self.assertEqual(products_founded.count(), counter)
        for element in products_founded:
            self.assertEqual(element.available, first_product.available)

    def test_find_by_category_a_product(self):
        """It sould find a product by category """

        products = []
        for _ in range(0, 10):
            product = ProductFactory()
            product.id = None
            self.assertEqual(str(product), f"<Product {product.name} id=[None]>")
            product.create()
            self.assertIsNotNone(product.id)
            products.append(product)

        first_product = products[0]
        counter = 0
        for element in products:
            if element.category == first_product.category:
                counter += 1

        products_founded = Product.find_by_category(first_product.category)
        self.assertEqual(products_founded.count(), counter)
        for element in products_founded:
            self.assertEqual(element.category, first_product.category)

    def test_find_by_price_a_product(self):
        """It sould find a product by price """

        products = []
        for _ in range(0, 10):
            product = ProductFactory()
            product.id = None
            self.assertEqual(str(product), f"<Product {product.name} id=[None]>")
            product.create()
            self.assertIsNotNone(product.id)
            products.append(product)

        first_product = products[0]
        counter = 0
        for element in products:
            if element.price == first_product.price:
                counter += 1

        products_founded = Product.find_by_price(first_product.price)
        self.assertEqual(products_founded.count(), counter)
        for element in products_founded:
            self.assertEqual(element.price, first_product.price)

    def test_find_by_price_as_str_a_product(self):
        """It sould find a product by price as str """

        products = []
        for _ in range(0, 10):
            product = ProductFactory()
            product.id = None
            self.assertEqual(str(product), f"<Product {product.name} id=[None]>")
            product.create()
            self.assertIsNotNone(product.id)
            products.append(product)

        first_product = products[0]
        first_product.price = '1000.0'
        counter = 0
        for element in products:
            if element.price == first_product.price:
                counter += 1

        products_founded = Product.find_by_price(first_product.price)
        self.assertEqual(products_founded.count(), counter)
        for element in products_founded:
            self.assertEqual(element.price, first_product.price)

    def test_deserialize_a_product_with_bad_availability(self):
        """It should not deserialize a product with bad availability"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)

        product.available = "BAD Value"
        data = product.serialize()
        with self.assertRaises(DataValidationError):
            product.deserialize(data)

    def test_deserialize_a_product_with_invalid_attribut(self):
        """It should not deserialize a product with invalid attribut"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        data = product.serialize()
        data['category'] = "Bad value"
        with self.assertRaises(DataValidationError):
            product.deserialize(data)

    def test_deserialize_a_product_with_bad_data(self):
        """It should not deserialize a product with bad data"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        with self.assertRaises(DataValidationError):
            product.deserialize([])
