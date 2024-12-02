import re

test_input = """3   4
4   3
2   5
1   3
3   9
3   3
"""


def get_lists_from_input(input: str) -> tuple[list[int], list[int]]:
    l1 = []
    l2 = []
    sanitized_input = re.sub(' +', ' ', input) # remove multiple spaces
    #print(sanitized_input)
    for line in sanitized_input.split("\n"):
        if line == "":
            continue
        vals_in_line = line.split()
        l1.append(int(vals_in_line[0]))
        l2.append(int(vals_in_line[1]))
    return l1, l2

def get_smallest_unused_number(input_l: list[int], used_indeces: list) -> tuple[int | None, int | None]:
    smallest = None
    smallest_index = None
    for i in range(len(input_l)):
        if i in used_indeces:
            continue

        if smallest is None:
            smallest = input_l[i]
            smallest_index = i
            continue

        if input_l[i] < smallest:
            smallest = input_l[i]
            smallest_index = i

    return smallest, smallest_index


def calc_total_distance_and_similarity_score(l1: list[int], l2: list[int]) -> tuple[int, int]:
    total_distance = 0
    total_similarity_score = 0
    l1_used_indeces = []
    l2_used_indeces = []
    for i in range(len(l1)):
        smallest_l1, smallest_l1_index = get_smallest_unused_number(l1, l1_used_indeces)
        smallest_l2, smallest_l2_index = get_smallest_unused_number(l2, l2_used_indeces)
        if smallest_l1 is None or smallest_l2 is None:
            break

        l1_used_indeces.append(smallest_l1_index)
        l2_used_indeces.append(smallest_l2_index)
        distance = abs(smallest_l1 - smallest_l2)
        total_distance += distance
        # Similarity score
        val = l1[i]
        occ = l2.count(val)
        total_similarity_score += (val * occ)

    return total_distance, total_similarity_score


def solve(input: str) -> int:
    l1, l2 = get_lists_from_input(input)
    distance = calc_total_distance_and_similarity_score(l1, l2)
    return distance

if __name__ == '__main__':
    answer = solve(test_input)
    print(f"Calculated total distance(test input): {answer}")
    with open("inputs/1_1") as f:
        input2 = f.read()

    answer2 = solve(input2)
    print(f"Calculated total distance: {answer2}")

