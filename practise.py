import cv2 as cv
import numpy as np
import random
from fractions import Fraction
import pandas as pd

class Expression:
    def __init__(self, a, b,s):
        self.a = a
        self.b = b
        self.sign = s
        if self.sign == '+':
            self.result = a + b
        elif self.sign == '-':
            self.result = a - b
        elif self.sign == '*':
            self.result = a * b
        elif self.sign == '/':
            self.result = Fraction(a, b)

    def expand(self):
        return '%d ' % self.a + self.sign + ' %d =  ' % self.b

    def expand_result(self):
        return '%d ' % self.a + self.sign + ' %d = %s ' % (self.b, str(self.result))


class AddMinusTest:
    def __init__(self, min, max, num, p_plus, p_carry):
        self.min = min #算式最小值
        self.max = max #算式最大值
        self.plus_proportion = p_plus #算式加法占比
        self.carry_proportion = p_carry#算式进位占比
        self.num = num #试题数目
        self.question = list() #试题算式


    def run(self):
        self._generate()
        self._select()
        return self.question

    # 根据比率，随机生成单步加减法
    def _generate(self):
        total_express = self.num
        plus_carry_num = int(total_express * self.plus_proportion * self.carry_proportion)
        plus_direct_num = int(total_express * self.plus_proportion * (1 - self.carry_proportion))
        minus_ab_num = int(total_express * (1 - self.plus_proportion) * self.carry_proportion)
        #minus_direct_num = int(total_express * (1 - self.plus_proportion) * (1 - self.carry_proportion))
        minus_direct_num = int(total_express - plus_carry_num - plus_direct_num - minus_ab_num)

        while len(self.question) < self.num:
            a = random.randint(self.min, self.max)
            b = random.randint(self.min, self.max)
            if a + b <= self.max:
                if (a % 10) + (b % 10) > 10 and plus_carry_num > 0:
                    self.question.append(Expression(a, b, '+'))
                    plus_carry_num = plus_carry_num - 1
                elif plus_direct_num > 0:
                    self.question.append(Expression(a, b, '+'))
                    plus_direct_num = plus_direct_num - 1
                continue
            if a - b >= 1 :
                if (a % 10) < (b % 10) and minus_ab_num > 0:
                    self.question.append(Expression(a, b, '-'))
                    minus_ab_num = minus_ab_num - 1
                elif minus_direct_num > 0:
                    self.question.append(Expression(a, b, '-'))
                    minus_direct_num = minus_direct_num - 1
                continue
        assert plus_carry_num == 0 and plus_direct_num == 0 and minus_ab_num == 0 and minus_direct_num == 0

    def __generate(self):
        for a in range(self.min, self.max):
            for b in range(self.min, self.max):
                if a + b <= self.max and (a % 10) + (b % 10) > 10:
                    self.question.append(Expression(a, b, '+'))
                if a - b >= 1 and (a % 10) < (b % 10):
                    self.question.append(Expression(a, b, '-'))

    def ___generate(self):
        while len(self.question) < self.shape[0] * self.shape[1]:
            a = random.randint(self.min, self.max)
            b = random.randint(self.min, self.max)
            sign = random.choice(('+', '-', '*', '/'))
            e = Expression(a, b, sign)
            if e.result < self.max:
                self.question.append(e)


    def _select(self):
        import random
        random.shuffle(self.question)
        self.question = self.question[:self.num:]
    #
    # def _tocsv(self):
    #     q = np.array([e.expand() for e in self.question])
    #     a = np.array([e.expand_result() for e in self.question])
    #     q = q.reshape(self.shape)
    #     a = a.reshape(self.shape)
    #     print(q)
    #     print(a)
    #     np.savetxt('test.csv', q, fmt='%s', delimiter=', ')
    #     np.savetxt('testa.csv', a, fmt='%s', delimiter=', ')


if __name__ == '__main__':
    num = 21
    tests = list()
    for _ in range(num):
        test = AddMinusTest(10, 100, 100, 0.5, 0.8)
        paper = test.run()
        tests.append(paper)
    print(tests)

    with pd.ExcelWriter('tests.xlsx') as writer:
        for i, t in enumerate(tests):
            q = np.array([e.expand() for e in t])
            a = np.array([e.expand_result() for e in t])
            q = q.reshape((25, 4))
            a = a.reshape((25, 4))
            df = pd.DataFrame(q)
            df.to_excel(writer, header=False, index=False, sheet_name=str(i + 1))
            df = pd.DataFrame(a)
            df.to_excel(writer, header=False, index=False,  sheet_name=str(i + 1) + 'a')

        fmt = writer.book.add_format({"font_name": u"宋体", 'bold': True, 'font_size': 16})
        for sheet in writer.sheets.values():
            sheet.set_column('A:D', 20.5, fmt)
            for i in range(25):
                sheet.set_row(i, 31, fmt)

        writer.save()
        writer.close()
