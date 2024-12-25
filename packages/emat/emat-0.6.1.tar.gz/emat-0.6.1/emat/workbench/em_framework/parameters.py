'''parameters and collections of parameters'''
import abc
import itertools
import numbers
import pandas as pd
import scipy as sp
import warnings

from .util import (NamedObject, Variable, NamedObjectMap, Counter,
                   NamedDict, combine)
from ..util import get_module_logger

# Created on Jul 14, 2016
#
# .. codeauthor::jhkwakkel <j.h.kwakkel (at) tudelft (dot) nl>

__all__ = [
    'Constant', 'RealParameter', 'IntegerParameter', 'CategoricalParameter',
    'BooleanParameter',
    'Policy', 'Scenario',
    'parameters_from_csv', 'parameters_to_csv', 'experiment_generator'
    'create_parameters',
    'experiment_generator',
    'Policy',
    'Scenario',
    'Experiment']
_logger = get_module_logger(__name__)



class Bound(metaclass=abc.ABCMeta):
    def __get__(self, instance, cls):
        try:
            bound = instance.__dict__[self.internal_name]
        except KeyError:
            bound =  self.get_bound(instance)
            self.__set__(instance, bound)
        return bound

    def __set__(self, instance, value):
        instance.__dict__[self.internal_name] = value

    def __set_name__(self, cls, name):
        self.name = name
        self.internal_name = '_' + name


class UpperBound(Bound):
    def get_bound(self, instance):
        bound = instance.dist.ppf(1.0)
        return bound


class LowerBound(Bound):
    def get_bound(self, owner):
        ppf_zero = 0
        
        if isinstance(owner.dist.dist, sp.stats.rv_discrete):  # @UndefinedVariable
            # ppf at actual zero for rv_discrete gives lower bound - 1
            # due to a quirk in the scipy.stats implementation
            # so we use the smallest positive float instead
            ppf_zero = 5e-324
    
        bound = owner.dist.ppf(ppf_zero)
        return bound


class Constant(NamedObject):
    '''Constant class,

    can be used for any parameter that has to be set to a fixed value

    '''

    def __init__(self, name, value):
        super(Constant, self).__init__(name)
        self.value = value

    def __repr__(self, *args, **kwargs):
        return '{}(\'{}\', {})'.format(self.__class__.__name__,
                                       self.name, self.value)


class Category(Constant):
    def __init__(self, name, value):
        super(Category, self).__init__(name, value)

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return super(Constant, self).__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name, self.value))

def create_category(cat):
    if isinstance(cat, Category):
        return cat
    else:
        return Category(str(cat), cat)


class Parameter(Variable, metaclass=abc.ABCMeta):
    ''' Base class for any model input parameter

    Parameters
    ----------
    name : str
    lower_bound : int or float
    upper_bound : int or float
    resolution : collection
    pff : bool
          if true, sample over this parameter using resolution in case of
          partial factorial sampling

    Raises
    ------
    ValueError
        if lower bound is larger than upper bound
    ValueError
        if entries in resolution are outside range of lower_bound and
        upper_bound

    '''
    lower_bound = LowerBound()
    upper_bound = UpperBound()
    default = None
    
    @property    
    def resolution(self):
        return self._resolution
    
    @resolution.setter
    def resolution(self, value):
        if value:
            if (min(value) < self.lower_bound) or (max(value) > self.upper_bound):
                raise ValueError('resolution not consistent with lower and '
                                  'upper bound')
        self._resolution = value


    def __init__(self, name, lower_bound, upper_bound, resolution=None,
                 default=None, variable_name=None, pff=False):
        super(Parameter, self).__init__(name)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.resolution = resolution
        self.default = default
        self.variable_name = variable_name
        self.pff = pff
        
    @classmethod
    def from_dist(cls, name, dist, **kwargs):
        '''alternative constructor for creating a parameter from a frozen
        scipy.stats distribution directly
        
        Parameters
        ----------
        dist : scipy stats frozen dist
        **kwargs : valid keyword arguments for Parameter instance
        
        '''
        assert(isinstance(dist, sp.stats._distn_infrastructure.rv_frozen))  # @UndefinedVariable
        self = cls.__new__(cls)
        self.dist = dist
        self.name = name
        self.resolution = None
        self.variable_name = None
        self.ppf = None
        
        for k, v in kwargs.items():
            if k in {"default", "resolution", "variable_name", "pff"}:
                setattr(self, k, v)
            else:
                raise ValueError(f"unknown property {k} for Parameter")
        
        return self


    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        
        self_keys = set(self.__dict__.keys())
        other_keys = set(other.__dict__.keys())
        if self_keys - other_keys:
            return False
        else:
            for key in self_keys:
                if key != 'dist':
                    if getattr(self, key) != getattr(other, key):
                        return False
                else:
                    # name, parameters
                    self_dist = getattr(self, key)
                    other_dist = getattr(other, key)
                    if self_dist.dist.name != other_dist.dist.name:
                        return False
                    if self_dist.args != other_dist.args:
                        return False
                    
            else:
                return True


    def __str__(self):
        return self.name

