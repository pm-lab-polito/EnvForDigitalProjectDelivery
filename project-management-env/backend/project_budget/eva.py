from datetime import date

#   Earned Value Analysis
class EVA:
    def __init__(self, **kwargs):
        self._total_scheduled_tasks = kwargs['total_scheduled_tasks']
        self._task_duration = kwargs['task_duration']
        self._employee_cost_day = kwargs['employee_cost_day']
        self._actual_activity = kwargs['actual_activity']

    @property
    def total_scheduled_tasks(self):
        return self._total_scheduled_tasks

    @total_scheduled_tasks.setter
    def total_scheduled_tasks(self, value):
        self._total_scheduled_tasks = value

    @property
    def task_duration(self):
        return self._task_duration

    @task_duration.setter
    def task_duration(self, value):
        self._task_duration = value

    @property
    def employee_cost_day(self):
        return self._employee_cost_day

    @employee_cost_day.setter
    def employee_cost_day(self, value):
        self._employee_cost_day = value

    @property
    def actual_activity(self):
        return self._actual_activity

    @actual_activity.setter
    def actual_activity(self, value):
        self._actual_activity = value

    def _divide(self, x, y):
        li = []
        init = 0
        for i in y:
            init += i/x
            li.append(init)
        return li

    def _multiply(self, x, y):
        li = []
        init = 0
        for i in y:
            init += i*x
            li.append(init)
        return li

    def _li_mul(self, i, j):
        return list(map(lambda x: x*i, j))
    
    def _li_div(self, i, j):
        return list(map(lambda x, y: x/y, i, j))

    def _li_sub(self, i, j):
        return list(map(lambda x, y: x-y, i, j))

    def _li_add(self, i, j):
        return list(map(lambda x, y: x+y, i, j))

    def effort_per_day(self):
        return int(self.total_scheduled_tasks/self.task_duration)

    def employee_cost_hour(self):
        return self.employee_cost_day/self.effort_per_day()

    #   budget at completion
    def bac(self):
        return self.employee_cost_hour()* self.effort_per_day()*self.task_duration

    def scheduled_acticity(self):
        return [self.effort_per_day() for _ in range(self.task_duration)]

    def planned_work_percentage(self):
        return self._divide(self.total_scheduled_tasks, self.scheduled_acticity())
    
    #   BW
    def budget_work(self):
        return list(range(self.effort_per_day(), self.total_scheduled_tasks+self.effort_per_day(), self.effort_per_day()))
    
    def actual_work_percentage(self):
        return self._divide(self.total_scheduled_tasks, self.actual_activity)

    def actual_work(self):
        return self._li_mul(self.total_scheduled_tasks, self.actual_work_percentage())
    
    #   BC
    def budgeted_cost(self):
        return self._multiply(self.employee_cost_hour(), self.scheduled_acticity())
    
    #   ACWP
    def actual_cost_of_work_performed(self):
        return self.budgeted_cost()

    #   BCWS
    def budgeted_cost_of_work_scheduled(self):
        return self._li_mul(self.bac(), self.planned_work_percentage())

    #   BCWP
    def budgeted_cost_of_work_performed(self):
        return self._li_mul(self.bac(), self.actual_work_percentage())
    
    #   EV
    def earned_value(self):
        return self.budgeted_cost_of_work_performed()

    #   SPI
    def schedule_performance_index(self):
        return self._li_div(self.budgeted_cost_of_work_performed(), self.budgeted_cost_of_work_scheduled())

    #   CPI
    def cost_performance_index(self):
        return self._li_div(self.budgeted_cost_of_work_performed(), self.actual_cost_of_work_performed())

    #   CV
    def cost_variance(self):
        return self._li_sub(self.budgeted_cost_of_work_performed(), self.actual_cost_of_work_performed())
    
    def cost_variance_percentage(self):
        return self._li_div(self.cost_variance(), self.budgeted_cost_of_work_performed())
    
    #   SV
    def schedule_variance(self):
        return self._li_sub(self.budgeted_cost_of_work_performed(), self.budgeted_cost_of_work_scheduled())
    
    def schedule_variance_percentage(self):
        return self._li_div(self.schedule_variance(), self.budgeted_cost_of_work_scheduled())

    def rv(self):
        return self._li_sub(self.budgeted_cost_of_work_scheduled(), self.actual_cost_of_work_performed())
    
    def ri(self):
        return self._li_div(self.budgeted_cost_of_work_scheduled(), self.actual_cost_of_work_performed())

    #   BAC
    def budget_at_completion(self):
        return self._li_mul(self.bac(), self.planned_work_percentage())

    #   ETC
    def estimate_to_complete(self):
        sub = self._li_sub(self.budget_at_completion(), self.budgeted_cost_of_work_performed())
        return self._li_div(sub, self.cost_performance_index())

    #   EAC
    def estimate_at_complete(self):
        return self._li_div(self.budget_at_completion(), self.cost_performance_index())
    
    #   CV at complation
    def cost_variance_at_completion(self):
        return self._li_sub(self.budget_at_completion(), self.estimate_at_complete())

    #   PAR
    def planned_accomplishment_rate(self):
        return self._li_div(self.budget_at_completion(), self.budget_work())
    
    #   TV
    def time_variance(self):
        return self._li_div(self.schedule_variance(), self.planned_accomplishment_rate())
    
    #   TV percentage
    def time_variance_percentage(self):
        return self._li_div(self.time_variance(), self.planned_accomplishment_rate())

    #   ES
    def earned_schedule(self):
        return self._li_div(self.earned_value(), self.planned_accomplishment_rate())

    #   TPI
    def time_performance_index(self):
        return self._li_div(self.earned_schedule(), self.budget_work())

    #   EAR
    def estimated_accomplishment_rate(self):
        return self._li_div(self.budgeted_cost_of_work_performed(), self.budget_work())

    #   TEAC
    def time_estimate_at_completion(self):
        sub = self._li_sub(self.budget_at_completion(), self.budgeted_cost_of_work_performed())
        div = self._li_div(sub, self.estimated_accomplishment_rate())
        return self._li_add(self.budget_work(), div)

    #   TVAC
    def time_variance_at_completion(self):
        return self._li_sub(self.time_estimate_at_completion(), self.budget_work())


    
    

