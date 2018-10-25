class Task:
    def __init__(self, name, description, date_added, date_to_finish, priority, task_type, occurrence, occurrence_list):
        self.name = name
        self.description = description
        self.date_added = date_added
        self.date_to_finish = date_to_finish
        self.priority = priority
        self.type = task_type
        self.occurrence = occurrence
        self.occurrence_list = occurrence_list

    def __str__(self):
        return self.name
