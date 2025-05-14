
import json

class Student(object):


    #定义类只能有这两个属性，不能动态添加了
    #__slots__=['name','age']

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value



if __name__=='__main__':
    student=Student();
    student.score=60

    print(student.score)

    str=json.dumps(student,default=lambda temp:{'score':temp.score})
    print(str)