#     def __repr__(self, *args, **kwargs):
#         start = '{}(\'{}\', {}, {}'.format(self.__class__.__name__,
#                                            self.name,
#                                            self.lower_bound, self.upper_bound)
# 
#         if self.resolution:
#             start += ', resolution={}'.format(self.resolution)
#         if self.default:
#             start += ', default={}'.format(self.default)
#         if self.variable_name != [self.name]:
#             start += ', variable_name={}'.format(self.variable_name)
#         if self.pff:
#             start += ', pff={}'.format(self.pff)
# 
#         start += ')'
# 
#         return start


class RealParameter(Parameter):
    ''' real valued model input parameter

    Parameters
    ----------
    name : str
    lower_bound : int or float
    upper_bound : int or float
    resolution : iterable
    variable_name : str, or list of str

    Raises
    ------
    ValueError
        if lower bound is larger than upper bound
    ValueError
        if entries in resolution are outside range of lower_bound and
        upper_bound

    '''

    def __init__(self, name, lower_bound, upper_bound, resolution=None,
                 default=None, variable_name=None, pff=False):
        super(
            RealParameter,
            self).__init__(
            name,
            lower_bound,
            upper_bound,
            resolution=resolution,
            default=default,
            variable_name=variable_name,
            pff=pff)

        self.dist = sp.stats.uniform(lower_bound, upper_bound-lower_bound)  # @UndefinedVariable


    @classmethod
    def from_dist(cls, name, dist, **kwargs):
        if not isinstance(dist.dist, sp.stats.rv_continuous):  # @UndefinedVariable
            raise ValueError("dist should be instance of rv_continouos")
        return super(RealParameter, cls).from_dist(name, dist, **kwargs)


class IntegerParameter(Parameter):
    ''' integer valued model input parameter

    Parameters
    ----------
    name : str
    lower_bound : int
    upper_bound : int
    resolution : iterable
    variable_name : str, or list of str

    Raises
    ------
    ValueError
        if lower bound is larger than upper bound
    ValueError
        if entries in resolution are outside range of lower_bound and
        upper_bound, or not an numbers.Integral instance
    ValueError
        if lower_bound or upper_bound is not an numbers.Integral instance

    '''

    def __init__(self, name, lower_bound, upper_bound, resolution=None,
                 default=None, variable_name=None, pff=False):
        super(IntegerParameter,self).__init__(name, lower_bound, upper_bound,
                                        resolution=resolution, default=default,
                                        variable_name=variable_name, pff=pff)

        lb_int = isinstance(lower_bound, numbers.Integral)
        up_int = isinstance(upper_bound, numbers.Integral)

        if not (lb_int or up_int):
            raise ValueError('lower bound and upper bound must be integers')

        self.dist = sp.stats.randint(self.lower_bound, self.upper_bound + 1)  # @UndefinedVariable

    @classmethod
    def from_dist(cls, name, dist, **kwargs):
        if not isinstance(dist.dist, sp.stats.rv_discrete):  # @UndefinedVariable
            raise ValueError("dist should be instance of rv_discrete")
        return super(IntegerParameter, cls).from_dist(name, dist, **kwargs)


