#!/usr/bin/python3

"""Drawing insights from the data"""

from data_ingress import FashionDataIterator


def compute_average_image_count(it: FashionDataIterator) -> float:
    """Compute the number of average images per data point in the data set"""
    total_count = 0
    num_data_points = 0
    for item in it:
        total_count += len(item.raw_image_data)
        num_data_points += 1
    return total_count / num_data_points
