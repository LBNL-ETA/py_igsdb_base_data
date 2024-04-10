import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
from unittest import TestCase

import pytest
from dataclasses_json import dataclass_json

from py_igsdb_base_data.product import BaseProduct, PhysicalProperties, ProductType, ProductSubtype, TokenType, \
    BlindGeometry


@dataclass_json
@dataclass
class TestList:
    some_list: Optional[List[str]] = None


class TestDataclass(TestCase):

    def test_dataclass_library(self):
        d = '{"sports": ["soccer", "basketball"]}'
        TestList.from_json(d)

    def test_create_empty_product(self):
        p = BaseProduct()
        self.assertIsNone(p.type)

    def test_create_product(self):
        p = BaseProduct(type=ProductType.GLAZING.name,
                        subtype=ProductSubtype.MONOLITHIC.name,
                        token='valid-monolithic-1',
                        token_type=TokenType.PUBLISHED.name,
                        data_file_name='valid_monolithic_1.abc')
        self.assertEquals(p.type, ProductType.GLAZING.name)
        self.assertEquals(p.subtype, ProductSubtype.MONOLITHIC.name)
        self.assertEquals(p.token_type, TokenType.PUBLISHED.name)

    def test_create_product_from_dict(self):
        example_product_json = Path('tests/data/valid_monolithic_1.json')
        if not example_product_json.exists():
            raise Exception(f"Cannot run test. Missing sample json file: {example_product_json}")

        with open(example_product_json, 'r') as f:
            json_content = f.read()
            original_dict = json.loads(json_content)

        # Load json string into our dataclass
        product: BaseProduct = BaseProduct.from_dict(original_dict)

        # Get original json properties to see if
        # they were preserved...
        expected_subtype = original_dict['subtype']

        # Check dataclass against original properties.
        self.assertEquals(product.subtype, expected_subtype)

        physical_properties = product.physical_properties
        # Makes sure nested data was transformed to dataclasses by dataclasses-json
        self.assertEquals(type(physical_properties), PhysicalProperties)

    def test_create_product_from_json_file(self):
        example_product_json = Path('tests/data/valid_monolithic_1.json')
        if not example_product_json.exists():
            raise Exception(f"Cannot run test. Missing sample json file: {example_product_json}")

        with open(example_product_json, 'r') as f:
            json_content = f.read()

        # Load json string into our dataclass
        product: BaseProduct = BaseProduct.from_json(json_content)

        # Get original json properties to see if
        # they were preserved...
        original_dict = json.loads(json_content)
        expected_subtype = original_dict['subtype']

        # Check dataclass against original properties.
        self.assertEquals(product.subtype, expected_subtype)

        physical_properties = product.physical_properties
        # Makes sure nested data was transformed to dataclasses by dataclasses-json
        self.assertEquals(type(physical_properties), PhysicalProperties)

    def test_cannot_set_wrong_product_type(self):
        # Test init
        with pytest.raises(ValueError):
            BaseProduct(type='INVALID_TYPE')
        # Test manual set
        with pytest.raises(ValueError):
            product = BaseProduct()
            product.type = "INVALID"

    def test_cannot_set_wrong_product_subtype(self):
        # Test init
        with pytest.raises(ValueError):
            BaseProduct(subtype='INVALID_TYPE')

        # Test manual set
        with pytest.raises(ValueError):
            product = BaseProduct()
            product.subtype = "INVALID"

    def test_cannot_set_wrong_product_token_type(self):
        # Test init
        with pytest.raises(ValueError):
            BaseProduct(token_type='INVALID_TYPE')

        # Test manual set
        with pytest.raises(ValueError):
            product = BaseProduct()
            product.token_type = "INVALID"


class TestBlindGeometry(TestCase):

    def test_set_curvature_from_rise_standard(self):
        t = BlindGeometry()
        t.slat_width = "10"
        t.rise = "2.5"
        t.set_curvature_from_rise()

        slat_curvature = float(t.slat_curvature)
        self.assertAlmostEqual(6.25, slat_curvature)

    def test_set_curvature_from_rise_at_0(self):
        t = BlindGeometry()
        t.slat_width = "10"
        t.rise = "0"
        t.set_curvature_from_rise()

        slat_curvature = float(t.slat_curvature)
        self.assertAlmostEqual(0.0, slat_curvature)

    def test_set_curvature_from_rise_at_negative(self):
        t = BlindGeometry()
        t.slat_width = "10"
        t.rise = "-10"
        t.set_curvature_from_rise()

        slat_curvature = float(t.slat_curvature)
        self.assertAlmostEqual(0.0, slat_curvature)


    def test_rise_from_curvature_at_0(self):
        t = BlindGeometry()
        t.slat_curvature = "0"  # mm
        t.slat_width = "10"  # mm
        t.set_rise_from_curvature()

        rise = float(t.rise)
        self.assertAlmostEqual(0.0, rise)

    def test_rise_from_curvature_at_negative(self):
        t = BlindGeometry()
        t.slat_curvature = "-10"  # mm
        t.slat_width = "10"  # mm
        t.set_rise_from_curvature()

        rise = float(t.rise)
        self.assertAlmostEqual(0.0, rise)

    def test_rise_from_curvature_standard(self):
        t = BlindGeometry()
        t.slat_curvature = "5"  # mm
        t.slat_width = "10"  # mm
        t.set_rise_from_curvature()

        rise = float(t.rise)
        self.assertAlmostEqual(5.0, rise)

