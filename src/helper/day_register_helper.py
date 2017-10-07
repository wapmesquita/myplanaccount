class DayRegisterHelper:

    def dayRegister(self, name, value, dayOfMonth, group=None):
        register = {}
        register['group'] = group
        register['name'] = name
        register['value'] = value
        register['dayOfMonth'] = dayOfMonth
        return register

    def createList(self, list, attr_name, attr_value, attr_dayOfMonth, attr_group=None):
        registers = []
        if attr_group is None:
            for item in list:
                registers.append(self.dayRegister(item[attr_name], item[attr_value], item[attr_dayOfMonth]))
        else:
            for item in list:
                registers.append(self.dayRegister(item[attr_name], item[attr_value], item[attr_dayOfMonth], item[attr_group]))

        return registers
