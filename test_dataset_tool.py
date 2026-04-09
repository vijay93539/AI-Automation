from tools.dataset_tool import (
    get_dataset_overview,
    highest_torque_machine,
    lowest_rpm_machine,
    highest_failure_machine,
    lowest_failure_machine
)

print("DATASET OVERVIEW:")
print(get_dataset_overview())

print("\nHIGHEST TORQUE MACHINE:")
print(highest_torque_machine())

print("\nLOWEST RPM MACHINE:")
print(lowest_rpm_machine())

print("\nHIGHEST FAILURE MACHINE:")
print(highest_failure_machine())

print("\nLOWEST FAILURE MACHINE:")
print(lowest_failure_machine())