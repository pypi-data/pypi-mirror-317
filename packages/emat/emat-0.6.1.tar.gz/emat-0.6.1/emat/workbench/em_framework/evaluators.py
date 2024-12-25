'''
collection of evaluators for performing experiments, optimization, and robust
optimization

'''
import enum
import multiprocessing
import numbers
import os
import random
import shutil
import string
import threading
import warnings
import operator
import functools
from .samplers import AbstractSampler

warnings.simplefilter("once", ImportWarning)

try:
    from .ema_ipyparallel import (start_logwatcher, set_engine_logger,
                                  initialize_engines, cleanup, _run_experiment)
except (ImportError, ModuleNotFoundError):
    warnings.warn(
        'ipyparallel not installed - IpyparalleEvaluator not available')

from ..util import EMAError, get_module_logger, ema_logging
from .util import NamedObjectMap, determine_objects, representation
from .salib_samplers import (SobolSampler, MorrisSampler, FASTSampler)
from .samplers import (MonteCarloSampler, FullFactorialSampler, LHSSampler,
                       PartialFactorialSampler, UniformLHSSampler, 
                       sample_levers, sample_uncertainties,
                       DefaultDesigns, determine_parameters)
from .parameters import (experiment_generator, Scenario, Policy)
from .outcomes import ScalarOutcome, AbstractOutcome
from .optimization import (evaluate_robust, evaluate, EpsNSGAII,
                           to_problem, to_robust_problem,
                           process_levers, process_uncertainties,
                           process_robust, _optimize)
from .model import AbstractModel
from .experiment_runner import ExperimentRunner
from .ema_multiprocessing import LogQueueReader, initializer, add_tasks
from .callbacks import DefaultCallback

# =======
# from .outcomes import ScalarOutcome, AbstractOutcome
# from .parameters import (experiment_generator, Scenario, Policy)
# from .samplers import (MonteCarloSampler, FullFactorialSampler, LHSSampler,
#                        PartialFactorialSampler, sample_levers,
#                        sample_uncertainties, determine_parameters,
#                        DefaultDesigns)
#
# # TODO:: should become optional import
# from .salib_samplers import (SobolSampler, MorrisSampler, FASTSampler)
# from .util import NamedObjectMap, determine_objects, representation
# from ..util import EMAError, get_module_logger, ema_logging
# >>>>>>> cs_master


# Created on 5 Mar 2017
#
# .. codeauthor::jhkwakkel <j.h.kwakkel (at) tudelft (dot) nl>

__all__ = ['MultiprocessingEvaluator', 'IpyparallelEvaluator',
           'optimize', 'perform_experiments', 'SequentialEvaluator',
           'Samplers']

_logger = get_module_logger(__name__)


class Samplers(enum.Enum):
    ## TODO:: have samplers register themselves on class instantiation
    
    MC = MonteCarloSampler()
    LHS = LHSSampler()
    UNIFORM_LHS = UniformLHSSampler()
    FF = FullFactorialSampler()
    PFF = PartialFactorialSampler()
    SOBOL = SobolSampler()
    FAST = FASTSampler()
    MORRIS = MorrisSampler()
    
    

