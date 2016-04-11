# encoding: utf-8
# module numpy.random.mtrand
# from /usr/lib/python2.7/dist-packages/numpy/random/mtrand.so
# by generator 1.138
# no doc

# imports
import operator as operator # /usr/local/lib/python2.7/lib-dynload/operator.so
import numpy as np # /usr/lib/python2.7/dist-packages/numpy/__init__.pyc
import __builtin__ as __builtins__ # <module '__builtin__' (built-in)>

# functions

def beta(a, b, size=None): # real signature unknown; restored from __doc__
    """
    beta(a, b, size=None)
    
            The Beta distribution over ``[0, 1]``.
    
            The Beta distribution is a special case of the Dirichlet distribution,
            and is related to the Gamma distribution.  It has the probability
            distribution function
    
            .. math:: f(x; a,b) = \frac{1}{B(\alpha, \beta)} x^{\alpha - 1}
                                                             (1 - x)^{\beta - 1},
    
            where the normalisation, B, is the beta function,
    
            .. math:: B(\alpha, \beta) = \int_0^1 t^{\alpha - 1}
                                         (1 - t)^{\beta - 1} dt.
    
            It is often seen in Bayesian inference and order statistics.
    
            Parameters
            ----------
            a : float
                Alpha, non-negative.
            b : float
                Beta, non-negative.
            size : tuple of ints, optional
                The number of samples to draw.  The output is packed according to
                the size given.
    
            Returns
            -------
            out : ndarray
                Array of the given shape, containing values drawn from a
                Beta distribution.
    """
    pass

def binomial(n, p, size=None): # real signature unknown; restored from __doc__
    """
    binomial(n, p, size=None)
    
            Draw samples from a binomial distribution.
    
            Samples are drawn from a Binomial distribution with specified
            parameters, n trials and p probability of success where
            n an integer >= 0 and p is in the interval [0,1]. (n may be
            input as a float, but it is truncated to an integer in use)
    
            Parameters
            ----------
            n : float (but truncated to an integer)
                    parameter, >= 0.
            p : float
                    parameter, >= 0 and <=1.
            size : {tuple, int}
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : {ndarray, scalar}
                      where the values are all integers in  [0, n].
    
            See Also
            --------
            scipy.stats.distributions.binom : probability density function,
                distribution or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the Binomial distribution is
    
            .. math:: P(N) = \binom{n}{N}p^N(1-p)^{n-N},
    
            where :math:`n` is the number of trials, :math:`p` is the probability
            of success, and :math:`N` is the number of successes.
    
            When estimating the standard error of a proportion in a population by
            using a random sample, the normal distribution works well unless the
            product p*n <=5, where p = population proportion estimate, and n =
            number of samples, in which case the binomial distribution is used
            instead. For example, a sample of 15 people shows 4 who are left
            handed, and 11 who are right handed. Then p = 4/15 = 27%. 0.27*15 = 4,
            so the binomial distribution should be used in this case.
    
            References
            ----------
            .. [1] Dalgaard, Peter, "Introductory Statistics with R",
                   Springer-Verlag, 2002.
            .. [2] Glantz, Stanton A. "Primer of Biostatistics.", McGraw-Hill,
                   Fifth Edition, 2002.
            .. [3] Lentner, Marvin, "Elementary Applied Statistics", Bogden
                   and Quigley, 1972.
            .. [4] Weisstein, Eric W. "Binomial Distribution." From MathWorld--A
                   Wolfram Web Resource.
                   http://mathworld.wolfram.com/BinomialDistribution.html
            .. [5] Wikipedia, "Binomial-distribution",
                   http://en.wikipedia.org/wiki/Binomial_distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> n, p = 10, .5 # number of trials, probability of each trial
            >>> s = np.random.binomial(n, p, 1000)
            # result of flipping a coin 10 times, tested 1000 times.
    
            A real world example. A company drills 9 wild-cat oil exploration
            wells, each with an estimated probability of success of 0.1. All nine
            wells fail. What is the probability of that happening?
    
            Let's do 20,000 trials of the model, and count the number that
            generate zero positive results.
    
            >>> sum(np.random.binomial(9,0.1,20000)==0)/20000.
            answer = 0.38885, or 38%.
    """
    pass

def bytes(length): # real signature unknown; restored from __doc__
    """
    bytes(length)
    
            Return random bytes.
    
            Parameters
            ----------
            length : int
                Number of random bytes.
    
            Returns
            -------
            out : str
                String of length `length`.
    
            Examples
            --------
            >>> np.random.bytes(10)
            ' eh\x85\x022SZ\xbf\xa4' #random
    """
    pass

def chisquare(df, size=None): # real signature unknown; restored from __doc__
    """
    chisquare(df, size=None)
    
            Draw samples from a chi-square distribution.
    
            When `df` independent random variables, each with standard normal
            distributions (mean 0, variance 1), are squared and summed, the
            resulting distribution is chi-square (see Notes).  This distribution
            is often used in hypothesis testing.
    
            Parameters
            ----------
            df : int
                 Number of degrees of freedom.
            size : tuple of ints, int, optional
                 Size of the returned array.  By default, a scalar is
                 returned.
    
            Returns
            -------
            output : ndarray
                Samples drawn from the distribution, packed in a `size`-shaped
                array.
    
            Raises
            ------
            ValueError
                When `df` <= 0 or when an inappropriate `size` (e.g. ``size=-1``)
                is given.
    
            Notes
            -----
            The variable obtained by summing the squares of `df` independent,
            standard normally distributed random variables:
    
            .. math:: Q = \sum_{i=0}^{\mathtt{df}} X^2_i
    
            is chi-square distributed, denoted
    
            .. math:: Q \sim \chi^2_k.
    
            The probability density function of the chi-squared distribution is
    
            .. math:: p(x) = \frac{(1/2)^{k/2}}{\Gamma(k/2)}
                             x^{k/2 - 1} e^{-x/2},
    
            where :math:`\Gamma` is the gamma function,
    
            .. math:: \Gamma(x) = \int_0^{-\infty} t^{x - 1} e^{-t} dt.
    
            References
            ----------
            `NIST/SEMATECH e-Handbook of Statistical Methods
            <http://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm>`_
    
            Examples
            --------
            >>> np.random.chisquare(2,4)
            array([ 1.89920014,  9.00867716,  3.13710533,  5.62318272])
    """
    pass

def choice(a, size=None, replace=True, p=None): # real signature unknown; restored from __doc__
    """
    choice(a, size=None, replace=True, p=None)
    
            Generates a random sample from a given 1-D array
    
                    .. versionadded:: 1.7.0
    
            Parameters
            -----------
            a : 1-D array-like or int
                If an ndarray, a random sample is generated from its elements.
                If an int, the random sample is generated as if a was np.arange(n)
            size : int or tuple of ints, optional
                Output shape. Default is None, in which case a single value is
                returned.
            replace : boolean, optional
                Whether the sample is with or without replacement
            p : 1-D array-like, optional
                The probabilities associated with each entry in a.
                If not given the sample assumes a uniform distribtion over all
                entries in a.
    
            Returns
            --------
            samples : 1-D ndarray, shape (size,)
                The generated random samples
    
            Raises
            -------
            ValueError
                If a is an int and less than zero, if a or p are not 1-dimensional,
                if a is an array-like of size 0, if p is not a vector of
                probabilities, if a and p have different lengths, or if
                replace=False and the sample size is greater than the population
                size
    
            See Also
            ---------
            randint, shuffle, permutation
    
            Examples
            ---------
            Generate a uniform random sample from np.arange(5) of size 3:
    
            >>> np.random.choice(5, 3)
            array([0, 3, 4])
            >>> #This is equivalent to np.random.randint(0,5,3)
    
            Generate a non-uniform random sample from np.arange(5) of size 3:
    
            >>> np.random.choice(5, 3, p=[0.1, 0, 0.3, 0.6, 0])
            array([3, 3, 0])
    
            Generate a uniform random sample from np.arange(5) of size 3 without
            replacement:
    
            >>> np.random.choice(5, 3, replace=False)
            array([3,1,0])
            >>> #This is equivalent to np.random.shuffle(np.arange(5))[:3]
    
            Generate a non-uniform random sample from np.arange(5) of size
            3 without replacement:
    
            >>> np.random.choice(5, 3, replace=False, p=[0.1, 0, 0.3, 0.6, 0])
            array([2, 3, 0])
    
            Any of the above can be repeated with an arbitrary array-like
            instead of just integers. For instance:
    
            >>> aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']
            >>> np.random.choice(aa_milne_arr, 5, p=[0.5, 0.1, 0.1, 0.3])
            array(['pooh', 'pooh', 'pooh', 'Christopher', 'piglet'],
                  dtype='|S11')
    """
    pass

def dirichlet(alpha, size=None): # real signature unknown; restored from __doc__
    """
    dirichlet(alpha, size=None)
    
            Draw samples from the Dirichlet distribution.
    
            Draw `size` samples of dimension k from a Dirichlet distribution. A
            Dirichlet-distributed random variable can be seen as a multivariate
            generalization of a Beta distribution. Dirichlet pdf is the conjugate
            prior of a multinomial in Bayesian inference.
    
            Parameters
            ----------
            alpha : array
                Parameter of the distribution (k dimension for sample of
                dimension k).
            size : array
                Number of samples to draw.
    
            Returns
            -------
            samples : ndarray,
                The drawn samples, of shape (alpha.ndim, size).
    
            Notes
            -----
            .. math:: X \approx \prod_{i=1}^{k}{x^{\alpha_i-1}_i}
    
            Uses the following property for computation: for each dimension,
            draw a random sample y_i from a standard gamma generator of shape
            `alpha_i`, then
            :math:`X = \frac{1}{\sum_{i=1}^k{y_i}} (y_1, \ldots, y_n)` is
            Dirichlet distributed.
    
            References
            ----------
            .. [1] David McKay, "Information Theory, Inference and Learning
                   Algorithms," chapter 23,
                   http://www.inference.phy.cam.ac.uk/mackay/
            .. [2] Wikipedia, "Dirichlet distribution",
                   http://en.wikipedia.org/wiki/Dirichlet_distribution
    
            Examples
            --------
            Taking an example cited in Wikipedia, this distribution can be used if
            one wanted to cut strings (each of initial length 1.0) into K pieces
            with different lengths, where each piece had, on average, a designated
            average length, but allowing some variation in the relative sizes of the
            pieces.
    
            >>> s = np.random.dirichlet((10, 5, 3), 20).transpose()
    
            >>> plt.barh(range(20), s[0])
            >>> plt.barh(range(20), s[1], left=s[0], color='g')
            >>> plt.barh(range(20), s[2], left=s[0]+s[1], color='r')
            >>> plt.title("Lengths of Strings")
    """
    pass

def exponential(scale=1.0, size=None): # real signature unknown; restored from __doc__
    """
    exponential(scale=1.0, size=None)
    
            Exponential distribution.
    
            Its probability density function is
    
            .. math:: f(x; \frac{1}{\beta}) = \frac{1}{\beta} \exp(-\frac{x}{\beta}),
    
            for ``x > 0`` and 0 elsewhere. :math:`\beta` is the scale parameter,
            which is the inverse of the rate parameter :math:`\lambda = 1/\beta`.
            The rate parameter is an alternative, widely used parameterization
            of the exponential distribution [3]_.
    
            The exponential distribution is a continuous analogue of the
            geometric distribution.  It describes many common situations, such as
            the size of raindrops measured over many rainstorms [1]_, or the time
            between page requests to Wikipedia [2]_.
    
            Parameters
            ----------
            scale : float
                The scale parameter, :math:`\beta = 1/\lambda`.
            size : tuple of ints
                Number of samples to draw.  The output is shaped
                according to `size`.
    
            References
            ----------
            .. [1] Peyton Z. Peebles Jr., "Probability, Random Variables and
                   Random Signal Principles", 4th ed, 2001, p. 57.
            .. [2] "Poisson Process", Wikipedia,
                   http://en.wikipedia.org/wiki/Poisson_process
            .. [3] "Exponential Distribution, Wikipedia,
                   http://en.wikipedia.org/wiki/Exponential_distribution
    """
    pass

def f(dfnum, dfden, size=None): # real signature unknown; restored from __doc__
    """
    f(dfnum, dfden, size=None)
    
            Draw samples from a F distribution.
    
            Samples are drawn from an F distribution with specified parameters,
            `dfnum` (degrees of freedom in numerator) and `dfden` (degrees of freedom
            in denominator), where both parameters should be greater than zero.
    
            The random variate of the F distribution (also known as the
            Fisher distribution) is a continuous probability distribution
            that arises in ANOVA tests, and is the ratio of two chi-square
            variates.
    
            Parameters
            ----------
            dfnum : float
                Degrees of freedom in numerator. Should be greater than zero.
            dfden : float
                Degrees of freedom in denominator. Should be greater than zero.
            size : {tuple, int}, optional
                Output shape.  If the given shape is, e.g., ``(m, n, k)``,
                then ``m * n * k`` samples are drawn. By default only one sample
                is returned.
    
            Returns
            -------
            samples : {ndarray, scalar}
                Samples from the Fisher distribution.
    
            See Also
            --------
            scipy.stats.distributions.f : probability density function,
                distribution or cumulative density function, etc.
    
            Notes
            -----
            The F statistic is used to compare in-group variances to between-group
            variances. Calculating the distribution depends on the sampling, and
            so it is a function of the respective degrees of freedom in the
            problem.  The variable `dfnum` is the number of samples minus one, the
            between-groups degrees of freedom, while `dfden` is the within-groups
            degrees of freedom, the sum of the number of samples in each group
            minus the number of groups.
    
            References
            ----------
            .. [1] Glantz, Stanton A. "Primer of Biostatistics.", McGraw-Hill,
                   Fifth Edition, 2002.
            .. [2] Wikipedia, "F-distribution",
                   http://en.wikipedia.org/wiki/F-distribution
    
            Examples
            --------
            An example from Glantz[1], pp 47-40.
            Two groups, children of diabetics (25 people) and children from people
            without diabetes (25 controls). Fasting blood glucose was measured,
            case group had a mean value of 86.1, controls had a mean value of
            82.2. Standard deviations were 2.09 and 2.49 respectively. Are these
            data consistent with the null hypothesis that the parents diabetic
            status does not affect their children's blood glucose levels?
            Calculating the F statistic from the data gives a value of 36.01.
    
            Draw samples from the distribution:
    
            >>> dfnum = 1. # between group degrees of freedom
            >>> dfden = 48. # within groups degrees of freedom
            >>> s = np.random.f(dfnum, dfden, 1000)
    
            The lower bound for the top 1% of the samples is :
    
            >>> sort(s)[-10]
            7.61988120985
    
            So there is about a 1% chance that the F statistic will exceed 7.62,
            the measured value is 36, so the null hypothesis is rejected at the 1%
            level.
    """
    pass

def gamma(shape, scale=1.0, size=None): # real signature unknown; restored from __doc__
    """
    gamma(shape, scale=1.0, size=None)
    
            Draw samples from a Gamma distribution.
    
            Samples are drawn from a Gamma distribution with specified parameters,
            `shape` (sometimes designated "k") and `scale` (sometimes designated
            "theta"), where both parameters are > 0.
    
            Parameters
            ----------
            shape : scalar > 0
                The shape of the gamma distribution.
            scale : scalar > 0, optional
                The scale of the gamma distribution.  Default is equal to 1.
            size : shape_tuple, optional
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            out : ndarray, float
                Returns one sample unless `size` parameter is specified.
    
            See Also
            --------
            scipy.stats.distributions.gamma : probability density function,
                distribution or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the Gamma distribution is
    
            .. math:: p(x) = x^{k-1}\frac{e^{-x/\theta}}{\theta^k\Gamma(k)},
    
            where :math:`k` is the shape and :math:`\theta` the scale,
            and :math:`\Gamma` is the Gamma function.
    
            The Gamma distribution is often used to model the times to failure of
            electronic components, and arises naturally in processes for which the
            waiting times between Poisson distributed events are relevant.
    
            References
            ----------
            .. [1] Weisstein, Eric W. "Gamma Distribution." From MathWorld--A
                   Wolfram Web Resource.
                   http://mathworld.wolfram.com/GammaDistribution.html
            .. [2] Wikipedia, "Gamma-distribution",
                   http://en.wikipedia.org/wiki/Gamma-distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> shape, scale = 2., 2. # mean and dispersion
            >>> s = np.random.gamma(shape, scale, 1000)
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> import scipy.special as sps
            >>> count, bins, ignored = plt.hist(s, 50, normed=True)
            >>> y = bins**(shape-1)*(np.exp(-bins/scale) /
            ...                      (sps.gamma(shape)*scale**shape))
            >>> plt.plot(bins, y, linewidth=2, color='r')
            >>> plt.show()
    """
    pass

def geometric(p, size=None): # real signature unknown; restored from __doc__
    """
    geometric(p, size=None)
    
            Draw samples from the geometric distribution.
    
            Bernoulli trials are experiments with one of two outcomes:
            success or failure (an example of such an experiment is flipping
            a coin).  The geometric distribution models the number of trials
            that must be run in order to achieve success.  It is therefore
            supported on the positive integers, ``k = 1, 2, ...``.
    
            The probability mass function of the geometric distribution is
    
            .. math:: f(k) = (1 - p)^{k - 1} p
    
            where `p` is the probability of success of an individual trial.
    
            Parameters
            ----------
            p : float
                The probability of success of an individual trial.
            size : tuple of ints
                Number of values to draw from the distribution.  The output
                is shaped according to `size`.
    
            Returns
            -------
            out : ndarray
                Samples from the geometric distribution, shaped according to
                `size`.
    
            Examples
            --------
            Draw ten thousand values from the geometric distribution,
            with the probability of an individual success equal to 0.35:
    
            >>> z = np.random.geometric(p=0.35, size=10000)
    
            How many trials succeeded after a single run?
    
            >>> (z == 1).sum() / 10000.
            0.34889999999999999 #random
    """
    pass

def get_state(): # real signature unknown; restored from __doc__
    """
    get_state()
    
            Return a tuple representing the internal state of the generator.
    
            For more details, see `set_state`.
    
            Returns
            -------
            out : tuple(str, ndarray of 624 uints, int, int, float)
                The returned tuple has the following items:
    
                1. the string 'MT19937'.
                2. a 1-D array of 624 unsigned integer keys.
                3. an integer ``pos``.
                4. an integer ``has_gauss``.
                5. a float ``cached_gaussian``.
    
            See Also
            --------
            set_state
    
            Notes
            -----
            `set_state` and `get_state` are not needed to work with any of the
            random distributions in NumPy. If the internal state is manually altered,
            the user should know exactly what he/she is doing.
    """
    pass

def gumbel(loc=0.0, scale=1.0, size=None): # real signature unknown; restored from __doc__
    """
    gumbel(loc=0.0, scale=1.0, size=None)
    
            Gumbel distribution.
    
            Draw samples from a Gumbel distribution with specified location and scale.
            For more information on the Gumbel distribution, see Notes and References
            below.
    
            Parameters
            ----------
            loc : float
                The location of the mode of the distribution.
            scale : float
                The scale parameter of the distribution.
            size : tuple of ints
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            out : ndarray
                The samples
    
            See Also
            --------
            scipy.stats.gumbel_l
            scipy.stats.gumbel_r
            scipy.stats.genextreme
                probability density function, distribution, or cumulative density
                function, etc. for each of the above
            weibull
    
            Notes
            -----
            The Gumbel (or Smallest Extreme Value (SEV) or the Smallest Extreme Value
            Type I) distribution is one of a class of Generalized Extreme Value (GEV)
            distributions used in modeling extreme value problems.  The Gumbel is a
            special case of the Extreme Value Type I distribution for maximums from
            distributions with "exponential-like" tails.
    
            The probability density for the Gumbel distribution is
    
            .. math:: p(x) = \frac{e^{-(x - \mu)/ \beta}}{\beta} e^{ -e^{-(x - \mu)/
                      \beta}},
    
            where :math:`\mu` is the mode, a location parameter, and :math:`\beta` is
            the scale parameter.
    
            The Gumbel (named for German mathematician Emil Julius Gumbel) was used
            very early in the hydrology literature, for modeling the occurrence of
            flood events. It is also used for modeling maximum wind speed and rainfall
            rates.  It is a "fat-tailed" distribution - the probability of an event in
            the tail of the distribution is larger than if one used a Gaussian, hence
            the surprisingly frequent occurrence of 100-year floods. Floods were
            initially modeled as a Gaussian process, which underestimated the frequency
            of extreme events.
    
    
            It is one of a class of extreme value distributions, the Generalized
            Extreme Value (GEV) distributions, which also includes the Weibull and
            Frechet.
    
            The function has a mean of :math:`\mu + 0.57721\beta` and a variance of
            :math:`\frac{\pi^2}{6}\beta^2`.
    
            References
            ----------
            Gumbel, E. J., *Statistics of Extremes*, New York: Columbia University
            Press, 1958.
    
            Reiss, R.-D. and Thomas, M., *Statistical Analysis of Extreme Values from
            Insurance, Finance, Hydrology and Other Fields*, Basel: Birkhauser Verlag,
            2001.
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> mu, beta = 0, 0.1 # location and scale
            >>> s = np.random.gumbel(mu, beta, 1000)
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> count, bins, ignored = plt.hist(s, 30, normed=True)
            >>> plt.plot(bins, (1/beta)*np.exp(-(bins - mu)/beta)
            ...          * np.exp( -np.exp( -(bins - mu) /beta) ),
            ...          linewidth=2, color='r')
            >>> plt.show()
    
            Show how an extreme value distribution can arise from a Gaussian process
            and compare to a Gaussian:
    
            >>> means = []
            >>> maxima = []
            >>> for i in range(0,1000) :
            ...    a = np.random.normal(mu, beta, 1000)
            ...    means.append(a.mean())
            ...    maxima.append(a.max())
            >>> count, bins, ignored = plt.hist(maxima, 30, normed=True)
            >>> beta = np.std(maxima)*np.pi/np.sqrt(6)
            >>> mu = np.mean(maxima) - 0.57721*beta
            >>> plt.plot(bins, (1/beta)*np.exp(-(bins - mu)/beta)
            ...          * np.exp(-np.exp(-(bins - mu)/beta)),
            ...          linewidth=2, color='r')
            >>> plt.plot(bins, 1/(beta * np.sqrt(2 * np.pi))
            ...          * np.exp(-(bins - mu)**2 / (2 * beta**2)),
            ...          linewidth=2, color='g')
            >>> plt.show()
    """
    pass

def hypergeometric(ngood, nbad, nsample, size=None): # real signature unknown; restored from __doc__
    """
    hypergeometric(ngood, nbad, nsample, size=None)
    
            Draw samples from a Hypergeometric distribution.
    
            Samples are drawn from a Hypergeometric distribution with specified
            parameters, ngood (ways to make a good selection), nbad (ways to make
            a bad selection), and nsample = number of items sampled, which is less
            than or equal to the sum ngood + nbad.
    
            Parameters
            ----------
            ngood : int or array_like
                Number of ways to make a good selection.  Must be nonnegative.
            nbad : int or array_like
                Number of ways to make a bad selection.  Must be nonnegative.
            nsample : int or array_like
                Number of items sampled.  Must be at least 1 and at most
                ``ngood + nbad``.
            size : int or tuple of int
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : ndarray or scalar
                The values are all integers in  [0, n].
    
            See Also
            --------
            scipy.stats.distributions.hypergeom : probability density function,
                distribution or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the Hypergeometric distribution is
    
            .. math:: P(x) = \frac{\binom{m}{n}\binom{N-m}{n-x}}{\binom{N}{n}},
    
            where :math:`0 \le x \le m` and :math:`n+m-N \le x \le n`
    
            for P(x) the probability of x successes, n = ngood, m = nbad, and
            N = number of samples.
    
            Consider an urn with black and white marbles in it, ngood of them
            black and nbad are white. If you draw nsample balls without
            replacement, then the Hypergeometric distribution describes the
            distribution of black balls in the drawn sample.
    
            Note that this distribution is very similar to the Binomial
            distribution, except that in this case, samples are drawn without
            replacement, whereas in the Binomial case samples are drawn with
            replacement (or the sample space is infinite). As the sample space
            becomes large, this distribution approaches the Binomial.
    
            References
            ----------
            .. [1] Lentner, Marvin, "Elementary Applied Statistics", Bogden
                   and Quigley, 1972.
            .. [2] Weisstein, Eric W. "Hypergeometric Distribution." From
                   MathWorld--A Wolfram Web Resource.
                   http://mathworld.wolfram.com/HypergeometricDistribution.html
            .. [3] Wikipedia, "Hypergeometric-distribution",
                   http://en.wikipedia.org/wiki/Hypergeometric-distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> ngood, nbad, nsamp = 100, 2, 10
            # number of good, number of bad, and number of samples
            >>> s = np.random.hypergeometric(ngood, nbad, nsamp, 1000)
            >>> hist(s)
            #   note that it is very unlikely to grab both bad items
    
            Suppose you have an urn with 15 white and 15 black marbles.
            If you pull 15 marbles at random, how likely is it that
            12 or more of them are one color?
    
            >>> s = np.random.hypergeometric(15, 15, 15, 100000)
            >>> sum(s>=12)/100000. + sum(s<=3)/100000.
            #   answer = 0.003 ... pretty unlikely!
    """
    pass

def laplace(loc=0.0, scale=1.0, size=None): # real signature unknown; restored from __doc__
    """
    laplace(loc=0.0, scale=1.0, size=None)
    
            Draw samples from the Laplace or double exponential distribution with
            specified location (or mean) and scale (decay).
    
            The Laplace distribution is similar to the Gaussian/normal distribution,
            but is sharper at the peak and has fatter tails. It represents the
            difference between two independent, identically distributed exponential
            random variables.
    
            Parameters
            ----------
            loc : float
                The position, :math:`\mu`, of the distribution peak.
            scale : float
                :math:`\lambda`, the exponential decay.
    
            Notes
            -----
            It has the probability density function
    
            .. math:: f(x; \mu, \lambda) = \frac{1}{2\lambda}
                                           \exp\left(-\frac{|x - \mu|}{\lambda}\right).
    
            The first law of Laplace, from 1774, states that the frequency of an error
            can be expressed as an exponential function of the absolute magnitude of
            the error, which leads to the Laplace distribution. For many problems in
            Economics and Health sciences, this distribution seems to model the data
            better than the standard Gaussian distribution
    
    
            References
            ----------
            .. [1] Abramowitz, M. and Stegun, I. A. (Eds.). Handbook of Mathematical
                   Functions with Formulas, Graphs, and Mathematical Tables, 9th
                   printing.  New York: Dover, 1972.
    
            .. [2] The Laplace distribution and generalizations
                   By Samuel Kotz, Tomasz J. Kozubowski, Krzysztof Podgorski,
                   Birkhauser, 2001.
    
            .. [3] Weisstein, Eric W. "Laplace Distribution."
                   From MathWorld--A Wolfram Web Resource.
                   http://mathworld.wolfram.com/LaplaceDistribution.html
    
            .. [4] Wikipedia, "Laplace distribution",
                   http://en.wikipedia.org/wiki/Laplace_distribution
    
            Examples
            --------
            Draw samples from the distribution
    
            >>> loc, scale = 0., 1.
            >>> s = np.random.laplace(loc, scale, 1000)
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> count, bins, ignored = plt.hist(s, 30, normed=True)
            >>> x = np.arange(-8., 8., .01)
            >>> pdf = np.exp(-abs(x-loc/scale))/(2.*scale)
            >>> plt.plot(x, pdf)
    
            Plot Gaussian for comparison:
    
            >>> g = (1/(scale * np.sqrt(2 * np.pi)) * 
            ...      np.exp( - (x - loc)**2 / (2 * scale**2) ))
            >>> plt.plot(x,g)
    """
    pass

def logistic(loc=0.0, scale=1.0, size=None): # real signature unknown; restored from __doc__
    """
    logistic(loc=0.0, scale=1.0, size=None)
    
            Draw samples from a Logistic distribution.
    
            Samples are drawn from a Logistic distribution with specified
            parameters, loc (location or mean, also median), and scale (>0).
    
            Parameters
            ----------
            loc : float
    
            scale : float > 0.
    
            size : {tuple, int}
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : {ndarray, scalar}
                      where the values are all integers in  [0, n].
    
            See Also
            --------
            scipy.stats.distributions.logistic : probability density function,
                distribution or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the Logistic distribution is
    
            .. math:: P(x) = P(x) = \frac{e^{-(x-\mu)/s}}{s(1+e^{-(x-\mu)/s})^2},
    
            where :math:`\mu` = location and :math:`s` = scale.
    
            The Logistic distribution is used in Extreme Value problems where it
            can act as a mixture of Gumbel distributions, in Epidemiology, and by
            the World Chess Federation (FIDE) where it is used in the Elo ranking
            system, assuming the performance of each player is a logistically
            distributed random variable.
    
            References
            ----------
            .. [1] Reiss, R.-D. and Thomas M. (2001), Statistical Analysis of Extreme
                   Values, from Insurance, Finance, Hydrology and Other Fields,
                   Birkhauser Verlag, Basel, pp 132-133.
            .. [2] Weisstein, Eric W. "Logistic Distribution." From
                   MathWorld--A Wolfram Web Resource.
                   http://mathworld.wolfram.com/LogisticDistribution.html
            .. [3] Wikipedia, "Logistic-distribution",
                   http://en.wikipedia.org/wiki/Logistic-distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> loc, scale = 10, 1
            >>> s = np.random.logistic(loc, scale, 10000)
            >>> count, bins, ignored = plt.hist(s, bins=50)
    
            #   plot against distribution
    
            >>> def logist(x, loc, scale):
            ...     return exp((loc-x)/scale)/(scale*(1+exp((loc-x)/scale))**2)
            >>> plt.plot(bins, logist(bins, loc, scale)*count.max()/\
            ... logist(bins, loc, scale).max())
            >>> plt.show()
    """
    pass

def lognormal(mean=0.0, sigma=1.0, size=None): # real signature unknown; restored from __doc__
    """
    lognormal(mean=0.0, sigma=1.0, size=None)
    
            Return samples drawn from a log-normal distribution.
    
            Draw samples from a log-normal distribution with specified mean,
            standard deviation, and array shape.  Note that the mean and standard
            deviation are not the values for the distribution itself, but of the
            underlying normal distribution it is derived from.
    
            Parameters
            ----------
            mean : float
                Mean value of the underlying normal distribution
            sigma : float, > 0.
                Standard deviation of the underlying normal distribution
            size : tuple of ints
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : ndarray or float
                The desired samples. An array of the same shape as `size` if given,
                if `size` is None a float is returned.
    
            See Also
            --------
            scipy.stats.lognorm : probability density function, distribution,
                cumulative density function, etc.
    
            Notes
            -----
            A variable `x` has a log-normal distribution if `log(x)` is normally
            distributed.  The probability density function for the log-normal
            distribution is:
    
            .. math:: p(x) = \frac{1}{\sigma x \sqrt{2\pi}}
                             e^{(-\frac{(ln(x)-\mu)^2}{2\sigma^2})}
    
            where :math:`\mu` is the mean and :math:`\sigma` is the standard
            deviation of the normally distributed logarithm of the variable.
            A log-normal distribution results if a random variable is the *product*
            of a large number of independent, identically-distributed variables in
            the same way that a normal distribution results if the variable is the
            *sum* of a large number of independent, identically-distributed
            variables.
    
            References
            ----------
            Limpert, E., Stahel, W. A., and Abbt, M., "Log-normal Distributions
            across the Sciences: Keys and Clues," *BioScience*, Vol. 51, No. 5,
            May, 2001.  http://stat.ethz.ch/~stahel/lognormal/bioscience.pdf
    
            Reiss, R.D. and Thomas, M., *Statistical Analysis of Extreme Values*,
            Basel: Birkhauser Verlag, 2001, pp. 31-32.
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> mu, sigma = 3., 1. # mean and standard deviation
            >>> s = np.random.lognormal(mu, sigma, 1000)
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> count, bins, ignored = plt.hist(s, 100, normed=True, align='mid')
    
            >>> x = np.linspace(min(bins), max(bins), 10000)
            >>> pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
            ...        / (x * sigma * np.sqrt(2 * np.pi)))
    
            >>> plt.plot(x, pdf, linewidth=2, color='r')
            >>> plt.axis('tight')
            >>> plt.show()
    
            Demonstrate that taking the products of random samples from a uniform
            distribution can be fit well by a log-normal probability density function.
    
            >>> # Generate a thousand samples: each is the product of 100 random
            >>> # values, drawn from a normal distribution.
            >>> b = []
            >>> for i in range(1000):
            ...    a = 10. + np.random.random(100)
            ...    b.append(np.product(a))
    
            >>> b = np.array(b) / np.min(b) # scale values to be positive
            >>> count, bins, ignored = plt.hist(b, 100, normed=True, align='center')
            >>> sigma = np.std(np.log(b))
            >>> mu = np.mean(np.log(b))
    
            >>> x = np.linspace(min(bins), max(bins), 10000)
            >>> pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
            ...        / (x * sigma * np.sqrt(2 * np.pi)))
    
            >>> plt.plot(x, pdf, color='r', linewidth=2)
            >>> plt.show()
    """
    pass