class CategoricalParameter(IntegerParameter):
    ''' categorical model input parameter

    Parameters
    ----------
    name : str
    categories : collection of obj
    variable_name : str, or list of str
    multivalue : boolean
                 if categories have a set of values, for each variable_name
                 a different one.

    '''

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, values):
        self._categories.extend(values)

    def __init__(self, name, categories, default=None, variable_name=None,
                 pff=False, multivalue=False):
        lower_bound = 0
        upper_bound = len(categories) - 1

        if upper_bound == 0:
            raise ValueError('there should be more than 1 category')

        super(
            CategoricalParameter,
            self).__init__(
            name,
            lower_bound,
            upper_bound,
            resolution=None,
            default=default,
            variable_name=variable_name,
            pff=pff)
        cats = [create_category(cat) for cat in categories]

        self._categories = NamedObjectMap(Category)

        self.categories = cats
        self.resolution = [i for i in range(len(self.categories))]
        self.multivalue = multivalue

    def index_for_cat(self, category):
        '''return index of category

        Parameters
        ----------
        category : object

        Returns
        -------
        int


        '''
        for i, cat in enumerate(self.categories):
            if cat.name == category:
                return i
        raise ValueError("category not found")

    def cat_for_index(self, index):
        '''return category given index

        Parameters
        ----------
        index  : int

        Returns
        -------
        object

        '''

        return self.categories[index]

    def invert(self, name):
        ''' invert a category to an integer

        Parameters
        ----------
        name : obj
               category

        Raises
        ------
        ValueError
            if category is not found

        '''
        warnings.warn('deprecated, use index_for_cat instead')
        return self.index_for_cat(name)

    def __repr__(self, *args, **kwargs):
        template1 = 'CategoricalParameter(\'{}\', {}, default={})'
        template2 = 'CategoricalParameter(\'{}\', {})'

        if self.default:
            representation = template1.format(self.name, self.resolution,
                                              self.default)
        else:
            representation = template2.format(self.name, self.resolution)

        return representation
    
    @classmethod
    def from_dist(cls, name, dist, **kwargs):
        # TODO:: how to handle this
        # probebly need to pass categories as list and zip
        # categories to integers implied by dist
        if cls is CategoricalParameter:
            # only not implemented if it is CategoricalParameter
            # allow BooleanParameter to pass through correctly.
            raise NotImplementedError(("custom distributions over categories "
                                       "not supported yet"))
        if not isinstance(dist.dist, sp.stats.rv_discrete):  # @UndefinedVariable
            raise ValueError("dist should be instance of rv_discrete")
        categories = kwargs.pop('categories')
        multivalue = kwargs.pop('multivalue', False)
        self = super(CategoricalParameter, cls).from_dist(name, dist, **kwargs)
        cats = [create_category(cat) for cat in categories]

        self._categories = NamedObjectMap(Category)

        self.categories = cats
        self.resolution = [i for i in range(len(self.categories))]
        self.multivalue = multivalue
        return self


class BooleanParameter(CategoricalParameter):
    ''' boolean model input parameter

    A BooleanParameter is similar to a CategoricalParameter, except
    the category values can only be True or False.

    Parameters
    ----------
    name : str
    variable_name : str, or list of str

    '''

    def __init__(self, name, default=None, variable_name=None,
                 pff=False):
        super(BooleanParameter, self).__init__(
            name, categories=[False, True], default=default,
            variable_name=variable_name, pff=pff)

    @classmethod
    def from_dist(cls, name, dist, **kwargs):
        if not isinstance(dist.dist, sp.stats.rv_discrete):  # @UndefinedVariable
            raise ValueError("dist should be instance of rv_discrete")

        if dist.ppf(5e-324) != 0:
            raise ValueError("dist should have minimum value of 0")

        if dist.ppf(1.0) != 1:
            raise ValueError("dist should have maximum value of 1")

        result = super().from_dist(name=name, dist=dist,
                                   categories=[False, True], **kwargs)
        # cats = [create_category(cat) for cat in [False, True]]
        # result._categories = NamedObjectMap(Category)
        # result.categories = cats
        return result

#     def __repr__(self, *args, **kwargs):
#         template1 = 'BooleanParameter(\'{}\', default={})'
#         template2 = 'BooleanParameter(\'{}\', )'
# 
#         if self.default:
#             representation = template1.format(self.name,
#                                               self.default)
#         else:
#             representation = template2.format(self.name, )
# 
#         return representation
# class BinaryParameter(CategoricalParameter):
#     ''' a categorical model input parameter that is only True or False
# 
#     Parameters
#     ----------
#     name : str
#     '''
# 
#     def __init__(self, name, default=None, ):
#         super(
#             BinaryParameter,
#             self).__init__(
#             name,
#             categories=[
#                 False,
#                 True],
#             default=default)

class Policy(NamedDict):
    '''Helper class representing a policy
    
    Attributes
    ----------
    name : str, int, or float
    id : int
    
    all keyword arguments are wrapped into a dict.
    
    '''
    # TODO:: separate id and name
    # if name is not provided fall back on id
    # id will always be a number and can be generated by
    # a counter
    # the new experiment class can than take the names from
    # policy and scenario to create a unique name while also
    # multiplying the ID's (assuming we count from 1 onward) to get
    # a unique experiment ID
    id_counter = Counter(1)

    def __init__(self, name=Counter(), **kwargs):

        # TODO: perhaps move this to seperate function that internally uses
        # counter
        if isinstance(name, int):
            name = f"policy {name}"

        super(Policy, self).__init__(name, **kwargs)
        self.id = Policy.id_counter()

    def to_list(self, parameters):
        '''get list like representation of policy where the
        parameters are in the order of levers'''

        return [self[param.name] for param in parameters]

    def __repr__(self):
        return "Policy({})".format(super(Policy, self).__repr__())