class BaseEvaluator(object):
    '''evaluator for experiments using a multiprocessing pool

    Parameters
    ----------
    msis : collection of models
    searchover : {None, 'levers', 'uncertainties'}, optional
                  to be used in combination with platypus

    Raises
    ------
    ValueError

    '''
    reporting_frequency = 3

    def __init__(self, msis):
        super(BaseEvaluator, self).__init__()

        if isinstance(msis, AbstractModel):
            msis = [msis]

        self._msis = msis

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finalize()

        if exc_type is not None:
            return False

    def initialize(self):
        '''initialize the evaluator'''
        raise NotImplementedError

    def finalize(self):
        ''' finalize the evaluator'''
        raise NotImplementedError

    def evaluate_experiments(self, scenarios, policies, callback, zip_over=None):
        '''used by ema_workbench'''
        raise NotImplementedError

    def evaluate_all(self, jobs, **kwargs):
        '''makes ema_workbench evaluators compatible with Platypus
        evaluators as used by platypus algorithms
        '''
        self.callback()

        problem = jobs[0].solution.problem
        searchover = problem.searchover

        if searchover == 'levers':
            scenarios, policies = process_levers(jobs)
            jobs_collection = zip(policies, jobs)
        elif searchover == 'uncertainties':
            scenarios, policies = process_uncertainties(jobs)
            jobs_collection = zip(scenarios, jobs)
        elif searchover == 'robust':
            scenarios, policies = process_robust(jobs)
            jobs_collection = zip(policies, jobs)
        else:
            raise NotImplementedError()

        # overwrite the default 10 progress reports  with 5 reports
        callback = perform_experiments(
            self._msis,
            evaluator=self,
            reporting_frequency=self.reporting_frequency,
            scenarios=scenarios,
            policies=policies,
            return_callback=True)

        experiments, outcomes = callback.get_results()

        if searchover in ('levers', 'uncertainties'):
            evaluate(jobs_collection, experiments, outcomes, problem)
        else:
            evaluate_robust(jobs_collection, experiments, outcomes, problem)

        return jobs

    def perform_experiments(self, scenarios=0, policies=0,
                            reporting_interval=None, reporting_frequency=10,
                            uncertainty_union=False, lever_union=False,
                            outcome_union=False,
                            uncertainty_sampling=Samplers.LHS,
                            levers_sampling=Samplers.LHS, callback=None,
                            zip_over=None, log_level=20):
        '''convenience method for performing experiments.

        is forwarded to :func:perform_experiments, with evaluator and
        models arguments added in.

        '''
        return perform_experiments(self._msis, scenarios=scenarios,
                                   policies=policies, evaluator=self,
                                   reporting_interval=reporting_interval,
                                   reporting_frequency=reporting_frequency,
                                   uncertainty_union=uncertainty_union,
                                   lever_union=lever_union,
                                   outcome_union=outcome_union,
                                   uncertainty_sampling=uncertainty_sampling,
                                   levers_sampling=levers_sampling,
                                   callback=callback,
                                   zip_over=zip_over,
                                   log_level=log_level)

    def optimize(self, algorithm=EpsNSGAII, nfe=10000, searchover='levers',
                 reference=None, constraints=None, convergence_freq=1000,
                 logging_freq=5, **kwargs):
        '''convenience method for outcome optimization.

        is forwarded to :func:optimize, with evaluator and models
        arguments added in.

        '''
        return optimize(self._msis, algorithm=algorithm, nfe=nfe,
                        searchover=searchover, evaluator=self,
                        reference=reference, constraints=constraints,
                        convergence_freq=convergence_freq,
                        logging_freq=logging_freq, **kwargs)

    def robust_optimize(self, robustness_functions, scenarios,
                        algorithm=EpsNSGAII, nfe=10000, convergence_freq=1000,
                        logging_freq=5, **kwargs):
        '''convenience method for robust optimization.

        is forwarded to :func:robust_optimize, with evaluator and models
        arguments added in.

        '''
        return robust_optimize(self._msis, robustness_functions, scenarios,
                               self, algorithm=algorithm, nfe=nfe,
                               convergence_freq=convergence_freq,
                               logging_freq=logging_freq, **kwargs)

    def robust_evaluate(self, robustness_functions, scenarios, policies,
                        **kwargs):
        '''convenience method for robust evaluation.

        is forwarded to :func:robust_evaluate, with evaluator and models
        arguments added in.

        '''
        return robust_evaluate(self._msis, robustness_functions, scenarios, policies,
                               self, **kwargs)


class SequentialEvaluator(BaseEvaluator):
    def __init__(self, models, **kwargs):
        super(SequentialEvaluator, self).__init__(models, **kwargs)

    def initialize(self):
        pass

    def finalize(self):
        pass

    def evaluate_experiments(self, scenarios, policies, callback, zip_over=None):
        _logger.info("performing experiments sequentially")

        ex_gen = experiment_generator(scenarios, self._msis, policies, zip_over)

        models = NamedObjectMap(AbstractModel)
        models.extend(self._msis)

        try:
            cwd = os.getcwd()
        except FileNotFoundError:
            cwd = None
        runner = ExperimentRunner(models)

        for experiment in ex_gen:
            outcomes = runner.run_experiment(experiment)
            callback(experiment, outcomes)
        runner.cleanup()
        if cwd is not None:
            os.chdir(cwd)


