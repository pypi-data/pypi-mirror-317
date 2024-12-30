# Helper functions for AND/OR logic
def AND(*conditions):
    return lambda item: all(condition(item) for condition in conditions)

def OR(*conditions):
    return lambda item: any(condition(item) for condition in conditions)