from collections import defaultdict


def are_arrays_equal(arr1, arr2):
    n = len(arr1)
    m = len(arr2)

    if n != m:
        return False

    # Create a defaultdict count to
    # store counts
    count = defaultdict(int)

    # Store the elements of arr1
    # and their counts in the dictionary
    for i in arr1:
        count[i] += 1

    # Traverse through arr2 and compare
    # the elements and its count with
    # the elements of arr1
    for i in arr2:

        # Return false if the elemnent
        # is not in arr2 or if any element
        # appears more no. of times than in arr1
        if count[i] == 0:
            return False

        # If element is found, decrement
        # its value in the dictionary
        else:
            count[i] -= 1

    # Return true if both arr1 and
    # arr2 are equal
    return True


def get_key_from_value_in_dict(value, dict):
    key_list = list(dict.keys())
    val_list = list(dict.values())

    position = val_list.index(value)
    return key_list[position]
