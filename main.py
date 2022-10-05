import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import kaleido

"""
 ==================================
 Input selection
 ==================================
"""

basicRate = 0.2
basicThresh = 12570
higherRate = 0.4
higherThresh = 37700
additionalRate = 0.45
additionalThresh = 150000

persAllowWithdrawalRate = 0.5
persAllowWithdrawalThresh = 100000

natInsLowRate = 0.1325
natInsLowThresh = 12570
natInsHighRate = 0.02
natInsHighThresh = 50270

childBenefitThresh = (50000, 60000)
childBenefitRate = 0.01
childBenefitClaw = 100

marriedAllowance = 1260
marriedAllowanceThresh = 50270

yearsSinceGrad = 9
loanBalance = 45800
plan1Threshold = 20184
plan1Rate = 0.09
assStartInc = 20000
avgIntRate = 0.015

"""
 ==================================
 Class creation
 ==================================
"""


class Person:
    def __init__(self, children, married, studentLoan, salary):
        self.child = children
        self.married = married
        self.loan = studentLoan
        self.salary = salary

    def personalAllowance(self):
        """
        :return: the amount of personal allowance the Person has
        """
        singlePart = basicThresh - max(0, min((self.salary - persAllowWithdrawalThresh) * 0.5, basicThresh))
        if self.married is True and self.salary <= marriedAllowanceThresh:
            marriedPart = marriedAllowance
        else:
            marriedPart = 0

        return singlePart + marriedPart

    def incomeTax(self):
        """
        :return: the amount of income tax Person pays
        """
        basic = max(0, min((self.salary - self.personalAllowance()), higherThresh) * basicRate)
        higher = max(0, (min(self.salary, additionalThresh) - (higherThresh + self.personalAllowance())) * higherRate)
        additional = max(0, (self.salary - additionalThresh) * additionalRate)
        return basic + higher + additional

    def nationalIns(self):
        """
        :return: the amount of national insurance Person pays
        """
        lowerNatIns = max(0, natInsLowRate * (min(self.salary, natInsHighThresh) - natInsLowThresh))
        higherNatIns = max(0, natInsHighRate * (self.salary - natInsHighThresh))
        return lowerNatIns + higherNatIns

    def childBenefitTax(self):
        """
        :return: the amount of child benefit that is clawed back from Person
        """
        if self.child > 0:
            childBenefitGross = (21.8 + 14.45 * (self.child - 1)) * 52
            return max(0, min((self.salary - childBenefitThresh[0]) / 10000, 1)) * childBenefitGross
        else:
            return 0

    def totalTax(self):
        return self.incomeTax() + self.nationalIns() + self.childBenefitTax()

    def takeHome(self):
        return self.salary - self.totalTax()

    def marginal(self):
        marginPerson = Person(self.child, self.married, self.loan, self.salary + 1)
        return round((marginPerson.totalTax() - self.totalTax()), 2)


"""
 ==================================
 Generating data
 ==================================
"""

salaries = [i * 100 for i in range(1500)]
marginals = [Person(3, False, True, i * 100).marginal() for i in range(1500)]

df = pd.DataFrame(salaries, columns=['Salary'])
dg = pd.DataFrame(marginals, columns=['Marginal tax rate'])
df = pd.concat([df, dg])

"""
 ==================================
 Outputting results
 ==================================
"""

title = 'UK marginal tax rate for single earner, family of 3 kids'
x = salaries
y = marginals

fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=y))
fig.update_layout(yaxis=dict(tickformat="2%"), title=title, xaxis_title='Gross salary', yaxis_title='Marginal tax rate')

fig.write_html('Marg Taxes.html')
fig.write_image('Marg Taxes.jpg')