class MultiprocessingEvaluator(BaseEvaluator):
    '''evaluator for experiments using a multiprocessing pool

    Parameters
    ----------
    msis : collection of models
    n_processes : int (optional)
    max_tasks : int (optional)

    '''

    def __init__(self, msis, n_processes=None,
                 maxtasksperchild=None, **kwargs):
        super(MultiprocessingEvaluator, self).__init__(msis, **kwargs)

        self._pool = None
        self.n_processes = n_processes
        self.maxtasksperchild = maxtasksperchild

    def initialize(self):
        log_queue = multiprocessing.Queue()

        log_queue_reader = LogQueueReader(log_queue)
        log_queue_reader.start()

        try:
            loglevel = ema_logging._rootlogger.getEffectiveLevel()
        except AttributeError:
            loglevel = 30

        # check if we need a working directory
        for model in self._msis:
            try:
                model.working_directory
            except AttributeError:
                self.root_dir = None
                break
        else:
            random_part = [random.choice(string.ascii_letters + string.digits)
                           for _ in range(5)]
            random_part = ''.join(random_part)
            self.root_dir = os.path.abspath("tmp" + random_part)
            os.makedirs(self.root_dir)

        self._pool = multiprocessing.Pool(self.n_processes, initializer,
                                          (self._msis, log_queue, loglevel,
                                           self.root_dir), self.maxtasksperchild)
        self.n_processes = self._pool._processes
        _logger.info("pool started")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _logger.info("terminating pool")

        if exc_type is not None:
            # When an exception is thrown stop accepting new jobs
            # and abort pending jobs without waiting.
            self._pool.terminate()
            return False

        super(MultiprocessingEvaluator, self).__exit__(exc_type, exc_value,
                                                       traceback)

    def finalize(self):
        # Stop accepting new jobs and wait for pending jobs to finish.
        self._pool.close()
        self._pool.join()

        if self.root_dir:
            shutil.rmtree(self.root_dir)

    def evaluate_experiments(self, scenarios, policies, callback, zip_over=None):
        ex_gen = experiment_generator(scenarios, self._msis, policies, zip_over)
        add_tasks(self.n_processes, self._pool, ex_gen, callback)


class IpyparallelEvaluator(BaseEvaluator):
    '''evaluator for using an ipypparallel pool'''

    def __init__(self, msis, client, **kwargs):
        super(IpyparallelEvaluator, self).__init__(msis, **kwargs)
        self.client = client

    def initialize(self):
        import ipyparallel

        _logger.debug("starting ipyparallel pool")

        try:
            TIMEOUT_MAX = threading.TIMEOUT_MAX
        except AttributeError:
            TIMEOUT_MAX = 1e10  # noqa
        ipyparallel.client.asyncresult._FOREVER = TIMEOUT_MAX
        # update loggers on all engines
        self.client[:].apply_sync(set_engine_logger)

        _logger.debug("initializing engines")
        initialize_engines(self.client, self._msis, os.getcwd())

        self.logwatcher, self.logwatcher_thread = start_logwatcher()

        _logger.debug("successfully started ipyparallel pool")
        _logger.info("performing experiments using ipyparallel")

        return self

    def finalize(self):
        self.logwatcher.stop()
        cleanup(self.client)

    def evaluate_experiments(self, scenarios, policies, callback, zip_over=None):
        ex_gen = experiment_generator(scenarios, self._msis, policies, zip_over)

        lb_view = self.client.load_balanced_view()
        results = lb_view.map(_run_experiment,
                              ex_gen, ordered=False, block=False)

        for entry in results:
            callback(*entry)


