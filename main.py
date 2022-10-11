import pandas as pd

'''
Setting global variables
'''

# children = 3
# married = True
# studentLoan = False

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


def genMarginals(children, married, studentLoan):
    """
    Takes basic parameters and generates list of Marginal Tax Rates as a DataSeries
    :param children: number of children (non-negative integer)
    :param married: Boolean
    :param studentLoan: Boolean
    :return: Marginal Tax Rates
    """

    '''
    Generating dataframe with income
    '''

    incomes = pd.Series(range(0, 200001, 100))
    df = pd.DataFrame(incomes, columns=['Gross Income'])

    '''
    Personal Allowance
    '''

    if married is True:
        df['Marriage Allowance'] = marriedAllowance
        df['Marriage Allowance'].where(df['Gross Income'] <= marriedAllowanceThresh, 0, inplace=True)
    else:
        df['Marriage Allowance'] = 0

    df['Personal Allowance'] = (df['Gross Income'] - persAllowWithdrawalThresh) * 0.5

    df['Personal Allowance'].where(df['Personal Allowance'] < basicThresh, basicThresh, inplace=True)

    df['Personal Allowance'].where(df['Personal Allowance'] > 0, 0, inplace=True)

    df['Personal Allowance'] = basicThresh - df['Personal Allowance']

    df['Personal Allowance'] += df['Marriage Allowance']

    '''
    Income tax
    '''

    df['Basic'] = df['Gross Income'] - df['Personal Allowance']

    df['Basic'].where(df['Basic'] < higherThresh, higherThresh, inplace=True)

    df['Basic'] *= basicRate

    df['Basic'].where(df['Basic'] > 0, 0, inplace=True)

    df['Higher'] = df['Gross Income'].where(df['Gross Income'] < additionalThresh, additionalThresh)

    df['Higher'] -= higherThresh

    df['Higher'] -= df['Personal Allowance']

    df['Higher'] *= higherRate

    df['Higher'].where(df['Higher'] > 0, 0, inplace=True)

    df['Additional'] = (df['Gross Income'] - additionalThresh) * additionalRate

    df['Additional'].where(df['Additional'] > 0, 0, inplace=True)

    df['Income Tax'] = df['Basic'] + df['Higher'] + df['Additional']

    '''
    National insurance
    '''

    df['National Insurance'] = df['Gross Income'].where(df['Gross Income'] < natInsHighThresh, natInsHighThresh) - \
                               natInsLowThresh

    df['National Insurance'] *= natInsLowRate

    df['National Insurance'].where(df['National Insurance'] > 0, 0, inplace=True)

    df['National Insurance Higher'] = (df['Gross Income'] - natInsHighThresh) * natInsHighRate

    df['National Insurance Higher'].where(df['National Insurance Higher'] > 0, 0, inplace=True)

    df['National Insurance'] += df['National Insurance Higher']

    df = df.drop(columns=['National Insurance Higher'])

    '''
    Child Benefit
    '''

    childBenefitGross = (21.8 + 14.45 * (children - 1)) * 52

    df['Child Benefit'] = (df['Gross Income'] - childBenefitThresh[0]) * childBenefitRate / childBenefitClaw

    df['Child Benefit'].where(df['Child Benefit'] < 1, 1, inplace=True)

    df['Child Benefit'].where(df['Child Benefit'] > 0, 0, inplace=True)

    df['Child Benefit'] *= childBenefitGross

    if children == 0:
        df['Child Benefit'] = 0

    '''
    Totals
    '''

    df['Total Tax'] = df['Income Tax'] + df['National Insurance'] + df['Child Benefit']

    df['Take Home Pay'] = df['Gross Income'] - df['Total Tax']

    df['Marginal Tax Rate'] = df['Total Tax'].diff() / 100

    return df[['Gross Income', 'Marginal Tax Rate']]