class Scenario(NamedDict):
    '''Helper class representing a scenario
    
    Attributes
    ----------
    name : str, int, or float
    id : int
    
    all keyword arguments are wrapped into a dict.
    
    '''
    
    # we need to start from 1 so scenario id is known
    id_counter = Counter(1)

    def __init__(self, name=Counter(), **kwargs):
        super(Scenario, self).__init__(name, **kwargs)
        self.id = Scenario.id_counter()

    def __repr__(self):
        return "Scenario({})".format(super(Scenario, self).__repr__())


class Case(NamedObject):
    '''A convenience object that contains a specification
    of the model, policy, and scenario to run

    '''

#     TODO:: we need a better name for this. probably this should be
#     named Experiment, while Experiment should be
#     ExperimentReplication

    def __init__(self, name, model_name, policy, scenario, experiment_id):
        super(Case, self).__init__(name)
        self.experiment_id = experiment_id
        self.policy = policy
        self.model_name = model_name
        self.scenario = scenario


class Experiment(NamedDict):
    '''helper class that combines scenario, policy, any constants, and
    replication information (seed etc) into a single dictionary.

    '''

    def __init__(self, scenario, policy, constants, replication=None):
        scenario_id = scenario.id
        policy_id = policy.id

        if replication is None:
            replication_id = 1
        else:
            replication_id = replication.id
            constants = combine(constants, replication)

        # this is a unique identifier for an experiment
        # we might also create a better looking name
        self.id = scenario_id * policy_id * replication_id
        name = '{}_{}_{}'.format(scenario.name, policy.name, replication_id)

        super(Experiment, self).__init__(
            name, **combine(scenario, policy, constants))

def zip_cycle(*args):
    maxlen = max(len(a) for a in args)
    return itertools.islice(zip(*(itertools.cycle(a) for a in args)), maxlen)


def experiment_generator(scenarios, model_structures, policies, zip_over=None):
    '''

    generator function which yields experiments

    Parameters
    ----------
    designs : iterable of dicts
    model_structures : list
    policies : list
    zip_over : Collection[str], optional
        A collection that contains exactly two or three members of the set
        {'scenarios', 'policies', 'models'}.  If a set is given, the length
        of all other arguments that are indicated in this set must be the
        same, and the experiment generator will create experiments based on
        a `zip` through the values in these collections, instead of creating
        experiments across all possible combinations of the values.

    Notes
    -----
    When called with zip_over as None, this generator is essentially
    three nested loops: for each model structure,
    for each policy, for each scenario, return the experiment. This means
    that designs should not be a generator because this will be exhausted after
    the running the first policy on the first model.  If zip_over contains
    two items, then those two will be paired up, but there will still be
    two nested loops.

    When called with zip_over set as not None, if the length of the lists
    identified in zip_over is unbalanced, the shorter list(s) will be
    recycled in the same order after they have been exhausted until the
    longest list is exhausted. If lists are randomly shuffled before being
    passed to this generator, this is equivalent to sampling (without
    replacement) from each space.

    '''
    if zip_over is None:
        zip_over = set()
    else:
        zip_over = set(zip_over)

    if not zip_over.issubset({'scenarios', 'policies', 'models'}):
        raise ValueError("zip_over must be subset of {'scenarios', 'policies', 'models'} or None")
    if len(zip_over) == 1:
        raise ValueError("zip_over cannot be one item")

    if zip_over == {'scenarios', 'policies', 'models'}:
        jobs = (
            (m_, p_, s_)
            for m_, p_, s_ in zip_cycle(
                model_structures, policies, scenarios
            )
        )
    elif zip_over == {'scenarios', 'policies'}:
        jobs = (
            (m_, p_, s_)
            for m_, (p_, s_) in itertools.product(
                model_structures, zip_cycle(policies, scenarios)
            )
        )
    elif zip_over == {'scenarios', 'models'}:
        jobs = (
            (m_, p_, s_)
            for p_, (m_, s_) in itertools.product(
                policies, zip_cycle(model_structures, scenarios)
            )
        )
    elif zip_over == {'policies', 'models'}:
        jobs = (
            (m_, p_, s_)
            for s_, (m_, p_) in itertools.product(
                scenarios, zip_cycle(model_structures, policies)
            )
        )
    else:
        jobs = itertools.product(model_structures, policies, scenarios)

    for i, job in enumerate(jobs):
        msi, policy, scenario = job
        name = '{} {} {}'.format(msi.name, policy.name, i)
        case = Case(name, msi.name, policy, scenario, i)
        yield case