def perform_experiments(models, scenarios=0, policies=0, evaluator=None,
                        reporting_interval=None, reporting_frequency=10,
                        uncertainty_union=False, lever_union=False,
                        outcome_union=False,
                        uncertainty_sampling=Samplers.LHS,
                        levers_sampling=Samplers.LHS, callback=None,
                        return_callback=False,
                        zip_over=None, log_level=20):
    '''sample uncertainties and levers, and perform the resulting experiments
    on each of the models

    Parameters
    ----------
    models : one or more AbstractModel instances
    scenarios : int or collection of Scenario instances, optional
    policies :  int or collection of Policy instances, optional
    evaluator : Evaluator instance, optional
    reporting interval : int, optional
    reporting_frequency: int, optional
    uncertainty_union : boolean, optional
    lever_union : boolean, optional
    uncertainty_sampling : {LHS, MC, FF, PFF, SOBOL, MORRIS, FAST}, optional
    lever_sampling : {LHS, MC, FF, PFF, SOBOL, MORRIS, FAST}, optional TODO:: update doc
    callback  : Callback instance, optional
    return_callback : boolean, optional
    zip_over : Collection[str], optional
        A collection that contains exactly two or three members of the set
        {'scenarios', 'policies', 'models'}.  If it is given, the length
        of all relevant arguments that are indicated in this set must be the
        same, and the experiment generator will create experiments based on
        a `zip` through the values in these collections, instead of creating
        experiments across all possible combinations of the values.

    Returns
    -------
    tuple
        the experiments as a dataframe, and a dict
        with the name of an outcome as key, and the associated values
        as numpy array. Experiments and outcomes are aligned on index.


    '''
    if not scenarios and not policies:
        raise EMAError(('no experiments possible since both '
                        'scenarios and policies are 0'))

    if not scenarios:
        scenarios = [Scenario("None", **{})]
        uncertainties = []
        n_scenarios = 1
    elif(isinstance(scenarios, numbers.Integral)):
        sampler = uncertainty_sampling
        if not isinstance(sampler, AbstractSampler):
            sampler = sampler.value
        scenarios = sample_uncertainties(models, scenarios, sampler=sampler,
                                         union=uncertainty_union)
        uncertainties = scenarios.parameters
        n_scenarios = scenarios.n
    else:
        try:
            uncertainties = scenarios.parameters
            n_scenarios = scenarios.n
        except AttributeError:
            uncertainties = determine_objects(models, "uncertainties",
                                              union=True)
            if isinstance(scenarios, Scenario):
                scenarios = [scenarios]

            uncertainties = [u for u in uncertainties if u.name in
                             scenarios[0]]
            n_scenarios = len(scenarios)

    if not policies:
        policies = [Policy("None", **{})]
        levers = []
        n_policies = 1
    elif(isinstance(policies, numbers.Integral)):
        sampler = levers_sampling
        
        if not isinstance(sampler, AbstractSampler):
            sampler = sampler.value
        
        policies = sample_levers(models, policies, union=lever_union,
                                 sampler=sampler)
        levers = policies.parameters
        n_policies = policies.n
    else:
        try:
            levers = policies.parameters
            n_policies = policies.n
        except AttributeError:
            levers = determine_objects(models, "levers", union=True)
            if isinstance(policies, Policy):
                policies = [policies]

            levers = [l for l in levers if l.name in policies[0]]
            n_policies = len(policies)
    try:
        n_models = len(models)
    except TypeError:
        n_models = 1

    outcomes = determine_objects(models, 'outcomes', union=outcome_union)

    if zip_over:
        zip_over = set(zip_over)
        if zip_over == {'policies', 'scenarios'}:
            nr_of_exp = n_models * max(n_policies, n_scenarios)
            _logger.log(log_level,('performing {} scenarios/policies * {} model(s) = '
                          '{} experiments').format(max(n_policies, n_scenarios),
                                                   n_models, nr_of_exp))

        elif zip_over == {'policies', 'models'}:
            nr_of_exp = max(n_models, n_policies) * n_scenarios
            _logger.log(log_level,('performing {} scenarios * {} policies/models = '
                          '{} experiments').format(n_scenarios,
                                                   max(n_models, n_policies), nr_of_exp))

        elif zip_over == {'scenarios', 'models'}:
            nr_of_exp = max(n_models, n_scenarios) * n_policies
            _logger.log(log_level,('performing {} policies * {} scenarios/models = '
                          '{} experiments').format(n_policies,
                                                   max(n_models, n_scenarios), nr_of_exp))

        elif zip_over == {'scenarios', 'models', 'policies'}:
            nr_of_exp = max(n_models, n_policies, n_scenarios)
            _logger.log(log_level,('performing {} scenarios/policies/models = '
                          '{} experiments').format(nr_of_exp, nr_of_exp))

    else:
        nr_of_exp = n_models * n_scenarios * n_policies
        _logger.log(log_level,('performing {} scenarios * {} policies * {} model(s) = '
                      '{} experiments').format(n_scenarios, n_policies,
                                               n_models, nr_of_exp))

    if not callback:
        callback = DefaultCallback(
            uncertainties,
            levers,
            outcomes,
            nr_of_exp,
            reporting_interval=reporting_interval,
            reporting_frequency=reporting_frequency)
    else:
        callback = callback(uncertainties, levers, outcomes, nr_of_exp,
                            reporting_interval=reporting_interval,
                            reporting_frequency=reporting_frequency)

    if not evaluator:
        evaluator = SequentialEvaluator(models)

    evaluator.evaluate_experiments(scenarios, policies, callback, zip_over=zip_over)

    if callback.i == 0 and getattr(evaluator, 'asynchronous', False):
        _logger.log(log_level,"experiments in asynchronous evaluator")
        return
    elif callback.i != nr_of_exp:
        raise EMAError(('some fatal error has occurred while '
                        'running the experiments, not all runs have '
                        'completed. expected {}, got {}').format(nr_of_exp,
                                                                 callback.i))
    else:
        _logger.log(log_level,"experiments finished")

    if return_callback:
        return callback

    results = callback.get_results()
    return results


