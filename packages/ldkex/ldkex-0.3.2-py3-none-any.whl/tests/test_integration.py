import os

import pytest

from ldkex import LdkExtractor


@pytest.fixture
def setup_extractor():
    extractor = LdkExtractor()
    return extractor


@pytest.mark.parametrize("file_path, "
                         "expected_geometries, "
                         "expected_geometries_no_duplicates, "
                         "expected_points, "
                         "expected_lines, "
                         "expected_polygons, "
                         "expected_points_no_duplicates, "
                         "expected_lines_no_duplicates, "
                         "expected_polygons_no_duplicates, "
                         "expected_geometries_with_observation_datetime", [
                             # ('test_data-01.ldk', 242830, 17762, 234713, 6183, 1934, 15620, 1798, 344, 0),
                             # ('test_data-02.ldk', 30932, 27215, 28258, 2368, 306, 24715, 2194, 306, 0),
                             ('test_data-03.trk', 1, 1, 0, 1, 0, 0, 1, 0, 1),
                             ('test_data-04.ldk', 205, 205, 205, 0, 0, 205, 0, 0, 0),
                             ('test_data-05.ldk', 7916, 7530, 6857, 884, 175, 6501, 856, 173, 2999),
                             ('test_data-06.ldk', 6702, 2211, 6332, 370, 0, 1897, 314, 0, 1895),
                             # ('test_data-07.ldk', 21404, 21404, 21404, 0, 0, 21404, 0, 0, 0),
                             ('ldk_file_with_information_field.ldk', 1006, 1002, 439, 65, 502, 439, 65, 498, 0),
                         ])
def test_extract_file(setup_extractor, file_path, expected_geometries, expected_geometries_no_duplicates,
                      expected_points, expected_lines, expected_polygons, expected_points_no_duplicates,
                      expected_lines_no_duplicates, expected_polygons_no_duplicates,
                      expected_geometries_with_observation_datetime):

    test_dir = os.path.dirname(__file__)
    full_file_path = os.path.join(test_dir, 'data', file_path)

    extractor = setup_extractor
    with open(full_file_path, 'rb') as file:
        extractor.extract(file)

    geometries = extractor.geometries

    print(len(geometries), len(geometries.get_points()), len(geometries.get_lines()), len(geometries.get_polygons())) # To make updating tests easier

    assert len(geometries) == expected_geometries
    assert len(geometries.get_points()) == expected_points
    assert len(geometries.get_lines()) == expected_lines
    assert len(geometries.get_polygons()) == expected_polygons

    geometries.remove_duplicates(fields=['name', 'coordinates', 'outline_color'])
    
    print(len(geometries), len(geometries.get_points()), len(geometries.get_lines()), len(geometries.get_polygons()), len([geometry for geometry in geometries if geometry.observation_datetime]))

    assert len(geometries) == expected_geometries_no_duplicates
    assert len(geometries.get_points()) == expected_points_no_duplicates
    assert len(geometries.get_lines()) == expected_lines_no_duplicates
    assert len(geometries.get_polygons()) == expected_polygons_no_duplicates
    assert len([geometry for geometry in geometries if geometry.observation_datetime]) == expected_geometries_with_observation_datetime