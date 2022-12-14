import numpy as np
from numpy.random import shuffle
from numba import njit


@njit(nogil=True)
def create_prisoner_box_dict(num: int) -> dict[int, int]:
    """
    Creates a dictionary of prisoner_num : box_num.
    :param num: number of prisoner boxes to create
    :return: dictionary of prisoner boxes
    """
    boxes_dict = {num: num for num in range(1, num + 1)}

    return boxes_dict


@njit(nogil=True)
def shuffle_dictionary_keys(dictionary: dict) -> dict:
    """
    Shuffles the main keys and values of a dictionary.
    :param dictionary: The dictionary to shuffle.
    :return: The shuffled dictionary.
    """
    dictionary_keylist = np.array(list(dictionary.keys()))
    dictionary_valuelist = np.array(list(dictionary.values()))

    shuffle(dictionary_keylist)
    shuffle(dictionary_valuelist)

    dictionary = {
        key: value for key, value in zip(dictionary_keylist, dictionary_valuelist)
    }

    return dictionary


@njit(nogil=True)
def calculate_prisoner_box_loops(box_dict: dict[int, int]) -> dict[int, int]:
    """
    This function takes a dictionary of prisoner boxes and calculates the
    number of loops that each prisoner will take to find their number, and
    it returns True if the loop number is less or equal to loop_pivot.
    :param box_dict: dictionary of prisoner:boxes
    generated by create_prisoner_box_dict()
    :return: dictionary of loops for each prisoner.
    """
    shuffled_boxes = shuffle_dictionary_keys(box_dict)
    prisoner_loops = dict()

    for prisoner_num in shuffled_boxes.keys():
        prisoner_loop = 0
        prisoner_box = shuffled_boxes[prisoner_num]
        prisoner_loop += 1

        while True:
            prisoner_box = shuffled_boxes[prisoner_box]
            prisoner_loop += 1

            if prisoner_box == prisoner_num:
                break

        prisoner_loops[prisoner_num] = prisoner_loop

    return prisoner_loops


@njit(nogil=True)
def prisoner_loops_subceed_max(
    prisoner_loops: dict[int, int], max_loop: int, print_loops: bool = False
) -> bool:
    """
    Check if the prisoner loops are higher than the max_loop.
    :prisoner_loops: The prisoner loops dict[int, int] to check, returned from
    calculate_prisoner_box_loops().
    :max_loop: The maximum number of loops to allow.
    :print_loops: Whether to print the prisoner_loops dict.
    :return: True if all prisoner loops subceed the max_loop.
    """
    if print_loops:
        for prisoner_num, prisoner_loop in prisoner_loops.items():
            print(f"Num of Loops: {prisoner_loop} || Prisoner Num: {prisoner_num}")

    for prisoner_num, prisoner_loop in prisoner_loops.items():
        if prisoner_loop > max_loop:
            return False
    return True


@njit(nogil=True)
def loop_calculations(iterations: int, max_loop: int = 50, print_loops=False) -> float:
    """
    This function loops the calculations for calculate_prisoner_box_loops,
    with the given number of iterations.
    :param iterations: number of iterations to loop
    :return: the percentage of the calculations that subceed the max_loop
    """
    subceed_max_counter = 0
    box_dict = create_prisoner_box_dict(100)

    for index in range(1, iterations + 1):
        prisoner_loops_dict = calculate_prisoner_box_loops(box_dict)
        loops_subceeds_max = prisoner_loops_subceed_max(
            prisoner_loops_dict, max_loop, print_loops=print_loops
        )
        if loops_subceeds_max:
            subceed_max_counter += 1

        if index % 1000 == 0:
            print(index)

    subceed_percentage = subceed_max_counter / iterations
    return subceed_percentage


# @njit(nogil=True)
# def create_box_dataset(num, iterations=1):
#     boxes_dataset = [create_prisoner_box_dict(num)
#                      for boxdict in np.arange(iterations)]
#     return boxes_dataset

if __name__ == "__main__":
    percentage = loop_calculations(iterations=100_000, print_loops=False)

    print(f"Percentage: {percentage:.2%}")