def logseries(p, size=None): # real signature unknown; restored from __doc__
    """
    logseries(p, size=None)
    
            Draw samples from a Logarithmic Series distribution.
    
            Samples are drawn from a Log Series distribution with specified
            parameter, p (probability, 0 < p < 1).
    
            Parameters
            ----------
            loc : float
    
            scale : float > 0.
    
            size : {tuple, int}
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : {ndarray, scalar}
                      where the values are all integers in  [0, n].
    
            See Also
            --------
            scipy.stats.distributions.logser : probability density function,
                distribution or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the Log Series distribution is
    
            .. math:: P(k) = \frac{-p^k}{k \ln(1-p)},
    
            where p = probability.
    
            The Log Series distribution is frequently used to represent species
            richness and occurrence, first proposed by Fisher, Corbet, and
            Williams in 1943 [2].  It may also be used to model the numbers of
            occupants seen in cars [3].
    
            References
            ----------
            .. [1] Buzas, Martin A.; Culver, Stephen J.,  Understanding regional
                   species diversity through the log series distribution of
                   occurrences: BIODIVERSITY RESEARCH Diversity & Distributions,
                   Volume 5, Number 5, September 1999 , pp. 187-195(9).
            .. [2] Fisher, R.A,, A.S. Corbet, and C.B. Williams. 1943. The
                   relation between the number of species and the number of
                   individuals in a random sample of an animal population.
                   Journal of Animal Ecology, 12:42-58.
            .. [3] D. J. Hand, F. Daly, D. Lunn, E. Ostrowski, A Handbook of Small
                   Data Sets, CRC Press, 1994.
            .. [4] Wikipedia, "Logarithmic-distribution",
                   http://en.wikipedia.org/wiki/Logarithmic-distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> a = .6
            >>> s = np.random.logseries(a, 10000)
            >>> count, bins, ignored = plt.hist(s)
    
            #   plot against distribution
    
            >>> def logseries(k, p):
            ...     return -p**k/(k*log(1-p))
            >>> plt.plot(bins, logseries(bins, a)*count.max()/
                         logseries(bins, a).max(), 'r')
            >>> plt.show()
    """
    pass

def multinomial(n, pvals, size=None): # real signature unknown; restored from __doc__
    """
    multinomial(n, pvals, size=None)
    
            Draw samples from a multinomial distribution.
    
            The multinomial distribution is a multivariate generalisation of the
            binomial distribution.  Take an experiment with one of ``p``
            possible outcomes.  An example of such an experiment is throwing a dice,
            where the outcome can be 1 through 6.  Each sample drawn from the
            distribution represents `n` such experiments.  Its values,
            ``X_i = [X_0, X_1, ..., X_p]``, represent the number of times the outcome
            was ``i``.
    
            Parameters
            ----------
            n : int
                Number of experiments.
            pvals : sequence of floats, length p
                Probabilities of each of the ``p`` different outcomes.  These
                should sum to 1 (however, the last element is always assumed to
                account for the remaining probability, as long as
                ``sum(pvals[:-1]) <= 1)``.
            size : tuple of ints
                Given a `size` of ``(M, N, K)``, then ``M*N*K`` samples are drawn,
                and the output shape becomes ``(M, N, K, p)``, since each sample
                has shape ``(p,)``.
    
            Examples
            --------
            Throw a dice 20 times:
    
            >>> np.random.multinomial(20, [1/6.]*6, size=1)
            array([[4, 1, 7, 5, 2, 1]])
    
            It landed 4 times on 1, once on 2, etc.
    
            Now, throw the dice 20 times, and 20 times again:
    
            >>> np.random.multinomial(20, [1/6.]*6, size=2)
            array([[3, 4, 3, 3, 4, 3],
                   [2, 4, 3, 4, 0, 7]])
    
            For the first run, we threw 3 times 1, 4 times 2, etc.  For the second,
            we threw 2 times 1, 4 times 2, etc.
    
            A loaded dice is more likely to land on number 6:
    
            >>> np.random.multinomial(100, [1/7.]*5)
            array([13, 16, 13, 16, 42])
    """
    pass

def multivariate_normal(mean, cov, size=None): # real signature unknown; restored from __doc__
    """
    multivariate_normal(mean, cov[, size])
    
            Draw random samples from a multivariate normal distribution.
    
            The multivariate normal, multinormal or Gaussian distribution is a
            generalization of the one-dimensional normal distribution to higher
            dimensions.  Such a distribution is specified by its mean and
            covariance matrix.  These parameters are analogous to the mean
            (average or "center") and variance (standard deviation, or "width,"
            squared) of the one-dimensional normal distribution.
    
            Parameters
            ----------
            mean : 1-D array_like, of length N
                Mean of the N-dimensional distribution.
            cov : 2-D array_like, of shape (N, N)
                Covariance matrix of the distribution.  Must be symmetric and
                positive semi-definite for "physically meaningful" results.
            size : int or tuple of ints, optional
                Given a shape of, for example, ``(m,n,k)``, ``m*n*k`` samples are
                generated, and packed in an `m`-by-`n`-by-`k` arrangement.  Because
                each sample is `N`-dimensional, the output shape is ``(m,n,k,N)``.
                If no shape is specified, a single (`N`-D) sample is returned.
    
            Returns
            -------
            out : ndarray
                The drawn samples, of shape *size*, if that was provided.  If not,
                the shape is ``(N,)``.
    
                In other words, each entry ``out[i,j,...,:]`` is an N-dimensional
                value drawn from the distribution.
    
            Notes
            -----
            The mean is a coordinate in N-dimensional space, which represents the
            location where samples are most likely to be generated.  This is
            analogous to the peak of the bell curve for the one-dimensional or
            univariate normal distribution.
    
            Covariance indicates the level to which two variables vary together.
            From the multivariate normal distribution, we draw N-dimensional
            samples, :math:`X = [x_1, x_2, ... x_N]`.  The covariance matrix
            element :math:`C_{ij}` is the covariance of :math:`x_i` and :math:`x_j`.
            The element :math:`C_{ii}` is the variance of :math:`x_i` (i.e. its
            "spread").
    
            Instead of specifying the full covariance matrix, popular
            approximations include:
    
              - Spherical covariance (*cov* is a multiple of the identity matrix)
              - Diagonal covariance (*cov* has non-negative elements, and only on
                the diagonal)
    
            This geometrical property can be seen in two dimensions by plotting
            generated data-points:
    
            >>> mean = [0,0]
            >>> cov = [[1,0],[0,100]] # diagonal covariance, points lie on x or y-axis
    
            >>> import matplotlib.pyplot as plt
            >>> x,y = np.random.multivariate_normal(mean,cov,5000).T
            >>> plt.plot(x,y,'x'); plt.axis('equal'); plt.show()
    
            Note that the covariance matrix must be non-negative definite.
    
            References
            ----------
            Papoulis, A., *Probability, Random Variables, and Stochastic Processes*,
            3rd ed., New York: McGraw-Hill, 1991.
    
            Duda, R. O., Hart, P. E., and Stork, D. G., *Pattern Classification*,
            2nd ed., New York: Wiley, 2001.
    
            Examples
            --------
            >>> mean = (1,2)
            >>> cov = [[1,0],[1,0]]
            >>> x = np.random.multivariate_normal(mean,cov,(3,3))
            >>> x.shape
            (3, 3, 2)
    
            The following is probably true, given that 0.6 is roughly twice the
            standard deviation:
    
            >>> print list( (x[0,0,:] - mean) < 0.6 )
            [True, True]
    """
    pass

def negative_binomial(n, p, size=None): # real signature unknown; restored from __doc__
    """
    negative_binomial(n, p, size=None)
    
            Draw samples from a negative_binomial distribution.
    
            Samples are drawn from a negative_Binomial distribution with specified
            parameters, `n` trials and `p` probability of success where `n` is an
            integer > 0 and `p` is in the interval [0, 1].
    
            Parameters
            ----------
            n : int
                Parameter, > 0.
            p : float
                Parameter, >= 0 and <=1.
            size : int or tuple of ints
                Output shape. If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : int or ndarray of ints
                Drawn samples.
    
            Notes
            -----
            The probability density for the Negative Binomial distribution is
    
            .. math:: P(N;n,p) = \binom{N+n-1}{n-1}p^{n}(1-p)^{N},
    
            where :math:`n-1` is the number of successes, :math:`p` is the probability
            of success, and :math:`N+n-1` is the number of trials.
    
            The negative binomial distribution gives the probability of n-1 successes
            and N failures in N+n-1 trials, and success on the (N+n)th trial.
    
            If one throws a die repeatedly until the third time a "1" appears, then the
            probability distribution of the number of non-"1"s that appear before the
            third "1" is a negative binomial distribution.
    
            References
            ----------
            .. [1] Weisstein, Eric W. "Negative Binomial Distribution." From
                   MathWorld--A Wolfram Web Resource.
                   http://mathworld.wolfram.com/NegativeBinomialDistribution.html
            .. [2] Wikipedia, "Negative binomial distribution",
                   http://en.wikipedia.org/wiki/Negative_binomial_distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            A real world example. A company drills wild-cat oil exploration wells, each
            with an estimated probability of success of 0.1.  What is the probability
            of having one success for each successive well, that is what is the
            probability of a single success after drilling 5 wells, after 6 wells,
            etc.?
    
            >>> s = np.random.negative_binomial(1, 0.1, 100000)
            >>> for i in range(1, 11):
            ...    probability = sum(s<i) / 100000.
            ...    print i, "wells drilled, probability of one success =", probability
    """
    pass

def noncentral_chisquare(df, nonc, size=None): # real signature unknown; restored from __doc__
    """
    noncentral_chisquare(df, nonc, size=None)
    
            Draw samples from a noncentral chi-square distribution.
    
            The noncentral :math:`\chi^2` distribution is a generalisation of
            the :math:`\chi^2` distribution.
    
            Parameters
            ----------
            df : int
                Degrees of freedom, should be >= 1.
            nonc : float
                Non-centrality, should be > 0.
            size : int or tuple of ints
                Shape of the output.
    
            Notes
            -----
            The probability density function for the noncentral Chi-square distribution
            is
    
            .. math:: P(x;df,nonc) = \sum^{\infty}_{i=0}
                                   \frac{e^{-nonc/2}(nonc/2)^{i}}{i!}P_{Y_{df+2i}}(x),
    
            where :math:`Y_{q}` is the Chi-square with q degrees of freedom.
    
            In Delhi (2007), it is noted that the noncentral chi-square is useful in
            bombing and coverage problems, the probability of killing the point target
            given by the noncentral chi-squared distribution.
    
            References
            ----------
            .. [1] Delhi, M.S. Holla, "On a noncentral chi-square distribution in the
                   analysis of weapon systems effectiveness", Metrika, Volume 15,
                   Number 1 / December, 1970.
            .. [2] Wikipedia, "Noncentral chi-square distribution"
                   http://en.wikipedia.org/wiki/Noncentral_chi-square_distribution
    
            Examples
            --------
            Draw values from the distribution and plot the histogram
    
            >>> import matplotlib.pyplot as plt
            >>> values = plt.hist(np.random.noncentral_chisquare(3, 20, 100000),
            ...                   bins=200, normed=True)
            >>> plt.show()
    
            Draw values from a noncentral chisquare with very small noncentrality,
            and compare to a chisquare.
    
            >>> plt.figure()
            >>> values = plt.hist(np.random.noncentral_chisquare(3, .0000001, 100000),
            ...                   bins=np.arange(0., 25, .1), normed=True)
            >>> values2 = plt.hist(np.random.chisquare(3, 100000),
            ...                    bins=np.arange(0., 25, .1), normed=True)
            >>> plt.plot(values[1][0:-1], values[0]-values2[0], 'ob')
            >>> plt.show()
    
            Demonstrate how large values of non-centrality lead to a more symmetric
            distribution.
    
            >>> plt.figure()
            >>> values = plt.hist(np.random.noncentral_chisquare(3, 20, 100000),
            ...                   bins=200, normed=True)
            >>> plt.show()
    """
    pass

def noncentral_f(dfnum, dfden, nonc, size=None): # real signature unknown; restored from __doc__
    """
    noncentral_f(dfnum, dfden, nonc, size=None)
    
            Draw samples from the noncentral F distribution.
    
            Samples are drawn from an F distribution with specified parameters,
            `dfnum` (degrees of freedom in numerator) and `dfden` (degrees of
            freedom in denominator), where both parameters > 1.
            `nonc` is the non-centrality parameter.
    
            Parameters
            ----------
            dfnum : int
                Parameter, should be > 1.
            dfden : int
                Parameter, should be > 1.
            nonc : float
                Parameter, should be >= 0.
            size : int or tuple of ints
                Output shape. If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : scalar or ndarray
                Drawn samples.
    
            Notes
            -----
            When calculating the power of an experiment (power = probability of
            rejecting the null hypothesis when a specific alternative is true) the
            non-central F statistic becomes important.  When the null hypothesis is
            true, the F statistic follows a central F distribution. When the null
            hypothesis is not true, then it follows a non-central F statistic.
    
            References
            ----------
            Weisstein, Eric W. "Noncentral F-Distribution." From MathWorld--A Wolfram
            Web Resource.  http://mathworld.wolfram.com/NoncentralF-Distribution.html
    
            Wikipedia, "Noncentral F distribution",
            http://en.wikipedia.org/wiki/Noncentral_F-distribution
    
            Examples
            --------
            In a study, testing for a specific alternative to the null hypothesis
            requires use of the Noncentral F distribution. We need to calculate the
            area in the tail of the distribution that exceeds the value of the F
            distribution for the null hypothesis.  We'll plot the two probability
            distributions for comparison.
    
            >>> dfnum = 3 # between group deg of freedom
            >>> dfden = 20 # within groups degrees of freedom
            >>> nonc = 3.0
            >>> nc_vals = np.random.noncentral_f(dfnum, dfden, nonc, 1000000)
            >>> NF = np.histogram(nc_vals, bins=50, normed=True)
            >>> c_vals = np.random.f(dfnum, dfden, 1000000)
            >>> F = np.histogram(c_vals, bins=50, normed=True)
            >>> plt.plot(F[1][1:], F[0])
            >>> plt.plot(NF[1][1:], NF[0])
            >>> plt.show()
    """
    pass

def normal(loc=0.0, scale=1.0, size=None): # real signature unknown; restored from __doc__
    """
    normal(loc=0.0, scale=1.0, size=None)
    
            Draw random samples from a normal (Gaussian) distribution.
    
            The probability density function of the normal distribution, first
            derived by De Moivre and 200 years later by both Gauss and Laplace
            independently [2]_, is often called the bell curve because of
            its characteristic shape (see the example below).
    
            The normal distributions occurs often in nature.  For example, it
            describes the commonly occurring distribution of samples influenced
            by a large number of tiny, random disturbances, each with its own
            unique distribution [2]_.
    
            Parameters
            ----------
            loc : float
                Mean ("centre") of the distribution.
            scale : float
                Standard deviation (spread or "width") of the distribution.
            size : tuple of ints
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            See Also
            --------
            scipy.stats.distributions.norm : probability density function,
                distribution or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the Gaussian distribution is
    
            .. math:: p(x) = \frac{1}{\sqrt{ 2 \pi \sigma^2 }}
                             e^{ - \frac{ (x - \mu)^2 } {2 \sigma^2} },
    
            where :math:`\mu` is the mean and :math:`\sigma` the standard deviation.
            The square of the standard deviation, :math:`\sigma^2`, is called the
            variance.
    
            The function has its peak at the mean, and its "spread" increases with
            the standard deviation (the function reaches 0.607 times its maximum at
            :math:`x + \sigma` and :math:`x - \sigma` [2]_).  This implies that
            `numpy.random.normal` is more likely to return samples lying close to the
            mean, rather than those far away.
    
            References
            ----------
            .. [1] Wikipedia, "Normal distribution",
                   http://en.wikipedia.org/wiki/Normal_distribution
            .. [2] P. R. Peebles Jr., "Central Limit Theorem" in "Probability, Random
                   Variables and Random Signal Principles", 4th ed., 2001,
                   pp. 51, 51, 125.
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> mu, sigma = 0, 0.1 # mean and standard deviation
            >>> s = np.random.normal(mu, sigma, 1000)
    
            Verify the mean and the variance:
    
            >>> abs(mu - np.mean(s)) < 0.01
            True
    
            >>> abs(sigma - np.std(s, ddof=1)) < 0.01
            True
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> count, bins, ignored = plt.hist(s, 30, normed=True)
            >>> plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
            ...                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
            ...          linewidth=2, color='r')
            >>> plt.show()
    """
    pass

def pareto(a, size=None): # real signature unknown; restored from __doc__
    """
    pareto(a, size=None)
    
            Draw samples from a Pareto II or Lomax distribution with specified shape.
    
            The Lomax or Pareto II distribution is a shifted Pareto distribution. The
            classical Pareto distribution can be obtained from the Lomax distribution
            by adding the location parameter m, see below. The smallest value of the
            Lomax distribution is zero while for the classical Pareto distribution it
            is m, where the standard Pareto distribution has location m=1.
            Lomax can also be considered as a simplified version of the Generalized
            Pareto distribution (available in SciPy), with the scale set to one and
            the location set to zero.
    
            The Pareto distribution must be greater than zero, and is unbounded above.
            It is also known as the "80-20 rule".  In this distribution, 80 percent of
            the weights are in the lowest 20 percent of the range, while the other 20
            percent fill the remaining 80 percent of the range.
    
            Parameters
            ----------
            shape : float, > 0.
                Shape of the distribution.
            size : tuple of ints
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            See Also
            --------
            scipy.stats.distributions.lomax.pdf : probability density function,
                distribution or cumulative density function, etc.
            scipy.stats.distributions.genpareto.pdf : probability density function,
                distribution or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the Pareto distribution is
    
            .. math:: p(x) = \frac{am^a}{x^{a+1}}
    
            where :math:`a` is the shape and :math:`m` the location
    
            The Pareto distribution, named after the Italian economist Vilfredo Pareto,
            is a power law probability distribution useful in many real world problems.
            Outside the field of economics it is generally referred to as the Bradford
            distribution. Pareto developed the distribution to describe the
            distribution of wealth in an economy.  It has also found use in insurance,
            web page access statistics, oil field sizes, and many other problems,
            including the download frequency for projects in Sourceforge [1].  It is
            one of the so-called "fat-tailed" distributions.
    
    
            References
            ----------
            .. [1] Francis Hunt and Paul Johnson, On the Pareto Distribution of
                   Sourceforge projects.
            .. [2] Pareto, V. (1896). Course of Political Economy. Lausanne.
            .. [3] Reiss, R.D., Thomas, M.(2001), Statistical Analysis of Extreme
                   Values, Birkhauser Verlag, Basel, pp 23-30.
            .. [4] Wikipedia, "Pareto distribution",
                   http://en.wikipedia.org/wiki/Pareto_distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> a, m = 3., 1. # shape and mode
            >>> s = np.random.pareto(a, 1000) + m
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> count, bins, ignored = plt.hist(s, 100, normed=True, align='center')
            >>> fit = a*m**a/bins**(a+1)
            >>> plt.plot(bins, max(count)*fit/max(fit),linewidth=2, color='r')
            >>> plt.show()
    """
    pass

def permutation(x): # real signature unknown; restored from __doc__
    """
    permutation(x)
    
            Randomly permute a sequence, or return a permuted range.
    
            If `x` is a multi-dimensional array, it is only shuffled along its
            first index.
    
            Parameters
            ----------
            x : int or array_like
                If `x` is an integer, randomly permute ``np.arange(x)``.
                If `x` is an array, make a copy and shuffle the elements
                randomly.
    
            Returns
            -------
            out : ndarray
                Permuted sequence or array range.
    
            Examples
            --------
            >>> np.random.permutation(10)
            array([1, 7, 4, 3, 0, 9, 2, 5, 8, 6])
    
            >>> np.random.permutation([1, 4, 9, 12, 15])
            array([15,  1,  9,  4, 12])
    
            >>> arr = np.arange(9).reshape((3, 3))
            >>> np.random.permutation(arr)
            array([[6, 7, 8],
                   [0, 1, 2],
                   [3, 4, 5]])
    """
    pass

def poisson(lam=1.0, size=None): # real signature unknown; restored from __doc__
    """
    poisson(lam=1.0, size=None)
    
            Draw samples from a Poisson distribution.
    
            The Poisson distribution is the limit of the Binomial
            distribution for large N.
    
            Parameters
            ----------
            lam : float
                Expectation of interval, should be >= 0.
            size : int or tuple of ints, optional
                Output shape. If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Notes
            -----
            The Poisson distribution
    
            .. math:: f(k; \lambda)=\frac{\lambda^k e^{-\lambda}}{k!}
    
            For events with an expected separation :math:`\lambda` the Poisson
            distribution :math:`f(k; \lambda)` describes the probability of
            :math:`k` events occurring within the observed interval :math:`\lambda`.
    
            Because the output is limited to the range of the C long type, a
            ValueError is raised when `lam` is within 10 sigma of the maximum
            representable value.
    
            References
            ----------
            .. [1] Weisstein, Eric W. "Poisson Distribution." From MathWorld--A Wolfram
                   Web Resource. http://mathworld.wolfram.com/PoissonDistribution.html
            .. [2] Wikipedia, "Poisson distribution",
               http://en.wikipedia.org/wiki/Poisson_distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> import numpy as np
            >>> s = np.random.poisson(5, 10000)
    
            Display histogram of the sample:
    
            >>> import matplotlib.pyplot as plt
            >>> count, bins, ignored = plt.hist(s, 14, normed=True)
            >>> plt.show()
    """
    pass

def power(a, size=None): # real signature unknown; restored from __doc__
    """
    power(a, size=None)
    
            Draws samples in [0, 1] from a power distribution with positive
            exponent a - 1.
    
            Also known as the power function distribution.
    
            Parameters
            ----------
            a : float
                parameter, > 0
            size : tuple of ints
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                        ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : {ndarray, scalar}
                The returned samples lie in [0, 1].
    
            Raises
            ------
            ValueError
                If a<1.
    
            Notes
            -----
            The probability density function is
    
            .. math:: P(x; a) = ax^{a-1}, 0 \le x \le 1, a>0.
    
            The power function distribution is just the inverse of the Pareto
            distribution. It may also be seen as a special case of the Beta
            distribution.
    
            It is used, for example, in modeling the over-reporting of insurance
            claims.
    
            References
            ----------
            .. [1] Christian Kleiber, Samuel Kotz, "Statistical size distributions
                   in economics and actuarial sciences", Wiley, 2003.
            .. [2] Heckert, N. A. and Filliben, James J. (2003). NIST Handbook 148:
                   Dataplot Reference Manual, Volume 2: Let Subcommands and Library
                   Functions", National Institute of Standards and Technology Handbook
                   Series, June 2003.
                   http://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/powpdf.pdf
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> a = 5. # shape
            >>> samples = 1000
            >>> s = np.random.power(a, samples)
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> count, bins, ignored = plt.hist(s, bins=30)
            >>> x = np.linspace(0, 1, 100)
            >>> y = a*x**(a-1.)
            >>> normed_y = samples*np.diff(bins)[0]*y
            >>> plt.plot(x, normed_y)
            >>> plt.show()
    
            Compare the power function distribution to the inverse of the Pareto.
    
            >>> from scipy import stats
            >>> rvs = np.random.power(5, 1000000)
            >>> rvsp = np.random.pareto(5, 1000000)
            >>> xx = np.linspace(0,1,100)
            >>> powpdf = stats.powerlaw.pdf(xx,5)
    
            >>> plt.figure()
            >>> plt.hist(rvs, bins=50, normed=True)
            >>> plt.plot(xx,powpdf,'r-')
            >>> plt.title('np.random.power(5)')
    
            >>> plt.figure()
            >>> plt.hist(1./(1.+rvsp), bins=50, normed=True)
            >>> plt.plot(xx,powpdf,'r-')
            >>> plt.title('inverse of 1 + np.random.pareto(5)')
    
            >>> plt.figure()
            >>> plt.hist(1./(1.+rvsp), bins=50, normed=True)
            >>> plt.plot(xx,powpdf,'r-')
            >>> plt.title('inverse of stats.pareto(5)')
    """
    pass