def optimize(models, algorithm=EpsNSGAII, nfe=10000,
             searchover='levers', evaluator=None, reference=None,
             convergence=None, constraints=None,
             convergence_freq=1000, logging_freq=5,
             **kwargs):
    '''optimize the model

    Parameters
    ----------
    models : 1 or more Model instances
    algorithm : a valid Platypus optimization algorithm
    nfe : int
    searchover : {'uncertainties', 'levers'}
    kwargs : additional arguments to pass on to algorithm
    convergence : function or collection of functions, optional
    constraints : list, optional
    convergence_freq :  int
                        nfe between convergence check
    logging_freq : int
                   number of generations between logging of progress
    kwargs : any additional arguments will be passed on to algorithm

    Returns
    -------
    pandas DataFrame

    Raises
    ------
    EMAError if searchover is not one of 'uncertainties' or 'levers'
    NotImplementedError if len(models) > 1

    '''
    if searchover not in ('levers', 'uncertainties'):
        raise EMAError(("searchover should be one of 'levers' or"
                        "'uncertainties' not {}".format(searchover)))

    try:
        if len(models) == 1:
            models = models[0]
        else:
            raise NotImplementedError(("optimization over multiple"
                                       "models yet supported"))
    except TypeError:
        pass

    problem = to_problem(models, searchover, constraints=constraints,
                         reference=reference)

    # solve the optimization problem
    if not evaluator:
        evaluator = SequentialEvaluator(models)

    return _optimize(problem, evaluator, algorithm, convergence, nfe,
                     convergence_freq, logging_freq, **kwargs)