def parameters_to_csv(parameters, file_name):
    '''Helper function for writing a collection of parameters to a csv file

    Parameters
    ----------
    parameters : collection of Parameter instances
    file_name :  str


    The function iterates over the collection and turns these into a data
    frame prior to storing them. The resulting csv can be loaded using the
    create_parameters function. Note that currently we don't store resolution
    and default attributes.

    '''

    params = {}

    for i, param in enumerate(parameters):

        if isinstance(param, CategoricalParameter):
            values = param.resolution
        else:
            values = param.lower_bound, param.upper_bound

        dict_repr = {j: value for j, value in enumerate(values)}
        dict_repr['name'] = param.name

        params[i] = dict_repr

    params = pd.DataFrame.from_dict(params, orient='index')

    # for readability it is nice if name is the first column, so let's
    # ensure this
    cols = params.columns.tolist()
    cols.insert(0, cols.pop(cols.index('name')))
    params = params.reindex(columns=cols)

    # we can now safely write the dataframe to a csv
    pd.DataFrame.to_csv(params, file_name, index=False)


def parameters_from_csv(uncertainties, **kwargs):
    '''Helper function for creating many Parameters based on a DataFrame
    or csv file

    Parameters
    ----------
    uncertainties : str, DataFrame
    **kwargs : dict, arguments to pass to pandas.read_csv

    Returns
    -------
    list of Parameter instances


    This helper function creates uncertainties. It assumes that the
    DataFrame or csv file has a column titled 'name', optionally a type column
    {int, real, cat}, can be included as well. the remainder of the columns
    are handled as values for the parameters. If type is not specified,
    the function will try to infer type from the values.

    Note that this function does not support the resolution and default kwargs
    on parameters.

    An example of a csv:

    NAME,TYPE,,,
    a_real,real,0,1.1,
    an_int,int,1,9,
    a_categorical,cat,a,b,c

    this CSV file would result in

    [RealParameter('a_real', 0, 1.1, resolution=[], default=None),
     IntegerParameter('an_int', 1, 9, resolution=[], default=None),
     CategoricalParameter('a_categorical', ['a', 'b', 'c'], default=None)]

    '''

    if isinstance(uncertainties, str):
        uncertainties = pd.read_csv(uncertainties, **kwargs)
    elif not isinstance(uncertainties, pd.DataFrame):
        uncertainties = pd.DataFrame.from_dict(uncertainties)
    else:
        uncertainties = uncertainties.copy()

    parameter_map = {'int': IntegerParameter,
                     'real': RealParameter,
                     'cat': CategoricalParameter,
                     'bool': BooleanParameter,
                     }

    # check if names column is there
    if ('NAME' not in uncertainties) and ('name' not in uncertainties):
        raise IndexError('name column missing')
    elif ('NAME' in uncertainties.columns):
        names = uncertainties.ix[:, 'NAME']
        uncertainties.drop(['NAME'], axis=1, inplace=True)
    else:
        names = uncertainties.ix[:, 'name']
        uncertainties.drop(['name'], axis=1, inplace=True)

    # check if type column is there
    infer_type = False
    if ('TYPE' not in uncertainties) and ('type' not in uncertainties):
        infer_type = True
    elif ('TYPE' in uncertainties):
        types = uncertainties.ix[:, 'TYPE']
        uncertainties.drop(['TYPE'], axis=1, inplace=True)
    else:
        types = uncertainties.ix[:, 'type']
        uncertainties.drop(['type'], axis=1, inplace=True)

    uncs = []
    for i, row in uncertainties.iterrows():
        name = names[i]
        values = row.values[row.notnull().values]
        type = None  # @ReservedAssignment

        if infer_type:
            if len(values) != 2:
                type = 'cat'  # @ReservedAssignment
            else:
                l, u = values

                if isinstance(
                        l, numbers.Integral) and isinstance(
                        u, numbers.Integral):
                    type = 'int'  # @ReservedAssignment
                else:
                    type = 'real'  # @ReservedAssignment

        else:
            type = types[i]  # @ReservedAssignment

            if (type != 'cat') and (len(values) != 2):
                raise ValueError(
                    'too many values specified for {}, is {}, should be 2'.format(
                        name, values.shape[0]))

        if type == 'cat':
            uncs.append(parameter_map[type](name, values))
        else:
            uncs.append(parameter_map[type](name, *values))
    return uncs
