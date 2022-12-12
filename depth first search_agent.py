#!/usr/bin/env python
# coding: utf-8

# In[2]:


import copy
import sys as sys

sys.setrecursionlimit(1000)

#--------------------------------------------------------------------------------------------------
class depth_search_functions:
    
    def skf(self,pan, root):
        index_record = []
        for i in range(0, len(root)):
            temp = []
            for j in range(0, len(pan)):
                if pan[j] == root[i]:
                    temp.append(j)
                if j + 1 == len(pan):
                    index_record = index_record + [temp]
        return index_record


    def sepr(self,sep, skf_record0):
        sep_record = []
        skf_record = copy.deepcopy(skf_record0)
        for i in range(0, len(skf_record)):
            temp = skf_record[i]
            for j in range(0, len(temp)):
                temp[j] = list(divmod(temp[j], sep))
            sep_record = sep_record + [temp]
        return sep_record


    def check(self,Q, W, E):
        a = (W[0] - Q[0])
        b = (W[1] - Q[1])
        c = (E[0] - W[0])
        d = (E[1] - W[1])
        if a == 0 or b == 0:
            if c == 0 or d == 0:
                if a!=0 or b!=0 and c!=0 or d!=0:
                    if (a * c) + (b * d) == 0:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


    def knockout(self,c, count):
        c_record = []
        for idle in range(0, len(c)):
            temp_c_element = c[idle]
            if len(temp_c_element) == count:
                c_record.append(c[idle])
        return c_record


    def possi_route(self,data, step, record):
        big_record = []

        if len(data) < 3:
            return False

        if step + 3 < len(data) or step + 3 == len(data):
            step_plus_one = data[step + 1]
            step_plus_two = data[step + 2]
            step_temp = data[step]

        if step + 2 == len(data):
            step_plus_one = data[step + 1]
            step_temp = data[step]

        if step + 1 == len(data):
            step_temp = data[step]

        if step + 1 > len(data):
            return big_record

        elif step + 3 == len(data) and step != 0 and step != 1:
            for idle in range(-len(record), 0):
                if len(record[idle]) < len(data):
                    forward_set = record[idle]
                    forward_two = forward_set[-2]
                    forward_one = forward_set[-1]
                    for i in range(0, len(step_temp)):
                        current = step_temp[i]
                        if self.check(forward_two, forward_one, current):
                            for j in range(0, len(step_plus_one)):
                                next_one = step_plus_one[j]
                                if self.check(forward_one, next_one, current):
                                    for k in range(0, len(step_plus_two)):
                                        next_two = step_plus_two[k]
                                        if self.check(next_two, next_one, current):
                                            record[idle] = record[idle] + [current] + [next_one] + [next_two]
                                            return record

        elif step + 2 == len(data) and step != 0 and step != 1:
            for idle in range(-len(record), 0):
                if len(record[idle]) < len(data):
                    forward_set = record[idle]
                    forward_two = forward_set[-2]
                    forward_one = forward_set[-1]
                    for i in range(0, len(step_temp)):
                        current = step_temp[i]
                        if self.check(forward_two, forward_one, current):
                            for j in range(0, len(step_plus_one)):
                                next_one = step_plus_one[j]
                                if self.check(forward_one, current, next_one):
                                    record[idle] = record[idle] + [current] + [next_one]
                                    return record

        elif step + 1 == len(data) and step != 0 and step != 1:
            for idle in range(-len(record), 0):
                if len(record[idle]) < len(data):
                    forward_set = record[idle]
                    forward_two = forward_set[-2]
                    forward_one = forward_set[-1]
                    for i in range(0, len(step_temp)):
                        current = step_temp[i]
                        if self.check(forward_two, forward_one, current):
                            record[idle] = record[idle] + [current]
                            return record

        elif step == 0 and len(data) > 3:
            for i in range(0, len(step_temp)):
                current = step_temp[i]
                for j in range(0, len(step_plus_one)):
                    next_one = step_plus_one[j]
                    for k in range(0, len(step_plus_two)):
                        next_two = step_plus_two[k]
                        if self.check(next_two, next_one, current):
                            record = record + [[current] + [next_one] + [next_two]]
                            for forward in self.possi_route(data, step + 3, record):
                                big_record.append(forward)

        elif step == 0 and len(data) == 3:
            for i in range(0, len(step_temp)):
                current = step_temp[i]
                for j in range(0, len(step_plus_one)):
                    next_one = step_plus_one[j]
                    for k in range(0, len(step_plus_two)):
                        next_two = step_plus_two[k]
                        if self.check(next_two, next_one, current):
                            big_record.append([current] + [next_one] + [next_two])

        elif step == 1:
            for idle in range(-len(record), 0):
                if len(record[idle]) < len(data):
                    forward_set = record[idle]
                    forward_one = forward_set[-1]
                    for i in range(0, len(step_temp)):
                        current = step_temp[i]
                        for j in range(0, len(step_plus_one)):
                            next_one = step_plus_one[j]
                            if self.check(forward_one, next_one, current):
                                record[idle] = record[idle] + [current]
                                for forward in self.possi_route(data, step + 3, record):
                                    big_record.append(forward)

        else:
            for idle in range(-len(record), 0):
                if len(record[idle]) < len(data):
                    forward_set = record[idle]
                    forward_two = forward_set[-2]
                    forward_one = forward_set[-1]
                    for i in range(0, len(step_temp)):
                        current = step_temp[i]
                        if self.check(forward_two, forward_one, current):
                            for j in range(0, len(step_plus_one)):
                                next_one = step_plus_one[j]
                                if self.check(forward_one, next_one, current):
                                    for k in range(0, len(step_plus_two)):
                                        next_two = step_plus_two[k]
                                        if self.check(next_two, next_one, current):
                                            record[idle] = record[idle] + [current] + [next_one] + [next_two]
                                            for forward in self.possi_route(data, step + 3, record):
                                                big_record.append(forward)

        return big_record
    
    def run(self,background, aim, sep, step, record, count):
        goal_0 = self.skf(background, aim)
        goal_1 = self.sepr(sep, goal_0)
        goal_2 = self.possi_route(goal_1, step, record)
        goal_3 = self.knockout(goal_2, count)
        return goal_3

#--------------------------------------------------------------------------------------------------------
class playsearch:

    def __init__(self, background, aim, sep, step,agent=depth_search_functions()):

        self.background = background
        self.object = aim
        self.sep = sep
        self.step = step
        self.count = len(self.object)
        self.record = []
        self.agent = agent

    def play(self,agent=depth_search_functions()):
        agent = depth_search_functions()
        return agent.run(self.background, self.object, self.sep, self.step, self.record, self.count)


goal = playsearch('VATVVVRSVVVRBA', 'ARSBA', 5, 0)
goal = goal.play()
print(goal)


# In[ ]:





# In[ ]:




