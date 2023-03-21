import numpy as np
import scipy
import scipy.stats as ss
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt

class ProbabilityDensityFunction:
    #Definition of the Probability Density Function

    def __init__(self, x, y, n):
        '''
        Constructor
        '''
        self._x = np.array([x]).astype('float64')
        self._y = np.array([y]).astype('float64')
        if (self._y.any() > 1) or (self._y.any() < 0):
            print(f'Error: There is at least one element of the distribution bigger than 1 or less than 0.')
        self._n = n #"[optional] add more arguments to the constructor to control the creation of the spline (e.g., its order)"
        self._spl = InterpolatedUnivariateSpline(self._x, self._y, k = self._n)
    
    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, n):
        self._n = n
        self._spl = InterpolatedUnivariateSpline(self._x, self._y, k = self._n)


    #"The class should be able to evaluate itself on a generic point or array of points"
    def pdf(self, random_value):
        return self._spl(random_value)
    
    #"Calculating the probability for the random variable to be included in a generic interval"
    def cdf(self, inizio, finale):
        return abs(self._spl.integral(inizio, finale))

    #"the class should be able to throw random numbers according to the distribution that it represents"
    def rand_num(self, amount):
        l = list()            
        for val in range(amount):
            f = scipy.optimize.root_scalar(lambda x: self.cdf(-np.inf, x) - np.random.uniform(), x0 = -100., x1 = 100., method='secant')
            l.append(f.root)
        return l
    '''
    def inaccuracy(self, max, min):
        testing = 1
        media = 0
        while (media < max):
            counts, bins = np.histogram(self.rand_num(testing), density = True)
            l = [abs(counts[i] - self.pdf(bins[i])) for i in range(len(counts))]
            for dif in l:
                media += dif
            media /= len(counts)
            testing += 1
            if (media == min):
                print(f'{testing}')
                break
        print(f'The minimum number of random numbers generated in order to have an accuracy of {max} has to be {testing}.')'''
        
    def inaccuracy(self, limit):
        testing = 1
        area = 0
        #while( area < (1+max)):
        l = []
        m = []
        for y in range(limit):
            area = 0
            testing += 1
            v = self.rand_num(testing)
            counts, bins = np.histogram(v, bins = 50)
            co = 0
            for c in counts:
                co += c
            
            for i in range(len(counts)):
                area += self.cdf(bins[i], bins[i+1]) - (counts[i] /co)
            #area /= len(counts)
            l.append(area)
            m.append(testing)
        #print(f'The minimum number of random numbers generated in order to have an accuracy of {max} has to be {testing}. Con area: {area}')
        plt.plot(m, l)
        plt.show()
        #plt.hist(v)
        #plt.show()



            
            
        #print(f'The minimum number of random numbers generated in order to have an accuracy of {max} has to be {testing}. Con area: {area}')



if __name__ == '__main__':
    x = np.sort(np.random.uniform(-100.,100.,1000))
    y = ss.norm.pdf(x)
    order = 3
    our_pdf = ProbabilityDensityFunction(x, y, order)
    our_pdf.inaccuracy(200)
    #alt = np.linspace(-50., 50., 1000)
    #plt.plot(alt, our_pdf.pdf(alt))
    #plt.plot(np.sort(our_pdf.rand_num(100)), our_pdf.pdf(np.sort(our_pdf.rand_num(100))))
    #plt.show()
    #plt.hist(our_pdf.rand_num(100), bins = 100, density= True)
    #plt.show()
    