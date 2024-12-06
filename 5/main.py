
test_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def parse_rules(rule_part: str) -> list[tuple[int, int]]:
  return [tuple(map(int, line.split("|"))) for line in rule_part.split("\n")]

def parse_updates(updates_part: str) -> list[list[int]]:
  return [list(map(int, line.split(","))) for line in updates_part.split("\n")]


def get_update_with_pages_in_right_order(update: list[int], rules: list[tuple[int,int]]) -> list[int]:
  new_update = [p for p in update]
  for rule in rules:
    if rule[0] in update and rule[1] in update:
      first_index = update.index(rule[0])
      second_index = update.index(rule[1])
      # The first page should be to the left of the second page
      if first_index > second_index:
        # Swap the pages - didnt work
        new_update.insert(second_index ,new_update.pop(first_index))
        # new_update[first_index], new_update[second_index] = new_update[second_index], new_update[first_index]

  return new_update


def get_updates_with_pages_in_right_order(updates: list[list[int]], rules: list[tuple[int,int]]) -> list[list[int]]:
  updates_with_pages_in_right_order = []
  for update in updates:
    u = get_update_with_pages_in_right_order(update, rules)
    #print(f"Update: {update} -> {u}")
    #u2 = get_update_with_pages_in_right_order(u, rules)
    #print(f"Update: {u} -> {u2}")
    updates_with_pages_in_right_order.append(u)

  return updates_with_pages_in_right_order

def get_updates_with_pages_already_in_right_order(updates: list[list[int]], rules: list[tuple[int,int]]) -> list[list[int]]:
  """
  Get only the updates that already had their pages in the right order
  """
  updates_with_pages_in_right_order = get_updates_with_pages_in_right_order(updates, rules)
  updates_with_pages_already_in_right_order = []
  for update in updates:
    if update in updates_with_pages_in_right_order:
      updates_with_pages_already_in_right_order.append(update)

  return updates_with_pages_already_in_right_order

def get_updates_with_corrected_page_order(updates: list[list[int]], rules: list[tuple[int,int]]) -> list[list[int]]:
  """
  Get only the updates that had their pages corrected
  """
  updates_with_pages_corrected = []
  updates_with_pages_in_right_order = get_updates_with_pages_in_right_order(updates, rules)
  for update in updates_with_pages_in_right_order:
    if update not in updates:
      updates_with_pages_corrected.append(update)

  return updates_with_pages_corrected

def solve(input: str) -> tuple[int, int]:
  sum_of_middle_page_numbers_already_correct = 0
  sum_of_middle_page_numbers_of_corrected = 0
  rule_part, updates_part = input.split("\n\n")
  rules = parse_rules(rule_part)
  #print(f"Rules: {rules}")
  updates = parse_updates(updates_part)
  #print(f"Updates: {updates}")
  updates_with_pages_already_in_right_order = get_updates_with_pages_already_in_right_order(updates, rules)
  updates_with_pages_corrected = get_updates_with_corrected_page_order(updates, rules)
  for update in updates_with_pages_already_in_right_order:
    sum_of_middle_page_numbers_already_correct += update[len(update) // 2]

  for update in updates_with_pages_corrected:
    sum_of_middle_page_numbers_of_corrected += update[len(update) // 2]

  return (sum_of_middle_page_numbers_already_correct, sum_of_middle_page_numbers_of_corrected)


def main():
  test_answer_already_correct, test_answer_corrected = solve(test_input)
  print(f"Test answer (already correct): {test_answer_already_correct}")
  print(f"Test answer (corrected): {test_answer_corrected}")
  with open("input.txt") as f:
    actual_input = f.read().strip()

  answer_already_correct, answer_corrected = solve(actual_input)
  print(f"Answer  (already correct): {answer_already_correct}")
  print(f"Answer (corrected): {answer_corrected}")


if __name__=='__main__':
  main()
