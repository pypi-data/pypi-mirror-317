from typing import List


def binary_search(sorted_list: List[int], number: int) -> int:
    """
    Search for a given number within the sorted list using a binary
    search. The complexity of this search is O(log n)

    :param sorted_list: The sorted list of integers to be searched.
    :param number: The number to search for within the list.
    :return: The index of the number within the list, or -1 if it is not found.
    """

    lower_bound = 0
    upper_bound = len(sorted_list)

    if not sorted_list or number < sorted_list[0] or number > sorted_list[-1]:
        # Out of range of contents in collection
        return -1

    while lower_bound != upper_bound:
        # index is half way between upper and lower bounds,
        # rounded down.
        index = (upper_bound + lower_bound) // 2

        if number == sorted_list[index]:
            # Found the number!
            return index
        elif number > sorted_list[index]:
            # The number is bigger than the one at the centre.
            # Move the lower bound to the index, i.e. halve the
            # search space.
            if lower_bound == index:
                # If the lower bound is already at the index,
                # upper and lower are only one apart and
                # the number is not here.
                break
            lower_bound = index
        else:
            # The number is smaller than the one at the centre.
            # Move the upper bound to the index, i.e. halve the
            # search space.
            if upper_bound == index:
                # If the upper bound is already at the index,
                # upper and lower are only one apart and
                # the number is not here.
                break
            upper_bound = index

    # number was not found within the collection
    return -1


def binary_search2(sorted_list: List[int], number: int) -> int:
    lower_bound = 0
    upper_bound = len(sorted_list)

    if not sorted_list or number < sorted_list[0] or number > sorted_list[-1]:
        # Out of range of contents in collection
        return -1

    while lower_bound != upper_bound:
        index = (upper_bound + lower_bound) // 2
        current_item = sorted_list[index]

        if number == current_item:
            return index
        elif number > current_item:
            if lower_bound == index:
                break
            lower_bound = index
        elif number < current_item:
            if upper_bound == index:
                break
            upper_bound = index

    return -1
