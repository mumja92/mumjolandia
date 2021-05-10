from src.interface.planner.plan import Plan
from src.utils.helpers import DateHelper
from src.utils.object_loader_pickle import ObjectLoaderPickle


class PlansHandler:
    def __init__(self, file_location: str):
        self.file_location = file_location
        self.object_loader_pickle = ObjectLoaderPickle(self.file_location)
        self.plans: [Plan] = []     # to avoid change date between 'get_id' and 'add' plans are saved to variable

    def add(self, day_shift: int, hour: str, duration: int, name: str):
        self.__load()   # has to be called to track current day that can change
        plan_id = self.__get_plan_id(day_shift)
        if plan_id is None:
            self.plans.append(Plan(day_shift))
            plan_id = len(self.plans) - 1
        add_success = self.plans[plan_id].add_task(name, duration, hour)
        if add_success:
            self.__save()
            dupa = self.object_loader_pickle.get()
        return add_success

    def remove(self, day_shift: int, hour: str):
        self.__load()
        plan_id = self.__get_plan_id(day_shift)
        if plan_id is None:
            return False
        remove_success = self.plans[plan_id].remove_task(hour)
        if remove_success:
            if self.plans[plan_id].is_empty():
                del self.plans[plan_id]
            self.__save()
        return remove_success

    def get(self, day_shift: int = None):  # return plan for one day, or all plans if parameter == None
        self.__load()
        if day_shift is None:
            return self.plans
        else:
            plan_id = self.__get_plan_id(day_shift)
            if plan_id is None:
                return Plan(day_shift)
            else:
                return self.plans[plan_id]

    def __get_plan_id(self, day_shift):
        current_index = 0
        for plan in self.plans:
            if plan.date == DateHelper.get_today_short(day_shift):
                return current_index
            current_index += 1
        return None

    def __save(self):
        self.object_loader_pickle.save(self.plans)

    def __load(self):
        plans = self.object_loader_pickle.get()
        if plans is None:
            plans = []
        self.plans = plans