def robust_optimize(model, robustness_functions, scenarios,
                    evaluator=None, algorithm=EpsNSGAII, nfe=10000,
                    convergence=None, constraints=None,
                    convergence_freq=1000, logging_freq=5, **kwargs):
    '''perform robust optimization

    Parameters
    ----------
    model : model instance
    robustness_functions : collection of ScalarOutcomes
    scenarios : int, or collection
    evaluator : Evaluator instance
    algorithm : platypus Algorithm instance
    nfe : int
    constraints : list
    convergence_freq :  int
                        nfe between convergence check
    logging_freq : int
                   number of generations between logging of progress
    kwargs : any additional arguments will be passed on to algorithm

    Raises
    ------
    AssertionError if robustness_function is not a ScalarOutcome,
    if robustness_funcion.kind is INFO, or
    if robustness_function.function is None

    robustness functions are scalar outcomes, kind should be MINIMIZE or
    MAXIMIZE, function is the robustness function you want to use.

    '''
    for rf in robustness_functions:
        assert(isinstance(rf, ScalarOutcome))
        # assert(rf.kind != AbstractOutcome.INFO)
        assert(rf.function is not None)

    problem = to_robust_problem(model, scenarios, constraints=constraints,
                                robustness_functions=robustness_functions)

    # solve the optimization problem
    if not evaluator:
        evaluator = SequentialEvaluator(model)

    result = _optimize(problem, evaluator, algorithm, convergence,
                     int(nfe), convergence_freq, logging_freq, **kwargs)

    if isinstance(result, tuple) and len(result)==2:
        result, result_convergence = result
    else:
        result_convergence = None


    # Platypus does not process or save output measures that are just for info,
    # so they must be re-created.
    any_info_items = False
    for rf in robustness_functions:
        if rf.kind == ScalarOutcome.INFO:
            any_info_items = True
            break

    if any_info_items:
        result = robust_evaluate(model, robustness_functions, scenarios, policies=result,
                        evaluator=evaluator, )

    if result_convergence is None:
        return result
    else:
        return result, result_convergence



def designed_levers(models, df, union=True,
                  name=representation):
    '''generate policies by reading levers from a dataframe

    Parameters
    ----------
    models : a collection of AbstractModel instances
    df : pandas.DataFrame
         Each row represents a policy in this design. Each lever
         given in `models` should have a column in this dataframe.
    union : bool, optional
            in case of multiple models, sample over the union of
            levers, or over the intersection of the levers
    name : callable, optional
           a callable to generate a name given the sampled values
          for each lever

    Returns
    -------
    generator yielding Policy instances

    '''
    levers = determine_parameters(models, 'levers', union=union)

    parameters = sorted(levers, key=operator.attrgetter('name'))

    designs = list(df[[p.name for p in parameters]].itertuples(index=False, name=None))

    designs = DefaultDesigns(designs, parameters, len(df))
    partial_policy = functools.partial(Policy, name=name)
    designs.kind = partial_policy

    return designs


def robust_evaluate(model, robustness_functions, scenarios, policies,
                    evaluator=None):
    '''perform one-time evaluation of a model with robustness functions

    Parameters
    ----------
    model : model instance
    robustness_functions : collection of ScalarOutcomes
    scenarios : int, or collection
    policies : int, or collection
    evaluator : Evaluator instance
    constraints : list


    '''
    import pandas

    for rf in robustness_functions:
        assert(isinstance(rf, ScalarOutcome))
        # assert(rf.kind != AbstractOutcome.INFO)
        assert(rf.function is not None)

    if (isinstance(policies, numbers.Integral)):
        policies = sample_levers(model, policies)

    if isinstance(policies, pandas.DataFrame):
        policies_df = policies
        policies_it = designed_levers(model, policies)
    else:
        policies_it = policies
        policies_df = pandas.DataFrame(policies)


    # solve the optimization problem
    if not evaluator:
        evaluator = SequentialEvaluator(model)

    from collections import OrderedDict
    robust_outcomes = OrderedDict()

    with evaluator as e:

        for policy_id,policy in zip(policies_df.index, policies_it):

            experiments, outcomes = e.perform_experiments(
                scenarios=scenarios,
                policies=[policy],
                reporting_interval=1e6,
            )

            job_outcomes_dict = {}
            job_outcomes = []
            for rf in robustness_functions:
                data = [outcomes[var_name] for var_name in
                        rf.variable_name]
                score = rf.function(*data)
                job_outcomes_dict[rf.name] = score
                job_outcomes.append(score)

            robust_outcomes[policy_id] = job_outcomes

    robust_outcomes = pandas.DataFrame.from_dict(
        robust_outcomes,
        orient='index',
        columns=[rf.name for rf in robustness_functions],
    )

    policy_names = [i for i in policies_df.columns if i not in robust_outcomes.columns]

    return pandas.concat([policies_df[policy_names], robust_outcomes], axis=1)