def rand(d0, d1, *more, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__ 
    """
    rand(d0, d1, ..., dn)
    
            Random values in a given shape.
    
            Create an array of the given shape and propagate it with
            random samples from a uniform distribution
            over ``[0, 1)``.
    
            Parameters
            ----------
            d0, d1, ..., dn : int, optional
                The dimensions of the returned array, should all be positive.
                If no argument is given a single Python float is returned.
    
            Returns
            -------
            out : ndarray, shape ``(d0, d1, ..., dn)``
                Random values.
    
            See Also
            --------
            random
    
            Notes
            -----
            This is a convenience function. If you want an interface that
            takes a shape-tuple as the first argument, refer to
            np.random.random_sample .
    
            Examples
            --------
            >>> np.random.rand(3,2)
            array([[ 0.14022471,  0.96360618],  #random
                   [ 0.37601032,  0.25528411],  #random
                   [ 0.49313049,  0.94909878]]) #random
    """
    pass

def randint(low, high=None, size=None): # real signature unknown; restored from __doc__
    """
    randint(low, high=None, size=None)
    
            Return random integers from `low` (inclusive) to `high` (exclusive).
    
            Return random integers from the "discrete uniform" distribution in the
            "half-open" interval [`low`, `high`). If `high` is None (the default),
            then results are from [0, `low`).
    
            Parameters
            ----------
            low : int
                Lowest (signed) integer to be drawn from the distribution (unless
                ``high=None``, in which case this parameter is the *highest* such
                integer).
            high : int, optional
                If provided, one above the largest (signed) integer to be drawn
                from the distribution (see above for behavior if ``high=None``).
            size : int or tuple of ints, optional
                Output shape. Default is None, in which case a single int is
                returned.
    
            Returns
            -------
            out : int or ndarray of ints
                `size`-shaped array of random integers from the appropriate
                distribution, or a single such random int if `size` not provided.
    
            See Also
            --------
            random.random_integers : similar to `randint`, only for the closed
                interval [`low`, `high`], and 1 is the lowest value if `high` is
                omitted. In particular, this other one is the one to use to generate
                uniformly distributed discrete non-integers.
    
            Examples
            --------
            >>> np.random.randint(2, size=10)
            array([1, 0, 0, 0, 1, 1, 0, 0, 1, 0])
            >>> np.random.randint(1, size=10)
            array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
            Generate a 2 x 4 array of ints between 0 and 4, inclusive:
    
            >>> np.random.randint(5, size=(2, 4))
            array([[4, 0, 2, 1],
                   [3, 2, 2, 0]])
    """
    pass

def randn(d0, d1, *more, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__ 
    """
    randn(d0, d1, ..., dn)
    
            Return a sample (or samples) from the "standard normal" distribution.
    
            If positive, int_like or int-convertible arguments are provided,
            `randn` generates an array of shape ``(d0, d1, ..., dn)``, filled
            with random floats sampled from a univariate "normal" (Gaussian)
            distribution of mean 0 and variance 1 (if any of the :math:`d_i` are
            floats, they are first converted to integers by truncation). A single
            float randomly sampled from the distribution is returned if no
            argument is provided.
    
            This is a convenience function.  If you want an interface that takes a
            tuple as the first argument, use `numpy.random.standard_normal` instead.
    
            Parameters
            ----------
            d0, d1, ..., dn : int, optional
                The dimensions of the returned array, should be all positive.
                If no argument is given a single Python float is returned.
    
            Returns
            -------
            Z : ndarray or float
                A ``(d0, d1, ..., dn)``-shaped array of floating-point samples from
                the standard normal distribution, or a single such float if
                no parameters were supplied.
    
            See Also
            --------
            random.standard_normal : Similar, but takes a tuple as its argument.
    
            Notes
            -----
            For random samples from :math:`N(\mu, \sigma^2)`, use:
    
            ``sigma * np.random.randn(...) + mu``
    
            Examples
            --------
            >>> np.random.randn()
            2.1923875335537315 #random
    
            Two-by-four array of samples from N(3, 6.25):
    
            >>> 2.5 * np.random.randn(2, 4) + 3
            array([[-4.49401501,  4.00950034, -1.81814867,  7.29718677],  #random
                   [ 0.39924804,  4.68456316,  4.99394529,  4.84057254]]) #random
    """
    pass

def random_integers(low, high=None, size=None): # real signature unknown; restored from __doc__
    """
    random_integers(low, high=None, size=None)
    
            Return random integers between `low` and `high`, inclusive.
    
            Return random integers from the "discrete uniform" distribution in the
            closed interval [`low`, `high`].  If `high` is None (the default),
            then results are from [1, `low`].
    
            Parameters
            ----------
            low : int
                Lowest (signed) integer to be drawn from the distribution (unless
                ``high=None``, in which case this parameter is the *highest* such
                integer).
            high : int, optional
                If provided, the largest (signed) integer to be drawn from the
                distribution (see above for behavior if ``high=None``).
            size : int or tuple of ints, optional
                Output shape. Default is None, in which case a single int is returned.
    
            Returns
            -------
            out : int or ndarray of ints
                `size`-shaped array of random integers from the appropriate
                distribution, or a single such random int if `size` not provided.
    
            See Also
            --------
            random.randint : Similar to `random_integers`, only for the half-open
                interval [`low`, `high`), and 0 is the lowest value if `high` is
                omitted.
    
            Notes
            -----
            To sample from N evenly spaced floating-point numbers between a and b,
            use::
    
              a + (b - a) * (np.random.random_integers(N) - 1) / (N - 1.)
    
            Examples
            --------
            >>> np.random.random_integers(5)
            4
            >>> type(np.random.random_integers(5))
            <type 'int'>
            >>> np.random.random_integers(5, size=(3.,2.))
            array([[5, 4],
                   [3, 3],
                   [4, 5]])
    
            Choose five random numbers from the set of five evenly-spaced
            numbers between 0 and 2.5, inclusive (*i.e.*, from the set
            :math:`{0, 5/8, 10/8, 15/8, 20/8}`):
    
            >>> 2.5 * (np.random.random_integers(5, size=(5,)) - 1) / 4.
            array([ 0.625,  1.25 ,  0.625,  0.625,  2.5  ])
    
            Roll two six sided dice 1000 times and sum the results:
    
            >>> d1 = np.random.random_integers(1, 6, 1000)
            >>> d2 = np.random.random_integers(1, 6, 1000)
            >>> dsums = d1 + d2
    
            Display results as a histogram:
    
            >>> import matplotlib.pyplot as plt
            >>> count, bins, ignored = plt.hist(dsums, 11, normed=True)
            >>> plt.show()
    """
    pass

def random_sample(size=None): # real signature unknown; restored from __doc__
    """
    random_sample(size=None)
    
            Return random floats in the half-open interval [0.0, 1.0).
    
            Results are from the "continuous uniform" distribution over the
            stated interval.  To sample :math:`Unif[a, b), b > a` multiply
            the output of `random_sample` by `(b-a)` and add `a`::
    
              (b - a) * random_sample() + a
    
            Parameters
            ----------
            size : int or tuple of ints, optional
                Defines the shape of the returned array of random floats. If None
                (the default), returns a single float.
    
            Returns
            -------
            out : float or ndarray of floats
                Array of random floats of shape `size` (unless ``size=None``, in which
                case a single float is returned).
    
            Examples
            --------
            >>> np.random.random_sample()
            0.47108547995356098
            >>> type(np.random.random_sample())
            <type 'float'>
            >>> np.random.random_sample((5,))
            array([ 0.30220482,  0.86820401,  0.1654503 ,  0.11659149,  0.54323428])
    
            Three-by-two array of random numbers from [-5, 0):
    
            >>> 5 * np.random.random_sample((3, 2)) - 5
            array([[-3.99149989, -0.52338984],
                   [-2.99091858, -0.79479508],
                   [-1.23204345, -1.75224494]])
    """
    pass

def rayleigh(scale=1.0, size=None): # real signature unknown; restored from __doc__
    """
    rayleigh(scale=1.0, size=None)
    
            Draw samples from a Rayleigh distribution.
    
            The :math:`\chi` and Weibull distributions are generalizations of the
            Rayleigh.
    
            Parameters
            ----------
            scale : scalar
                Scale, also equals the mode. Should be >= 0.
            size : int or tuple of ints, optional
                Shape of the output. Default is None, in which case a single
                value is returned.
    
            Notes
            -----
            The probability density function for the Rayleigh distribution is
    
            .. math:: P(x;scale) = \frac{x}{scale^2}e^{\frac{-x^2}{2 \cdotp scale^2}}
    
            The Rayleigh distribution arises if the wind speed and wind direction are
            both gaussian variables, then the vector wind velocity forms a Rayleigh
            distribution. The Rayleigh distribution is used to model the expected
            output from wind turbines.
    
            References
            ----------
            .. [1] Brighton Webs Ltd., Rayleigh Distribution,
                  http://www.brighton-webs.co.uk/distributions/rayleigh.asp
            .. [2] Wikipedia, "Rayleigh distribution"
                  http://en.wikipedia.org/wiki/Rayleigh_distribution
    
            Examples
            --------
            Draw values from the distribution and plot the histogram
    
            >>> values = hist(np.random.rayleigh(3, 100000), bins=200, normed=True)
    
            Wave heights tend to follow a Rayleigh distribution. If the mean wave
            height is 1 meter, what fraction of waves are likely to be larger than 3
            meters?
    
            >>> meanvalue = 1
            >>> modevalue = np.sqrt(2 / np.pi) * meanvalue
            >>> s = np.random.rayleigh(modevalue, 1000000)
    
            The percentage of waves larger than 3 meters is:
    
            >>> 100.*sum(s>3)/1000000.
            0.087300000000000003
    """
    pass

def seed(seed=None): # real signature unknown; restored from __doc__
    """
    seed(seed=None)
    
            Seed the generator.
    
            This method is called when `RandomState` is initialized. It can be
            called again to re-seed the generator. For details, see `RandomState`.
    
            Parameters
            ----------
            seed : int or array_like, optional
                Seed for `RandomState`.
    
            See Also
            --------
            RandomState
    """
    pass

def set_state(state): # real signature unknown; restored from __doc__
    """
    set_state(state)
    
            Set the internal state of the generator from a tuple.
    
            For use if one has reason to manually (re-)set the internal state of the
            "Mersenne Twister"[1]_ pseudo-random number generating algorithm.
    
            Parameters
            ----------
            state : tuple(str, ndarray of 624 uints, int, int, float)
                The `state` tuple has the following items:
    
                1. the string 'MT19937', specifying the Mersenne Twister algorithm.
                2. a 1-D array of 624 unsigned integers ``keys``.
                3. an integer ``pos``.
                4. an integer ``has_gauss``.
                5. a float ``cached_gaussian``.
    
            Returns
            -------
            out : None
                Returns 'None' on success.
    
            See Also
            --------
            get_state
    
            Notes
            -----
            `set_state` and `get_state` are not needed to work with any of the
            random distributions in NumPy. If the internal state is manually altered,
            the user should know exactly what he/she is doing.
    
            For backwards compatibility, the form (str, array of 624 uints, int) is
            also accepted although it is missing some information about the cached
            Gaussian value: ``state = ('MT19937', keys, pos)``.
    
            References
            ----------
            .. [1] M. Matsumoto and T. Nishimura, "Mersenne Twister: A
               623-dimensionally equidistributed uniform pseudorandom number
               generator," *ACM Trans. on Modeling and Computer Simulation*,
               Vol. 8, No. 1, pp. 3-30, Jan. 1998.
    """
    pass

def shuffle(x): # real signature unknown; restored from __doc__
    """
    shuffle(x)
    
            Modify a sequence in-place by shuffling its contents.
    
            Parameters
            ----------
            x : array_like
                The array or list to be shuffled.
    
            Returns
            -------
            None
    
            Examples
            --------
            >>> arr = np.arange(10)
            >>> np.random.shuffle(arr)
            >>> arr
            [1 7 5 2 9 4 3 6 0 8]
    
            This function only shuffles the array along the first index of a
            multi-dimensional array:
    
            >>> arr = np.arange(9).reshape((3, 3))
            >>> np.random.shuffle(arr)
            >>> arr
            array([[3, 4, 5],
                   [6, 7, 8],
                   [0, 1, 2]])
    """
    pass

def standard_cauchy(size=None): # real signature unknown; restored from __doc__
    """
    standard_cauchy(size=None)
    
            Standard Cauchy distribution with mode = 0.
    
            Also known as the Lorentz distribution.
    
            Parameters
            ----------
            size : int or tuple of ints
                Shape of the output.
    
            Returns
            -------
            samples : ndarray or scalar
                The drawn samples.
    
            Notes
            -----
            The probability density function for the full Cauchy distribution is
    
            .. math:: P(x; x_0, \gamma) = \frac{1}{\pi \gamma \bigl[ 1+
                      (\frac{x-x_0}{\gamma})^2 \bigr] }
    
            and the Standard Cauchy distribution just sets :math:`x_0=0` and
            :math:`\gamma=1`
    
            The Cauchy distribution arises in the solution to the driven harmonic
            oscillator problem, and also describes spectral line broadening. It
            also describes the distribution of values at which a line tilted at
            a random angle will cut the x axis.
    
            When studying hypothesis tests that assume normality, seeing how the
            tests perform on data from a Cauchy distribution is a good indicator of
            their sensitivity to a heavy-tailed distribution, since the Cauchy looks
            very much like a Gaussian distribution, but with heavier tails.
    
            References
            ----------
            .. [1] NIST/SEMATECH e-Handbook of Statistical Methods, "Cauchy
                  Distribution",
                  http://www.itl.nist.gov/div898/handbook/eda/section3/eda3663.htm
            .. [2] Weisstein, Eric W. "Cauchy Distribution." From MathWorld--A
                  Wolfram Web Resource.
                  http://mathworld.wolfram.com/CauchyDistribution.html
            .. [3] Wikipedia, "Cauchy distribution"
                  http://en.wikipedia.org/wiki/Cauchy_distribution
    
            Examples
            --------
            Draw samples and plot the distribution:
    
            >>> s = np.random.standard_cauchy(1000000)
            >>> s = s[(s>-25) & (s<25)]  # truncate distribution so it plots well
            >>> plt.hist(s, bins=100)
            >>> plt.show()
    """
    pass

def standard_exponential(size=None): # real signature unknown; restored from __doc__
    """
    standard_exponential(size=None)
    
            Draw samples from the standard exponential distribution.
    
            `standard_exponential` is identical to the exponential distribution
            with a scale parameter of 1.
    
            Parameters
            ----------
            size : int or tuple of ints
                Shape of the output.
    
            Returns
            -------
            out : float or ndarray
                Drawn samples.
    
            Examples
            --------
            Output a 3x8000 array:
    
            >>> n = np.random.standard_exponential((3, 8000))
    """
    pass

def standard_gamma(shape, size=None): # real signature unknown; restored from __doc__
    """
    standard_gamma(shape, size=None)
    
            Draw samples from a Standard Gamma distribution.
    
            Samples are drawn from a Gamma distribution with specified parameters,
            shape (sometimes designated "k") and scale=1.
    
            Parameters
            ----------
            shape : float
                Parameter, should be > 0.
            size : int or tuple of ints
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : ndarray or scalar
                The drawn samples.
    
            See Also
            --------
            scipy.stats.distributions.gamma : probability density function,
                distribution or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the Gamma distribution is
    
            .. math:: p(x) = x^{k-1}\frac{e^{-x/\theta}}{\theta^k\Gamma(k)},
    
            where :math:`k` is the shape and :math:`\theta` the scale,
            and :math:`\Gamma` is the Gamma function.
    
            The Gamma distribution is often used to model the times to failure of
            electronic components, and arises naturally in processes for which the
            waiting times between Poisson distributed events are relevant.
    
            References
            ----------
            .. [1] Weisstein, Eric W. "Gamma Distribution." From MathWorld--A
                   Wolfram Web Resource.
                   http://mathworld.wolfram.com/GammaDistribution.html
            .. [2] Wikipedia, "Gamma-distribution",
                   http://en.wikipedia.org/wiki/Gamma-distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> shape, scale = 2., 1. # mean and width
            >>> s = np.random.standard_gamma(shape, 1000000)
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> import scipy.special as sps
            >>> count, bins, ignored = plt.hist(s, 50, normed=True)
            >>> y = bins**(shape-1) * ((np.exp(-bins/scale))/ \
            ...                       (sps.gamma(shape) * scale**shape))
            >>> plt.plot(bins, y, linewidth=2, color='r')
            >>> plt.show()
    """
    pass

def standard_normal(size=None): # real signature unknown; restored from __doc__
    """
    standard_normal(size=None)
    
            Returns samples from a Standard Normal distribution (mean=0, stdev=1).
    
            Parameters
            ----------
            size : int or tuple of ints, optional
                Output shape. Default is None, in which case a single value is
                returned.
    
            Returns
            -------
            out : float or ndarray
                Drawn samples.
    
            Examples
            --------
            >>> s = np.random.standard_normal(8000)
            >>> s
            array([ 0.6888893 ,  0.78096262, -0.89086505, ...,  0.49876311, #random
                   -0.38672696, -0.4685006 ])                               #random
            >>> s.shape
            (8000,)
            >>> s = np.random.standard_normal(size=(3, 4, 2))
            >>> s.shape
            (3, 4, 2)
    """
    pass

def standard_t(df, size=None): # real signature unknown; restored from __doc__
    """
    standard_t(df, size=None)
    
            Standard Student's t distribution with df degrees of freedom.
    
            A special case of the hyperbolic distribution.
            As `df` gets large, the result resembles that of the standard normal
            distribution (`standard_normal`).
    
            Parameters
            ----------
            df : int
                Degrees of freedom, should be > 0.
            size : int or tuple of ints, optional
                Output shape. Default is None, in which case a single value is
                returned.
    
            Returns
            -------
            samples : ndarray or scalar
                Drawn samples.
    
            Notes
            -----
            The probability density function for the t distribution is
    
            .. math:: P(x, df) = \frac{\Gamma(\frac{df+1}{2})}{\sqrt{\pi df}
                      \Gamma(\frac{df}{2})}\Bigl( 1+\frac{x^2}{df} \Bigr)^{-(df+1)/2}
    
            The t test is based on an assumption that the data come from a Normal
            distribution. The t test provides a way to test whether the sample mean
            (that is the mean calculated from the data) is a good estimate of the true
            mean.
    
            The derivation of the t-distribution was forst published in 1908 by William
            Gisset while working for the Guinness Brewery in Dublin. Due to proprietary
            issues, he had to publish under a pseudonym, and so he used the name
            Student.
    
            References
            ----------
            .. [1] Dalgaard, Peter, "Introductory Statistics With R",
                   Springer, 2002.
            .. [2] Wikipedia, "Student's t-distribution"
                   http://en.wikipedia.org/wiki/Student's_t-distribution
    
            Examples
            --------
            From Dalgaard page 83 [1]_, suppose the daily energy intake for 11
            women in Kj is:
    
            >>> intake = np.array([5260., 5470, 5640, 6180, 6390, 6515, 6805, 7515, \
            ...                    7515, 8230, 8770])
    
            Does their energy intake deviate systematically from the recommended
            value of 7725 kJ?
    
            We have 10 degrees of freedom, so is the sample mean within 95% of the
            recommended value?
    
            >>> s = np.random.standard_t(10, size=100000)
            >>> np.mean(intake)
            6753.636363636364
            >>> intake.std(ddof=1)
            1142.1232221373727
    
            Calculate the t statistic, setting the ddof parameter to the unbiased
            value so the divisor in the standard deviation will be degrees of
            freedom, N-1.
    
            >>> t = (np.mean(intake)-7725)/(intake.std(ddof=1)/np.sqrt(len(intake)))
            >>> import matplotlib.pyplot as plt
            >>> h = plt.hist(s, bins=100, normed=True)
    
            For a one-sided t-test, how far out in the distribution does the t
            statistic appear?
    
            >>> >>> np.sum(s<t) / float(len(s))
            0.0090699999999999999  #random
    
            So the p-value is about 0.009, which says the null hypothesis has a
            probability of about 99% of being true.
    """
    pass

def triangular(left, mode, right, size=None): # real signature unknown; restored from __doc__
    """
    triangular(left, mode, right, size=None)
    
            Draw samples from the triangular distribution.
    
            The triangular distribution is a continuous probability distribution with
            lower limit left, peak at mode, and upper limit right. Unlike the other
            distributions, these parameters directly define the shape of the pdf.
    
            Parameters
            ----------
            left : scalar
                Lower limit.
            mode : scalar
                The value where the peak of the distribution occurs.
                The value should fulfill the condition ``left <= mode <= right``.
            right : scalar
                Upper limit, should be larger than `left`.
            size : int or tuple of ints, optional
                Output shape. Default is None, in which case a single value is
                returned.
    
            Returns
            -------
            samples : ndarray or scalar
                The returned samples all lie in the interval [left, right].
    
            Notes
            -----
            The probability density function for the Triangular distribution is
    
            .. math:: P(x;l, m, r) = \begin{cases}
                      \frac{2(x-l)}{(r-l)(m-l)}& \text{for $l \leq x \leq m$},\\
                      \frac{2(m-x)}{(r-l)(r-m)}& \text{for $m \leq x \leq r$},\\
                      0& \text{otherwise}.
                      \end{cases}
    
            The triangular distribution is often used in ill-defined problems where the
            underlying distribution is not known, but some knowledge of the limits and
            mode exists. Often it is used in simulations.
    
            References
            ----------
            .. [1] Wikipedia, "Triangular distribution"
                  http://en.wikipedia.org/wiki/Triangular_distribution
    
            Examples
            --------
            Draw values from the distribution and plot the histogram:
    
            >>> import matplotlib.pyplot as plt
            >>> h = plt.hist(np.random.triangular(-3, 0, 8, 100000), bins=200,
            ...              normed=True)
            >>> plt.show()
    """
    pass

def uniform(low=0.0, high=1.0, size=1): # real signature unknown; restored from __doc__
    """
    uniform(low=0.0, high=1.0, size=1)
    
            Draw samples from a uniform distribution.
    
            Samples are uniformly distributed over the half-open interval
            ``[low, high)`` (includes low, but excludes high).  In other words,
            any value within the given interval is equally likely to be drawn
            by `uniform`.
    
            Parameters
            ----------
            low : float, optional
                Lower boundary of the output interval.  All values generated will be
                greater than or equal to low.  The default value is 0.
            high : float
                Upper boundary of the output interval.  All values generated will be
                less than high.  The default value is 1.0.
            size : int or tuple of ints, optional
                Shape of output.  If the given size is, for example, (m,n,k),
                m*n*k samples are generated.  If no shape is specified, a single sample
                is returned.
    
            Returns
            -------
            out : ndarray
                Drawn samples, with shape `size`.
    
            See Also
            --------
            randint : Discrete uniform distribution, yielding integers.
            random_integers : Discrete uniform distribution over the closed
                              interval ``[low, high]``.
            random_sample : Floats uniformly distributed over ``[0, 1)``.
            random : Alias for `random_sample`.
            rand : Convenience function that accepts dimensions as input, e.g.,
                   ``rand(2,2)`` would generate a 2-by-2 array of floats,
                   uniformly distributed over ``[0, 1)``.
    
            Notes
            -----
            The probability density function of the uniform distribution is
    
            .. math:: p(x) = \frac{1}{b - a}
    
            anywhere within the interval ``[a, b)``, and zero elsewhere.
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> s = np.random.uniform(-1,0,1000)
    
            All values are within the given interval:
    
            >>> np.all(s >= -1)
            True
            >>> np.all(s < 0)
            True
    
            Display the histogram of the samples, along with the
            probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> count, bins, ignored = plt.hist(s, 15, normed=True)
            >>> plt.plot(bins, np.ones_like(bins), linewidth=2, color='r')
            >>> plt.show()
    """
    pass

def vonmises(mu, kappa, size=None): # real signature unknown; restored from __doc__
    """
    vonmises(mu, kappa, size=None)
    
            Draw samples from a von Mises distribution.
    
            Samples are drawn from a von Mises distribution with specified mode
            (mu) and dispersion (kappa), on the interval [-pi, pi].
    
            The von Mises distribution (also known as the circular normal
            distribution) is a continuous probability distribution on the unit
            circle.  It may be thought of as the circular analogue of the normal
            distribution.
    
            Parameters
            ----------
            mu : float
                Mode ("center") of the distribution.
            kappa : float
                Dispersion of the distribution, has to be >=0.
            size : int or tuple of int
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            Returns
            -------
            samples : scalar or ndarray
                The returned samples, which are in the interval [-pi, pi].
    
            See Also
            --------
            scipy.stats.distributions.vonmises : probability density function,
                distribution, or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the von Mises distribution is
    
            .. math:: p(x) = \frac{e^{\kappa cos(x-\mu)}}{2\pi I_0(\kappa)},
    
            where :math:`\mu` is the mode and :math:`\kappa` the dispersion,
            and :math:`I_0(\kappa)` is the modified Bessel function of order 0.
    
            The von Mises is named for Richard Edler von Mises, who was born in
            Austria-Hungary, in what is now the Ukraine.  He fled to the United
            States in 1939 and became a professor at Harvard.  He worked in
            probability theory, aerodynamics, fluid mechanics, and philosophy of
            science.
    
            References
            ----------
            Abramowitz, M. and Stegun, I. A. (ed.), *Handbook of Mathematical
            Functions*, New York: Dover, 1965.
    
            von Mises, R., *Mathematical Theory of Probability and Statistics*,
            New York: Academic Press, 1964.
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> mu, kappa = 0.0, 4.0 # mean and dispersion
            >>> s = np.random.vonmises(mu, kappa, 1000)
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> import scipy.special as sps
            >>> count, bins, ignored = plt.hist(s, 50, normed=True)
            >>> x = np.arange(-np.pi, np.pi, 2*np.pi/50.)
            >>> y = -np.exp(kappa*np.cos(x-mu))/(2*np.pi*sps.jn(0,kappa))
            >>> plt.plot(x, y/max(y), linewidth=2, color='r')
            >>> plt.show()
    """
    pass

def wald(mean, scale, size=None): # real signature unknown; restored from __doc__
    """
    wald(mean, scale, size=None)
    
            Draw samples from a Wald, or Inverse Gaussian, distribution.
    
            As the scale approaches infinity, the distribution becomes more like a
            Gaussian.
    
            Some references claim that the Wald is an Inverse Gaussian with mean=1, but
            this is by no means universal.
    
            The Inverse Gaussian distribution was first studied in relationship to
            Brownian motion. In 1956 M.C.K. Tweedie used the name Inverse Gaussian
            because there is an inverse relationship between the time to cover a unit
            distance and distance covered in unit time.
    
            Parameters
            ----------
            mean : scalar
                Distribution mean, should be > 0.
            scale : scalar
                Scale parameter, should be >= 0.
            size : int or tuple of ints, optional
                Output shape. Default is None, in which case a single value is
                returned.
    
            Returns
            -------
            samples : ndarray or scalar
                Drawn sample, all greater than zero.
    
            Notes
            -----
            The probability density function for the Wald distribution is
    
            .. math:: P(x;mean,scale) = \sqrt{\frac{scale}{2\pi x^3}}e^
                                        \frac{-scale(x-mean)^2}{2\cdotp mean^2x}
    
            As noted above the Inverse Gaussian distribution first arise from attempts
            to model Brownian Motion. It is also a competitor to the Weibull for use in
            reliability modeling and modeling stock returns and interest rate
            processes.
    
            References
            ----------
            .. [1] Brighton Webs Ltd., Wald Distribution,
                  http://www.brighton-webs.co.uk/distributions/wald.asp
            .. [2] Chhikara, Raj S., and Folks, J. Leroy, "The Inverse Gaussian
                  Distribution: Theory : Methodology, and Applications", CRC Press,
                  1988.
            .. [3] Wikipedia, "Wald distribution"
                  http://en.wikipedia.org/wiki/Wald_distribution
    
            Examples
            --------
            Draw values from the distribution and plot the histogram:
    
            >>> import matplotlib.pyplot as plt
            >>> h = plt.hist(np.random.wald(3, 2, 100000), bins=200, normed=True)
            >>> plt.show()
    """
    pass

def weibull(a, size=None): # real signature unknown; restored from __doc__
    """
    weibull(a, size=None)
    
            Weibull distribution.
    
            Draw samples from a 1-parameter Weibull distribution with the given
            shape parameter `a`.
    
            .. math:: X = (-ln(U))^{1/a}
    
            Here, U is drawn from the uniform distribution over (0,1].
    
            The more common 2-parameter Weibull, including a scale parameter
            :math:`\lambda` is just :math:`X = \lambda(-ln(U))^{1/a}`.
    
            Parameters
            ----------
            a : float
                Shape of the distribution.
            size : tuple of ints
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn.
    
            See Also
            --------
            scipy.stats.distributions.weibull_max
            scipy.stats.distributions.weibull_min
            scipy.stats.distributions.genextreme
            gumbel
    
            Notes
            -----
            The Weibull (or Type III asymptotic extreme value distribution for smallest
            values, SEV Type III, or Rosin-Rammler distribution) is one of a class of
            Generalized Extreme Value (GEV) distributions used in modeling extreme
            value problems.  This class includes the Gumbel and Frechet distributions.
    
            The probability density for the Weibull distribution is
    
            .. math:: p(x) = \frac{a}
                             {\lambda}(\frac{x}{\lambda})^{a-1}e^{-(x/\lambda)^a},
    
            where :math:`a` is the shape and :math:`\lambda` the scale.
    
            The function has its peak (the mode) at
            :math:`\lambda(\frac{a-1}{a})^{1/a}`.
    
            When ``a = 1``, the Weibull distribution reduces to the exponential
            distribution.
    
            References
            ----------
            .. [1] Waloddi Weibull, Professor, Royal Technical University, Stockholm,
                   1939 "A Statistical Theory Of The Strength Of Materials",
                   Ingeniorsvetenskapsakademiens Handlingar Nr 151, 1939,
                   Generalstabens Litografiska Anstalts Forlag, Stockholm.
            .. [2] Waloddi Weibull, 1951 "A Statistical Distribution Function of Wide
                   Applicability",  Journal Of Applied Mechanics ASME Paper.
            .. [3] Wikipedia, "Weibull distribution",
                   http://en.wikipedia.org/wiki/Weibull_distribution
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> a = 5. # shape
            >>> s = np.random.weibull(a, 1000)
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> x = np.arange(1,100.)/50.
            >>> def weib(x,n,a):
            ...     return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)
    
            >>> count, bins, ignored = plt.hist(np.random.weibull(5.,1000))
            >>> x = np.arange(1,100.)/50.
            >>> scale = count.max()/weib(x, 1., 5.).max()
            >>> plt.plot(x, weib(x, 1., 5.)*scale)
            >>> plt.show()
    """
    pass

def zipf(a, size=None): # real signature unknown; restored from __doc__
    """
    zipf(a, size=None)
    
            Draw samples from a Zipf distribution.
    
            Samples are drawn from a Zipf distribution with specified parameter
            `a` > 1.
    
            The Zipf distribution (also known as the zeta distribution) is a
            continuous probability distribution that satisfies Zipf's law: the
            frequency of an item is inversely proportional to its rank in a
            frequency table.
    
            Parameters
            ----------
            a : float > 1
                Distribution parameter.
            size : int or tuple of int, optional
                Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                ``m * n * k`` samples are drawn; a single integer is equivalent in
                its result to providing a mono-tuple, i.e., a 1-D array of length
                *size* is returned.  The default is None, in which case a single
                scalar is returned.
    
            Returns
            -------
            samples : scalar or ndarray
                The returned samples are greater than or equal to one.
    
            See Also
            --------
            scipy.stats.distributions.zipf : probability density function,
                distribution, or cumulative density function, etc.
    
            Notes
            -----
            The probability density for the Zipf distribution is
    
            .. math:: p(x) = \frac{x^{-a}}{\zeta(a)},
    
            where :math:`\zeta` is the Riemann Zeta function.
    
            It is named for the American linguist George Kingsley Zipf, who noted
            that the frequency of any word in a sample of a language is inversely
            proportional to its rank in the frequency table.
    
            References
            ----------
            Zipf, G. K., *Selected Studies of the Principle of Relative Frequency
            in Language*, Cambridge, MA: Harvard Univ. Press, 1932.
    
            Examples
            --------
            Draw samples from the distribution:
    
            >>> a = 2. # parameter
            >>> s = np.random.zipf(a, 1000)
    
            Display the histogram of the samples, along with
            the probability density function:
    
            >>> import matplotlib.pyplot as plt
            >>> import scipy.special as sps
            Truncate s values at 50 so plot is interesting
            >>> count, bins, ignored = plt.hist(s[s<50], 50, normed=True)
            >>> x = np.arange(1., 50.)
            >>> y = x**(-a)/sps.zetac(a)
            >>> plt.plot(x, y/max(y), linewidth=2, color='r')
            >>> plt.show()
    """
    pass

def _shape_from_size(*args, **kwargs): # real signature unknown
    pass

# classes

class RandomState(object):
    """
    RandomState(seed=None)
    
        Container for the Mersenne Twister pseudo-random number generator.
    
        `RandomState` exposes a number of methods for generating random numbers
        drawn from a variety of probability distributions. In addition to the
        distribution-specific arguments, each method takes a keyword argument
        `size` that defaults to ``None``. If `size` is ``None``, then a single
        value is generated and returned. If `size` is an integer, then a 1-D
        array filled with generated values is returned. If `size` is a tuple,
        then an array with that shape is filled and returned.
    
        Parameters
        ----------
        seed : {None, int, array_like}, optional
            Random seed initializing the pseudo-random number generator.
            Can be an integer, an array (or other sequence) of integers of
            any length, or ``None`` (the default).
            If `seed` is ``None``, then `RandomState` will try to read data from
            ``/dev/urandom`` (or the Windows analogue) if available or seed from
            the clock otherwise.
    
        Notes
        -----
        The Python stdlib module "random" also contains a Mersenne Twister
        pseudo-random number generator with a number of methods that are similar
        to the ones available in `RandomState`. `RandomState`, besides being
        NumPy-aware, has the advantage that it provides a much larger number
        of probability distributions to choose from.
    """
    def beta(self, a, b, size=None): # real signature unknown; restored from __doc__
        """
        beta(a, b, size=None)
        
                The Beta distribution over ``[0, 1]``.
        
                The Beta distribution is a special case of the Dirichlet distribution,
                and is related to the Gamma distribution.  It has the probability
                distribution function
        
                .. math:: f(x; a,b) = \frac{1}{B(\alpha, \beta)} x^{\alpha - 1}
                                                                 (1 - x)^{\beta - 1},
        
                where the normalisation, B, is the beta function,
        
                .. math:: B(\alpha, \beta) = \int_0^1 t^{\alpha - 1}
                                             (1 - t)^{\beta - 1} dt.
        
                It is often seen in Bayesian inference and order statistics.
        
                Parameters
                ----------
                a : float
                    Alpha, non-negative.
                b : float
                    Beta, non-negative.
                size : tuple of ints, optional
                    The number of samples to draw.  The output is packed according to
                    the size given.
        
                Returns
                -------
                out : ndarray
                    Array of the given shape, containing values drawn from a
                    Beta distribution.
        """
        pass

    def binomial(self, n, p, size=None): # real signature unknown; restored from __doc__
        """
        binomial(n, p, size=None)
        
                Draw samples from a binomial distribution.
        
                Samples are drawn from a Binomial distribution with specified
                parameters, n trials and p probability of success where
                n an integer >= 0 and p is in the interval [0,1]. (n may be
                input as a float, but it is truncated to an integer in use)
        
                Parameters
                ----------
                n : float (but truncated to an integer)
                        parameter, >= 0.
                p : float
                        parameter, >= 0 and <=1.
                size : {tuple, int}
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : {ndarray, scalar}
                          where the values are all integers in  [0, n].
        
                See Also
                --------
                scipy.stats.distributions.binom : probability density function,
                    distribution or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the Binomial distribution is
        
                .. math:: P(N) = \binom{n}{N}p^N(1-p)^{n-N},
        
                where :math:`n` is the number of trials, :math:`p` is the probability
                of success, and :math:`N` is the number of successes.
        
                When estimating the standard error of a proportion in a population by
                using a random sample, the normal distribution works well unless the
                product p*n <=5, where p = population proportion estimate, and n =
                number of samples, in which case the binomial distribution is used
                instead. For example, a sample of 15 people shows 4 who are left
                handed, and 11 who are right handed. Then p = 4/15 = 27%. 0.27*15 = 4,
                so the binomial distribution should be used in this case.
        
                References
                ----------
                .. [1] Dalgaard, Peter, "Introductory Statistics with R",
                       Springer-Verlag, 2002.
                .. [2] Glantz, Stanton A. "Primer of Biostatistics.", McGraw-Hill,
                       Fifth Edition, 2002.
                .. [3] Lentner, Marvin, "Elementary Applied Statistics", Bogden
                       and Quigley, 1972.
                .. [4] Weisstein, Eric W. "Binomial Distribution." From MathWorld--A
                       Wolfram Web Resource.
                       http://mathworld.wolfram.com/BinomialDistribution.html
                .. [5] Wikipedia, "Binomial-distribution",
                       http://en.wikipedia.org/wiki/Binomial_distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> n, p = 10, .5 # number of trials, probability of each trial
                >>> s = np.random.binomial(n, p, 1000)
                # result of flipping a coin 10 times, tested 1000 times.
        
                A real world example. A company drills 9 wild-cat oil exploration
                wells, each with an estimated probability of success of 0.1. All nine
                wells fail. What is the probability of that happening?
        
                Let's do 20,000 trials of the model, and count the number that
                generate zero positive results.
        
                >>> sum(np.random.binomial(9,0.1,20000)==0)/20000.
                answer = 0.38885, or 38%.
        """
        pass

    def bytes(self, length): # real signature unknown; restored from __doc__
        """
        bytes(length)
        
                Return random bytes.
        
                Parameters
                ----------
                length : int
                    Number of random bytes.
        
                Returns
                -------
                out : str
                    String of length `length`.
        
                Examples
                --------
                >>> np.random.bytes(10)
                ' eh\x85\x022SZ\xbf\xa4' #random
        """
        pass

    def chisquare(self, df, size=None): # real signature unknown; restored from __doc__
        """
        chisquare(df, size=None)
        
                Draw samples from a chi-square distribution.
        
                When `df` independent random variables, each with standard normal
                distributions (mean 0, variance 1), are squared and summed, the
                resulting distribution is chi-square (see Notes).  This distribution
                is often used in hypothesis testing.
        
                Parameters
                ----------
                df : int
                     Number of degrees of freedom.
                size : tuple of ints, int, optional
                     Size of the returned array.  By default, a scalar is
                     returned.
        
                Returns
                -------
                output : ndarray
                    Samples drawn from the distribution, packed in a `size`-shaped
                    array.
        
                Raises
                ------
                ValueError
                    When `df` <= 0 or when an inappropriate `size` (e.g. ``size=-1``)
                    is given.
        
                Notes
                -----
                The variable obtained by summing the squares of `df` independent,
                standard normally distributed random variables:
        
                .. math:: Q = \sum_{i=0}^{\mathtt{df}} X^2_i
        
                is chi-square distributed, denoted
        
                .. math:: Q \sim \chi^2_k.
        
                The probability density function of the chi-squared distribution is
        
                .. math:: p(x) = \frac{(1/2)^{k/2}}{\Gamma(k/2)}
                                 x^{k/2 - 1} e^{-x/2},
        
                where :math:`\Gamma` is the gamma function,
        
                .. math:: \Gamma(x) = \int_0^{-\infty} t^{x - 1} e^{-t} dt.
        
                References
                ----------
                `NIST/SEMATECH e-Handbook of Statistical Methods
                <http://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm>`_
        
                Examples
                --------
                >>> np.random.chisquare(2,4)
                array([ 1.89920014,  9.00867716,  3.13710533,  5.62318272])
        """
        pass

    def choice(self, a, size=None, replace=True, p=None): # real signature unknown; restored from __doc__
        """
        choice(a, size=None, replace=True, p=None)
        
                Generates a random sample from a given 1-D array
        
                        .. versionadded:: 1.7.0
        
                Parameters
                -----------
                a : 1-D array-like or int
                    If an ndarray, a random sample is generated from its elements.
                    If an int, the random sample is generated as if a was np.arange(n)
                size : int or tuple of ints, optional
                    Output shape. Default is None, in which case a single value is
                    returned.
                replace : boolean, optional
                    Whether the sample is with or without replacement
                p : 1-D array-like, optional
                    The probabilities associated with each entry in a.
                    If not given the sample assumes a uniform distribtion over all
                    entries in a.
        
                Returns
                --------
                samples : 1-D ndarray, shape (size,)
                    The generated random samples
        
                Raises
                -------
                ValueError
                    If a is an int and less than zero, if a or p are not 1-dimensional,
                    if a is an array-like of size 0, if p is not a vector of
                    probabilities, if a and p have different lengths, or if
                    replace=False and the sample size is greater than the population
                    size
        
                See Also
                ---------
                randint, shuffle, permutation
        
                Examples
                ---------
                Generate a uniform random sample from np.arange(5) of size 3:
        
                >>> np.random.choice(5, 3)
                array([0, 3, 4])
                >>> #This is equivalent to np.random.randint(0,5,3)
        
                Generate a non-uniform random sample from np.arange(5) of size 3:
        
                >>> np.random.choice(5, 3, p=[0.1, 0, 0.3, 0.6, 0])
                array([3, 3, 0])
        
                Generate a uniform random sample from np.arange(5) of size 3 without
                replacement:
        
                >>> np.random.choice(5, 3, replace=False)
                array([3,1,0])
                >>> #This is equivalent to np.random.shuffle(np.arange(5))[:3]
        
                Generate a non-uniform random sample from np.arange(5) of size
                3 without replacement:
        
                >>> np.random.choice(5, 3, replace=False, p=[0.1, 0, 0.3, 0.6, 0])
                array([2, 3, 0])
        
                Any of the above can be repeated with an arbitrary array-like
                instead of just integers. For instance:
        
                >>> aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']
                >>> np.random.choice(aa_milne_arr, 5, p=[0.5, 0.1, 0.1, 0.3])
                array(['pooh', 'pooh', 'pooh', 'Christopher', 'piglet'],
                      dtype='|S11')
        """
        pass

    def dirichlet(self, alpha, size=None): # real signature unknown; restored from __doc__
        """
        dirichlet(alpha, size=None)
        
                Draw samples from the Dirichlet distribution.
        
                Draw `size` samples of dimension k from a Dirichlet distribution. A
                Dirichlet-distributed random variable can be seen as a multivariate
                generalization of a Beta distribution. Dirichlet pdf is the conjugate
                prior of a multinomial in Bayesian inference.
        
                Parameters
                ----------
                alpha : array
                    Parameter of the distribution (k dimension for sample of
                    dimension k).
                size : array
                    Number of samples to draw.
        
                Returns
                -------
                samples : ndarray,
                    The drawn samples, of shape (alpha.ndim, size).
        
                Notes
                -----
                .. math:: X \approx \prod_{i=1}^{k}{x^{\alpha_i-1}_i}
        
                Uses the following property for computation: for each dimension,
                draw a random sample y_i from a standard gamma generator of shape
                `alpha_i`, then
                :math:`X = \frac{1}{\sum_{i=1}^k{y_i}} (y_1, \ldots, y_n)` is
                Dirichlet distributed.
        
                References
                ----------
                .. [1] David McKay, "Information Theory, Inference and Learning
                       Algorithms," chapter 23,
                       http://www.inference.phy.cam.ac.uk/mackay/
                .. [2] Wikipedia, "Dirichlet distribution",
                       http://en.wikipedia.org/wiki/Dirichlet_distribution
        
                Examples
                --------
                Taking an example cited in Wikipedia, this distribution can be used if
                one wanted to cut strings (each of initial length 1.0) into K pieces
                with different lengths, where each piece had, on average, a designated
                average length, but allowing some variation in the relative sizes of the
                pieces.
        
                >>> s = np.random.dirichlet((10, 5, 3), 20).transpose()
        
                >>> plt.barh(range(20), s[0])
                >>> plt.barh(range(20), s[1], left=s[0], color='g')
                >>> plt.barh(range(20), s[2], left=s[0]+s[1], color='r')
                >>> plt.title("Lengths of Strings")
        """
        pass

    def exponential(self, scale=1.0, size=None): # real signature unknown; restored from __doc__
        """
        exponential(scale=1.0, size=None)
        
                Exponential distribution.
        
                Its probability density function is
        
                .. math:: f(x; \frac{1}{\beta}) = \frac{1}{\beta} \exp(-\frac{x}{\beta}),
        
                for ``x > 0`` and 0 elsewhere. :math:`\beta` is the scale parameter,
                which is the inverse of the rate parameter :math:`\lambda = 1/\beta`.
                The rate parameter is an alternative, widely used parameterization
                of the exponential distribution [3]_.
        
                The exponential distribution is a continuous analogue of the
                geometric distribution.  It describes many common situations, such as
                the size of raindrops measured over many rainstorms [1]_, or the time
                between page requests to Wikipedia [2]_.
        
                Parameters
                ----------
                scale : float
                    The scale parameter, :math:`\beta = 1/\lambda`.
                size : tuple of ints
                    Number of samples to draw.  The output is shaped
                    according to `size`.
        
                References
                ----------
                .. [1] Peyton Z. Peebles Jr., "Probability, Random Variables and
                       Random Signal Principles", 4th ed, 2001, p. 57.
                .. [2] "Poisson Process", Wikipedia,
                       http://en.wikipedia.org/wiki/Poisson_process
                .. [3] "Exponential Distribution, Wikipedia,
                       http://en.wikipedia.org/wiki/Exponential_distribution
        """
        pass

    def f(self, dfnum, dfden, size=None): # real signature unknown; restored from __doc__
        """
        f(dfnum, dfden, size=None)
        
                Draw samples from a F distribution.
        
                Samples are drawn from an F distribution with specified parameters,
                `dfnum` (degrees of freedom in numerator) and `dfden` (degrees of freedom
                in denominator), where both parameters should be greater than zero.
        
                The random variate of the F distribution (also known as the
                Fisher distribution) is a continuous probability distribution
                that arises in ANOVA tests, and is the ratio of two chi-square
                variates.
        
                Parameters
                ----------
                dfnum : float
                    Degrees of freedom in numerator. Should be greater than zero.
                dfden : float
                    Degrees of freedom in denominator. Should be greater than zero.
                size : {tuple, int}, optional
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``,
                    then ``m * n * k`` samples are drawn. By default only one sample
                    is returned.
        
                Returns
                -------
                samples : {ndarray, scalar}
                    Samples from the Fisher distribution.
        
                See Also
                --------
                scipy.stats.distributions.f : probability density function,
                    distribution or cumulative density function, etc.
        
                Notes
                -----
                The F statistic is used to compare in-group variances to between-group
                variances. Calculating the distribution depends on the sampling, and
                so it is a function of the respective degrees of freedom in the
                problem.  The variable `dfnum` is the number of samples minus one, the
                between-groups degrees of freedom, while `dfden` is the within-groups
                degrees of freedom, the sum of the number of samples in each group
                minus the number of groups.
        
                References
                ----------
                .. [1] Glantz, Stanton A. "Primer of Biostatistics.", McGraw-Hill,
                       Fifth Edition, 2002.
                .. [2] Wikipedia, "F-distribution",
                       http://en.wikipedia.org/wiki/F-distribution
        
                Examples
                --------
                An example from Glantz[1], pp 47-40.
                Two groups, children of diabetics (25 people) and children from people
                without diabetes (25 controls). Fasting blood glucose was measured,
                case group had a mean value of 86.1, controls had a mean value of
                82.2. Standard deviations were 2.09 and 2.49 respectively. Are these
                data consistent with the null hypothesis that the parents diabetic
                status does not affect their children's blood glucose levels?
                Calculating the F statistic from the data gives a value of 36.01.
        
                Draw samples from the distribution:
        
                >>> dfnum = 1. # between group degrees of freedom
                >>> dfden = 48. # within groups degrees of freedom
                >>> s = np.random.f(dfnum, dfden, 1000)
        
                The lower bound for the top 1% of the samples is :
        
                >>> sort(s)[-10]
                7.61988120985
        
                So there is about a 1% chance that the F statistic will exceed 7.62,
                the measured value is 36, so the null hypothesis is rejected at the 1%
                level.
        """
        pass

    def gamma(self, shape, scale=1.0, size=None): # real signature unknown; restored from __doc__
        """
        gamma(shape, scale=1.0, size=None)
        
                Draw samples from a Gamma distribution.
        
                Samples are drawn from a Gamma distribution with specified parameters,
                `shape` (sometimes designated "k") and `scale` (sometimes designated
                "theta"), where both parameters are > 0.
        
                Parameters
                ----------
                shape : scalar > 0
                    The shape of the gamma distribution.
                scale : scalar > 0, optional
                    The scale of the gamma distribution.  Default is equal to 1.
                size : shape_tuple, optional
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                out : ndarray, float
                    Returns one sample unless `size` parameter is specified.
        
                See Also
                --------
                scipy.stats.distributions.gamma : probability density function,
                    distribution or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the Gamma distribution is
        
                .. math:: p(x) = x^{k-1}\frac{e^{-x/\theta}}{\theta^k\Gamma(k)},
        
                where :math:`k` is the shape and :math:`\theta` the scale,
                and :math:`\Gamma` is the Gamma function.
        
                The Gamma distribution is often used to model the times to failure of
                electronic components, and arises naturally in processes for which the
                waiting times between Poisson distributed events are relevant.
        
                References
                ----------
                .. [1] Weisstein, Eric W. "Gamma Distribution." From MathWorld--A
                       Wolfram Web Resource.
                       http://mathworld.wolfram.com/GammaDistribution.html
                .. [2] Wikipedia, "Gamma-distribution",
                       http://en.wikipedia.org/wiki/Gamma-distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> shape, scale = 2., 2. # mean and dispersion
                >>> s = np.random.gamma(shape, scale, 1000)
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> import scipy.special as sps
                >>> count, bins, ignored = plt.hist(s, 50, normed=True)
                >>> y = bins**(shape-1)*(np.exp(-bins/scale) /
                ...                      (sps.gamma(shape)*scale**shape))
                >>> plt.plot(bins, y, linewidth=2, color='r')
                >>> plt.show()
        """
        pass

    def geometric(self, p, size=None): # real signature unknown; restored from __doc__
        """
        geometric(p, size=None)
        
                Draw samples from the geometric distribution.
        
                Bernoulli trials are experiments with one of two outcomes:
                success or failure (an example of such an experiment is flipping
                a coin).  The geometric distribution models the number of trials
                that must be run in order to achieve success.  It is therefore
                supported on the positive integers, ``k = 1, 2, ...``.
        
                The probability mass function of the geometric distribution is
        
                .. math:: f(k) = (1 - p)^{k - 1} p
        
                where `p` is the probability of success of an individual trial.
        
                Parameters
                ----------
                p : float
                    The probability of success of an individual trial.
                size : tuple of ints
                    Number of values to draw from the distribution.  The output
                    is shaped according to `size`.
        
                Returns
                -------
                out : ndarray
                    Samples from the geometric distribution, shaped according to
                    `size`.
        
                Examples
                --------
                Draw ten thousand values from the geometric distribution,
                with the probability of an individual success equal to 0.35:
        
                >>> z = np.random.geometric(p=0.35, size=10000)
        
                How many trials succeeded after a single run?
        
                >>> (z == 1).sum() / 10000.
                0.34889999999999999 #random
        """
        pass

    def get_state(self): # real signature unknown; restored from __doc__
        """
        get_state()
        
                Return a tuple representing the internal state of the generator.
        
                For more details, see `set_state`.
        
                Returns
                -------
                out : tuple(str, ndarray of 624 uints, int, int, float)
                    The returned tuple has the following items:
        
                    1. the string 'MT19937'.
                    2. a 1-D array of 624 unsigned integer keys.
                    3. an integer ``pos``.
                    4. an integer ``has_gauss``.
                    5. a float ``cached_gaussian``.
        
                See Also
                --------
                set_state
        
                Notes
                -----
                `set_state` and `get_state` are not needed to work with any of the
                random distributions in NumPy. If the internal state is manually altered,
                the user should know exactly what he/she is doing.
        """
        pass

    def gumbel(self, loc=0.0, scale=1.0, size=None): # real signature unknown; restored from __doc__
        """
        gumbel(loc=0.0, scale=1.0, size=None)
        
                Gumbel distribution.
        
                Draw samples from a Gumbel distribution with specified location and scale.
                For more information on the Gumbel distribution, see Notes and References
                below.
        
                Parameters
                ----------
                loc : float
                    The location of the mode of the distribution.
                scale : float
                    The scale parameter of the distribution.
                size : tuple of ints
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                out : ndarray
                    The samples
        
                See Also
                --------
                scipy.stats.gumbel_l
                scipy.stats.gumbel_r
                scipy.stats.genextreme
                    probability density function, distribution, or cumulative density
                    function, etc. for each of the above
                weibull
        
                Notes
                -----
                The Gumbel (or Smallest Extreme Value (SEV) or the Smallest Extreme Value
                Type I) distribution is one of a class of Generalized Extreme Value (GEV)
                distributions used in modeling extreme value problems.  The Gumbel is a
                special case of the Extreme Value Type I distribution for maximums from
                distributions with "exponential-like" tails.
        
                The probability density for the Gumbel distribution is
        
                .. math:: p(x) = \frac{e^{-(x - \mu)/ \beta}}{\beta} e^{ -e^{-(x - \mu)/
                          \beta}},
        
                where :math:`\mu` is the mode, a location parameter, and :math:`\beta` is
                the scale parameter.
        
                The Gumbel (named for German mathematician Emil Julius Gumbel) was used
                very early in the hydrology literature, for modeling the occurrence of
                flood events. It is also used for modeling maximum wind speed and rainfall
                rates.  It is a "fat-tailed" distribution - the probability of an event in
                the tail of the distribution is larger than if one used a Gaussian, hence
                the surprisingly frequent occurrence of 100-year floods. Floods were
                initially modeled as a Gaussian process, which underestimated the frequency
                of extreme events.
        
        
                It is one of a class of extreme value distributions, the Generalized
                Extreme Value (GEV) distributions, which also includes the Weibull and
                Frechet.
        
                The function has a mean of :math:`\mu + 0.57721\beta` and a variance of
                :math:`\frac{\pi^2}{6}\beta^2`.
        
                References
                ----------
                Gumbel, E. J., *Statistics of Extremes*, New York: Columbia University
                Press, 1958.
        
                Reiss, R.-D. and Thomas, M., *Statistical Analysis of Extreme Values from
                Insurance, Finance, Hydrology and Other Fields*, Basel: Birkhauser Verlag,
                2001.
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> mu, beta = 0, 0.1 # location and scale
                >>> s = np.random.gumbel(mu, beta, 1000)
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> count, bins, ignored = plt.hist(s, 30, normed=True)
                >>> plt.plot(bins, (1/beta)*np.exp(-(bins - mu)/beta)
                ...          * np.exp( -np.exp( -(bins - mu) /beta) ),
                ...          linewidth=2, color='r')
                >>> plt.show()
        
                Show how an extreme value distribution can arise from a Gaussian process
                and compare to a Gaussian:
        
                >>> means = []
                >>> maxima = []
                >>> for i in range(0,1000) :
                ...    a = np.random.normal(mu, beta, 1000)
                ...    means.append(a.mean())
                ...    maxima.append(a.max())
                >>> count, bins, ignored = plt.hist(maxima, 30, normed=True)
                >>> beta = np.std(maxima)*np.pi/np.sqrt(6)
                >>> mu = np.mean(maxima) - 0.57721*beta
                >>> plt.plot(bins, (1/beta)*np.exp(-(bins - mu)/beta)
                ...          * np.exp(-np.exp(-(bins - mu)/beta)),
                ...          linewidth=2, color='r')
                >>> plt.plot(bins, 1/(beta * np.sqrt(2 * np.pi))
                ...          * np.exp(-(bins - mu)**2 / (2 * beta**2)),
                ...          linewidth=2, color='g')
                >>> plt.show()
        """
        pass

    def hypergeometric(self, ngood, nbad, nsample, size=None): # real signature unknown; restored from __doc__
        """
        hypergeometric(ngood, nbad, nsample, size=None)
        
                Draw samples from a Hypergeometric distribution.
        
                Samples are drawn from a Hypergeometric distribution with specified
                parameters, ngood (ways to make a good selection), nbad (ways to make
                a bad selection), and nsample = number of items sampled, which is less
                than or equal to the sum ngood + nbad.
        
                Parameters
                ----------
                ngood : int or array_like
                    Number of ways to make a good selection.  Must be nonnegative.
                nbad : int or array_like
                    Number of ways to make a bad selection.  Must be nonnegative.
                nsample : int or array_like
                    Number of items sampled.  Must be at least 1 and at most
                    ``ngood + nbad``.
                size : int or tuple of int
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : ndarray or scalar
                    The values are all integers in  [0, n].
        
                See Also
                --------
                scipy.stats.distributions.hypergeom : probability density function,
                    distribution or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the Hypergeometric distribution is
        
                .. math:: P(x) = \frac{\binom{m}{n}\binom{N-m}{n-x}}{\binom{N}{n}},
        
                where :math:`0 \le x \le m` and :math:`n+m-N \le x \le n`
        
                for P(x) the probability of x successes, n = ngood, m = nbad, and
                N = number of samples.
        
                Consider an urn with black and white marbles in it, ngood of them
                black and nbad are white. If you draw nsample balls without
                replacement, then the Hypergeometric distribution describes the
                distribution of black balls in the drawn sample.
        
                Note that this distribution is very similar to the Binomial
                distribution, except that in this case, samples are drawn without
                replacement, whereas in the Binomial case samples are drawn with
                replacement (or the sample space is infinite). As the sample space
                becomes large, this distribution approaches the Binomial.
        
                References
                ----------
                .. [1] Lentner, Marvin, "Elementary Applied Statistics", Bogden
                       and Quigley, 1972.
                .. [2] Weisstein, Eric W. "Hypergeometric Distribution." From
                       MathWorld--A Wolfram Web Resource.
                       http://mathworld.wolfram.com/HypergeometricDistribution.html
                .. [3] Wikipedia, "Hypergeometric-distribution",
                       http://en.wikipedia.org/wiki/Hypergeometric-distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> ngood, nbad, nsamp = 100, 2, 10
                # number of good, number of bad, and number of samples
                >>> s = np.random.hypergeometric(ngood, nbad, nsamp, 1000)
                >>> hist(s)
                #   note that it is very unlikely to grab both bad items
        
                Suppose you have an urn with 15 white and 15 black marbles.
                If you pull 15 marbles at random, how likely is it that
                12 or more of them are one color?
        
                >>> s = np.random.hypergeometric(15, 15, 15, 100000)
                >>> sum(s>=12)/100000. + sum(s<=3)/100000.
                #   answer = 0.003 ... pretty unlikely!
        """
        pass

    def laplace(self, loc=0.0, scale=1.0, size=None): # real signature unknown; restored from __doc__
        """
        laplace(loc=0.0, scale=1.0, size=None)
        
                Draw samples from the Laplace or double exponential distribution with
                specified location (or mean) and scale (decay).
        
                The Laplace distribution is similar to the Gaussian/normal distribution,
                but is sharper at the peak and has fatter tails. It represents the
                difference between two independent, identically distributed exponential
                random variables.
        
                Parameters
                ----------
                loc : float
                    The position, :math:`\mu`, of the distribution peak.
                scale : float
                    :math:`\lambda`, the exponential decay.
        
                Notes
                -----
                It has the probability density function
        
                .. math:: f(x; \mu, \lambda) = \frac{1}{2\lambda}
                                               \exp\left(-\frac{|x - \mu|}{\lambda}\right).
        
                The first law of Laplace, from 1774, states that the frequency of an error
                can be expressed as an exponential function of the absolute magnitude of
                the error, which leads to the Laplace distribution. For many problems in
                Economics and Health sciences, this distribution seems to model the data
                better than the standard Gaussian distribution
        
        
                References
                ----------
                .. [1] Abramowitz, M. and Stegun, I. A. (Eds.). Handbook of Mathematical
                       Functions with Formulas, Graphs, and Mathematical Tables, 9th
                       printing.  New York: Dover, 1972.
        
                .. [2] The Laplace distribution and generalizations
                       By Samuel Kotz, Tomasz J. Kozubowski, Krzysztof Podgorski,
                       Birkhauser, 2001.
        
                .. [3] Weisstein, Eric W. "Laplace Distribution."
                       From MathWorld--A Wolfram Web Resource.
                       http://mathworld.wolfram.com/LaplaceDistribution.html
        
                .. [4] Wikipedia, "Laplace distribution",
                       http://en.wikipedia.org/wiki/Laplace_distribution
        
                Examples
                --------
                Draw samples from the distribution
        
                >>> loc, scale = 0., 1.
                >>> s = np.random.laplace(loc, scale, 1000)
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> count, bins, ignored = plt.hist(s, 30, normed=True)
                >>> x = np.arange(-8., 8., .01)
                >>> pdf = np.exp(-abs(x-loc/scale))/(2.*scale)
                >>> plt.plot(x, pdf)
        
                Plot Gaussian for comparison:
        
                >>> g = (1/(scale * np.sqrt(2 * np.pi)) * 
                ...      np.exp( - (x - loc)**2 / (2 * scale**2) ))
                >>> plt.plot(x,g)
        """
        pass

    def logistic(self, loc=0.0, scale=1.0, size=None): # real signature unknown; restored from __doc__
        """
        logistic(loc=0.0, scale=1.0, size=None)
        
                Draw samples from a Logistic distribution.
        
                Samples are drawn from a Logistic distribution with specified
                parameters, loc (location or mean, also median), and scale (>0).
        
                Parameters
                ----------
                loc : float
        
                scale : float > 0.
        
                size : {tuple, int}
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : {ndarray, scalar}
                          where the values are all integers in  [0, n].
        
                See Also
                --------
                scipy.stats.distributions.logistic : probability density function,
                    distribution or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the Logistic distribution is
        
                .. math:: P(x) = P(x) = \frac{e^{-(x-\mu)/s}}{s(1+e^{-(x-\mu)/s})^2},
        
                where :math:`\mu` = location and :math:`s` = scale.
        
                The Logistic distribution is used in Extreme Value problems where it
                can act as a mixture of Gumbel distributions, in Epidemiology, and by
                the World Chess Federation (FIDE) where it is used in the Elo ranking
                system, assuming the performance of each player is a logistically
                distributed random variable.
        
                References
                ----------
                .. [1] Reiss, R.-D. and Thomas M. (2001), Statistical Analysis of Extreme
                       Values, from Insurance, Finance, Hydrology and Other Fields,
                       Birkhauser Verlag, Basel, pp 132-133.
                .. [2] Weisstein, Eric W. "Logistic Distribution." From
                       MathWorld--A Wolfram Web Resource.
                       http://mathworld.wolfram.com/LogisticDistribution.html
                .. [3] Wikipedia, "Logistic-distribution",
                       http://en.wikipedia.org/wiki/Logistic-distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> loc, scale = 10, 1
                >>> s = np.random.logistic(loc, scale, 10000)
                >>> count, bins, ignored = plt.hist(s, bins=50)
        
                #   plot against distribution
        
                >>> def logist(x, loc, scale):
                ...     return exp((loc-x)/scale)/(scale*(1+exp((loc-x)/scale))**2)
                >>> plt.plot(bins, logist(bins, loc, scale)*count.max()/\
                ... logist(bins, loc, scale).max())
                >>> plt.show()
        """
        pass

    def lognormal(self, mean=0.0, sigma=1.0, size=None): # real signature unknown; restored from __doc__
        """
        lognormal(mean=0.0, sigma=1.0, size=None)
        
                Return samples drawn from a log-normal distribution.
        
                Draw samples from a log-normal distribution with specified mean,
                standard deviation, and array shape.  Note that the mean and standard
                deviation are not the values for the distribution itself, but of the
                underlying normal distribution it is derived from.
        
                Parameters
                ----------
                mean : float
                    Mean value of the underlying normal distribution
                sigma : float, > 0.
                    Standard deviation of the underlying normal distribution
                size : tuple of ints
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : ndarray or float
                    The desired samples. An array of the same shape as `size` if given,
                    if `size` is None a float is returned.
        
                See Also
                --------
                scipy.stats.lognorm : probability density function, distribution,
                    cumulative density function, etc.
        
                Notes
                -----
                A variable `x` has a log-normal distribution if `log(x)` is normally
                distributed.  The probability density function for the log-normal
                distribution is:
        
                .. math:: p(x) = \frac{1}{\sigma x \sqrt{2\pi}}
                                 e^{(-\frac{(ln(x)-\mu)^2}{2\sigma^2})}
        
                where :math:`\mu` is the mean and :math:`\sigma` is the standard
                deviation of the normally distributed logarithm of the variable.
                A log-normal distribution results if a random variable is the *product*
                of a large number of independent, identically-distributed variables in
                the same way that a normal distribution results if the variable is the
                *sum* of a large number of independent, identically-distributed
                variables.
        
                References
                ----------
                Limpert, E., Stahel, W. A., and Abbt, M., "Log-normal Distributions
                across the Sciences: Keys and Clues," *BioScience*, Vol. 51, No. 5,
                May, 2001.  http://stat.ethz.ch/~stahel/lognormal/bioscience.pdf
        
                Reiss, R.D. and Thomas, M., *Statistical Analysis of Extreme Values*,
                Basel: Birkhauser Verlag, 2001, pp. 31-32.
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> mu, sigma = 3., 1. # mean and standard deviation
                >>> s = np.random.lognormal(mu, sigma, 1000)
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> count, bins, ignored = plt.hist(s, 100, normed=True, align='mid')
        
                >>> x = np.linspace(min(bins), max(bins), 10000)
                >>> pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
                ...        / (x * sigma * np.sqrt(2 * np.pi)))
        
                >>> plt.plot(x, pdf, linewidth=2, color='r')
                >>> plt.axis('tight')
                >>> plt.show()
        
                Demonstrate that taking the products of random samples from a uniform
                distribution can be fit well by a log-normal probability density function.
        
                >>> # Generate a thousand samples: each is the product of 100 random
                >>> # values, drawn from a normal distribution.
                >>> b = []
                >>> for i in range(1000):
                ...    a = 10. + np.random.random(100)
                ...    b.append(np.product(a))
        
                >>> b = np.array(b) / np.min(b) # scale values to be positive
                >>> count, bins, ignored = plt.hist(b, 100, normed=True, align='center')
                >>> sigma = np.std(np.log(b))
                >>> mu = np.mean(np.log(b))
        
                >>> x = np.linspace(min(bins), max(bins), 10000)
                >>> pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
                ...        / (x * sigma * np.sqrt(2 * np.pi)))
        
                >>> plt.plot(x, pdf, color='r', linewidth=2)
                >>> plt.show()
        """
        pass

    def logseries(self, p, size=None): # real signature unknown; restored from __doc__
        """
        logseries(p, size=None)
        
                Draw samples from a Logarithmic Series distribution.
        
                Samples are drawn from a Log Series distribution with specified
                parameter, p (probability, 0 < p < 1).
        
                Parameters
                ----------
                loc : float
        
                scale : float > 0.
        
                size : {tuple, int}
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : {ndarray, scalar}
                          where the values are all integers in  [0, n].
        
                See Also
                --------
                scipy.stats.distributions.logser : probability density function,
                    distribution or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the Log Series distribution is
        
                .. math:: P(k) = \frac{-p^k}{k \ln(1-p)},
        
                where p = probability.
        
                The Log Series distribution is frequently used to represent species
                richness and occurrence, first proposed by Fisher, Corbet, and
                Williams in 1943 [2].  It may also be used to model the numbers of
                occupants seen in cars [3].
        
                References
                ----------
                .. [1] Buzas, Martin A.; Culver, Stephen J.,  Understanding regional
                       species diversity through the log series distribution of
                       occurrences: BIODIVERSITY RESEARCH Diversity & Distributions,
                       Volume 5, Number 5, September 1999 , pp. 187-195(9).
                .. [2] Fisher, R.A,, A.S. Corbet, and C.B. Williams. 1943. The
                       relation between the number of species and the number of
                       individuals in a random sample of an animal population.
                       Journal of Animal Ecology, 12:42-58.
                .. [3] D. J. Hand, F. Daly, D. Lunn, E. Ostrowski, A Handbook of Small
                       Data Sets, CRC Press, 1994.
                .. [4] Wikipedia, "Logarithmic-distribution",
                       http://en.wikipedia.org/wiki/Logarithmic-distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> a = .6
                >>> s = np.random.logseries(a, 10000)
                >>> count, bins, ignored = plt.hist(s)
        
                #   plot against distribution
        
                >>> def logseries(k, p):
                ...     return -p**k/(k*log(1-p))
                >>> plt.plot(bins, logseries(bins, a)*count.max()/
                             logseries(bins, a).max(), 'r')
                >>> plt.show()
        """
        pass

    def multinomial(self, n, pvals, size=None): # real signature unknown; restored from __doc__
        """
        multinomial(n, pvals, size=None)
        
                Draw samples from a multinomial distribution.
        
                The multinomial distribution is a multivariate generalisation of the
                binomial distribution.  Take an experiment with one of ``p``
                possible outcomes.  An example of such an experiment is throwing a dice,
                where the outcome can be 1 through 6.  Each sample drawn from the
                distribution represents `n` such experiments.  Its values,
                ``X_i = [X_0, X_1, ..., X_p]``, represent the number of times the outcome
                was ``i``.
        
                Parameters
                ----------
                n : int
                    Number of experiments.
                pvals : sequence of floats, length p
                    Probabilities of each of the ``p`` different outcomes.  These
                    should sum to 1 (however, the last element is always assumed to
                    account for the remaining probability, as long as
                    ``sum(pvals[:-1]) <= 1)``.
                size : tuple of ints
                    Given a `size` of ``(M, N, K)``, then ``M*N*K`` samples are drawn,
                    and the output shape becomes ``(M, N, K, p)``, since each sample
                    has shape ``(p,)``.
        
                Examples
                --------
                Throw a dice 20 times:
        
                >>> np.random.multinomial(20, [1/6.]*6, size=1)
                array([[4, 1, 7, 5, 2, 1]])
        
                It landed 4 times on 1, once on 2, etc.
        
                Now, throw the dice 20 times, and 20 times again:
        
                >>> np.random.multinomial(20, [1/6.]*6, size=2)
                array([[3, 4, 3, 3, 4, 3],
                       [2, 4, 3, 4, 0, 7]])
        
                For the first run, we threw 3 times 1, 4 times 2, etc.  For the second,
                we threw 2 times 1, 4 times 2, etc.
        
                A loaded dice is more likely to land on number 6:
        
                >>> np.random.multinomial(100, [1/7.]*5)
                array([13, 16, 13, 16, 42])
        """
        pass

    def multivariate_normal(self, mean, cov, size=None): # real signature unknown; restored from __doc__
        """
        multivariate_normal(mean, cov[, size])
        
                Draw random samples from a multivariate normal distribution.
        
                The multivariate normal, multinormal or Gaussian distribution is a
                generalization of the one-dimensional normal distribution to higher
                dimensions.  Such a distribution is specified by its mean and
                covariance matrix.  These parameters are analogous to the mean
                (average or "center") and variance (standard deviation, or "width,"
                squared) of the one-dimensional normal distribution.
        
                Parameters
                ----------
                mean : 1-D array_like, of length N
                    Mean of the N-dimensional distribution.
                cov : 2-D array_like, of shape (N, N)
                    Covariance matrix of the distribution.  Must be symmetric and
                    positive semi-definite for "physically meaningful" results.
                size : int or tuple of ints, optional
                    Given a shape of, for example, ``(m,n,k)``, ``m*n*k`` samples are
                    generated, and packed in an `m`-by-`n`-by-`k` arrangement.  Because
                    each sample is `N`-dimensional, the output shape is ``(m,n,k,N)``.
                    If no shape is specified, a single (`N`-D) sample is returned.
        
                Returns
                -------
                out : ndarray
                    The drawn samples, of shape *size*, if that was provided.  If not,
                    the shape is ``(N,)``.
        
                    In other words, each entry ``out[i,j,...,:]`` is an N-dimensional
                    value drawn from the distribution.
        
                Notes
                -----
                The mean is a coordinate in N-dimensional space, which represents the
                location where samples are most likely to be generated.  This is
                analogous to the peak of the bell curve for the one-dimensional or
                univariate normal distribution.
        
                Covariance indicates the level to which two variables vary together.
                From the multivariate normal distribution, we draw N-dimensional
                samples, :math:`X = [x_1, x_2, ... x_N]`.  The covariance matrix
                element :math:`C_{ij}` is the covariance of :math:`x_i` and :math:`x_j`.
                The element :math:`C_{ii}` is the variance of :math:`x_i` (i.e. its
                "spread").
        
                Instead of specifying the full covariance matrix, popular
                approximations include:
        
                  - Spherical covariance (*cov* is a multiple of the identity matrix)
                  - Diagonal covariance (*cov* has non-negative elements, and only on
                    the diagonal)
        
                This geometrical property can be seen in two dimensions by plotting
                generated data-points:
        
                >>> mean = [0,0]
                >>> cov = [[1,0],[0,100]] # diagonal covariance, points lie on x or y-axis
        
                >>> import matplotlib.pyplot as plt
                >>> x,y = np.random.multivariate_normal(mean,cov,5000).T
                >>> plt.plot(x,y,'x'); plt.axis('equal'); plt.show()
        
                Note that the covariance matrix must be non-negative definite.
        
                References
                ----------
                Papoulis, A., *Probability, Random Variables, and Stochastic Processes*,
                3rd ed., New York: McGraw-Hill, 1991.
        
                Duda, R. O., Hart, P. E., and Stork, D. G., *Pattern Classification*,
                2nd ed., New York: Wiley, 2001.
        
                Examples
                --------
                >>> mean = (1,2)
                >>> cov = [[1,0],[1,0]]
                >>> x = np.random.multivariate_normal(mean,cov,(3,3))
                >>> x.shape
                (3, 3, 2)
        
                The following is probably true, given that 0.6 is roughly twice the
                standard deviation:
        
                >>> print list( (x[0,0,:] - mean) < 0.6 )
                [True, True]
        """
        pass

    def negative_binomial(self, n, p, size=None): # real signature unknown; restored from __doc__
        """
        negative_binomial(n, p, size=None)
        
                Draw samples from a negative_binomial distribution.
        
                Samples are drawn from a negative_Binomial distribution with specified
                parameters, `n` trials and `p` probability of success where `n` is an
                integer > 0 and `p` is in the interval [0, 1].
        
                Parameters
                ----------
                n : int
                    Parameter, > 0.
                p : float
                    Parameter, >= 0 and <=1.
                size : int or tuple of ints
                    Output shape. If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : int or ndarray of ints
                    Drawn samples.
        
                Notes
                -----
                The probability density for the Negative Binomial distribution is
        
                .. math:: P(N;n,p) = \binom{N+n-1}{n-1}p^{n}(1-p)^{N},
        
                where :math:`n-1` is the number of successes, :math:`p` is the probability
                of success, and :math:`N+n-1` is the number of trials.
        
                The negative binomial distribution gives the probability of n-1 successes
                and N failures in N+n-1 trials, and success on the (N+n)th trial.
        
                If one throws a die repeatedly until the third time a "1" appears, then the
                probability distribution of the number of non-"1"s that appear before the
                third "1" is a negative binomial distribution.
        
                References
                ----------
                .. [1] Weisstein, Eric W. "Negative Binomial Distribution." From
                       MathWorld--A Wolfram Web Resource.
                       http://mathworld.wolfram.com/NegativeBinomialDistribution.html
                .. [2] Wikipedia, "Negative binomial distribution",
                       http://en.wikipedia.org/wiki/Negative_binomial_distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                A real world example. A company drills wild-cat oil exploration wells, each
                with an estimated probability of success of 0.1.  What is the probability
                of having one success for each successive well, that is what is the
                probability of a single success after drilling 5 wells, after 6 wells,
                etc.?
        
                >>> s = np.random.negative_binomial(1, 0.1, 100000)
                >>> for i in range(1, 11):
                ...    probability = sum(s<i) / 100000.
                ...    print i, "wells drilled, probability of one success =", probability
        """
        pass

    def noncentral_chisquare(self, df, nonc, size=None): # real signature unknown; restored from __doc__
        """
        noncentral_chisquare(df, nonc, size=None)
        
                Draw samples from a noncentral chi-square distribution.
        
                The noncentral :math:`\chi^2` distribution is a generalisation of
                the :math:`\chi^2` distribution.
        
                Parameters
                ----------
                df : int
                    Degrees of freedom, should be >= 1.
                nonc : float
                    Non-centrality, should be > 0.
                size : int or tuple of ints
                    Shape of the output.
        
                Notes
                -----
                The probability density function for the noncentral Chi-square distribution
                is
        
                .. math:: P(x;df,nonc) = \sum^{\infty}_{i=0}
                                       \frac{e^{-nonc/2}(nonc/2)^{i}}{i!}P_{Y_{df+2i}}(x),
        
                where :math:`Y_{q}` is the Chi-square with q degrees of freedom.
        
                In Delhi (2007), it is noted that the noncentral chi-square is useful in
                bombing and coverage problems, the probability of killing the point target
                given by the noncentral chi-squared distribution.
        
                References
                ----------
                .. [1] Delhi, M.S. Holla, "On a noncentral chi-square distribution in the
                       analysis of weapon systems effectiveness", Metrika, Volume 15,
                       Number 1 / December, 1970.
                .. [2] Wikipedia, "Noncentral chi-square distribution"
                       http://en.wikipedia.org/wiki/Noncentral_chi-square_distribution
        
                Examples
                --------
                Draw values from the distribution and plot the histogram
        
                >>> import matplotlib.pyplot as plt
                >>> values = plt.hist(np.random.noncentral_chisquare(3, 20, 100000),
                ...                   bins=200, normed=True)
                >>> plt.show()
        
                Draw values from a noncentral chisquare with very small noncentrality,
                and compare to a chisquare.
        
                >>> plt.figure()
                >>> values = plt.hist(np.random.noncentral_chisquare(3, .0000001, 100000),
                ...                   bins=np.arange(0., 25, .1), normed=True)
                >>> values2 = plt.hist(np.random.chisquare(3, 100000),
                ...                    bins=np.arange(0., 25, .1), normed=True)
                >>> plt.plot(values[1][0:-1], values[0]-values2[0], 'ob')
                >>> plt.show()
        
                Demonstrate how large values of non-centrality lead to a more symmetric
                distribution.
        
                >>> plt.figure()
                >>> values = plt.hist(np.random.noncentral_chisquare(3, 20, 100000),
                ...                   bins=200, normed=True)
                >>> plt.show()
        """
        pass

    def noncentral_f(self, dfnum, dfden, nonc, size=None): # real signature unknown; restored from __doc__
        """
        noncentral_f(dfnum, dfden, nonc, size=None)
        
                Draw samples from the noncentral F distribution.
        
                Samples are drawn from an F distribution with specified parameters,
                `dfnum` (degrees of freedom in numerator) and `dfden` (degrees of
                freedom in denominator), where both parameters > 1.
                `nonc` is the non-centrality parameter.
        
                Parameters
                ----------
                dfnum : int
                    Parameter, should be > 1.
                dfden : int
                    Parameter, should be > 1.
                nonc : float
                    Parameter, should be >= 0.
                size : int or tuple of ints
                    Output shape. If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : scalar or ndarray
                    Drawn samples.
        
                Notes
                -----
                When calculating the power of an experiment (power = probability of
                rejecting the null hypothesis when a specific alternative is true) the
                non-central F statistic becomes important.  When the null hypothesis is
                true, the F statistic follows a central F distribution. When the null
                hypothesis is not true, then it follows a non-central F statistic.
        
                References
                ----------
                Weisstein, Eric W. "Noncentral F-Distribution." From MathWorld--A Wolfram
                Web Resource.  http://mathworld.wolfram.com/NoncentralF-Distribution.html
        
                Wikipedia, "Noncentral F distribution",
                http://en.wikipedia.org/wiki/Noncentral_F-distribution
        
                Examples
                --------
                In a study, testing for a specific alternative to the null hypothesis
                requires use of the Noncentral F distribution. We need to calculate the
                area in the tail of the distribution that exceeds the value of the F
                distribution for the null hypothesis.  We'll plot the two probability
                distributions for comparison.
        
                >>> dfnum = 3 # between group deg of freedom
                >>> dfden = 20 # within groups degrees of freedom
                >>> nonc = 3.0
                >>> nc_vals = np.random.noncentral_f(dfnum, dfden, nonc, 1000000)
                >>> NF = np.histogram(nc_vals, bins=50, normed=True)
                >>> c_vals = np.random.f(dfnum, dfden, 1000000)
                >>> F = np.histogram(c_vals, bins=50, normed=True)
                >>> plt.plot(F[1][1:], F[0])
                >>> plt.plot(NF[1][1:], NF[0])
                >>> plt.show()
        """
        pass

    def normal(self, loc=0.0, scale=1.0, size=None): # real signature unknown; restored from __doc__
        """
        normal(loc=0.0, scale=1.0, size=None)
        
                Draw random samples from a normal (Gaussian) distribution.
        
                The probability density function of the normal distribution, first
                derived by De Moivre and 200 years later by both Gauss and Laplace
                independently [2]_, is often called the bell curve because of
                its characteristic shape (see the example below).
        
                The normal distributions occurs often in nature.  For example, it
                describes the commonly occurring distribution of samples influenced
                by a large number of tiny, random disturbances, each with its own
                unique distribution [2]_.
        
                Parameters
                ----------
                loc : float
                    Mean ("centre") of the distribution.
                scale : float
                    Standard deviation (spread or "width") of the distribution.
                size : tuple of ints
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                See Also
                --------
                scipy.stats.distributions.norm : probability density function,
                    distribution or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the Gaussian distribution is
        
                .. math:: p(x) = \frac{1}{\sqrt{ 2 \pi \sigma^2 }}
                                 e^{ - \frac{ (x - \mu)^2 } {2 \sigma^2} },
        
                where :math:`\mu` is the mean and :math:`\sigma` the standard deviation.
                The square of the standard deviation, :math:`\sigma^2`, is called the
                variance.
        
                The function has its peak at the mean, and its "spread" increases with
                the standard deviation (the function reaches 0.607 times its maximum at
                :math:`x + \sigma` and :math:`x - \sigma` [2]_).  This implies that
                `numpy.random.normal` is more likely to return samples lying close to the
                mean, rather than those far away.
        
                References
                ----------
                .. [1] Wikipedia, "Normal distribution",
                       http://en.wikipedia.org/wiki/Normal_distribution
                .. [2] P. R. Peebles Jr., "Central Limit Theorem" in "Probability, Random
                       Variables and Random Signal Principles", 4th ed., 2001,
                       pp. 51, 51, 125.
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> mu, sigma = 0, 0.1 # mean and standard deviation
                >>> s = np.random.normal(mu, sigma, 1000)
        
                Verify the mean and the variance:
        
                >>> abs(mu - np.mean(s)) < 0.01
                True
        
                >>> abs(sigma - np.std(s, ddof=1)) < 0.01
                True
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> count, bins, ignored = plt.hist(s, 30, normed=True)
                >>> plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
                ...                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
                ...          linewidth=2, color='r')
                >>> plt.show()
        """
        pass

    def pareto(self, a, size=None): # real signature unknown; restored from __doc__
        """
        pareto(a, size=None)
        
                Draw samples from a Pareto II or Lomax distribution with specified shape.
        
                The Lomax or Pareto II distribution is a shifted Pareto distribution. The
                classical Pareto distribution can be obtained from the Lomax distribution
                by adding the location parameter m, see below. The smallest value of the
                Lomax distribution is zero while for the classical Pareto distribution it
                is m, where the standard Pareto distribution has location m=1.
                Lomax can also be considered as a simplified version of the Generalized
                Pareto distribution (available in SciPy), with the scale set to one and
                the location set to zero.
        
                The Pareto distribution must be greater than zero, and is unbounded above.
                It is also known as the "80-20 rule".  In this distribution, 80 percent of
                the weights are in the lowest 20 percent of the range, while the other 20
                percent fill the remaining 80 percent of the range.
        
                Parameters
                ----------
                shape : float, > 0.
                    Shape of the distribution.
                size : tuple of ints
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                See Also
                --------
                scipy.stats.distributions.lomax.pdf : probability density function,
                    distribution or cumulative density function, etc.
                scipy.stats.distributions.genpareto.pdf : probability density function,
                    distribution or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the Pareto distribution is
        
                .. math:: p(x) = \frac{am^a}{x^{a+1}}
        
                where :math:`a` is the shape and :math:`m` the location
        
                The Pareto distribution, named after the Italian economist Vilfredo Pareto,
                is a power law probability distribution useful in many real world problems.
                Outside the field of economics it is generally referred to as the Bradford
                distribution. Pareto developed the distribution to describe the
                distribution of wealth in an economy.  It has also found use in insurance,
                web page access statistics, oil field sizes, and many other problems,
                including the download frequency for projects in Sourceforge [1].  It is
                one of the so-called "fat-tailed" distributions.
        
        
                References
                ----------
                .. [1] Francis Hunt and Paul Johnson, On the Pareto Distribution of
                       Sourceforge projects.
                .. [2] Pareto, V. (1896). Course of Political Economy. Lausanne.
                .. [3] Reiss, R.D., Thomas, M.(2001), Statistical Analysis of Extreme
                       Values, Birkhauser Verlag, Basel, pp 23-30.
                .. [4] Wikipedia, "Pareto distribution",
                       http://en.wikipedia.org/wiki/Pareto_distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> a, m = 3., 1. # shape and mode
                >>> s = np.random.pareto(a, 1000) + m
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> count, bins, ignored = plt.hist(s, 100, normed=True, align='center')
                >>> fit = a*m**a/bins**(a+1)
                >>> plt.plot(bins, max(count)*fit/max(fit),linewidth=2, color='r')
                >>> plt.show()
        """
        pass

    def permutation(self, x): # real signature unknown; restored from __doc__
        """
        permutation(x)
        
                Randomly permute a sequence, or return a permuted range.
        
                If `x` is a multi-dimensional array, it is only shuffled along its
                first index.
        
                Parameters
                ----------
                x : int or array_like
                    If `x` is an integer, randomly permute ``np.arange(x)``.
                    If `x` is an array, make a copy and shuffle the elements
                    randomly.
        
                Returns
                -------
                out : ndarray
                    Permuted sequence or array range.
        
                Examples
                --------
                >>> np.random.permutation(10)
                array([1, 7, 4, 3, 0, 9, 2, 5, 8, 6])
        
                >>> np.random.permutation([1, 4, 9, 12, 15])
                array([15,  1,  9,  4, 12])
        
                >>> arr = np.arange(9).reshape((3, 3))
                >>> np.random.permutation(arr)
                array([[6, 7, 8],
                       [0, 1, 2],
                       [3, 4, 5]])
        """
        pass

    def poisson(self, lam=1.0, size=None): # real signature unknown; restored from __doc__
        """
        poisson(lam=1.0, size=None)
        
                Draw samples from a Poisson distribution.
        
                The Poisson distribution is the limit of the Binomial
                distribution for large N.
        
                Parameters
                ----------
                lam : float
                    Expectation of interval, should be >= 0.
                size : int or tuple of ints, optional
                    Output shape. If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Notes
                -----
                The Poisson distribution
        
                .. math:: f(k; \lambda)=\frac{\lambda^k e^{-\lambda}}{k!}
        
                For events with an expected separation :math:`\lambda` the Poisson
                distribution :math:`f(k; \lambda)` describes the probability of
                :math:`k` events occurring within the observed interval :math:`\lambda`.
        
                Because the output is limited to the range of the C long type, a
                ValueError is raised when `lam` is within 10 sigma of the maximum
                representable value.
        
                References
                ----------
                .. [1] Weisstein, Eric W. "Poisson Distribution." From MathWorld--A Wolfram
                       Web Resource. http://mathworld.wolfram.com/PoissonDistribution.html
                .. [2] Wikipedia, "Poisson distribution",
                   http://en.wikipedia.org/wiki/Poisson_distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> import numpy as np
                >>> s = np.random.poisson(5, 10000)
        
                Display histogram of the sample:
        
                >>> import matplotlib.pyplot as plt
                >>> count, bins, ignored = plt.hist(s, 14, normed=True)
                >>> plt.show()
        """
        pass

    def power(self, a, size=None): # real signature unknown; restored from __doc__
        """
        power(a, size=None)
        
                Draws samples in [0, 1] from a power distribution with positive
                exponent a - 1.
        
                Also known as the power function distribution.
        
                Parameters
                ----------
                a : float
                    parameter, > 0
                size : tuple of ints
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                            ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : {ndarray, scalar}
                    The returned samples lie in [0, 1].
        
                Raises
                ------
                ValueError
                    If a<1.
        
                Notes
                -----
                The probability density function is
        
                .. math:: P(x; a) = ax^{a-1}, 0 \le x \le 1, a>0.
        
                The power function distribution is just the inverse of the Pareto
                distribution. It may also be seen as a special case of the Beta
                distribution.
        
                It is used, for example, in modeling the over-reporting of insurance
                claims.
        
                References
                ----------
                .. [1] Christian Kleiber, Samuel Kotz, "Statistical size distributions
                       in economics and actuarial sciences", Wiley, 2003.
                .. [2] Heckert, N. A. and Filliben, James J. (2003). NIST Handbook 148:
                       Dataplot Reference Manual, Volume 2: Let Subcommands and Library
                       Functions", National Institute of Standards and Technology Handbook
                       Series, June 2003.
                       http://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/powpdf.pdf
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> a = 5. # shape
                >>> samples = 1000
                >>> s = np.random.power(a, samples)
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> count, bins, ignored = plt.hist(s, bins=30)
                >>> x = np.linspace(0, 1, 100)
                >>> y = a*x**(a-1.)
                >>> normed_y = samples*np.diff(bins)[0]*y
                >>> plt.plot(x, normed_y)
                >>> plt.show()
        
                Compare the power function distribution to the inverse of the Pareto.
        
                >>> from scipy import stats
                >>> rvs = np.random.power(5, 1000000)
                >>> rvsp = np.random.pareto(5, 1000000)
                >>> xx = np.linspace(0,1,100)
                >>> powpdf = stats.powerlaw.pdf(xx,5)
        
                >>> plt.figure()
                >>> plt.hist(rvs, bins=50, normed=True)
                >>> plt.plot(xx,powpdf,'r-')
                >>> plt.title('np.random.power(5)')
        
                >>> plt.figure()
                >>> plt.hist(1./(1.+rvsp), bins=50, normed=True)
                >>> plt.plot(xx,powpdf,'r-')
                >>> plt.title('inverse of 1 + np.random.pareto(5)')
        
                >>> plt.figure()
                >>> plt.hist(1./(1.+rvsp), bins=50, normed=True)
                >>> plt.plot(xx,powpdf,'r-')
                >>> plt.title('inverse of stats.pareto(5)')
        """
        pass

    def rand(self, d0, d1, *more, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__ 
        """
        rand(d0, d1, ..., dn)
        
                Random values in a given shape.
        
                Create an array of the given shape and propagate it with
                random samples from a uniform distribution
                over ``[0, 1)``.
        
                Parameters
                ----------
                d0, d1, ..., dn : int, optional
                    The dimensions of the returned array, should all be positive.
                    If no argument is given a single Python float is returned.
        
                Returns
                -------
                out : ndarray, shape ``(d0, d1, ..., dn)``
                    Random values.
        
                See Also
                --------
                random
        
                Notes
                -----
                This is a convenience function. If you want an interface that
                takes a shape-tuple as the first argument, refer to
                np.random.random_sample .
        
                Examples
                --------
                >>> np.random.rand(3,2)
                array([[ 0.14022471,  0.96360618],  #random
                       [ 0.37601032,  0.25528411],  #random
                       [ 0.49313049,  0.94909878]]) #random
        """
        pass

    def randint(self, low, high=None, size=None): # real signature unknown; restored from __doc__
        """
        randint(low, high=None, size=None)
        
                Return random integers from `low` (inclusive) to `high` (exclusive).
        
                Return random integers from the "discrete uniform" distribution in the
                "half-open" interval [`low`, `high`). If `high` is None (the default),
                then results are from [0, `low`).
        
                Parameters
                ----------
                low : int
                    Lowest (signed) integer to be drawn from the distribution (unless
                    ``high=None``, in which case this parameter is the *highest* such
                    integer).
                high : int, optional
                    If provided, one above the largest (signed) integer to be drawn
                    from the distribution (see above for behavior if ``high=None``).
                size : int or tuple of ints, optional
                    Output shape. Default is None, in which case a single int is
                    returned.
        
                Returns
                -------
                out : int or ndarray of ints
                    `size`-shaped array of random integers from the appropriate
                    distribution, or a single such random int if `size` not provided.
        
                See Also
                --------
                random.random_integers : similar to `randint`, only for the closed
                    interval [`low`, `high`], and 1 is the lowest value if `high` is
                    omitted. In particular, this other one is the one to use to generate
                    uniformly distributed discrete non-integers.
        
                Examples
                --------
                >>> np.random.randint(2, size=10)
                array([1, 0, 0, 0, 1, 1, 0, 0, 1, 0])
                >>> np.random.randint(1, size=10)
                array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        
                Generate a 2 x 4 array of ints between 0 and 4, inclusive:
        
                >>> np.random.randint(5, size=(2, 4))
                array([[4, 0, 2, 1],
                       [3, 2, 2, 0]])
        """
        pass

    def randn(self, d0, d1, *more, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__ 
        """
        randn(d0, d1, ..., dn)
        
                Return a sample (or samples) from the "standard normal" distribution.
        
                If positive, int_like or int-convertible arguments are provided,
                `randn` generates an array of shape ``(d0, d1, ..., dn)``, filled
                with random floats sampled from a univariate "normal" (Gaussian)
                distribution of mean 0 and variance 1 (if any of the :math:`d_i` are
                floats, they are first converted to integers by truncation). A single
                float randomly sampled from the distribution is returned if no
                argument is provided.
        
                This is a convenience function.  If you want an interface that takes a
                tuple as the first argument, use `numpy.random.standard_normal` instead.
        
                Parameters
                ----------
                d0, d1, ..., dn : int, optional
                    The dimensions of the returned array, should be all positive.
                    If no argument is given a single Python float is returned.
        
                Returns
                -------
                Z : ndarray or float
                    A ``(d0, d1, ..., dn)``-shaped array of floating-point samples from
                    the standard normal distribution, or a single such float if
                    no parameters were supplied.
        
                See Also
                --------
                random.standard_normal : Similar, but takes a tuple as its argument.
        
                Notes
                -----
                For random samples from :math:`N(\mu, \sigma^2)`, use:
        
                ``sigma * np.random.randn(...) + mu``
        
                Examples
                --------
                >>> np.random.randn()
                2.1923875335537315 #random
        
                Two-by-four array of samples from N(3, 6.25):
        
                >>> 2.5 * np.random.randn(2, 4) + 3
                array([[-4.49401501,  4.00950034, -1.81814867,  7.29718677],  #random
                       [ 0.39924804,  4.68456316,  4.99394529,  4.84057254]]) #random
        """
        pass

    def random_integers(self, low, high=None, size=None): # real signature unknown; restored from __doc__
        """
        random_integers(low, high=None, size=None)
        
                Return random integers between `low` and `high`, inclusive.
        
                Return random integers from the "discrete uniform" distribution in the
                closed interval [`low`, `high`].  If `high` is None (the default),
                then results are from [1, `low`].
        
                Parameters
                ----------
                low : int
                    Lowest (signed) integer to be drawn from the distribution (unless
                    ``high=None``, in which case this parameter is the *highest* such
                    integer).
                high : int, optional
                    If provided, the largest (signed) integer to be drawn from the
                    distribution (see above for behavior if ``high=None``).
                size : int or tuple of ints, optional
                    Output shape. Default is None, in which case a single int is returned.
        
                Returns
                -------
                out : int or ndarray of ints
                    `size`-shaped array of random integers from the appropriate
                    distribution, or a single such random int if `size` not provided.
        
                See Also
                --------
                random.randint : Similar to `random_integers`, only for the half-open
                    interval [`low`, `high`), and 0 is the lowest value if `high` is
                    omitted.
        
                Notes
                -----
                To sample from N evenly spaced floating-point numbers between a and b,
                use::
        
                  a + (b - a) * (np.random.random_integers(N) - 1) / (N - 1.)
        
                Examples
                --------
                >>> np.random.random_integers(5)
                4
                >>> type(np.random.random_integers(5))
                <type 'int'>
                >>> np.random.random_integers(5, size=(3.,2.))
                array([[5, 4],
                       [3, 3],
                       [4, 5]])
        
                Choose five random numbers from the set of five evenly-spaced
                numbers between 0 and 2.5, inclusive (*i.e.*, from the set
                :math:`{0, 5/8, 10/8, 15/8, 20/8}`):
        
                >>> 2.5 * (np.random.random_integers(5, size=(5,)) - 1) / 4.
                array([ 0.625,  1.25 ,  0.625,  0.625,  2.5  ])
        
                Roll two six sided dice 1000 times and sum the results:
        
                >>> d1 = np.random.random_integers(1, 6, 1000)
                >>> d2 = np.random.random_integers(1, 6, 1000)
                >>> dsums = d1 + d2
        
                Display results as a histogram:
        
                >>> import matplotlib.pyplot as plt
                >>> count, bins, ignored = plt.hist(dsums, 11, normed=True)
                >>> plt.show()
        """
        pass

    def random_sample(self, size=None): # real signature unknown; restored from __doc__
        """
        random_sample(size=None)
        
                Return random floats in the half-open interval [0.0, 1.0).
        
                Results are from the "continuous uniform" distribution over the
                stated interval.  To sample :math:`Unif[a, b), b > a` multiply
                the output of `random_sample` by `(b-a)` and add `a`::
        
                  (b - a) * random_sample() + a
        
                Parameters
                ----------
                size : int or tuple of ints, optional
                    Defines the shape of the returned array of random floats. If None
                    (the default), returns a single float.
        
                Returns
                -------
                out : float or ndarray of floats
                    Array of random floats of shape `size` (unless ``size=None``, in which
                    case a single float is returned).
        
                Examples
                --------
                >>> np.random.random_sample()
                0.47108547995356098
                >>> type(np.random.random_sample())
                <type 'float'>
                >>> np.random.random_sample((5,))
                array([ 0.30220482,  0.86820401,  0.1654503 ,  0.11659149,  0.54323428])
        
                Three-by-two array of random numbers from [-5, 0):
        
                >>> 5 * np.random.random_sample((3, 2)) - 5
                array([[-3.99149989, -0.52338984],
                       [-2.99091858, -0.79479508],
                       [-1.23204345, -1.75224494]])
        """
        pass

    def rayleigh(self, scale=1.0, size=None): # real signature unknown; restored from __doc__
        """
        rayleigh(scale=1.0, size=None)
        
                Draw samples from a Rayleigh distribution.
        
                The :math:`\chi` and Weibull distributions are generalizations of the
                Rayleigh.
        
                Parameters
                ----------
                scale : scalar
                    Scale, also equals the mode. Should be >= 0.
                size : int or tuple of ints, optional
                    Shape of the output. Default is None, in which case a single
                    value is returned.
        
                Notes
                -----
                The probability density function for the Rayleigh distribution is
        
                .. math:: P(x;scale) = \frac{x}{scale^2}e^{\frac{-x^2}{2 \cdotp scale^2}}
        
                The Rayleigh distribution arises if the wind speed and wind direction are
                both gaussian variables, then the vector wind velocity forms a Rayleigh
                distribution. The Rayleigh distribution is used to model the expected
                output from wind turbines.
        
                References
                ----------
                .. [1] Brighton Webs Ltd., Rayleigh Distribution,
                      http://www.brighton-webs.co.uk/distributions/rayleigh.asp
                .. [2] Wikipedia, "Rayleigh distribution"
                      http://en.wikipedia.org/wiki/Rayleigh_distribution
        
                Examples
                --------
                Draw values from the distribution and plot the histogram
        
                >>> values = hist(np.random.rayleigh(3, 100000), bins=200, normed=True)
        
                Wave heights tend to follow a Rayleigh distribution. If the mean wave
                height is 1 meter, what fraction of waves are likely to be larger than 3
                meters?
        
                >>> meanvalue = 1
                >>> modevalue = np.sqrt(2 / np.pi) * meanvalue
                >>> s = np.random.rayleigh(modevalue, 1000000)
        
                The percentage of waves larger than 3 meters is:
        
                >>> 100.*sum(s>3)/1000000.
                0.087300000000000003
        """
        pass

    def seed(self, seed=None): # real signature unknown; restored from __doc__
        """
        seed(seed=None)
        
                Seed the generator.
        
                This method is called when `RandomState` is initialized. It can be
                called again to re-seed the generator. For details, see `RandomState`.
        
                Parameters
                ----------
                seed : int or array_like, optional
                    Seed for `RandomState`.
        
                See Also
                --------
                RandomState
        """
        pass

    def set_state(self, state): # real signature unknown; restored from __doc__
        """
        set_state(state)
        
                Set the internal state of the generator from a tuple.
        
                For use if one has reason to manually (re-)set the internal state of the
                "Mersenne Twister"[1]_ pseudo-random number generating algorithm.
        
                Parameters
                ----------
                state : tuple(str, ndarray of 624 uints, int, int, float)
                    The `state` tuple has the following items:
        
                    1. the string 'MT19937', specifying the Mersenne Twister algorithm.
                    2. a 1-D array of 624 unsigned integers ``keys``.
                    3. an integer ``pos``.
                    4. an integer ``has_gauss``.
                    5. a float ``cached_gaussian``.
        
                Returns
                -------
                out : None
                    Returns 'None' on success.
        
                See Also
                --------
                get_state
        
                Notes
                -----
                `set_state` and `get_state` are not needed to work with any of the
                random distributions in NumPy. If the internal state is manually altered,
                the user should know exactly what he/she is doing.
        
                For backwards compatibility, the form (str, array of 624 uints, int) is
                also accepted although it is missing some information about the cached
                Gaussian value: ``state = ('MT19937', keys, pos)``.
        
                References
                ----------
                .. [1] M. Matsumoto and T. Nishimura, "Mersenne Twister: A
                   623-dimensionally equidistributed uniform pseudorandom number
                   generator," *ACM Trans. on Modeling and Computer Simulation*,
                   Vol. 8, No. 1, pp. 3-30, Jan. 1998.
        """
        pass

    def shuffle(self, x): # real signature unknown; restored from __doc__
        """
        shuffle(x)
        
                Modify a sequence in-place by shuffling its contents.
        
                Parameters
                ----------
                x : array_like
                    The array or list to be shuffled.
        
                Returns
                -------
                None
        
                Examples
                --------
                >>> arr = np.arange(10)
                >>> np.random.shuffle(arr)
                >>> arr
                [1 7 5 2 9 4 3 6 0 8]
        
                This function only shuffles the array along the first index of a
                multi-dimensional array:
        
                >>> arr = np.arange(9).reshape((3, 3))
                >>> np.random.shuffle(arr)
                >>> arr
                array([[3, 4, 5],
                       [6, 7, 8],
                       [0, 1, 2]])
        """
        pass

    def standard_cauchy(self, size=None): # real signature unknown; restored from __doc__
        """
        standard_cauchy(size=None)
        
                Standard Cauchy distribution with mode = 0.
        
                Also known as the Lorentz distribution.
        
                Parameters
                ----------
                size : int or tuple of ints
                    Shape of the output.
        
                Returns
                -------
                samples : ndarray or scalar
                    The drawn samples.
        
                Notes
                -----
                The probability density function for the full Cauchy distribution is
        
                .. math:: P(x; x_0, \gamma) = \frac{1}{\pi \gamma \bigl[ 1+
                          (\frac{x-x_0}{\gamma})^2 \bigr] }
        
                and the Standard Cauchy distribution just sets :math:`x_0=0` and
                :math:`\gamma=1`
        
                The Cauchy distribution arises in the solution to the driven harmonic
                oscillator problem, and also describes spectral line broadening. It
                also describes the distribution of values at which a line tilted at
                a random angle will cut the x axis.
        
                When studying hypothesis tests that assume normality, seeing how the
                tests perform on data from a Cauchy distribution is a good indicator of
                their sensitivity to a heavy-tailed distribution, since the Cauchy looks
                very much like a Gaussian distribution, but with heavier tails.
        
                References
                ----------
                .. [1] NIST/SEMATECH e-Handbook of Statistical Methods, "Cauchy
                      Distribution",
                      http://www.itl.nist.gov/div898/handbook/eda/section3/eda3663.htm
                .. [2] Weisstein, Eric W. "Cauchy Distribution." From MathWorld--A
                      Wolfram Web Resource.
                      http://mathworld.wolfram.com/CauchyDistribution.html
                .. [3] Wikipedia, "Cauchy distribution"
                      http://en.wikipedia.org/wiki/Cauchy_distribution
        
                Examples
                --------
                Draw samples and plot the distribution:
        
                >>> s = np.random.standard_cauchy(1000000)
                >>> s = s[(s>-25) & (s<25)]  # truncate distribution so it plots well
                >>> plt.hist(s, bins=100)
                >>> plt.show()
        """
        pass

    def standard_exponential(self, size=None): # real signature unknown; restored from __doc__
        """
        standard_exponential(size=None)
        
                Draw samples from the standard exponential distribution.
        
                `standard_exponential` is identical to the exponential distribution
                with a scale parameter of 1.
        
                Parameters
                ----------
                size : int or tuple of ints
                    Shape of the output.
        
                Returns
                -------
                out : float or ndarray
                    Drawn samples.
        
                Examples
                --------
                Output a 3x8000 array:
        
                >>> n = np.random.standard_exponential((3, 8000))
        """
        pass

    def standard_gamma(self, shape, size=None): # real signature unknown; restored from __doc__
        """
        standard_gamma(shape, size=None)
        
                Draw samples from a Standard Gamma distribution.
        
                Samples are drawn from a Gamma distribution with specified parameters,
                shape (sometimes designated "k") and scale=1.
        
                Parameters
                ----------
                shape : float
                    Parameter, should be > 0.
                size : int or tuple of ints
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : ndarray or scalar
                    The drawn samples.
        
                See Also
                --------
                scipy.stats.distributions.gamma : probability density function,
                    distribution or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the Gamma distribution is
        
                .. math:: p(x) = x^{k-1}\frac{e^{-x/\theta}}{\theta^k\Gamma(k)},
        
                where :math:`k` is the shape and :math:`\theta` the scale,
                and :math:`\Gamma` is the Gamma function.
        
                The Gamma distribution is often used to model the times to failure of
                electronic components, and arises naturally in processes for which the
                waiting times between Poisson distributed events are relevant.
        
                References
                ----------
                .. [1] Weisstein, Eric W. "Gamma Distribution." From MathWorld--A
                       Wolfram Web Resource.
                       http://mathworld.wolfram.com/GammaDistribution.html
                .. [2] Wikipedia, "Gamma-distribution",
                       http://en.wikipedia.org/wiki/Gamma-distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> shape, scale = 2., 1. # mean and width
                >>> s = np.random.standard_gamma(shape, 1000000)
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> import scipy.special as sps
                >>> count, bins, ignored = plt.hist(s, 50, normed=True)
                >>> y = bins**(shape-1) * ((np.exp(-bins/scale))/ \
                ...                       (sps.gamma(shape) * scale**shape))
                >>> plt.plot(bins, y, linewidth=2, color='r')
                >>> plt.show()
        """
        pass

    def standard_normal(self, size=None): # real signature unknown; restored from __doc__
        """
        standard_normal(size=None)
        
                Returns samples from a Standard Normal distribution (mean=0, stdev=1).
        
                Parameters
                ----------
                size : int or tuple of ints, optional
                    Output shape. Default is None, in which case a single value is
                    returned.
        
                Returns
                -------
                out : float or ndarray
                    Drawn samples.
        
                Examples
                --------
                >>> s = np.random.standard_normal(8000)
                >>> s
                array([ 0.6888893 ,  0.78096262, -0.89086505, ...,  0.49876311, #random
                       -0.38672696, -0.4685006 ])                               #random
                >>> s.shape
                (8000,)
                >>> s = np.random.standard_normal(size=(3, 4, 2))
                >>> s.shape
                (3, 4, 2)
        """
        pass

    def standard_t(self, df, size=None): # real signature unknown; restored from __doc__
        """
        standard_t(df, size=None)
        
                Standard Student's t distribution with df degrees of freedom.
        
                A special case of the hyperbolic distribution.
                As `df` gets large, the result resembles that of the standard normal
                distribution (`standard_normal`).
        
                Parameters
                ----------
                df : int
                    Degrees of freedom, should be > 0.
                size : int or tuple of ints, optional
                    Output shape. Default is None, in which case a single value is
                    returned.
        
                Returns
                -------
                samples : ndarray or scalar
                    Drawn samples.
        
                Notes
                -----
                The probability density function for the t distribution is
        
                .. math:: P(x, df) = \frac{\Gamma(\frac{df+1}{2})}{\sqrt{\pi df}
                          \Gamma(\frac{df}{2})}\Bigl( 1+\frac{x^2}{df} \Bigr)^{-(df+1)/2}
        
                The t test is based on an assumption that the data come from a Normal
                distribution. The t test provides a way to test whether the sample mean
                (that is the mean calculated from the data) is a good estimate of the true
                mean.
        
                The derivation of the t-distribution was forst published in 1908 by William
                Gisset while working for the Guinness Brewery in Dublin. Due to proprietary
                issues, he had to publish under a pseudonym, and so he used the name
                Student.
        
                References
                ----------
                .. [1] Dalgaard, Peter, "Introductory Statistics With R",
                       Springer, 2002.
                .. [2] Wikipedia, "Student's t-distribution"
                       http://en.wikipedia.org/wiki/Student's_t-distribution
        
                Examples
                --------
                From Dalgaard page 83 [1]_, suppose the daily energy intake for 11
                women in Kj is:
        
                >>> intake = np.array([5260., 5470, 5640, 6180, 6390, 6515, 6805, 7515, \
                ...                    7515, 8230, 8770])
        
                Does their energy intake deviate systematically from the recommended
                value of 7725 kJ?
        
                We have 10 degrees of freedom, so is the sample mean within 95% of the
                recommended value?
        
                >>> s = np.random.standard_t(10, size=100000)
                >>> np.mean(intake)
                6753.636363636364
                >>> intake.std(ddof=1)
                1142.1232221373727
        
                Calculate the t statistic, setting the ddof parameter to the unbiased
                value so the divisor in the standard deviation will be degrees of
                freedom, N-1.
        
                >>> t = (np.mean(intake)-7725)/(intake.std(ddof=1)/np.sqrt(len(intake)))
                >>> import matplotlib.pyplot as plt
                >>> h = plt.hist(s, bins=100, normed=True)
        
                For a one-sided t-test, how far out in the distribution does the t
                statistic appear?
        
                >>> >>> np.sum(s<t) / float(len(s))
                0.0090699999999999999  #random
        
                So the p-value is about 0.009, which says the null hypothesis has a
                probability of about 99% of being true.
        """
        pass

    def tomaxint(self, size=None): # real signature unknown; restored from __doc__
        """
        tomaxint(size=None)
        
                Random integers between 0 and ``sys.maxint``, inclusive.
        
                Return a sample of uniformly distributed random integers in the interval
                [0, ``sys.maxint``].
        
                Parameters
                ----------
                size : tuple of ints, int, optional
                    Shape of output.  If this is, for example, (m,n,k), m*n*k samples
                    are generated.  If no shape is specified, a single sample is
                    returned.
        
                Returns
                -------
                out : ndarray
                    Drawn samples, with shape `size`.
        
                See Also
                --------
                randint : Uniform sampling over a given half-open interval of integers.
                random_integers : Uniform sampling over a given closed interval of
                    integers.
        
                Examples
                --------
                >>> RS = np.random.mtrand.RandomState() # need a RandomState object
                >>> RS.tomaxint((2,2,2))
                array([[[1170048599, 1600360186],
                        [ 739731006, 1947757578]],
                       [[1871712945,  752307660],
                        [1601631370, 1479324245]]])
                >>> import sys
                >>> sys.maxint
                2147483647
                >>> RS.tomaxint((2,2,2)) < sys.maxint
                array([[[ True,  True],
                        [ True,  True]],
                       [[ True,  True],
                        [ True,  True]]], dtype=bool)
        """
        pass

    def triangular(self, left, mode, right, size=None): # real signature unknown; restored from __doc__
        """
        triangular(left, mode, right, size=None)
        
                Draw samples from the triangular distribution.
        
                The triangular distribution is a continuous probability distribution with
                lower limit left, peak at mode, and upper limit right. Unlike the other
                distributions, these parameters directly define the shape of the pdf.
        
                Parameters
                ----------
                left : scalar
                    Lower limit.
                mode : scalar
                    The value where the peak of the distribution occurs.
                    The value should fulfill the condition ``left <= mode <= right``.
                right : scalar
                    Upper limit, should be larger than `left`.
                size : int or tuple of ints, optional
                    Output shape. Default is None, in which case a single value is
                    returned.
        
                Returns
                -------
                samples : ndarray or scalar
                    The returned samples all lie in the interval [left, right].
        
                Notes
                -----
                The probability density function for the Triangular distribution is
        
                .. math:: P(x;l, m, r) = \begin{cases}
                          \frac{2(x-l)}{(r-l)(m-l)}& \text{for $l \leq x \leq m$},\\
                          \frac{2(m-x)}{(r-l)(r-m)}& \text{for $m \leq x \leq r$},\\
                          0& \text{otherwise}.
                          \end{cases}
        
                The triangular distribution is often used in ill-defined problems where the
                underlying distribution is not known, but some knowledge of the limits and
                mode exists. Often it is used in simulations.
        
                References
                ----------
                .. [1] Wikipedia, "Triangular distribution"
                      http://en.wikipedia.org/wiki/Triangular_distribution
        
                Examples
                --------
                Draw values from the distribution and plot the histogram:
        
                >>> import matplotlib.pyplot as plt
                >>> h = plt.hist(np.random.triangular(-3, 0, 8, 100000), bins=200,
                ...              normed=True)
                >>> plt.show()
        """
        pass

    def uniform(self, low=0.0, high=1.0, size=1): # real signature unknown; restored from __doc__
        """
        uniform(low=0.0, high=1.0, size=1)
        
                Draw samples from a uniform distribution.
        
                Samples are uniformly distributed over the half-open interval
                ``[low, high)`` (includes low, but excludes high).  In other words,
                any value within the given interval is equally likely to be drawn
                by `uniform`.
        
                Parameters
                ----------
                low : float, optional
                    Lower boundary of the output interval.  All values generated will be
                    greater than or equal to low.  The default value is 0.
                high : float
                    Upper boundary of the output interval.  All values generated will be
                    less than high.  The default value is 1.0.
                size : int or tuple of ints, optional
                    Shape of output.  If the given size is, for example, (m,n,k),
                    m*n*k samples are generated.  If no shape is specified, a single sample
                    is returned.
        
                Returns
                -------
                out : ndarray
                    Drawn samples, with shape `size`.
        
                See Also
                --------
                randint : Discrete uniform distribution, yielding integers.
                random_integers : Discrete uniform distribution over the closed
                                  interval ``[low, high]``.
                random_sample : Floats uniformly distributed over ``[0, 1)``.
                random : Alias for `random_sample`.
                rand : Convenience function that accepts dimensions as input, e.g.,
                       ``rand(2,2)`` would generate a 2-by-2 array of floats,
                       uniformly distributed over ``[0, 1)``.
        
                Notes
                -----
                The probability density function of the uniform distribution is
        
                .. math:: p(x) = \frac{1}{b - a}
        
                anywhere within the interval ``[a, b)``, and zero elsewhere.
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> s = np.random.uniform(-1,0,1000)
        
                All values are within the given interval:
        
                >>> np.all(s >= -1)
                True
                >>> np.all(s < 0)
                True
        
                Display the histogram of the samples, along with the
                probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> count, bins, ignored = plt.hist(s, 15, normed=True)
                >>> plt.plot(bins, np.ones_like(bins), linewidth=2, color='r')
                >>> plt.show()
        """
        pass

    def vonmises(self, mu, kappa, size=None): # real signature unknown; restored from __doc__
        """
        vonmises(mu, kappa, size=None)
        
                Draw samples from a von Mises distribution.
        
                Samples are drawn from a von Mises distribution with specified mode
                (mu) and dispersion (kappa), on the interval [-pi, pi].
        
                The von Mises distribution (also known as the circular normal
                distribution) is a continuous probability distribution on the unit
                circle.  It may be thought of as the circular analogue of the normal
                distribution.
        
                Parameters
                ----------
                mu : float
                    Mode ("center") of the distribution.
                kappa : float
                    Dispersion of the distribution, has to be >=0.
                size : int or tuple of int
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                Returns
                -------
                samples : scalar or ndarray
                    The returned samples, which are in the interval [-pi, pi].
        
                See Also
                --------
                scipy.stats.distributions.vonmises : probability density function,
                    distribution, or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the von Mises distribution is
        
                .. math:: p(x) = \frac{e^{\kappa cos(x-\mu)}}{2\pi I_0(\kappa)},
        
                where :math:`\mu` is the mode and :math:`\kappa` the dispersion,
                and :math:`I_0(\kappa)` is the modified Bessel function of order 0.
        
                The von Mises is named for Richard Edler von Mises, who was born in
                Austria-Hungary, in what is now the Ukraine.  He fled to the United
                States in 1939 and became a professor at Harvard.  He worked in
                probability theory, aerodynamics, fluid mechanics, and philosophy of
                science.
        
                References
                ----------
                Abramowitz, M. and Stegun, I. A. (ed.), *Handbook of Mathematical
                Functions*, New York: Dover, 1965.
        
                von Mises, R., *Mathematical Theory of Probability and Statistics*,
                New York: Academic Press, 1964.
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> mu, kappa = 0.0, 4.0 # mean and dispersion
                >>> s = np.random.vonmises(mu, kappa, 1000)
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> import scipy.special as sps
                >>> count, bins, ignored = plt.hist(s, 50, normed=True)
                >>> x = np.arange(-np.pi, np.pi, 2*np.pi/50.)
                >>> y = -np.exp(kappa*np.cos(x-mu))/(2*np.pi*sps.jn(0,kappa))
                >>> plt.plot(x, y/max(y), linewidth=2, color='r')
                >>> plt.show()
        """
        pass

    def wald(self, mean, scale, size=None): # real signature unknown; restored from __doc__
        """
        wald(mean, scale, size=None)
        
                Draw samples from a Wald, or Inverse Gaussian, distribution.
        
                As the scale approaches infinity, the distribution becomes more like a
                Gaussian.
        
                Some references claim that the Wald is an Inverse Gaussian with mean=1, but
                this is by no means universal.
        
                The Inverse Gaussian distribution was first studied in relationship to
                Brownian motion. In 1956 M.C.K. Tweedie used the name Inverse Gaussian
                because there is an inverse relationship between the time to cover a unit
                distance and distance covered in unit time.
        
                Parameters
                ----------
                mean : scalar
                    Distribution mean, should be > 0.
                scale : scalar
                    Scale parameter, should be >= 0.
                size : int or tuple of ints, optional
                    Output shape. Default is None, in which case a single value is
                    returned.
        
                Returns
                -------
                samples : ndarray or scalar
                    Drawn sample, all greater than zero.
        
                Notes
                -----
                The probability density function for the Wald distribution is
        
                .. math:: P(x;mean,scale) = \sqrt{\frac{scale}{2\pi x^3}}e^
                                            \frac{-scale(x-mean)^2}{2\cdotp mean^2x}
        
                As noted above the Inverse Gaussian distribution first arise from attempts
                to model Brownian Motion. It is also a competitor to the Weibull for use in
                reliability modeling and modeling stock returns and interest rate
                processes.
        
                References
                ----------
                .. [1] Brighton Webs Ltd., Wald Distribution,
                      http://www.brighton-webs.co.uk/distributions/wald.asp
                .. [2] Chhikara, Raj S., and Folks, J. Leroy, "The Inverse Gaussian
                      Distribution: Theory : Methodology, and Applications", CRC Press,
                      1988.
                .. [3] Wikipedia, "Wald distribution"
                      http://en.wikipedia.org/wiki/Wald_distribution
        
                Examples
                --------
                Draw values from the distribution and plot the histogram:
        
                >>> import matplotlib.pyplot as plt
                >>> h = plt.hist(np.random.wald(3, 2, 100000), bins=200, normed=True)
                >>> plt.show()
        """
        pass

    def weibull(self, a, size=None): # real signature unknown; restored from __doc__
        """
        weibull(a, size=None)
        
                Weibull distribution.
        
                Draw samples from a 1-parameter Weibull distribution with the given
                shape parameter `a`.
        
                .. math:: X = (-ln(U))^{1/a}
        
                Here, U is drawn from the uniform distribution over (0,1].
        
                The more common 2-parameter Weibull, including a scale parameter
                :math:`\lambda` is just :math:`X = \lambda(-ln(U))^{1/a}`.
        
                Parameters
                ----------
                a : float
                    Shape of the distribution.
                size : tuple of ints
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn.
        
                See Also
                --------
                scipy.stats.distributions.weibull_max
                scipy.stats.distributions.weibull_min
                scipy.stats.distributions.genextreme
                gumbel
        
                Notes
                -----
                The Weibull (or Type III asymptotic extreme value distribution for smallest
                values, SEV Type III, or Rosin-Rammler distribution) is one of a class of
                Generalized Extreme Value (GEV) distributions used in modeling extreme
                value problems.  This class includes the Gumbel and Frechet distributions.
        
                The probability density for the Weibull distribution is
        
                .. math:: p(x) = \frac{a}
                                 {\lambda}(\frac{x}{\lambda})^{a-1}e^{-(x/\lambda)^a},
        
                where :math:`a` is the shape and :math:`\lambda` the scale.
        
                The function has its peak (the mode) at
                :math:`\lambda(\frac{a-1}{a})^{1/a}`.
        
                When ``a = 1``, the Weibull distribution reduces to the exponential
                distribution.
        
                References
                ----------
                .. [1] Waloddi Weibull, Professor, Royal Technical University, Stockholm,
                       1939 "A Statistical Theory Of The Strength Of Materials",
                       Ingeniorsvetenskapsakademiens Handlingar Nr 151, 1939,
                       Generalstabens Litografiska Anstalts Forlag, Stockholm.
                .. [2] Waloddi Weibull, 1951 "A Statistical Distribution Function of Wide
                       Applicability",  Journal Of Applied Mechanics ASME Paper.
                .. [3] Wikipedia, "Weibull distribution",
                       http://en.wikipedia.org/wiki/Weibull_distribution
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> a = 5. # shape
                >>> s = np.random.weibull(a, 1000)
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> x = np.arange(1,100.)/50.
                >>> def weib(x,n,a):
                ...     return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)
        
                >>> count, bins, ignored = plt.hist(np.random.weibull(5.,1000))
                >>> x = np.arange(1,100.)/50.
                >>> scale = count.max()/weib(x, 1., 5.).max()
                >>> plt.plot(x, weib(x, 1., 5.)*scale)
                >>> plt.show()
        """
        pass

    def zipf(self, a, size=None): # real signature unknown; restored from __doc__
        """
        zipf(a, size=None)
        
                Draw samples from a Zipf distribution.
        
                Samples are drawn from a Zipf distribution with specified parameter
                `a` > 1.
        
                The Zipf distribution (also known as the zeta distribution) is a
                continuous probability distribution that satisfies Zipf's law: the
                frequency of an item is inversely proportional to its rank in a
                frequency table.
        
                Parameters
                ----------
                a : float > 1
                    Distribution parameter.
                size : int or tuple of int, optional
                    Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
                    ``m * n * k`` samples are drawn; a single integer is equivalent in
                    its result to providing a mono-tuple, i.e., a 1-D array of length
                    *size* is returned.  The default is None, in which case a single
                    scalar is returned.
        
                Returns
                -------
                samples : scalar or ndarray
                    The returned samples are greater than or equal to one.
        
                See Also
                --------
                scipy.stats.distributions.zipf : probability density function,
                    distribution, or cumulative density function, etc.
        
                Notes
                -----
                The probability density for the Zipf distribution is
        
                .. math:: p(x) = \frac{x^{-a}}{\zeta(a)},
        
                where :math:`\zeta` is the Riemann Zeta function.
        
                It is named for the American linguist George Kingsley Zipf, who noted
                that the frequency of any word in a sample of a language is inversely
                proportional to its rank in the frequency table.
        
                References
                ----------
                Zipf, G. K., *Selected Studies of the Principle of Relative Frequency
                in Language*, Cambridge, MA: Harvard Univ. Press, 1932.
        
                Examples
                --------
                Draw samples from the distribution:
        
                >>> a = 2. # parameter
                >>> s = np.random.zipf(a, 1000)
        
                Display the histogram of the samples, along with
                the probability density function:
        
                >>> import matplotlib.pyplot as plt
                >>> import scipy.special as sps
                Truncate s values at 50 so plot is interesting
                >>> count, bins, ignored = plt.hist(s[s<50], 50, normed=True)
                >>> x = np.arange(1., 50.)
                >>> y = x**(-a)/sps.zetac(a)
                >>> plt.plot(x, y/max(y), linewidth=2, color='r')
                >>> plt.show()
        """
        pass

    def __getstate__(self, *args, **kwargs): # real signature unknown
        pass

    def __init__(self, seed=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __reduce__(self, *args, **kwargs): # real signature unknown
        pass

    def __setstate__(self, *args, **kwargs): # real signature unknown
        pass

    poisson_lam_max = 9.223372006484771e+18


# variables with complex values

_rand = None # (!) real value is ''

__test__ = {
    u'RandomState.binomial (line 3416)': u'\n        binomial(n, p, size=None)\n\n        Draw samples from a binomial distribution.\n\n        Samples are drawn from a Binomial distribution with specified\n        parameters, n trials and p probability of success where\n        n an integer >= 0 and p is in the interval [0,1]. (n may be\n        input as a float, but it is truncated to an integer in use)\n\n        Parameters\n        ----------\n        n : float (but truncated to an integer)\n                parameter, >= 0.\n        p : float\n                parameter, >= 0 and <=1.\n        size : {tuple, int}\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : {ndarray, scalar}\n                  where the values are all integers in  [0, n].\n\n        See Also\n        --------\n        scipy.stats.distributions.binom : probability density function,\n            distribution or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the Binomial distribution is\n\n        .. math:: P(N) = \\binom{n}{N}p^N(1-p)^{n-N},\n\n        where :math:`n` is the number of trials, :math:`p` is the probability\n        of success, and :math:`N` is the number of successes.\n\n        When estimating the standard error of a proportion in a population by\n        using a random sample, the normal distribution works well unless the\n        product p*n <=5, where p = population proportion estimate, and n =\n        number of samples, in which case the binomial distribution is used\n        instead. For example, a sample of 15 people shows 4 who are left\n        handed, and 11 who are right handed. Then p = 4/15 = 27%. 0.27*15 = 4,\n        so the binomial distribution should be used in this case.\n\n        References\n        ----------\n        .. [1] Dalgaard, Peter, "Introductory Statistics with R",\n               Springer-Verlag, 2002.\n        .. [2] Glantz, Stanton A. "Primer of Biostatistics.", McGraw-Hill,\n               Fifth Edition, 2002.\n        .. [3] Lentner, Marvin, "Elementary Applied Statistics", Bogden\n               and Quigley, 1972.\n        .. [4] Weisstein, Eric W. "Binomial Distribution." From MathWorld--A\n               Wolfram Web Resource.\n               http://mathworld.wolfram.com/BinomialDistribution.html\n        .. [5] Wikipedia, "Binomial-distribution",\n               http://en.wikipedia.org/wiki/Binomial_distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> n, p = 10, .5 # number of trials, probability of each trial\n        >>> s = np.random.binomial(n, p, 1000)\n        # result of flipping a coin 10 times, tested 1000 times.\n\n        A real world example. A company drills 9 wild-cat oil exploration\n        wells, each with an estimated probability of success of 0.1. All nine\n        wells fail. What is the probability of that happening?\n\n        Let\'s do 20,000 trials of the model, and count the number that\n        generate zero positive results.\n\n        >>> sum(np.random.binomial(9,0.1,20000)==0)/20000.\n        answer = 0.38885, or 38%.\n\n        ',
    u'RandomState.bytes (line 900)': u"\n        bytes(length)\n\n        Return random bytes.\n\n        Parameters\n        ----------\n        length : int\n            Number of random bytes.\n\n        Returns\n        -------\n        out : str\n            String of length `length`.\n\n        Examples\n        --------\n        >>> np.random.bytes(10)\n        ' eh\\x85\\x022SZ\\xbf\\xa4' #random\n\n        ",
    u'RandomState.chisquare (line 2009)': u'\n        chisquare(df, size=None)\n\n        Draw samples from a chi-square distribution.\n\n        When `df` independent random variables, each with standard normal\n        distributions (mean 0, variance 1), are squared and summed, the\n        resulting distribution is chi-square (see Notes).  This distribution\n        is often used in hypothesis testing.\n\n        Parameters\n        ----------\n        df : int\n             Number of degrees of freedom.\n        size : tuple of ints, int, optional\n             Size of the returned array.  By default, a scalar is\n             returned.\n\n        Returns\n        -------\n        output : ndarray\n            Samples drawn from the distribution, packed in a `size`-shaped\n            array.\n\n        Raises\n        ------\n        ValueError\n            When `df` <= 0 or when an inappropriate `size` (e.g. ``size=-1``)\n            is given.\n\n        Notes\n        -----\n        The variable obtained by summing the squares of `df` independent,\n        standard normally distributed random variables:\n\n        .. math:: Q = \\sum_{i=0}^{\\mathtt{df}} X^2_i\n\n        is chi-square distributed, denoted\n\n        .. math:: Q \\sim \\chi^2_k.\n\n        The probability density function of the chi-squared distribution is\n\n        .. math:: p(x) = \\frac{(1/2)^{k/2}}{\\Gamma(k/2)}\n                         x^{k/2 - 1} e^{-x/2},\n\n        where :math:`\\Gamma` is the gamma function,\n\n        .. math:: \\Gamma(x) = \\int_0^{-\\infty} t^{x - 1} e^{-t} dt.\n\n        References\n        ----------\n        `NIST/SEMATECH e-Handbook of Statistical Methods\n        <http://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm>`_\n\n        Examples\n        --------\n        >>> np.random.chisquare(2,4)\n        array([ 1.89920014,  9.00867716,  3.13710533,  5.62318272])\n\n        ',
    u'RandomState.choice (line 928)': u"\n        choice(a, size=None, replace=True, p=None)\n\n        Generates a random sample from a given 1-D array\n\n                .. versionadded:: 1.7.0\n\n        Parameters\n        -----------\n        a : 1-D array-like or int\n            If an ndarray, a random sample is generated from its elements.\n            If an int, the random sample is generated as if a was np.arange(n)\n        size : int or tuple of ints, optional\n            Output shape. Default is None, in which case a single value is\n            returned.\n        replace : boolean, optional\n            Whether the sample is with or without replacement\n        p : 1-D array-like, optional\n            The probabilities associated with each entry in a.\n            If not given the sample assumes a uniform distribtion over all\n            entries in a.\n\n        Returns\n        --------\n        samples : 1-D ndarray, shape (size,)\n            The generated random samples\n\n        Raises\n        -------\n        ValueError\n            If a is an int and less than zero, if a or p are not 1-dimensional,\n            if a is an array-like of size 0, if p is not a vector of\n            probabilities, if a and p have different lengths, or if\n            replace=False and the sample size is greater than the population\n            size\n\n        See Also\n        ---------\n        randint, shuffle, permutation\n\n        Examples\n        ---------\n        Generate a uniform random sample from np.arange(5) of size 3:\n\n        >>> np.random.choice(5, 3)\n        array([0, 3, 4])\n        >>> #This is equivalent to np.random.randint(0,5,3)\n\n        Generate a non-uniform random sample from np.arange(5) of size 3:\n\n        >>> np.random.choice(5, 3, p=[0.1, 0, 0.3, 0.6, 0])\n        array([3, 3, 0])\n\n        Generate a uniform random sample from np.arange(5) of size 3 without\n        replacement:\n\n        >>> np.random.choice(5, 3, replace=False)\n        array([3,1,0])\n        >>> #This is equivalent to np.random.shuffle(np.arange(5))[:3]\n\n        Generate a non-uniform random sample from np.arange(5) of size\n        3 without replacement:\n\n        >>> np.random.choice(5, 3, replace=False, p=[0.1, 0, 0.3, 0.6, 0])\n        array([2, 3, 0])\n\n        Any of the above can be repeated with an arbitrary array-like\n        instead of just integers. For instance:\n\n        >>> aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']\n        >>> np.random.choice(aa_milne_arr, 5, p=[0.5, 0.1, 0.1, 0.3])\n        array(['pooh', 'pooh', 'pooh', 'Christopher', 'piglet'],\n              dtype='|S11')\n\n        ",
    u'RandomState.dirichlet (line 4278)': u'\n        dirichlet(alpha, size=None)\n\n        Draw samples from the Dirichlet distribution.\n\n        Draw `size` samples of dimension k from a Dirichlet distribution. A\n        Dirichlet-distributed random variable can be seen as a multivariate\n        generalization of a Beta distribution. Dirichlet pdf is the conjugate\n        prior of a multinomial in Bayesian inference.\n\n        Parameters\n        ----------\n        alpha : array\n            Parameter of the distribution (k dimension for sample of\n            dimension k).\n        size : array\n            Number of samples to draw.\n\n        Returns\n        -------\n        samples : ndarray,\n            The drawn samples, of shape (alpha.ndim, size).\n\n        Notes\n        -----\n        .. math:: X \\approx \\prod_{i=1}^{k}{x^{\\alpha_i-1}_i}\n\n        Uses the following property for computation: for each dimension,\n        draw a random sample y_i from a standard gamma generator of shape\n        `alpha_i`, then\n        :math:`X = \\frac{1}{\\sum_{i=1}^k{y_i}} (y_1, \\ldots, y_n)` is\n        Dirichlet distributed.\n\n        References\n        ----------\n        .. [1] David McKay, "Information Theory, Inference and Learning\n               Algorithms," chapter 23,\n               http://www.inference.phy.cam.ac.uk/mackay/\n        .. [2] Wikipedia, "Dirichlet distribution",\n               http://en.wikipedia.org/wiki/Dirichlet_distribution\n\n        Examples\n        --------\n        Taking an example cited in Wikipedia, this distribution can be used if\n        one wanted to cut strings (each of initial length 1.0) into K pieces\n        with different lengths, where each piece had, on average, a designated\n        average length, but allowing some variation in the relative sizes of the\n        pieces.\n\n        >>> s = np.random.dirichlet((10, 5, 3), 20).transpose()\n\n        >>> plt.barh(range(20), s[0])\n        >>> plt.barh(range(20), s[1], left=s[0], color=\'g\')\n        >>> plt.barh(range(20), s[2], left=s[0]+s[1], color=\'r\')\n        >>> plt.title("Lengths of Strings")\n\n        ',
    u'RandomState.f (line 1812)': u'\n        f(dfnum, dfden, size=None)\n\n        Draw samples from a F distribution.\n\n        Samples are drawn from an F distribution with specified parameters,\n        `dfnum` (degrees of freedom in numerator) and `dfden` (degrees of freedom\n        in denominator), where both parameters should be greater than zero.\n\n        The random variate of the F distribution (also known as the\n        Fisher distribution) is a continuous probability distribution\n        that arises in ANOVA tests, and is the ratio of two chi-square\n        variates.\n\n        Parameters\n        ----------\n        dfnum : float\n            Degrees of freedom in numerator. Should be greater than zero.\n        dfden : float\n            Degrees of freedom in denominator. Should be greater than zero.\n        size : {tuple, int}, optional\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``,\n            then ``m * n * k`` samples are drawn. By default only one sample\n            is returned.\n\n        Returns\n        -------\n        samples : {ndarray, scalar}\n            Samples from the Fisher distribution.\n\n        See Also\n        --------\n        scipy.stats.distributions.f : probability density function,\n            distribution or cumulative density function, etc.\n\n        Notes\n        -----\n        The F statistic is used to compare in-group variances to between-group\n        variances. Calculating the distribution depends on the sampling, and\n        so it is a function of the respective degrees of freedom in the\n        problem.  The variable `dfnum` is the number of samples minus one, the\n        between-groups degrees of freedom, while `dfden` is the within-groups\n        degrees of freedom, the sum of the number of samples in each group\n        minus the number of groups.\n\n        References\n        ----------\n        .. [1] Glantz, Stanton A. "Primer of Biostatistics.", McGraw-Hill,\n               Fifth Edition, 2002.\n        .. [2] Wikipedia, "F-distribution",\n               http://en.wikipedia.org/wiki/F-distribution\n\n        Examples\n        --------\n        An example from Glantz[1], pp 47-40.\n        Two groups, children of diabetics (25 people) and children from people\n        without diabetes (25 controls). Fasting blood glucose was measured,\n        case group had a mean value of 86.1, controls had a mean value of\n        82.2. Standard deviations were 2.09 and 2.49 respectively. Are these\n        data consistent with the null hypothesis that the parents diabetic\n        status does not affect their children\'s blood glucose levels?\n        Calculating the F statistic from the data gives a value of 36.01.\n\n        Draw samples from the distribution:\n\n        >>> dfnum = 1. # between group degrees of freedom\n        >>> dfden = 48. # within groups degrees of freedom\n        >>> s = np.random.f(dfnum, dfden, 1000)\n\n        The lower bound for the top 1% of the samples is :\n\n        >>> sort(s)[-10]\n        7.61988120985\n\n        So there is about a 1% chance that the F statistic will exceed 7.62,\n        the measured value is 36, so the null hypothesis is rejected at the 1%\n        level.\n\n        ',
    u'RandomState.gamma (line 1721)': u'\n        gamma(shape, scale=1.0, size=None)\n\n        Draw samples from a Gamma distribution.\n\n        Samples are drawn from a Gamma distribution with specified parameters,\n        `shape` (sometimes designated "k") and `scale` (sometimes designated\n        "theta"), where both parameters are > 0.\n\n        Parameters\n        ----------\n        shape : scalar > 0\n            The shape of the gamma distribution.\n        scale : scalar > 0, optional\n            The scale of the gamma distribution.  Default is equal to 1.\n        size : shape_tuple, optional\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        out : ndarray, float\n            Returns one sample unless `size` parameter is specified.\n\n        See Also\n        --------\n        scipy.stats.distributions.gamma : probability density function,\n            distribution or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the Gamma distribution is\n\n        .. math:: p(x) = x^{k-1}\\frac{e^{-x/\\theta}}{\\theta^k\\Gamma(k)},\n\n        where :math:`k` is the shape and :math:`\\theta` the scale,\n        and :math:`\\Gamma` is the Gamma function.\n\n        The Gamma distribution is often used to model the times to failure of\n        electronic components, and arises naturally in processes for which the\n        waiting times between Poisson distributed events are relevant.\n\n        References\n        ----------\n        .. [1] Weisstein, Eric W. "Gamma Distribution." From MathWorld--A\n               Wolfram Web Resource.\n               http://mathworld.wolfram.com/GammaDistribution.html\n        .. [2] Wikipedia, "Gamma-distribution",\n               http://en.wikipedia.org/wiki/Gamma-distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> shape, scale = 2., 2. # mean and dispersion\n        >>> s = np.random.gamma(shape, scale, 1000)\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> import scipy.special as sps\n        >>> count, bins, ignored = plt.hist(s, 50, normed=True)\n        >>> y = bins**(shape-1)*(np.exp(-bins/scale) /\n        ...                      (sps.gamma(shape)*scale**shape))\n        >>> plt.plot(bins, y, linewidth=2, color=\'r\')\n        >>> plt.show()\n\n        ',
    u'RandomState.geometric (line 3778)': u'\n        geometric(p, size=None)\n\n        Draw samples from the geometric distribution.\n\n        Bernoulli trials are experiments with one of two outcomes:\n        success or failure (an example of such an experiment is flipping\n        a coin).  The geometric distribution models the number of trials\n        that must be run in order to achieve success.  It is therefore\n        supported on the positive integers, ``k = 1, 2, ...``.\n\n        The probability mass function of the geometric distribution is\n\n        .. math:: f(k) = (1 - p)^{k - 1} p\n\n        where `p` is the probability of success of an individual trial.\n\n        Parameters\n        ----------\n        p : float\n            The probability of success of an individual trial.\n        size : tuple of ints\n            Number of values to draw from the distribution.  The output\n            is shaped according to `size`.\n\n        Returns\n        -------\n        out : ndarray\n            Samples from the geometric distribution, shaped according to\n            `size`.\n\n        Examples\n        --------\n        Draw ten thousand values from the geometric distribution,\n        with the probability of an individual success equal to 0.35:\n\n        >>> z = np.random.geometric(p=0.35, size=10000)\n\n        How many trials succeeded after a single run?\n\n        >>> (z == 1).sum() / 10000.\n        0.34889999999999999 #random\n\n        ',
    u'RandomState.gumbel (line 2830)': u'\n        gumbel(loc=0.0, scale=1.0, size=None)\n\n        Gumbel distribution.\n\n        Draw samples from a Gumbel distribution with specified location and scale.\n        For more information on the Gumbel distribution, see Notes and References\n        below.\n\n        Parameters\n        ----------\n        loc : float\n            The location of the mode of the distribution.\n        scale : float\n            The scale parameter of the distribution.\n        size : tuple of ints\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        out : ndarray\n            The samples\n\n        See Also\n        --------\n        scipy.stats.gumbel_l\n        scipy.stats.gumbel_r\n        scipy.stats.genextreme\n            probability density function, distribution, or cumulative density\n            function, etc. for each of the above\n        weibull\n\n        Notes\n        -----\n        The Gumbel (or Smallest Extreme Value (SEV) or the Smallest Extreme Value\n        Type I) distribution is one of a class of Generalized Extreme Value (GEV)\n        distributions used in modeling extreme value problems.  The Gumbel is a\n        special case of the Extreme Value Type I distribution for maximums from\n        distributions with "exponential-like" tails.\n\n        The probability density for the Gumbel distribution is\n\n        .. math:: p(x) = \\frac{e^{-(x - \\mu)/ \\beta}}{\\beta} e^{ -e^{-(x - \\mu)/\n                  \\beta}},\n\n        where :math:`\\mu` is the mode, a location parameter, and :math:`\\beta` is\n        the scale parameter.\n\n        The Gumbel (named for German mathematician Emil Julius Gumbel) was used\n        very early in the hydrology literature, for modeling the occurrence of\n        flood events. It is also used for modeling maximum wind speed and rainfall\n        rates.  It is a "fat-tailed" distribution - the probability of an event in\n        the tail of the distribution is larger than if one used a Gaussian, hence\n        the surprisingly frequent occurrence of 100-year floods. Floods were\n        initially modeled as a Gaussian process, which underestimated the frequency\n        of extreme events.\n\n\n        It is one of a class of extreme value distributions, the Generalized\n        Extreme Value (GEV) distributions, which also includes the Weibull and\n        Frechet.\n\n        The function has a mean of :math:`\\mu + 0.57721\\beta` and a variance of\n        :math:`\\frac{\\pi^2}{6}\\beta^2`.\n\n        References\n        ----------\n        Gumbel, E. J., *Statistics of Extremes*, New York: Columbia University\n        Press, 1958.\n\n        Reiss, R.-D. and Thomas, M., *Statistical Analysis of Extreme Values from\n        Insurance, Finance, Hydrology and Other Fields*, Basel: Birkhauser Verlag,\n        2001.\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> mu, beta = 0, 0.1 # location and scale\n        >>> s = np.random.gumbel(mu, beta, 1000)\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> count, bins, ignored = plt.hist(s, 30, normed=True)\n        >>> plt.plot(bins, (1/beta)*np.exp(-(bins - mu)/beta)\n        ...          * np.exp( -np.exp( -(bins - mu) /beta) ),\n        ...          linewidth=2, color=\'r\')\n        >>> plt.show()\n\n        Show how an extreme value distribution can arise from a Gaussian process\n        and compare to a Gaussian:\n\n        >>> means = []\n        >>> maxima = []\n        >>> for i in range(0,1000) :\n        ...    a = np.random.normal(mu, beta, 1000)\n        ...    means.append(a.mean())\n        ...    maxima.append(a.max())\n        >>> count, bins, ignored = plt.hist(maxima, 30, normed=True)\n        >>> beta = np.std(maxima)*np.pi/np.sqrt(6)\n        >>> mu = np.mean(maxima) - 0.57721*beta\n        >>> plt.plot(bins, (1/beta)*np.exp(-(bins - mu)/beta)\n        ...          * np.exp(-np.exp(-(bins - mu)/beta)),\n        ...          linewidth=2, color=\'r\')\n        >>> plt.plot(bins, 1/(beta * np.sqrt(2 * np.pi))\n        ...          * np.exp(-(bins - mu)**2 / (2 * beta**2)),\n        ...          linewidth=2, color=\'g\')\n        >>> plt.show()\n\n        ',
    u'RandomState.hypergeometric (line 3844)': u'\n        hypergeometric(ngood, nbad, nsample, size=None)\n\n        Draw samples from a Hypergeometric distribution.\n\n        Samples are drawn from a Hypergeometric distribution with specified\n        parameters, ngood (ways to make a good selection), nbad (ways to make\n        a bad selection), and nsample = number of items sampled, which is less\n        than or equal to the sum ngood + nbad.\n\n        Parameters\n        ----------\n        ngood : int or array_like\n            Number of ways to make a good selection.  Must be nonnegative.\n        nbad : int or array_like\n            Number of ways to make a bad selection.  Must be nonnegative.\n        nsample : int or array_like\n            Number of items sampled.  Must be at least 1 and at most\n            ``ngood + nbad``.\n        size : int or tuple of int\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : ndarray or scalar\n            The values are all integers in  [0, n].\n\n        See Also\n        --------\n        scipy.stats.distributions.hypergeom : probability density function,\n            distribution or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the Hypergeometric distribution is\n\n        .. math:: P(x) = \\frac{\\binom{m}{n}\\binom{N-m}{n-x}}{\\binom{N}{n}},\n\n        where :math:`0 \\le x \\le m` and :math:`n+m-N \\le x \\le n`\n\n        for P(x) the probability of x successes, n = ngood, m = nbad, and\n        N = number of samples.\n\n        Consider an urn with black and white marbles in it, ngood of them\n        black and nbad are white. If you draw nsample balls without\n        replacement, then the Hypergeometric distribution describes the\n        distribution of black balls in the drawn sample.\n\n        Note that this distribution is very similar to the Binomial\n        distribution, except that in this case, samples are drawn without\n        replacement, whereas in the Binomial case samples are drawn with\n        replacement (or the sample space is infinite). As the sample space\n        becomes large, this distribution approaches the Binomial.\n\n        References\n        ----------\n        .. [1] Lentner, Marvin, "Elementary Applied Statistics", Bogden\n               and Quigley, 1972.\n        .. [2] Weisstein, Eric W. "Hypergeometric Distribution." From\n               MathWorld--A Wolfram Web Resource.\n               http://mathworld.wolfram.com/HypergeometricDistribution.html\n        .. [3] Wikipedia, "Hypergeometric-distribution",\n               http://en.wikipedia.org/wiki/Hypergeometric-distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> ngood, nbad, nsamp = 100, 2, 10\n        # number of good, number of bad, and number of samples\n        >>> s = np.random.hypergeometric(ngood, nbad, nsamp, 1000)\n        >>> hist(s)\n        #   note that it is very unlikely to grab both bad items\n\n        Suppose you have an urn with 15 white and 15 black marbles.\n        If you pull 15 marbles at random, how likely is it that\n        12 or more of them are one color?\n\n        >>> s = np.random.hypergeometric(15, 15, 15, 100000)\n        >>> sum(s>=12)/100000. + sum(s<=3)/100000.\n        #   answer = 0.003 ... pretty unlikely!\n\n        ',
    u'RandomState.laplace (line 2740)': u'\n        laplace(loc=0.0, scale=1.0, size=None)\n\n        Draw samples from the Laplace or double exponential distribution with\n        specified location (or mean) and scale (decay).\n\n        The Laplace distribution is similar to the Gaussian/normal distribution,\n        but is sharper at the peak and has fatter tails. It represents the\n        difference between two independent, identically distributed exponential\n        random variables.\n\n        Parameters\n        ----------\n        loc : float\n            The position, :math:`\\mu`, of the distribution peak.\n        scale : float\n            :math:`\\lambda`, the exponential decay.\n\n        Notes\n        -----\n        It has the probability density function\n\n        .. math:: f(x; \\mu, \\lambda) = \\frac{1}{2\\lambda}\n                                       \\exp\\left(-\\frac{|x - \\mu|}{\\lambda}\\right).\n\n        The first law of Laplace, from 1774, states that the frequency of an error\n        can be expressed as an exponential function of the absolute magnitude of\n        the error, which leads to the Laplace distribution. For many problems in\n        Economics and Health sciences, this distribution seems to model the data\n        better than the standard Gaussian distribution\n\n\n        References\n        ----------\n        .. [1] Abramowitz, M. and Stegun, I. A. (Eds.). Handbook of Mathematical\n               Functions with Formulas, Graphs, and Mathematical Tables, 9th\n               printing.  New York: Dover, 1972.\n\n        .. [2] The Laplace distribution and generalizations\n               By Samuel Kotz, Tomasz J. Kozubowski, Krzysztof Podgorski,\n               Birkhauser, 2001.\n\n        .. [3] Weisstein, Eric W. "Laplace Distribution."\n               From MathWorld--A Wolfram Web Resource.\n               http://mathworld.wolfram.com/LaplaceDistribution.html\n\n        .. [4] Wikipedia, "Laplace distribution",\n               http://en.wikipedia.org/wiki/Laplace_distribution\n\n        Examples\n        --------\n        Draw samples from the distribution\n\n        >>> loc, scale = 0., 1.\n        >>> s = np.random.laplace(loc, scale, 1000)\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> count, bins, ignored = plt.hist(s, 30, normed=True)\n        >>> x = np.arange(-8., 8., .01)\n        >>> pdf = np.exp(-abs(x-loc/scale))/(2.*scale)\n        >>> plt.plot(x, pdf)\n\n        Plot Gaussian for comparison:\n\n        >>> g = (1/(scale * np.sqrt(2 * np.pi)) * \n        ...      np.exp( - (x - loc)**2 / (2 * scale**2) ))\n        >>> plt.plot(x,g)\n\n        ',
    u'RandomState.logistic (line 2961)': u'\n        logistic(loc=0.0, scale=1.0, size=None)\n\n        Draw samples from a Logistic distribution.\n\n        Samples are drawn from a Logistic distribution with specified\n        parameters, loc (location or mean, also median), and scale (>0).\n\n        Parameters\n        ----------\n        loc : float\n\n        scale : float > 0.\n\n        size : {tuple, int}\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : {ndarray, scalar}\n                  where the values are all integers in  [0, n].\n\n        See Also\n        --------\n        scipy.stats.distributions.logistic : probability density function,\n            distribution or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the Logistic distribution is\n\n        .. math:: P(x) = P(x) = \\frac{e^{-(x-\\mu)/s}}{s(1+e^{-(x-\\mu)/s})^2},\n\n        where :math:`\\mu` = location and :math:`s` = scale.\n\n        The Logistic distribution is used in Extreme Value problems where it\n        can act as a mixture of Gumbel distributions, in Epidemiology, and by\n        the World Chess Federation (FIDE) where it is used in the Elo ranking\n        system, assuming the performance of each player is a logistically\n        distributed random variable.\n\n        References\n        ----------\n        .. [1] Reiss, R.-D. and Thomas M. (2001), Statistical Analysis of Extreme\n               Values, from Insurance, Finance, Hydrology and Other Fields,\n               Birkhauser Verlag, Basel, pp 132-133.\n        .. [2] Weisstein, Eric W. "Logistic Distribution." From\n               MathWorld--A Wolfram Web Resource.\n               http://mathworld.wolfram.com/LogisticDistribution.html\n        .. [3] Wikipedia, "Logistic-distribution",\n               http://en.wikipedia.org/wiki/Logistic-distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> loc, scale = 10, 1\n        >>> s = np.random.logistic(loc, scale, 10000)\n        >>> count, bins, ignored = plt.hist(s, bins=50)\n\n        #   plot against distribution\n\n        >>> def logist(x, loc, scale):\n        ...     return exp((loc-x)/scale)/(scale*(1+exp((loc-x)/scale))**2)\n        >>> plt.plot(bins, logist(bins, loc, scale)*count.max()/\\\n        ... logist(bins, loc, scale).max())\n        >>> plt.show()\n\n        ',
    u'RandomState.lognormal (line 3049)': u'\n        lognormal(mean=0.0, sigma=1.0, size=None)\n\n        Return samples drawn from a log-normal distribution.\n\n        Draw samples from a log-normal distribution with specified mean,\n        standard deviation, and array shape.  Note that the mean and standard\n        deviation are not the values for the distribution itself, but of the\n        underlying normal distribution it is derived from.\n\n        Parameters\n        ----------\n        mean : float\n            Mean value of the underlying normal distribution\n        sigma : float, > 0.\n            Standard deviation of the underlying normal distribution\n        size : tuple of ints\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : ndarray or float\n            The desired samples. An array of the same shape as `size` if given,\n            if `size` is None a float is returned.\n\n        See Also\n        --------\n        scipy.stats.lognorm : probability density function, distribution,\n            cumulative density function, etc.\n\n        Notes\n        -----\n        A variable `x` has a log-normal distribution if `log(x)` is normally\n        distributed.  The probability density function for the log-normal\n        distribution is:\n\n        .. math:: p(x) = \\frac{1}{\\sigma x \\sqrt{2\\pi}}\n                         e^{(-\\frac{(ln(x)-\\mu)^2}{2\\sigma^2})}\n\n        where :math:`\\mu` is the mean and :math:`\\sigma` is the standard\n        deviation of the normally distributed logarithm of the variable.\n        A log-normal distribution results if a random variable is the *product*\n        of a large number of independent, identically-distributed variables in\n        the same way that a normal distribution results if the variable is the\n        *sum* of a large number of independent, identically-distributed\n        variables.\n\n        References\n        ----------\n        Limpert, E., Stahel, W. A., and Abbt, M., "Log-normal Distributions\n        across the Sciences: Keys and Clues," *BioScience*, Vol. 51, No. 5,\n        May, 2001.  http://stat.ethz.ch/~stahel/lognormal/bioscience.pdf\n\n        Reiss, R.D. and Thomas, M., *Statistical Analysis of Extreme Values*,\n        Basel: Birkhauser Verlag, 2001, pp. 31-32.\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> mu, sigma = 3., 1. # mean and standard deviation\n        >>> s = np.random.lognormal(mu, sigma, 1000)\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> count, bins, ignored = plt.hist(s, 100, normed=True, align=\'mid\')\n\n        >>> x = np.linspace(min(bins), max(bins), 10000)\n        >>> pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))\n        ...        / (x * sigma * np.sqrt(2 * np.pi)))\n\n        >>> plt.plot(x, pdf, linewidth=2, color=\'r\')\n        >>> plt.axis(\'tight\')\n        >>> plt.show()\n\n        Demonstrate that taking the products of random samples from a uniform\n        distribution can be fit well by a log-normal probability density function.\n\n        >>> # Generate a thousand samples: each is the product of 100 random\n        >>> # values, drawn from a normal distribution.\n        >>> b = []\n        >>> for i in range(1000):\n        ...    a = 10. + np.random.random(100)\n        ...    b.append(np.product(a))\n\n        >>> b = np.array(b) / np.min(b) # scale values to be positive\n        >>> count, bins, ignored = plt.hist(b, 100, normed=True, align=\'center\')\n        >>> sigma = np.std(np.log(b))\n        >>> mu = np.mean(np.log(b))\n\n        >>> x = np.linspace(min(bins), max(bins), 10000)\n        >>> pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))\n        ...        / (x * sigma * np.sqrt(2 * np.pi)))\n\n        >>> plt.plot(x, pdf, color=\'r\', linewidth=2)\n        >>> plt.show()\n\n        ',
    u'RandomState.logseries (line 3963)': u'\n        logseries(p, size=None)\n\n        Draw samples from a Logarithmic Series distribution.\n\n        Samples are drawn from a Log Series distribution with specified\n        parameter, p (probability, 0 < p < 1).\n\n        Parameters\n        ----------\n        loc : float\n\n        scale : float > 0.\n\n        size : {tuple, int}\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : {ndarray, scalar}\n                  where the values are all integers in  [0, n].\n\n        See Also\n        --------\n        scipy.stats.distributions.logser : probability density function,\n            distribution or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the Log Series distribution is\n\n        .. math:: P(k) = \\frac{-p^k}{k \\ln(1-p)},\n\n        where p = probability.\n\n        The Log Series distribution is frequently used to represent species\n        richness and occurrence, first proposed by Fisher, Corbet, and\n        Williams in 1943 [2].  It may also be used to model the numbers of\n        occupants seen in cars [3].\n\n        References\n        ----------\n        .. [1] Buzas, Martin A.; Culver, Stephen J.,  Understanding regional\n               species diversity through the log series distribution of\n               occurrences: BIODIVERSITY RESEARCH Diversity & Distributions,\n               Volume 5, Number 5, September 1999 , pp. 187-195(9).\n        .. [2] Fisher, R.A,, A.S. Corbet, and C.B. Williams. 1943. The\n               relation between the number of species and the number of\n               individuals in a random sample of an animal population.\n               Journal of Animal Ecology, 12:42-58.\n        .. [3] D. J. Hand, F. Daly, D. Lunn, E. Ostrowski, A Handbook of Small\n               Data Sets, CRC Press, 1994.\n        .. [4] Wikipedia, "Logarithmic-distribution",\n               http://en.wikipedia.org/wiki/Logarithmic-distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> a = .6\n        >>> s = np.random.logseries(a, 10000)\n        >>> count, bins, ignored = plt.hist(s)\n\n        #   plot against distribution\n\n        >>> def logseries(k, p):\n        ...     return -p**k/(k*log(1-p))\n        >>> plt.plot(bins, logseries(bins, a)*count.max()/\n                     logseries(bins, a).max(), \'r\')\n        >>> plt.show()\n\n        ',
    u'RandomState.multinomial (line 4190)': u'\n        multinomial(n, pvals, size=None)\n\n        Draw samples from a multinomial distribution.\n\n        The multinomial distribution is a multivariate generalisation of the\n        binomial distribution.  Take an experiment with one of ``p``\n        possible outcomes.  An example of such an experiment is throwing a dice,\n        where the outcome can be 1 through 6.  Each sample drawn from the\n        distribution represents `n` such experiments.  Its values,\n        ``X_i = [X_0, X_1, ..., X_p]``, represent the number of times the outcome\n        was ``i``.\n\n        Parameters\n        ----------\n        n : int\n            Number of experiments.\n        pvals : sequence of floats, length p\n            Probabilities of each of the ``p`` different outcomes.  These\n            should sum to 1 (however, the last element is always assumed to\n            account for the remaining probability, as long as\n            ``sum(pvals[:-1]) <= 1)``.\n        size : tuple of ints\n            Given a `size` of ``(M, N, K)``, then ``M*N*K`` samples are drawn,\n            and the output shape becomes ``(M, N, K, p)``, since each sample\n            has shape ``(p,)``.\n\n        Examples\n        --------\n        Throw a dice 20 times:\n\n        >>> np.random.multinomial(20, [1/6.]*6, size=1)\n        array([[4, 1, 7, 5, 2, 1]])\n\n        It landed 4 times on 1, once on 2, etc.\n\n        Now, throw the dice 20 times, and 20 times again:\n\n        >>> np.random.multinomial(20, [1/6.]*6, size=2)\n        array([[3, 4, 3, 3, 4, 3],\n               [2, 4, 3, 4, 0, 7]])\n\n        For the first run, we threw 3 times 1, 4 times 2, etc.  For the second,\n        we threw 2 times 1, 4 times 2, etc.\n\n        A loaded dice is more likely to land on number 6:\n\n        >>> np.random.multinomial(100, [1/7.]*5)\n        array([13, 16, 13, 16, 42])\n\n        ',
    u'RandomState.multivariate_normal (line 4058)': u'\n        multivariate_normal(mean, cov[, size])\n\n        Draw random samples from a multivariate normal distribution.\n\n        The multivariate normal, multinormal or Gaussian distribution is a\n        generalization of the one-dimensional normal distribution to higher\n        dimensions.  Such a distribution is specified by its mean and\n        covariance matrix.  These parameters are analogous to the mean\n        (average or "center") and variance (standard deviation, or "width,"\n        squared) of the one-dimensional normal distribution.\n\n        Parameters\n        ----------\n        mean : 1-D array_like, of length N\n            Mean of the N-dimensional distribution.\n        cov : 2-D array_like, of shape (N, N)\n            Covariance matrix of the distribution.  Must be symmetric and\n            positive semi-definite for "physically meaningful" results.\n        size : int or tuple of ints, optional\n            Given a shape of, for example, ``(m,n,k)``, ``m*n*k`` samples are\n            generated, and packed in an `m`-by-`n`-by-`k` arrangement.  Because\n            each sample is `N`-dimensional, the output shape is ``(m,n,k,N)``.\n            If no shape is specified, a single (`N`-D) sample is returned.\n\n        Returns\n        -------\n        out : ndarray\n            The drawn samples, of shape *size*, if that was provided.  If not,\n            the shape is ``(N,)``.\n\n            In other words, each entry ``out[i,j,...,:]`` is an N-dimensional\n            value drawn from the distribution.\n\n        Notes\n        -----\n        The mean is a coordinate in N-dimensional space, which represents the\n        location where samples are most likely to be generated.  This is\n        analogous to the peak of the bell curve for the one-dimensional or\n        univariate normal distribution.\n\n        Covariance indicates the level to which two variables vary together.\n        From the multivariate normal distribution, we draw N-dimensional\n        samples, :math:`X = [x_1, x_2, ... x_N]`.  The covariance matrix\n        element :math:`C_{ij}` is the covariance of :math:`x_i` and :math:`x_j`.\n        The element :math:`C_{ii}` is the variance of :math:`x_i` (i.e. its\n        "spread").\n\n        Instead of specifying the full covariance matrix, popular\n        approximations include:\n\n          - Spherical covariance (*cov* is a multiple of the identity matrix)\n          - Diagonal covariance (*cov* has non-negative elements, and only on\n            the diagonal)\n\n        This geometrical property can be seen in two dimensions by plotting\n        generated data-points:\n\n        >>> mean = [0,0]\n        >>> cov = [[1,0],[0,100]] # diagonal covariance, points lie on x or y-axis\n\n        >>> import matplotlib.pyplot as plt\n        >>> x,y = np.random.multivariate_normal(mean,cov,5000).T\n        >>> plt.plot(x,y,\'x\'); plt.axis(\'equal\'); plt.show()\n\n        Note that the covariance matrix must be non-negative definite.\n\n        References\n        ----------\n        Papoulis, A., *Probability, Random Variables, and Stochastic Processes*,\n        3rd ed., New York: McGraw-Hill, 1991.\n\n        Duda, R. O., Hart, P. E., and Stork, D. G., *Pattern Classification*,\n        2nd ed., New York: Wiley, 2001.\n\n        Examples\n        --------\n        >>> mean = (1,2)\n        >>> cov = [[1,0],[1,0]]\n        >>> x = np.random.multivariate_normal(mean,cov,(3,3))\n        >>> x.shape\n        (3, 3, 2)\n\n        The following is probably true, given that 0.6 is roughly twice the\n        standard deviation:\n\n        >>> print list( (x[0,0,:] - mean) < 0.6 )\n        [True, True]\n\n        ',
    u'RandomState.negative_binomial (line 3524)': u'\n        negative_binomial(n, p, size=None)\n\n        Draw samples from a negative_binomial distribution.\n\n        Samples are drawn from a negative_Binomial distribution with specified\n        parameters, `n` trials and `p` probability of success where `n` is an\n        integer > 0 and `p` is in the interval [0, 1].\n\n        Parameters\n        ----------\n        n : int\n            Parameter, > 0.\n        p : float\n            Parameter, >= 0 and <=1.\n        size : int or tuple of ints\n            Output shape. If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : int or ndarray of ints\n            Drawn samples.\n\n        Notes\n        -----\n        The probability density for the Negative Binomial distribution is\n\n        .. math:: P(N;n,p) = \\binom{N+n-1}{n-1}p^{n}(1-p)^{N},\n\n        where :math:`n-1` is the number of successes, :math:`p` is the probability\n        of success, and :math:`N+n-1` is the number of trials.\n\n        The negative binomial distribution gives the probability of n-1 successes\n        and N failures in N+n-1 trials, and success on the (N+n)th trial.\n\n        If one throws a die repeatedly until the third time a "1" appears, then the\n        probability distribution of the number of non-"1"s that appear before the\n        third "1" is a negative binomial distribution.\n\n        References\n        ----------\n        .. [1] Weisstein, Eric W. "Negative Binomial Distribution." From\n               MathWorld--A Wolfram Web Resource.\n               http://mathworld.wolfram.com/NegativeBinomialDistribution.html\n        .. [2] Wikipedia, "Negative binomial distribution",\n               http://en.wikipedia.org/wiki/Negative_binomial_distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        A real world example. A company drills wild-cat oil exploration wells, each\n        with an estimated probability of success of 0.1.  What is the probability\n        of having one success for each successive well, that is what is the\n        probability of a single success after drilling 5 wells, after 6 wells,\n        etc.?\n\n        >>> s = np.random.negative_binomial(1, 0.1, 100000)\n        >>> for i in range(1, 11):\n        ...    probability = sum(s<i) / 100000.\n        ...    print i, "wells drilled, probability of one success =", probability\n\n        ',
    u'RandomState.noncentral_chisquare (line 2087)': u'\n        noncentral_chisquare(df, nonc, size=None)\n\n        Draw samples from a noncentral chi-square distribution.\n\n        The noncentral :math:`\\chi^2` distribution is a generalisation of\n        the :math:`\\chi^2` distribution.\n\n        Parameters\n        ----------\n        df : int\n            Degrees of freedom, should be >= 1.\n        nonc : float\n            Non-centrality, should be > 0.\n        size : int or tuple of ints\n            Shape of the output.\n\n        Notes\n        -----\n        The probability density function for the noncentral Chi-square distribution\n        is\n\n        .. math:: P(x;df,nonc) = \\sum^{\\infty}_{i=0}\n                               \\frac{e^{-nonc/2}(nonc/2)^{i}}{i!}P_{Y_{df+2i}}(x),\n\n        where :math:`Y_{q}` is the Chi-square with q degrees of freedom.\n\n        In Delhi (2007), it is noted that the noncentral chi-square is useful in\n        bombing and coverage problems, the probability of killing the point target\n        given by the noncentral chi-squared distribution.\n\n        References\n        ----------\n        .. [1] Delhi, M.S. Holla, "On a noncentral chi-square distribution in the\n               analysis of weapon systems effectiveness", Metrika, Volume 15,\n               Number 1 / December, 1970.\n        .. [2] Wikipedia, "Noncentral chi-square distribution"\n               http://en.wikipedia.org/wiki/Noncentral_chi-square_distribution\n\n        Examples\n        --------\n        Draw values from the distribution and plot the histogram\n\n        >>> import matplotlib.pyplot as plt\n        >>> values = plt.hist(np.random.noncentral_chisquare(3, 20, 100000),\n        ...                   bins=200, normed=True)\n        >>> plt.show()\n\n        Draw values from a noncentral chisquare with very small noncentrality,\n        and compare to a chisquare.\n\n        >>> plt.figure()\n        >>> values = plt.hist(np.random.noncentral_chisquare(3, .0000001, 100000),\n        ...                   bins=np.arange(0., 25, .1), normed=True)\n        >>> values2 = plt.hist(np.random.chisquare(3, 100000),\n        ...                    bins=np.arange(0., 25, .1), normed=True)\n        >>> plt.plot(values[1][0:-1], values[0]-values2[0], \'ob\')\n        >>> plt.show()\n\n        Demonstrate how large values of non-centrality lead to a more symmetric\n        distribution.\n\n        >>> plt.figure()\n        >>> values = plt.hist(np.random.noncentral_chisquare(3, 20, 100000),\n        ...                   bins=200, normed=True)\n        >>> plt.show()\n\n        ',
    u'RandomState.noncentral_f (line 1914)': u'\n        noncentral_f(dfnum, dfden, nonc, size=None)\n\n        Draw samples from the noncentral F distribution.\n\n        Samples are drawn from an F distribution with specified parameters,\n        `dfnum` (degrees of freedom in numerator) and `dfden` (degrees of\n        freedom in denominator), where both parameters > 1.\n        `nonc` is the non-centrality parameter.\n\n        Parameters\n        ----------\n        dfnum : int\n            Parameter, should be > 1.\n        dfden : int\n            Parameter, should be > 1.\n        nonc : float\n            Parameter, should be >= 0.\n        size : int or tuple of ints\n            Output shape. If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : scalar or ndarray\n            Drawn samples.\n\n        Notes\n        -----\n        When calculating the power of an experiment (power = probability of\n        rejecting the null hypothesis when a specific alternative is true) the\n        non-central F statistic becomes important.  When the null hypothesis is\n        true, the F statistic follows a central F distribution. When the null\n        hypothesis is not true, then it follows a non-central F statistic.\n\n        References\n        ----------\n        Weisstein, Eric W. "Noncentral F-Distribution." From MathWorld--A Wolfram\n        Web Resource.  http://mathworld.wolfram.com/NoncentralF-Distribution.html\n\n        Wikipedia, "Noncentral F distribution",\n        http://en.wikipedia.org/wiki/Noncentral_F-distribution\n\n        Examples\n        --------\n        In a study, testing for a specific alternative to the null hypothesis\n        requires use of the Noncentral F distribution. We need to calculate the\n        area in the tail of the distribution that exceeds the value of the F\n        distribution for the null hypothesis.  We\'ll plot the two probability\n        distributions for comparison.\n\n        >>> dfnum = 3 # between group deg of freedom\n        >>> dfden = 20 # within groups degrees of freedom\n        >>> nonc = 3.0\n        >>> nc_vals = np.random.noncentral_f(dfnum, dfden, nonc, 1000000)\n        >>> NF = np.histogram(nc_vals, bins=50, normed=True)\n        >>> c_vals = np.random.f(dfnum, dfden, 1000000)\n        >>> F = np.histogram(c_vals, bins=50, normed=True)\n        >>> plt.plot(F[1][1:], F[0])\n        >>> plt.plot(NF[1][1:], NF[0])\n        >>> plt.show()\n\n        ',
    u'RandomState.normal (line 1398)': u'\n        normal(loc=0.0, scale=1.0, size=None)\n\n        Draw random samples from a normal (Gaussian) distribution.\n\n        The probability density function of the normal distribution, first\n        derived by De Moivre and 200 years later by both Gauss and Laplace\n        independently [2]_, is often called the bell curve because of\n        its characteristic shape (see the example below).\n\n        The normal distributions occurs often in nature.  For example, it\n        describes the commonly occurring distribution of samples influenced\n        by a large number of tiny, random disturbances, each with its own\n        unique distribution [2]_.\n\n        Parameters\n        ----------\n        loc : float\n            Mean ("centre") of the distribution.\n        scale : float\n            Standard deviation (spread or "width") of the distribution.\n        size : tuple of ints\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        See Also\n        --------\n        scipy.stats.distributions.norm : probability density function,\n            distribution or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the Gaussian distribution is\n\n        .. math:: p(x) = \\frac{1}{\\sqrt{ 2 \\pi \\sigma^2 }}\n                         e^{ - \\frac{ (x - \\mu)^2 } {2 \\sigma^2} },\n\n        where :math:`\\mu` is the mean and :math:`\\sigma` the standard deviation.\n        The square of the standard deviation, :math:`\\sigma^2`, is called the\n        variance.\n\n        The function has its peak at the mean, and its "spread" increases with\n        the standard deviation (the function reaches 0.607 times its maximum at\n        :math:`x + \\sigma` and :math:`x - \\sigma` [2]_).  This implies that\n        `numpy.random.normal` is more likely to return samples lying close to the\n        mean, rather than those far away.\n\n        References\n        ----------\n        .. [1] Wikipedia, "Normal distribution",\n               http://en.wikipedia.org/wiki/Normal_distribution\n        .. [2] P. R. Peebles Jr., "Central Limit Theorem" in "Probability, Random\n               Variables and Random Signal Principles", 4th ed., 2001,\n               pp. 51, 51, 125.\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> mu, sigma = 0, 0.1 # mean and standard deviation\n        >>> s = np.random.normal(mu, sigma, 1000)\n\n        Verify the mean and the variance:\n\n        >>> abs(mu - np.mean(s)) < 0.01\n        True\n\n        >>> abs(sigma - np.std(s, ddof=1)) < 0.01\n        True\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> count, bins, ignored = plt.hist(s, 30, normed=True)\n        >>> plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *\n        ...                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),\n        ...          linewidth=2, color=\'r\')\n        >>> plt.show()\n\n        ',
    u'RandomState.pareto (line 2435)': u'\n        pareto(a, size=None)\n\n        Draw samples from a Pareto II or Lomax distribution with specified shape.\n\n        The Lomax or Pareto II distribution is a shifted Pareto distribution. The\n        classical Pareto distribution can be obtained from the Lomax distribution\n        by adding the location parameter m, see below. The smallest value of the\n        Lomax distribution is zero while for the classical Pareto distribution it\n        is m, where the standard Pareto distribution has location m=1.\n        Lomax can also be considered as a simplified version of the Generalized\n        Pareto distribution (available in SciPy), with the scale set to one and\n        the location set to zero.\n\n        The Pareto distribution must be greater than zero, and is unbounded above.\n        It is also known as the "80-20 rule".  In this distribution, 80 percent of\n        the weights are in the lowest 20 percent of the range, while the other 20\n        percent fill the remaining 80 percent of the range.\n\n        Parameters\n        ----------\n        shape : float, > 0.\n            Shape of the distribution.\n        size : tuple of ints\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        See Also\n        --------\n        scipy.stats.distributions.lomax.pdf : probability density function,\n            distribution or cumulative density function, etc.\n        scipy.stats.distributions.genpareto.pdf : probability density function,\n            distribution or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the Pareto distribution is\n\n        .. math:: p(x) = \\frac{am^a}{x^{a+1}}\n\n        where :math:`a` is the shape and :math:`m` the location\n\n        The Pareto distribution, named after the Italian economist Vilfredo Pareto,\n        is a power law probability distribution useful in many real world problems.\n        Outside the field of economics it is generally referred to as the Bradford\n        distribution. Pareto developed the distribution to describe the\n        distribution of wealth in an economy.  It has also found use in insurance,\n        web page access statistics, oil field sizes, and many other problems,\n        including the download frequency for projects in Sourceforge [1].  It is\n        one of the so-called "fat-tailed" distributions.\n\n\n        References\n        ----------\n        .. [1] Francis Hunt and Paul Johnson, On the Pareto Distribution of\n               Sourceforge projects.\n        .. [2] Pareto, V. (1896). Course of Political Economy. Lausanne.\n        .. [3] Reiss, R.D., Thomas, M.(2001), Statistical Analysis of Extreme\n               Values, Birkhauser Verlag, Basel, pp 23-30.\n        .. [4] Wikipedia, "Pareto distribution",\n               http://en.wikipedia.org/wiki/Pareto_distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> a, m = 3., 1. # shape and mode\n        >>> s = np.random.pareto(a, 1000) + m\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> count, bins, ignored = plt.hist(s, 100, normed=True, align=\'center\')\n        >>> fit = a*m**a/bins**(a+1)\n        >>> plt.plot(bins, max(count)*fit/max(fit),linewidth=2, color=\'r\')\n        >>> plt.show()\n\n        ',
    u'RandomState.permutation (line 4448)': u'\n        permutation(x)\n\n        Randomly permute a sequence, or return a permuted range.\n\n        If `x` is a multi-dimensional array, it is only shuffled along its\n        first index.\n\n        Parameters\n        ----------\n        x : int or array_like\n            If `x` is an integer, randomly permute ``np.arange(x)``.\n            If `x` is an array, make a copy and shuffle the elements\n            randomly.\n\n        Returns\n        -------\n        out : ndarray\n            Permuted sequence or array range.\n\n        Examples\n        --------\n        >>> np.random.permutation(10)\n        array([1, 7, 4, 3, 0, 9, 2, 5, 8, 6])\n\n        >>> np.random.permutation([1, 4, 9, 12, 15])\n        array([15,  1,  9,  4, 12])\n\n        >>> arr = np.arange(9).reshape((3, 3))\n        >>> np.random.permutation(arr)\n        array([[6, 7, 8],\n               [0, 1, 2],\n               [3, 4, 5]])\n\n        ',
    u'RandomState.poisson (line 3619)': u'\n        poisson(lam=1.0, size=None)\n\n        Draw samples from a Poisson distribution.\n\n        The Poisson distribution is the limit of the Binomial\n        distribution for large N.\n\n        Parameters\n        ----------\n        lam : float\n            Expectation of interval, should be >= 0.\n        size : int or tuple of ints, optional\n            Output shape. If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Notes\n        -----\n        The Poisson distribution\n\n        .. math:: f(k; \\lambda)=\\frac{\\lambda^k e^{-\\lambda}}{k!}\n\n        For events with an expected separation :math:`\\lambda` the Poisson\n        distribution :math:`f(k; \\lambda)` describes the probability of\n        :math:`k` events occurring within the observed interval :math:`\\lambda`.\n\n        Because the output is limited to the range of the C long type, a\n        ValueError is raised when `lam` is within 10 sigma of the maximum\n        representable value.\n\n        References\n        ----------\n        .. [1] Weisstein, Eric W. "Poisson Distribution." From MathWorld--A Wolfram\n               Web Resource. http://mathworld.wolfram.com/PoissonDistribution.html\n        .. [2] Wikipedia, "Poisson distribution",\n           http://en.wikipedia.org/wiki/Poisson_distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> import numpy as np\n        >>> s = np.random.poisson(5, 10000)\n\n        Display histogram of the sample:\n\n        >>> import matplotlib.pyplot as plt\n        >>> count, bins, ignored = plt.hist(s, 14, normed=True)\n        >>> plt.show()\n\n        ',
    u'RandomState.power (line 2631)': u'\n        power(a, size=None)\n\n        Draws samples in [0, 1] from a power distribution with positive\n        exponent a - 1.\n\n        Also known as the power function distribution.\n\n        Parameters\n        ----------\n        a : float\n            parameter, > 0\n        size : tuple of ints\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n                    ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : {ndarray, scalar}\n            The returned samples lie in [0, 1].\n\n        Raises\n        ------\n        ValueError\n            If a<1.\n\n        Notes\n        -----\n        The probability density function is\n\n        .. math:: P(x; a) = ax^{a-1}, 0 \\le x \\le 1, a>0.\n\n        The power function distribution is just the inverse of the Pareto\n        distribution. It may also be seen as a special case of the Beta\n        distribution.\n\n        It is used, for example, in modeling the over-reporting of insurance\n        claims.\n\n        References\n        ----------\n        .. [1] Christian Kleiber, Samuel Kotz, "Statistical size distributions\n               in economics and actuarial sciences", Wiley, 2003.\n        .. [2] Heckert, N. A. and Filliben, James J. (2003). NIST Handbook 148:\n               Dataplot Reference Manual, Volume 2: Let Subcommands and Library\n               Functions", National Institute of Standards and Technology Handbook\n               Series, June 2003.\n               http://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/powpdf.pdf\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> a = 5. # shape\n        >>> samples = 1000\n        >>> s = np.random.power(a, samples)\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> count, bins, ignored = plt.hist(s, bins=30)\n        >>> x = np.linspace(0, 1, 100)\n        >>> y = a*x**(a-1.)\n        >>> normed_y = samples*np.diff(bins)[0]*y\n        >>> plt.plot(x, normed_y)\n        >>> plt.show()\n\n        Compare the power function distribution to the inverse of the Pareto.\n\n        >>> from scipy import stats\n        >>> rvs = np.random.power(5, 1000000)\n        >>> rvsp = np.random.pareto(5, 1000000)\n        >>> xx = np.linspace(0,1,100)\n        >>> powpdf = stats.powerlaw.pdf(xx,5)\n\n        >>> plt.figure()\n        >>> plt.hist(rvs, bins=50, normed=True)\n        >>> plt.plot(xx,powpdf,\'r-\')\n        >>> plt.title(\'np.random.power(5)\')\n\n        >>> plt.figure()\n        >>> plt.hist(1./(1.+rvsp), bins=50, normed=True)\n        >>> plt.plot(xx,powpdf,\'r-\')\n        >>> plt.title(\'inverse of 1 + np.random.pareto(5)\')\n\n        >>> plt.figure()\n        >>> plt.hist(1./(1.+rvsp), bins=50, normed=True)\n        >>> plt.plot(xx,powpdf,\'r-\')\n        >>> plt.title(\'inverse of stats.pareto(5)\')\n\n        ',
    u'RandomState.rand (line 1187)': u'\n        rand(d0, d1, ..., dn)\n\n        Random values in a given shape.\n\n        Create an array of the given shape and propagate it with\n        random samples from a uniform distribution\n        over ``[0, 1)``.\n\n        Parameters\n        ----------\n        d0, d1, ..., dn : int, optional\n            The dimensions of the returned array, should all be positive.\n            If no argument is given a single Python float is returned.\n\n        Returns\n        -------\n        out : ndarray, shape ``(d0, d1, ..., dn)``\n            Random values.\n\n        See Also\n        --------\n        random\n\n        Notes\n        -----\n        This is a convenience function. If you want an interface that\n        takes a shape-tuple as the first argument, refer to\n        np.random.random_sample .\n\n        Examples\n        --------\n        >>> np.random.rand(3,2)\n        array([[ 0.14022471,  0.96360618],  #random\n               [ 0.37601032,  0.25528411],  #random\n               [ 0.49313049,  0.94909878]]) #random\n\n        ',
    u'RandomState.randint (line 820)': u'\n        randint(low, high=None, size=None)\n\n        Return random integers from `low` (inclusive) to `high` (exclusive).\n\n        Return random integers from the "discrete uniform" distribution in the\n        "half-open" interval [`low`, `high`). If `high` is None (the default),\n        then results are from [0, `low`).\n\n        Parameters\n        ----------\n        low : int\n            Lowest (signed) integer to be drawn from the distribution (unless\n            ``high=None``, in which case this parameter is the *highest* such\n            integer).\n        high : int, optional\n            If provided, one above the largest (signed) integer to be drawn\n            from the distribution (see above for behavior if ``high=None``).\n        size : int or tuple of ints, optional\n            Output shape. Default is None, in which case a single int is\n            returned.\n\n        Returns\n        -------\n        out : int or ndarray of ints\n            `size`-shaped array of random integers from the appropriate\n            distribution, or a single such random int if `size` not provided.\n\n        See Also\n        --------\n        random.random_integers : similar to `randint`, only for the closed\n            interval [`low`, `high`], and 1 is the lowest value if `high` is\n            omitted. In particular, this other one is the one to use to generate\n            uniformly distributed discrete non-integers.\n\n        Examples\n        --------\n        >>> np.random.randint(2, size=10)\n        array([1, 0, 0, 0, 1, 1, 0, 0, 1, 0])\n        >>> np.random.randint(1, size=10)\n        array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])\n\n        Generate a 2 x 4 array of ints between 0 and 4, inclusive:\n\n        >>> np.random.randint(5, size=(2, 4))\n        array([[4, 0, 2, 1],\n               [3, 2, 2, 0]])\n\n        ',
    u'RandomState.randn (line 1231)': u'\n        randn(d0, d1, ..., dn)\n\n        Return a sample (or samples) from the "standard normal" distribution.\n\n        If positive, int_like or int-convertible arguments are provided,\n        `randn` generates an array of shape ``(d0, d1, ..., dn)``, filled\n        with random floats sampled from a univariate "normal" (Gaussian)\n        distribution of mean 0 and variance 1 (if any of the :math:`d_i` are\n        floats, they are first converted to integers by truncation). A single\n        float randomly sampled from the distribution is returned if no\n        argument is provided.\n\n        This is a convenience function.  If you want an interface that takes a\n        tuple as the first argument, use `numpy.random.standard_normal` instead.\n\n        Parameters\n        ----------\n        d0, d1, ..., dn : int, optional\n            The dimensions of the returned array, should be all positive.\n            If no argument is given a single Python float is returned.\n\n        Returns\n        -------\n        Z : ndarray or float\n            A ``(d0, d1, ..., dn)``-shaped array of floating-point samples from\n            the standard normal distribution, or a single such float if\n            no parameters were supplied.\n\n        See Also\n        --------\n        random.standard_normal : Similar, but takes a tuple as its argument.\n\n        Notes\n        -----\n        For random samples from :math:`N(\\mu, \\sigma^2)`, use:\n\n        ``sigma * np.random.randn(...) + mu``\n\n        Examples\n        --------\n        >>> np.random.randn()\n        2.1923875335537315 #random\n\n        Two-by-four array of samples from N(3, 6.25):\n\n        >>> 2.5 * np.random.randn(2, 4) + 3\n        array([[-4.49401501,  4.00950034, -1.81814867,  7.29718677],  #random\n               [ 0.39924804,  4.68456316,  4.99394529,  4.84057254]]) #random\n\n        ',
    u'RandomState.random_integers (line 1288)': u'\n        random_integers(low, high=None, size=None)\n\n        Return random integers between `low` and `high`, inclusive.\n\n        Return random integers from the "discrete uniform" distribution in the\n        closed interval [`low`, `high`].  If `high` is None (the default),\n        then results are from [1, `low`].\n\n        Parameters\n        ----------\n        low : int\n            Lowest (signed) integer to be drawn from the distribution (unless\n            ``high=None``, in which case this parameter is the *highest* such\n            integer).\n        high : int, optional\n            If provided, the largest (signed) integer to be drawn from the\n            distribution (see above for behavior if ``high=None``).\n        size : int or tuple of ints, optional\n            Output shape. Default is None, in which case a single int is returned.\n\n        Returns\n        -------\n        out : int or ndarray of ints\n            `size`-shaped array of random integers from the appropriate\n            distribution, or a single such random int if `size` not provided.\n\n        See Also\n        --------\n        random.randint : Similar to `random_integers`, only for the half-open\n            interval [`low`, `high`), and 0 is the lowest value if `high` is\n            omitted.\n\n        Notes\n        -----\n        To sample from N evenly spaced floating-point numbers between a and b,\n        use::\n\n          a + (b - a) * (np.random.random_integers(N) - 1) / (N - 1.)\n\n        Examples\n        --------\n        >>> np.random.random_integers(5)\n        4\n        >>> type(np.random.random_integers(5))\n        <type \'int\'>\n        >>> np.random.random_integers(5, size=(3.,2.))\n        array([[5, 4],\n               [3, 3],\n               [4, 5]])\n\n        Choose five random numbers from the set of five evenly-spaced\n        numbers between 0 and 2.5, inclusive (*i.e.*, from the set\n        :math:`{0, 5/8, 10/8, 15/8, 20/8}`):\n\n        >>> 2.5 * (np.random.random_integers(5, size=(5,)) - 1) / 4.\n        array([ 0.625,  1.25 ,  0.625,  0.625,  2.5  ])\n\n        Roll two six sided dice 1000 times and sum the results:\n\n        >>> d1 = np.random.random_integers(1, 6, 1000)\n        >>> d2 = np.random.random_integers(1, 6, 1000)\n        >>> dsums = d1 + d2\n\n        Display results as a histogram:\n\n        >>> import matplotlib.pyplot as plt\n        >>> count, bins, ignored = plt.hist(dsums, 11, normed=True)\n        >>> plt.show()\n\n        ',
    u'RandomState.random_sample (line 730)': u'\n        random_sample(size=None)\n\n        Return random floats in the half-open interval [0.0, 1.0).\n\n        Results are from the "continuous uniform" distribution over the\n        stated interval.  To sample :math:`Unif[a, b), b > a` multiply\n        the output of `random_sample` by `(b-a)` and add `a`::\n\n          (b - a) * random_sample() + a\n\n        Parameters\n        ----------\n        size : int or tuple of ints, optional\n            Defines the shape of the returned array of random floats. If None\n            (the default), returns a single float.\n\n        Returns\n        -------\n        out : float or ndarray of floats\n            Array of random floats of shape `size` (unless ``size=None``, in which\n            case a single float is returned).\n\n        Examples\n        --------\n        >>> np.random.random_sample()\n        0.47108547995356098\n        >>> type(np.random.random_sample())\n        <type \'float\'>\n        >>> np.random.random_sample((5,))\n        array([ 0.30220482,  0.86820401,  0.1654503 ,  0.11659149,  0.54323428])\n\n        Three-by-two array of random numbers from [-5, 0):\n\n        >>> 5 * np.random.random_sample((3, 2)) - 5\n        array([[-3.99149989, -0.52338984],\n               [-2.99091858, -0.79479508],\n               [-1.23204345, -1.75224494]])\n\n        ',
    u'RandomState.rayleigh (line 3170)': u'\n        rayleigh(scale=1.0, size=None)\n\n        Draw samples from a Rayleigh distribution.\n\n        The :math:`\\chi` and Weibull distributions are generalizations of the\n        Rayleigh.\n\n        Parameters\n        ----------\n        scale : scalar\n            Scale, also equals the mode. Should be >= 0.\n        size : int or tuple of ints, optional\n            Shape of the output. Default is None, in which case a single\n            value is returned.\n\n        Notes\n        -----\n        The probability density function for the Rayleigh distribution is\n\n        .. math:: P(x;scale) = \\frac{x}{scale^2}e^{\\frac{-x^2}{2 \\cdotp scale^2}}\n\n        The Rayleigh distribution arises if the wind speed and wind direction are\n        both gaussian variables, then the vector wind velocity forms a Rayleigh\n        distribution. The Rayleigh distribution is used to model the expected\n        output from wind turbines.\n\n        References\n        ----------\n        .. [1] Brighton Webs Ltd., Rayleigh Distribution,\n              http://www.brighton-webs.co.uk/distributions/rayleigh.asp\n        .. [2] Wikipedia, "Rayleigh distribution"\n              http://en.wikipedia.org/wiki/Rayleigh_distribution\n\n        Examples\n        --------\n        Draw values from the distribution and plot the histogram\n\n        >>> values = hist(np.random.rayleigh(3, 100000), bins=200, normed=True)\n\n        Wave heights tend to follow a Rayleigh distribution. If the mean wave\n        height is 1 meter, what fraction of waves are likely to be larger than 3\n        meters?\n\n        >>> meanvalue = 1\n        >>> modevalue = np.sqrt(2 / np.pi) * meanvalue\n        >>> s = np.random.rayleigh(modevalue, 1000000)\n\n        The percentage of waves larger than 3 meters is:\n\n        >>> 100.*sum(s>3)/1000000.\n        0.087300000000000003\n\n        ',
    u'RandomState.shuffle (line 4389)': u'\n        shuffle(x)\n\n        Modify a sequence in-place by shuffling its contents.\n\n        Parameters\n        ----------\n        x : array_like\n            The array or list to be shuffled.\n\n        Returns\n        -------\n        None\n\n        Examples\n        --------\n        >>> arr = np.arange(10)\n        >>> np.random.shuffle(arr)\n        >>> arr\n        [1 7 5 2 9 4 3 6 0 8]\n\n        This function only shuffles the array along the first index of a\n        multi-dimensional array:\n\n        >>> arr = np.arange(9).reshape((3, 3))\n        >>> np.random.shuffle(arr)\n        >>> arr\n        array([[3, 4, 5],\n               [6, 7, 8],\n               [0, 1, 2]])\n\n        ',
    u'RandomState.standard_cauchy (line 2179)': u'\n        standard_cauchy(size=None)\n\n        Standard Cauchy distribution with mode = 0.\n\n        Also known as the Lorentz distribution.\n\n        Parameters\n        ----------\n        size : int or tuple of ints\n            Shape of the output.\n\n        Returns\n        -------\n        samples : ndarray or scalar\n            The drawn samples.\n\n        Notes\n        -----\n        The probability density function for the full Cauchy distribution is\n\n        .. math:: P(x; x_0, \\gamma) = \\frac{1}{\\pi \\gamma \\bigl[ 1+\n                  (\\frac{x-x_0}{\\gamma})^2 \\bigr] }\n\n        and the Standard Cauchy distribution just sets :math:`x_0=0` and\n        :math:`\\gamma=1`\n\n        The Cauchy distribution arises in the solution to the driven harmonic\n        oscillator problem, and also describes spectral line broadening. It\n        also describes the distribution of values at which a line tilted at\n        a random angle will cut the x axis.\n\n        When studying hypothesis tests that assume normality, seeing how the\n        tests perform on data from a Cauchy distribution is a good indicator of\n        their sensitivity to a heavy-tailed distribution, since the Cauchy looks\n        very much like a Gaussian distribution, but with heavier tails.\n\n        References\n        ----------\n        .. [1] NIST/SEMATECH e-Handbook of Statistical Methods, "Cauchy\n              Distribution",\n              http://www.itl.nist.gov/div898/handbook/eda/section3/eda3663.htm\n        .. [2] Weisstein, Eric W. "Cauchy Distribution." From MathWorld--A\n              Wolfram Web Resource.\n              http://mathworld.wolfram.com/CauchyDistribution.html\n        .. [3] Wikipedia, "Cauchy distribution"\n              http://en.wikipedia.org/wiki/Cauchy_distribution\n\n        Examples\n        --------\n        Draw samples and plot the distribution:\n\n        >>> s = np.random.standard_cauchy(1000000)\n        >>> s = s[(s>-25) & (s<25)]  # truncate distribution so it plots well\n        >>> plt.hist(s, bins=100)\n        >>> plt.show()\n\n        ',
    u'RandomState.standard_exponential (line 1611)': u'\n        standard_exponential(size=None)\n\n        Draw samples from the standard exponential distribution.\n\n        `standard_exponential` is identical to the exponential distribution\n        with a scale parameter of 1.\n\n        Parameters\n        ----------\n        size : int or tuple of ints\n            Shape of the output.\n\n        Returns\n        -------\n        out : float or ndarray\n            Drawn samples.\n\n        Examples\n        --------\n        Output a 3x8000 array:\n\n        >>> n = np.random.standard_exponential((3, 8000))\n\n        ',
    u'RandomState.standard_gamma (line 1639)': u'\n        standard_gamma(shape, size=None)\n\n        Draw samples from a Standard Gamma distribution.\n\n        Samples are drawn from a Gamma distribution with specified parameters,\n        shape (sometimes designated "k") and scale=1.\n\n        Parameters\n        ----------\n        shape : float\n            Parameter, should be > 0.\n        size : int or tuple of ints\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : ndarray or scalar\n            The drawn samples.\n\n        See Also\n        --------\n        scipy.stats.distributions.gamma : probability density function,\n            distribution or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the Gamma distribution is\n\n        .. math:: p(x) = x^{k-1}\\frac{e^{-x/\\theta}}{\\theta^k\\Gamma(k)},\n\n        where :math:`k` is the shape and :math:`\\theta` the scale,\n        and :math:`\\Gamma` is the Gamma function.\n\n        The Gamma distribution is often used to model the times to failure of\n        electronic components, and arises naturally in processes for which the\n        waiting times between Poisson distributed events are relevant.\n\n        References\n        ----------\n        .. [1] Weisstein, Eric W. "Gamma Distribution." From MathWorld--A\n               Wolfram Web Resource.\n               http://mathworld.wolfram.com/GammaDistribution.html\n        .. [2] Wikipedia, "Gamma-distribution",\n               http://en.wikipedia.org/wiki/Gamma-distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> shape, scale = 2., 1. # mean and width\n        >>> s = np.random.standard_gamma(shape, 1000000)\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> import scipy.special as sps\n        >>> count, bins, ignored = plt.hist(s, 50, normed=True)\n        >>> y = bins**(shape-1) * ((np.exp(-bins/scale))/ \\\n        ...                       (sps.gamma(shape) * scale**shape))\n        >>> plt.plot(bins, y, linewidth=2, color=\'r\')\n        >>> plt.show()\n\n        ',
    u'RandomState.standard_normal (line 1366)': u'\n        standard_normal(size=None)\n\n        Returns samples from a Standard Normal distribution (mean=0, stdev=1).\n\n        Parameters\n        ----------\n        size : int or tuple of ints, optional\n            Output shape. Default is None, in which case a single value is\n            returned.\n\n        Returns\n        -------\n        out : float or ndarray\n            Drawn samples.\n\n        Examples\n        --------\n        >>> s = np.random.standard_normal(8000)\n        >>> s\n        array([ 0.6888893 ,  0.78096262, -0.89086505, ...,  0.49876311, #random\n               -0.38672696, -0.4685006 ])                               #random\n        >>> s.shape\n        (8000,)\n        >>> s = np.random.standard_normal(size=(3, 4, 2))\n        >>> s.shape\n        (3, 4, 2)\n\n        ',
    u'RandomState.standard_t (line 2240)': u'\n        standard_t(df, size=None)\n\n        Standard Student\'s t distribution with df degrees of freedom.\n\n        A special case of the hyperbolic distribution.\n        As `df` gets large, the result resembles that of the standard normal\n        distribution (`standard_normal`).\n\n        Parameters\n        ----------\n        df : int\n            Degrees of freedom, should be > 0.\n        size : int or tuple of ints, optional\n            Output shape. Default is None, in which case a single value is\n            returned.\n\n        Returns\n        -------\n        samples : ndarray or scalar\n            Drawn samples.\n\n        Notes\n        -----\n        The probability density function for the t distribution is\n\n        .. math:: P(x, df) = \\frac{\\Gamma(\\frac{df+1}{2})}{\\sqrt{\\pi df}\n                  \\Gamma(\\frac{df}{2})}\\Bigl( 1+\\frac{x^2}{df} \\Bigr)^{-(df+1)/2}\n\n        The t test is based on an assumption that the data come from a Normal\n        distribution. The t test provides a way to test whether the sample mean\n        (that is the mean calculated from the data) is a good estimate of the true\n        mean.\n\n        The derivation of the t-distribution was forst published in 1908 by William\n        Gisset while working for the Guinness Brewery in Dublin. Due to proprietary\n        issues, he had to publish under a pseudonym, and so he used the name\n        Student.\n\n        References\n        ----------\n        .. [1] Dalgaard, Peter, "Introductory Statistics With R",\n               Springer, 2002.\n        .. [2] Wikipedia, "Student\'s t-distribution"\n               http://en.wikipedia.org/wiki/Student\'s_t-distribution\n\n        Examples\n        --------\n        From Dalgaard page 83 [1]_, suppose the daily energy intake for 11\n        women in Kj is:\n\n        >>> intake = np.array([5260., 5470, 5640, 6180, 6390, 6515, 6805, 7515, \\\n        ...                    7515, 8230, 8770])\n\n        Does their energy intake deviate systematically from the recommended\n        value of 7725 kJ?\n\n        We have 10 degrees of freedom, so is the sample mean within 95% of the\n        recommended value?\n\n        >>> s = np.random.standard_t(10, size=100000)\n        >>> np.mean(intake)\n        6753.636363636364\n        >>> intake.std(ddof=1)\n        1142.1232221373727\n\n        Calculate the t statistic, setting the ddof parameter to the unbiased\n        value so the divisor in the standard deviation will be degrees of\n        freedom, N-1.\n\n        >>> t = (np.mean(intake)-7725)/(intake.std(ddof=1)/np.sqrt(len(intake)))\n        >>> import matplotlib.pyplot as plt\n        >>> h = plt.hist(s, bins=100, normed=True)\n\n        For a one-sided t-test, how far out in the distribution does the t\n        statistic appear?\n\n        >>> >>> np.sum(s<t) / float(len(s))\n        0.0090699999999999999  #random\n\n        So the p-value is about 0.009, which says the null hypothesis has a\n        probability of about 99% of being true.\n\n        ',
    u'RandomState.tomaxint (line 773)': u'\n        tomaxint(size=None)\n\n        Random integers between 0 and ``sys.maxint``, inclusive.\n\n        Return a sample of uniformly distributed random integers in the interval\n        [0, ``sys.maxint``].\n\n        Parameters\n        ----------\n        size : tuple of ints, int, optional\n            Shape of output.  If this is, for example, (m,n,k), m*n*k samples\n            are generated.  If no shape is specified, a single sample is\n            returned.\n\n        Returns\n        -------\n        out : ndarray\n            Drawn samples, with shape `size`.\n\n        See Also\n        --------\n        randint : Uniform sampling over a given half-open interval of integers.\n        random_integers : Uniform sampling over a given closed interval of\n            integers.\n\n        Examples\n        --------\n        >>> RS = np.random.mtrand.RandomState() # need a RandomState object\n        >>> RS.tomaxint((2,2,2))\n        array([[[1170048599, 1600360186],\n                [ 739731006, 1947757578]],\n               [[1871712945,  752307660],\n                [1601631370, 1479324245]]])\n        >>> import sys\n        >>> sys.maxint\n        2147483647\n        >>> RS.tomaxint((2,2,2)) < sys.maxint\n        array([[[ True,  True],\n                [ True,  True]],\n               [[ True,  True],\n                [ True,  True]]], dtype=bool)\n\n        ',
    u'RandomState.triangular (line 3328)': u'\n        triangular(left, mode, right, size=None)\n\n        Draw samples from the triangular distribution.\n\n        The triangular distribution is a continuous probability distribution with\n        lower limit left, peak at mode, and upper limit right. Unlike the other\n        distributions, these parameters directly define the shape of the pdf.\n\n        Parameters\n        ----------\n        left : scalar\n            Lower limit.\n        mode : scalar\n            The value where the peak of the distribution occurs.\n            The value should fulfill the condition ``left <= mode <= right``.\n        right : scalar\n            Upper limit, should be larger than `left`.\n        size : int or tuple of ints, optional\n            Output shape. Default is None, in which case a single value is\n            returned.\n\n        Returns\n        -------\n        samples : ndarray or scalar\n            The returned samples all lie in the interval [left, right].\n\n        Notes\n        -----\n        The probability density function for the Triangular distribution is\n\n        .. math:: P(x;l, m, r) = \\begin{cases}\n                  \\frac{2(x-l)}{(r-l)(m-l)}& \\text{for $l \\leq x \\leq m$},\\\\\n                  \\frac{2(m-x)}{(r-l)(r-m)}& \\text{for $m \\leq x \\leq r$},\\\\\n                  0& \\text{otherwise}.\n                  \\end{cases}\n\n        The triangular distribution is often used in ill-defined problems where the\n        underlying distribution is not known, but some knowledge of the limits and\n        mode exists. Often it is used in simulations.\n\n        References\n        ----------\n        .. [1] Wikipedia, "Triangular distribution"\n              http://en.wikipedia.org/wiki/Triangular_distribution\n\n        Examples\n        --------\n        Draw values from the distribution and plot the histogram:\n\n        >>> import matplotlib.pyplot as plt\n        >>> h = plt.hist(np.random.triangular(-3, 0, 8, 100000), bins=200,\n        ...              normed=True)\n        >>> plt.show()\n\n        ',
    u'RandomState.uniform (line 1100)': u"\n        uniform(low=0.0, high=1.0, size=1)\n\n        Draw samples from a uniform distribution.\n\n        Samples are uniformly distributed over the half-open interval\n        ``[low, high)`` (includes low, but excludes high).  In other words,\n        any value within the given interval is equally likely to be drawn\n        by `uniform`.\n\n        Parameters\n        ----------\n        low : float, optional\n            Lower boundary of the output interval.  All values generated will be\n            greater than or equal to low.  The default value is 0.\n        high : float\n            Upper boundary of the output interval.  All values generated will be\n            less than high.  The default value is 1.0.\n        size : int or tuple of ints, optional\n            Shape of output.  If the given size is, for example, (m,n,k),\n            m*n*k samples are generated.  If no shape is specified, a single sample\n            is returned.\n\n        Returns\n        -------\n        out : ndarray\n            Drawn samples, with shape `size`.\n\n        See Also\n        --------\n        randint : Discrete uniform distribution, yielding integers.\n        random_integers : Discrete uniform distribution over the closed\n                          interval ``[low, high]``.\n        random_sample : Floats uniformly distributed over ``[0, 1)``.\n        random : Alias for `random_sample`.\n        rand : Convenience function that accepts dimensions as input, e.g.,\n               ``rand(2,2)`` would generate a 2-by-2 array of floats,\n               uniformly distributed over ``[0, 1)``.\n\n        Notes\n        -----\n        The probability density function of the uniform distribution is\n\n        .. math:: p(x) = \\frac{1}{b - a}\n\n        anywhere within the interval ``[a, b)``, and zero elsewhere.\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> s = np.random.uniform(-1,0,1000)\n\n        All values are within the given interval:\n\n        >>> np.all(s >= -1)\n        True\n        >>> np.all(s < 0)\n        True\n\n        Display the histogram of the samples, along with the\n        probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> count, bins, ignored = plt.hist(s, 15, normed=True)\n        >>> plt.plot(bins, np.ones_like(bins), linewidth=2, color='r')\n        >>> plt.show()\n\n        ",
    u'RandomState.vonmises (line 2341)': u'\n        vonmises(mu, kappa, size=None)\n\n        Draw samples from a von Mises distribution.\n\n        Samples are drawn from a von Mises distribution with specified mode\n        (mu) and dispersion (kappa), on the interval [-pi, pi].\n\n        The von Mises distribution (also known as the circular normal\n        distribution) is a continuous probability distribution on the unit\n        circle.  It may be thought of as the circular analogue of the normal\n        distribution.\n\n        Parameters\n        ----------\n        mu : float\n            Mode ("center") of the distribution.\n        kappa : float\n            Dispersion of the distribution, has to be >=0.\n        size : int or tuple of int\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        Returns\n        -------\n        samples : scalar or ndarray\n            The returned samples, which are in the interval [-pi, pi].\n\n        See Also\n        --------\n        scipy.stats.distributions.vonmises : probability density function,\n            distribution, or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the von Mises distribution is\n\n        .. math:: p(x) = \\frac{e^{\\kappa cos(x-\\mu)}}{2\\pi I_0(\\kappa)},\n\n        where :math:`\\mu` is the mode and :math:`\\kappa` the dispersion,\n        and :math:`I_0(\\kappa)` is the modified Bessel function of order 0.\n\n        The von Mises is named for Richard Edler von Mises, who was born in\n        Austria-Hungary, in what is now the Ukraine.  He fled to the United\n        States in 1939 and became a professor at Harvard.  He worked in\n        probability theory, aerodynamics, fluid mechanics, and philosophy of\n        science.\n\n        References\n        ----------\n        Abramowitz, M. and Stegun, I. A. (ed.), *Handbook of Mathematical\n        Functions*, New York: Dover, 1965.\n\n        von Mises, R., *Mathematical Theory of Probability and Statistics*,\n        New York: Academic Press, 1964.\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> mu, kappa = 0.0, 4.0 # mean and dispersion\n        >>> s = np.random.vonmises(mu, kappa, 1000)\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> import scipy.special as sps\n        >>> count, bins, ignored = plt.hist(s, 50, normed=True)\n        >>> x = np.arange(-np.pi, np.pi, 2*np.pi/50.)\n        >>> y = -np.exp(kappa*np.cos(x-mu))/(2*np.pi*sps.jn(0,kappa))\n        >>> plt.plot(x, y/max(y), linewidth=2, color=\'r\')\n        >>> plt.show()\n\n        ',
    u'RandomState.wald (line 3242)': u'\n        wald(mean, scale, size=None)\n\n        Draw samples from a Wald, or Inverse Gaussian, distribution.\n\n        As the scale approaches infinity, the distribution becomes more like a\n        Gaussian.\n\n        Some references claim that the Wald is an Inverse Gaussian with mean=1, but\n        this is by no means universal.\n\n        The Inverse Gaussian distribution was first studied in relationship to\n        Brownian motion. In 1956 M.C.K. Tweedie used the name Inverse Gaussian\n        because there is an inverse relationship between the time to cover a unit\n        distance and distance covered in unit time.\n\n        Parameters\n        ----------\n        mean : scalar\n            Distribution mean, should be > 0.\n        scale : scalar\n            Scale parameter, should be >= 0.\n        size : int or tuple of ints, optional\n            Output shape. Default is None, in which case a single value is\n            returned.\n\n        Returns\n        -------\n        samples : ndarray or scalar\n            Drawn sample, all greater than zero.\n\n        Notes\n        -----\n        The probability density function for the Wald distribution is\n\n        .. math:: P(x;mean,scale) = \\sqrt{\\frac{scale}{2\\pi x^3}}e^\n                                    \\frac{-scale(x-mean)^2}{2\\cdotp mean^2x}\n\n        As noted above the Inverse Gaussian distribution first arise from attempts\n        to model Brownian Motion. It is also a competitor to the Weibull for use in\n        reliability modeling and modeling stock returns and interest rate\n        processes.\n\n        References\n        ----------\n        .. [1] Brighton Webs Ltd., Wald Distribution,\n              http://www.brighton-webs.co.uk/distributions/wald.asp\n        .. [2] Chhikara, Raj S., and Folks, J. Leroy, "The Inverse Gaussian\n              Distribution: Theory : Methodology, and Applications", CRC Press,\n              1988.\n        .. [3] Wikipedia, "Wald distribution"\n              http://en.wikipedia.org/wiki/Wald_distribution\n\n        Examples\n        --------\n        Draw values from the distribution and plot the histogram:\n\n        >>> import matplotlib.pyplot as plt\n        >>> h = plt.hist(np.random.wald(3, 2, 100000), bins=200, normed=True)\n        >>> plt.show()\n\n        ',
    u'RandomState.weibull (line 2531)': u'\n        weibull(a, size=None)\n\n        Weibull distribution.\n\n        Draw samples from a 1-parameter Weibull distribution with the given\n        shape parameter `a`.\n\n        .. math:: X = (-ln(U))^{1/a}\n\n        Here, U is drawn from the uniform distribution over (0,1].\n\n        The more common 2-parameter Weibull, including a scale parameter\n        :math:`\\lambda` is just :math:`X = \\lambda(-ln(U))^{1/a}`.\n\n        Parameters\n        ----------\n        a : float\n            Shape of the distribution.\n        size : tuple of ints\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn.\n\n        See Also\n        --------\n        scipy.stats.distributions.weibull_max\n        scipy.stats.distributions.weibull_min\n        scipy.stats.distributions.genextreme\n        gumbel\n\n        Notes\n        -----\n        The Weibull (or Type III asymptotic extreme value distribution for smallest\n        values, SEV Type III, or Rosin-Rammler distribution) is one of a class of\n        Generalized Extreme Value (GEV) distributions used in modeling extreme\n        value problems.  This class includes the Gumbel and Frechet distributions.\n\n        The probability density for the Weibull distribution is\n\n        .. math:: p(x) = \\frac{a}\n                         {\\lambda}(\\frac{x}{\\lambda})^{a-1}e^{-(x/\\lambda)^a},\n\n        where :math:`a` is the shape and :math:`\\lambda` the scale.\n\n        The function has its peak (the mode) at\n        :math:`\\lambda(\\frac{a-1}{a})^{1/a}`.\n\n        When ``a = 1``, the Weibull distribution reduces to the exponential\n        distribution.\n\n        References\n        ----------\n        .. [1] Waloddi Weibull, Professor, Royal Technical University, Stockholm,\n               1939 "A Statistical Theory Of The Strength Of Materials",\n               Ingeniorsvetenskapsakademiens Handlingar Nr 151, 1939,\n               Generalstabens Litografiska Anstalts Forlag, Stockholm.\n        .. [2] Waloddi Weibull, 1951 "A Statistical Distribution Function of Wide\n               Applicability",  Journal Of Applied Mechanics ASME Paper.\n        .. [3] Wikipedia, "Weibull distribution",\n               http://en.wikipedia.org/wiki/Weibull_distribution\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> a = 5. # shape\n        >>> s = np.random.weibull(a, 1000)\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> x = np.arange(1,100.)/50.\n        >>> def weib(x,n,a):\n        ...     return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)\n\n        >>> count, bins, ignored = plt.hist(np.random.weibull(5.,1000))\n        >>> x = np.arange(1,100.)/50.\n        >>> scale = count.max()/weib(x, 1., 5.).max()\n        >>> plt.plot(x, weib(x, 1., 5.)*scale)\n        >>> plt.show()\n\n        ',
    u'RandomState.zipf (line 3690)': u"\n        zipf(a, size=None)\n\n        Draw samples from a Zipf distribution.\n\n        Samples are drawn from a Zipf distribution with specified parameter\n        `a` > 1.\n\n        The Zipf distribution (also known as the zeta distribution) is a\n        continuous probability distribution that satisfies Zipf's law: the\n        frequency of an item is inversely proportional to its rank in a\n        frequency table.\n\n        Parameters\n        ----------\n        a : float > 1\n            Distribution parameter.\n        size : int or tuple of int, optional\n            Output shape.  If the given shape is, e.g., ``(m, n, k)``, then\n            ``m * n * k`` samples are drawn; a single integer is equivalent in\n            its result to providing a mono-tuple, i.e., a 1-D array of length\n            *size* is returned.  The default is None, in which case a single\n            scalar is returned.\n\n        Returns\n        -------\n        samples : scalar or ndarray\n            The returned samples are greater than or equal to one.\n\n        See Also\n        --------\n        scipy.stats.distributions.zipf : probability density function,\n            distribution, or cumulative density function, etc.\n\n        Notes\n        -----\n        The probability density for the Zipf distribution is\n\n        .. math:: p(x) = \\frac{x^{-a}}{\\zeta(a)},\n\n        where :math:`\\zeta` is the Riemann Zeta function.\n\n        It is named for the American linguist George Kingsley Zipf, who noted\n        that the frequency of any word in a sample of a language is inversely\n        proportional to its rank in the frequency table.\n\n        References\n        ----------\n        Zipf, G. K., *Selected Studies of the Principle of Relative Frequency\n        in Language*, Cambridge, MA: Harvard Univ. Press, 1932.\n\n        Examples\n        --------\n        Draw samples from the distribution:\n\n        >>> a = 2. # parameter\n        >>> s = np.random.zipf(a, 1000)\n\n        Display the histogram of the samples, along with\n        the probability density function:\n\n        >>> import matplotlib.pyplot as plt\n        >>> import scipy.special as sps\n        Truncate s values at 50 so plot is interesting\n        >>> count, bins, ignored = plt.hist(s[s<50], 50, normed=True)\n        >>> x = np.arange(1., 50.)\n        >>> y = x**(-a)/sps.zetac(a)\n        >>> plt.plot(x, y/max(y), linewidth=2, color='r')\n        >>> plt.show()\n\n        ",
}

