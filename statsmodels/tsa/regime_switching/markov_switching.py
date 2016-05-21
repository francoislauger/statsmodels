"""
Markov switching models

Author: Chad Fulton
License: BSD
"""

from __future__ import division, absolute_import, print_function

import warnings
import numpy as np
import pandas as pd
from collections import OrderedDict

import statsmodels.tsa.base.tsa_model as tsbase
from statsmodels.tools.data import _is_using_pandas
from statsmodels.tools.tools import Bunch
from statsmodels.tools.numdiff import approx_fprime_cs, approx_hess_cs
from statsmodels.tools.decorators import cache_readonly, resettable_cache
from statsmodels.tools.eval_measures import aic, bic, hqic
from statsmodels.tools.tools import pinv_extended
import statsmodels.base.wrapper as wrap


def _prepare_exog(exog):
    k_exog = 0
    if exog is not None:
        exog_is_using_pandas = _is_using_pandas(exog, None)
        if not exog_is_using_pandas:
            exog = np.asarray(exog)

        # Make sure we have 2-dimensional array
        if exog.ndim == 1:
            if not exog_is_using_pandas:
                exog = exog[:, None]
            else:
                exog = pd.DataFrame(exog)

        k_exog = exog.shape[1]
    return k_exog, exog


def py_hamilton_filter(initial_probabilities, transition,
                       conditional_likelihoods):
    # Dimensions
    k_regimes = len(initial_probabilities)
    nobs = conditional_likelihoods.shape[-1]
    dtype = conditional_likelihoods.dtype

    # Storage
    filtered_marginal_probabilities = (
        np.zeros((k_regimes, nobs + 1), dtype=dtype))
    filtered_marginal_probabilities[:, 0] = initial_probabilities
    predicted_joint_probabilities = np.zeros(
        (k_regimes, k_regimes, nobs), dtype=dtype)
    joint_likelihoods = np.zeros((nobs,), dtype)
    filtered_joint_probabilities = np.zeros(
        (k_regimes, k_regimes, nobs), dtype=dtype)

    # Hamilton filter iterations
    transition_t = 0
    for t in range(nobs):
        if transition.shape[-1] > 1:
            transition_t = t
        # k_regimes x k_regimes
        #             k_regimes
        predicted_joint_probabilities[:, :, t] = (
            transition[:, :, transition_t] *
            filtered_marginal_probabilities[:, t])

        tmp = (conditional_likelihoods[:, :, t] *
               predicted_joint_probabilities[:, :, t])
        joint_likelihoods[t] = np.sum(tmp)

        filtered_joint_probabilities[:, :, t] = tmp / joint_likelihoods[t]

        filtered_marginal_probabilities[:, t+1] = np.sum(
            filtered_joint_probabilities[:, :, t], axis=1)

    return (filtered_marginal_probabilities, predicted_joint_probabilities,
            joint_likelihoods, filtered_joint_probabilities)


def py_kim_smoother(transition, filtered_marginal_probabilities,
                    predicted_joint_probabilities,
                    filtered_joint_probabilities):
    # Dimensions
    k_regimes = filtered_joint_probabilities.shape[0]
    nobs = filtered_joint_probabilities.shape[2]
    dtype = filtered_joint_probabilities.dtype

    # Storage
    smoothed_joint_probabilities = np.zeros(
        (k_regimes, k_regimes, nobs), dtype=dtype)
    smoothed_marginal_probabilities = np.zeros((k_regimes, nobs), dtype=dtype)

    # t=T
    smoothed_joint_probabilities[:, :, -1] = (
        filtered_joint_probabilities[:, :, -1])
    smoothed_marginal_probabilities[:, -1] = (
        filtered_marginal_probabilities[:, -1])

    # Kim smoother iterations
    transition_t = 0
    for t in range(nobs-2, -1, -1):
        if transition.shape[-1] > 1:
            transition_t = t+1

        predicted_marginal_probability = np.sum(
            predicted_joint_probabilities[:, :, t+1:t+2], axis=1)

        smoothed_joint_probabilities[:, :, t] = (
            smoothed_marginal_probabilities[:, t+1:t+2] *
            filtered_marginal_probabilities[:, t+1:t+2].T *
            transition[:, :, transition_t] /
            predicted_marginal_probability)

        smoothed_marginal_probabilities[:, t] = np.sum(
            smoothed_joint_probabilities[:, :, t], axis=0)

    return smoothed_joint_probabilities, smoothed_marginal_probabilities


class MarkovSwitchingParams(object):
    def __init__(self, k_regimes):
        self.k_regimes = k_regimes

        self.k_params = 0
        self.k_parameters = OrderedDict()
        self.switching = OrderedDict()
        self.slices_purpose = OrderedDict()
        self.relative_index_regime_purpose = [OrderedDict() for i in range(self.k_regimes)]
        self.index_regime_purpose = [OrderedDict() for i in range(self.k_regimes)]
        self.index_regime = [[] for i in range(self.k_regimes)]

    def __getitem__(self, key):
        _type = type(key)

        # Get a slice for a block of parameters by purpose
        if _type is str:
            return self.slices_purpose[key]
        # Get a slice for a block of parameters by regime
        elif _type is int:
            return self.index_regime[key]
        elif _type is tuple:
            if not len(key) == 2:
                raise IndexError('Invalid index')
            if type(key[1]) == str and type(key[0]) == int:
                return self.index_regime_purpose[key[0]][key[1]]
            elif type(key[0]) == str and type(key[1]) == int:
                return self.index_regime_purpose[key[1]][key[0]]
            else:
                raise IndexError('Invalid index')
        else:
            raise IndexError('Invalid index')

    def __setitem__(self, key, value):
        _type = type(key)

        if _type is str:
            value = np.array(value, dtype=bool, ndmin=1)
            k_params = self.k_params
            self.k_parameters[key] = (
                value.size + np.sum(value) * (self.k_regimes - 1))
            self.k_params += self.k_parameters[key]
            self.switching[key] = value
            self.slices_purpose[key] = np.s_[k_params:self.k_params]

            for j in range(self.k_regimes):
                self.relative_index_regime_purpose[j][key] = []
                self.index_regime_purpose[j][key] = []

            offset = 0
            for i in range(value.size):
                switching = value[i]
                for j in range(self.k_regimes):
                    # Non-switching parameters
                    if not switching:
                        self.relative_index_regime_purpose[j][key].append(offset)
                    # Switching parameters
                    else:
                        self.relative_index_regime_purpose[j][key].append(offset + j)
                offset += 1 if not switching else self.k_regimes

            for j in range(self.k_regimes):
                offset = 0
                indices = []
                for k, v in self.relative_index_regime_purpose[j].items():
                    v = (np.r_[v] + offset).tolist()
                    self.index_regime_purpose[j][k] = v
                    indices.append(v)
                    offset += self.k_parameters[k]
                self.index_regime[j] = np.concatenate(indices)
        else:
            raise IndexError('Invalid index')


class MarkovSwitching(tsbase.TimeSeriesModel):
    """
    First-order k-regime Markov switching model

    Parameters
    ----------
    endog : array_like
        The endogenous variable.
    k_regimes : integer
        The number of regimes.
    exog_tvtp : array_like, optional
        Array of exogenous or lagged variables to use in calculating
        time-varying transition probabilities (TVTP). TVTP is only used if this
        variable is provided. If an intercept is desired, a column of ones must
        be explicitly included in this array.

    References
    ----------
    Kim, Chang-Jin, and Charles R. Nelson. 1999.
    "State-Space Models with Regime Switching:
    Classical and Gibbs-Sampling Approaches with Applications".
    MIT Press Books. The MIT Press.

    """

    def __init__(self, endog, k_regimes, exog_tvtp=None, exog=None, dates=None,
                 freq=None, missing='none'):

        # Properties
        self.k_regimes = k_regimes
        self.tvtp = exog_tvtp is not None

        # Exogenous data
        # TODO add checks for exog_tvtp consistent shape and indices
        self.k_tvtp, self.exog_tvtp = _prepare_exog(exog_tvtp)

        # Initialize the base model
        super(MarkovSwitching, self).__init__(endog, exog, dates=dates,
                                              freq=freq, missing=missing)

        # Dimensions
        self.nobs = self.endog.shape[0]

        # Sanity checks
        if self.endog.ndim > 1 and self.endog.shape[1] > 1:
            raise ValueError('Must have univariate endogenous data.')
        if self.k_regimes < 2:
            raise ValueError('Markov switching models must have at least two'
                             ' regimes.')
        if not(self.exog_tvtp is None or self.exog_tvtp.shape[0] == self.nobs):
            raise ValueError('Time-varying transition probabilities exogenous'
                             ' array must have the same number of observations'
                             ' as the endogenous array.')

        # Parameters
        self.parameters = MarkovSwitchingParams(self.k_regimes)
        k_transition = self.k_regimes - 1
        if self.tvtp:
            k_transition *= self.k_tvtp
        self.parameters['transition'] = [1] * k_transition

        # Internal model properties: default is steady-state initialization
        self._initialization = 'steady-state'
        self._initial_probabilities = None

    @property
    def k_params(self):
        return self.parameters.k_params

    def initialize_steady_state(self):
        """
        Set initialization of regime probabilities to be steady-state values

        Notes
        -----
        Only valid if there are not time-varying transition probabilities.

        """
        if self.tvtp:
            raise ValueError('Cannot use steady-state initialization when'
                             ' the transition matrix is time-varying.')

        self._initialization = 'steady-state'
        self._initial_probabilities = None

    def initialize_known(self, probabilities, tol=1e-8):
        """
        Set initialization of regime probabilities to use known values
        """
        self._initialization = 'known'
        probabilities = np.array(probabilities, ndmin=1)
        if not probabilities.shape == (self.k_regimes,):
            raise ValueError('Initial probabilities must be a vector of shape'
                             ' (k_regimes,).')
        if not np.abs(np.sum(probabilities) - 1) < tol:
            raise ValueError('Initial probabilities vector must sum to one.')
        self._initial_probabilities = probabilities

    def initial_probabilities(self, params, transition=None):
        """
        Retrieve initial probabilities
        """
        params = np.array(params, ndmin=1)
        if self._initialization == 'steady-state':
            if transition is None:
                transition = self.transition_matrix(params)
            if transition.ndim == 3:
                transition = transition[:, :, 0]
            m = self.k_regimes
            A = np.c_[(np.eye(m) - transition).T, np.ones(m)].T
            try:
                probabilities = np.linalg.pinv(A)[:, -1]
            except np.linalg.LinAlgError:
                raise RuntimeError('Steady-state probabilities could not be'
                                   ' constructed.')
        elif self._initialization == 'known':
            probabilities = self._initial_probabilities
        else:
            raise RuntimeError('Invalid initialization method selected.')

        return probabilities

    def _transition_matrix_tvtp(self, params):
        transition_matrix = np.zeros(
            (self.k_regimes, self.k_regimes, self.nobs),
            dtype=np.promote_types(np.float64, params.dtype))

        # Compute the predicted values from the regression
        for i in range(self.k_regimes):
            coeffs = params[self.parameters[i, 'transition']]
            transition_matrix[:-1, i, :] = np.dot(
                self.exog_tvtp,
                np.reshape(coeffs, (self.k_regimes-1, self.k_tvtp)).T).T

        # Perform the logit transformation
        tmp = np.exp(transition_matrix[:-1, :, :])
        transition_matrix[:-1, :, :] = tmp / (1 + np.sum(tmp, axis=0))

        # Compute the last column of the transition matrix
        transition_matrix[-1, :, :] = (
            1 - np.sum(transition_matrix[:-1, :, :], axis=0))

        return transition_matrix

    def transition_matrix(self, params):
        """
        Construct the left-stochastic transition matrix

        Notes
        -----
        This matrix will either be shaped (k_regimes, k_regimes, 1) or if there
        are time-varying transition probabilities, it will be shaped
        (k_regimes, k_regimes, nobs).

        The (i,j)th element of this matrix is the probability of transitioning
        from regime j to regime i; thus the previous regime is represented in a
        column and the next regime is represented by a row.

        It is left-stochastic, meaning that each column sums to one (because
        it is certain that from one regime (j) you will transition to *some
        other regime*).

        """
        params = np.array(params, ndmin=1)
        if not self.tvtp:
            transition_matrix = np.zeros((self.k_regimes, self.k_regimes, 1),
                                         dtype=np.promote_types(np.float64,
                                                                params.dtype))
            transition_matrix[:-1, :, 0] = np.reshape(
                params[self.parameters['transition']],
                (self.k_regimes, self.k_regimes - 1)).T
            transition_matrix[-1, :, 0] = (
                1 - np.sum(transition_matrix[:-1, :, 0], axis=0))
        else:
            transition_matrix = self._transition_matrix_tvtp(params)

        return transition_matrix

    def _conditional_likelihoods(self, params):
        raise NotImplementedError

    def _filter(self, params, transition=None):
        # Get the transition matrix if not provided
        if transition is None:
            transition = self.transition_matrix(params)
        # Get the initial probabilities
        initial_probabilities = self.initial_probabilities(params, transition)

        # Compute the conditional likelihoods
        conditional_likelihoods = self._conditional_likelihoods(params)

        # Apply the filter
        return ((transition, initial_probabilities, conditional_likelihoods) +
                py_hamilton_filter(initial_probabilities, transition,
                                   conditional_likelihoods))

    def filter(self, params, transformed=True, cov_type=None, cov_kwds=None,
               return_raw=False, results_class=None,
               results_wrapper_class=None):
        """
        Apply the Hamilton filter
        """
        params = np.array(params, ndmin=1)

        if not transformed:
            params = self.transform_params(params)

        # Save the parameter names
        self.data.param_names = self.param_names

        # Get the result
        names = ['transition', 'initial_probabilities',
                 'conditional_likelihoods', 'filtered_marginal_probabilities',
                 'predicted_joint_probabilities', 'joint_likelihoods',
                 'filtered_joint_probabilities']
        result = HamiltonFilterResults(
            self, Bunch(**dict(zip(names, self._filter(params)))))

        # Wrap in a results object
        if not return_raw:
            result_kwargs = {}
            if cov_type is not None:
                result_kwargs['cov_type'] = cov_type
            if cov_kwds is not None:
                result_kwargs['cov_kwds'] = cov_kwds

            if results_class is None:
                results_class = MarkovSwitchingResults
            if results_wrapper_class is None:
                results_wrapper_class = MarkovSwitchingResultsWrapper

            result = results_wrapper_class(
                results_class(self, params, result, **result_kwargs)
            )

        return result

    def _smooth(self, params, filtered_marginal_probabilities,
                predicted_joint_probabilities,
                filtered_joint_probabilities, transition=None):
        # Get the transition matrix
        if transition is None:
            transition = self.transition_matrix(params)

        # Apply the smoother
        return py_kim_smoother(transition, filtered_marginal_probabilities,
                               predicted_joint_probabilities,
                               filtered_joint_probabilities)

    def smooth(self, params, transformed=True, cov_type=None, cov_kwds=None,
               return_raw=False, results_class=None,
               results_wrapper_class=None):
        """
        Apply the Kim smoother
        """
        params = np.array(params, ndmin=1)

        if not transformed:
            params = self.transform_params(params)

        # Save the parameter names
        self.data.param_names = self.param_names

        # Hamilton filter
        names = ['transition', 'initial_probabilities',
                 'conditional_likelihoods', 'filtered_marginal_probabilities',
                 'predicted_joint_probabilities', 'joint_likelihoods',
                 'filtered_joint_probabilities']
        result = Bunch(**dict(zip(names, self._filter(params))))

        # Kim smoother
        out = self._smooth(params, result.filtered_marginal_probabilities,
                           result.predicted_joint_probabilities,
                           result.filtered_joint_probabilities)
        result['smoothed_joint_probabilities'] = out[0]
        result['smoothed_marginal_probabilities'] = out[1]
        result = KimSmootherResults(self, result)

        # Wrap in a results object
        if not return_raw:
            result_kwargs = {}
            if cov_type is not None:
                result_kwargs['cov_type'] = cov_type
            if cov_kwds is not None:
                result_kwargs['cov_kwds'] = cov_kwds

            if results_class is None:
                results_class = MarkovSwitchingResults
            if results_wrapper_class is None:
                results_wrapper_class = MarkovSwitchingResultsWrapper

            result = results_wrapper_class(
                results_class(self, params, result, **result_kwargs)
            )

        return result

    def loglikeobs(self, params, transformed=True):
        """
        Compute the loglikelihood
        """
        params = np.array(params, ndmin=1)

        if not transformed:
            params = self.transform_params(params)

        results = self._filter(params)

        return np.log(results[5])

    def loglike(self, params, transformed=True):
        """
        Compute the loglikelihood
        """
        return np.sum(self.loglikeobs(params, transformed))

    def score(self, params, transformed=True):
        """
        Compute the score function at params.
        """
        params = np.array(params, ndmin=1)

        return approx_fprime_cs(params, self.loglike, args=(transformed,))

    def score_obs(self, params, transformed=True):
        """
        Compute the score per observation, evaluated at params
        """
        params = np.array(params, ndmin=1)

        return approx_fprime_cs(params, self.loglikeobs, args=(transformed,))

    def hessian(self, params, transformed=True):
        """
        Hessian matrix of the likelihood function, evaluated at the given
        parameters
        """
        params = np.array(params, ndmin=1)

        return approx_hess_cs(params, self.loglike)

    def fit(self, start_params=None, transformed=True, cov_type='opg',
            cov_kwds=None, method='lbfgs', maxiter=50, full_output=1, disp=5,
            callback=None, return_params=False, em_iter=5, **kwargs):

        if start_params is None:
            start_params = self.start_params
            transformed = True
        else:
            start_params = np.array(start_params, ndmin=1)

        # Get better start params through EM algorithm
        if em_iter:
            start_params = self.fit_em(start_params, transformed=transformed,
                                       maxiter=em_iter, tolerance=0,
                                       return_params=True)
            transformed = True

        if transformed:
            start_params = self.untransform_params(start_params)

        # Maximum likelihood estimation by scoring
        fargs = (False,)
        mlefit = super(MarkovSwitching, self).fit(start_params, method=method,
                                                  fargs=fargs,
                                                  maxiter=maxiter,
                                                  full_output=full_output,
                                                  disp=disp, callback=callback,
                                                  skip_hessian=True, **kwargs)

        # Just return the fitted parameters if requested
        if return_params:
            result = self.transform_params(mlefit.params)
        # Otherwise construct the results class if desired
        else:
            result = self.smooth(mlefit.params, transformed=False,
                                 cov_type=cov_type, cov_kwds=cov_kwds)

            result.mlefit = mlefit
            result.mle_retvals = mlefit.mle_retvals
            result.mle_settings = mlefit.mle_settings

        return result

    def fit_em(self, start_params=None, transformed=True, cov_type='opg',
               cov_kwds=None, maxiter=50, tolerance=1e-6, full_output=True,
               return_params=False, **kwargs):

        if start_params is None:
            start_params = self.start_params
            transformed = True
        else:
            start_params = np.array(start_params, ndmin=1)

        if not transformed:
            start_params = self.transform(start_params)

        # Sanity checks
        if self.tvtp:
            raise NotImplementedError('The EM algorithm is not available with'
                                      ' time-varying transition probabilities')

        # Perform expectation-maximization
        llf = []
        params = [start_params]
        i = 0
        delta = 0
        while i < maxiter and (i < 2 or (delta > tolerance)):
            out = self._em_iteration(params[-1])
            llf.append(out[0].llf)
            params.append(out[1])
            if i > 0:
                delta = 2 * (llf[-1] - llf[-2]) / np.abs((llf[-1] + llf[-2]))
            i += 1

        # Just return the fitted parameters if requested
        if return_params:
            result = params[-1]
        # Otherwise construct the results class if desired
        else:
            result = self.filter(params[-1], transformed=True,
                                 cov_type=cov_type, cov_kwds=cov_kwds)

            # Save the output
            if full_output:
                em_retvals = Bunch(**{'params': np.array(params),
                                      'llf': np.array(llf),
                                      'iter': i})
                em_settings = Bunch(**{'tolerance': tolerance,
                                       'maxiter': maxiter})
            else:
                em_retvals = None
                em_settings = None

            result.mle_retvals = em_retvals
            result.mle_settings = em_settings

        return result

    def _em_iteration(self, params0):
        params1 = np.zeros(params0.shape,
                           dtype=np.promote_types(np.float64, params0.dtype))

        # Smooth at the given parameters
        result = self.smooth(params0, transformed=True, return_raw=True)

        # Transition parameters (recall we're not supporting TVTP here)
        for i in range(self.k_regimes):  # S_{t_1}
            _params1 = params1[self.parameters[i, 'transition']]
            for j in range(self.k_regimes - 1):  # S_t
                _params1[j] = (
                    np.sum(result.smoothed_joint_probabilities[j, i]) /
                    np.sum(result.smoothed_marginal_probabilities[i]))

            # It may be the case that due to rounding error this estimates
            # transition probabilities that sum to greater than one. If so,
            # re-scale the probabilities and warn the user that something
            # is not quite right
            delta = np.sum(_params1) - 1
            if delta > 0:
                warnings.warn('Invalid transition probabilities estimated in'
                              ' EM iteration; probabilities have been'
                              ' re-scaled to continue estimation.')
                _params1 /= 1 + delta + 1e-6
            params1[self.parameters[i, 'transition']] = _params1

        return result, params1

    @property
    def start_params(self):
        params = np.zeros(self.k_params, dtype=np.float64)

        # Transition probabilities
        if self.tvtp:
            params[self.parameters['transition']] = 0.
        else:
            params[self.parameters['transition']] = 1. / self.k_regimes

        return params

    @property
    def param_names(self):
        param_names = np.zeros(self.k_params, dtype=object)

        # Transition probabilities
        if self.tvtp:
            # TODO add support for exog_tvtp_names
            param_names[self.parameters['transition']] = [
                'p[%d][%d].tvtp%d' % (j, i, k)
                for j in range(self.k_regimes)
                for i in range(self.k_regimes-1)
                for k in range(self.k_tvtp)]
        else:
            param_names[self.parameters['transition']] = [
                'p[%d][%d]' % (j, i)
                for j in range(self.k_regimes)
                for i in range(self.k_regimes-1)]

        return param_names.tolist()

    def transform_params(self, unconstrained):
        constrained = np.array(unconstrained, copy=True)
        constrained = constrained.astype(
            np.promote_types(np.float64, constrained.dtype))

        # Nothing to do for transition probabilities if TVTP
        if self.tvtp:
            constrained[self.parameters['transition']] = (
                unconstrained[self.parameters['transition']])
        # Otherwise do logit transformation
        else:
            # Transition probabilities
            offset = 0
            for i in range(self.k_regimes):
                tmp = np.exp(unconstrained[self.parameters[i, 'transition']])
                constrained[self.parameters[i, 'transition']] = (
                    tmp / (1 + np.sum(tmp)))

        # Do not do anything for the rest of the parameters

        return constrained

    def _untransform_logit(self, unconstrained, constrained):
        resid = np.zeros(unconstrained.shape, dtype=unconstrained.dtype)
        exp = np.exp(unconstrained)
        sum_exp = np.sum(exp)
        for i in range(len(unconstrained)):
            resid[i] = (unconstrained[i] -
                        np.log(1 + sum_exp - exp[i]) +
                        np.log(1 / constrained[i] - 1))
        return resid

    def untransform_params(self, constrained):
        unconstrained = np.array(constrained, copy=True)
        unconstrained = unconstrained.astype(
            np.promote_types(np.float64, unconstrained.dtype))

        # Nothing to do for transition probabilities if TVTP
        if self.tvtp:
            unconstrained[self.parameters['transition']] = (
                constrained[self.parameters['transition']])
        # Otherwise reverse logit transformation
        else:
            for i in range(self.k_regimes):
                s = self.parameters[i, 'transition']
                if self.k_regimes == 2:
                    unconstrained[s] = -np.log(1. / constrained[s] - 1)
                else:
                    from scipy.optimize import root
                    out = root(self._untransform_logit,
                               np.zeros(unconstrained[s].shape,
                                        unconstrained.dtype),
                               args=(constrained[s],))
                    if not out['success']:
                        raise ValueError('Could not untransform parameters.')
                    unconstrained[s] = out['x']

        # Do not do anything for the rest of the parameters

        return unconstrained


class HamiltonFilterResults(object):
    def __init__(self, model, result):

        self.model = model

        self.nobs = model.nobs
        self.k_regimes = model.k_regimes

        attributes = ['transition', 'initial_probabilities',
                      'conditional_likelihoods',
                      'predicted_joint_probabilities',
                      'filtered_marginal_probabilities',
                      'filtered_joint_probabilities',
                      'joint_likelihoods']
        for name in attributes:
            setattr(self, name, getattr(result, name))

        # Eliminate the first filtered marginal probability, which is just the
        # initial probabilities
        self.filtered_marginal_probabilities = (
            self.filtered_marginal_probabilities[:, 1:])

        self.llf_obs = np.log(self.joint_likelihoods)
        self.llf = np.sum(self.llf_obs)


class KimSmootherResults(HamiltonFilterResults):
    def __init__(self, model, result):
        super(KimSmootherResults, self).__init__(model, result)

        attributes = ['smoothed_joint_probabilities',
                      'smoothed_marginal_probabilities']

        for name in attributes:
            setattr(self, name, getattr(result, name))


class MarkovSwitchingResults(tsbase.TimeSeriesModelResults):
    def __init__(self, model, params, results, cov_type='opg', cov_kwds=None,
                 **kwargs):
        self.data = model.data

        tsbase.TimeSeriesModelResults.__init__(self, model, params,
                                               normalized_cov_params=None,
                                               scale=1.)

        # Save the filter / smoother output
        self.filter_results = results
        if isinstance(results, KimSmootherResults):
            self.smoother_results = results
        else:
            self.smoother_results = None

        # Dimensions
        self.nobs = model.nobs

        # Setup covariance matrix notes dictionary
        if not hasattr(self, 'cov_kwds'):
            self.cov_kwds = {}
        self.cov_type = cov_type

        # Setup the cache
        self._cache = resettable_cache()

        # Handle covariance matrix calculation
        if cov_kwds is None:
                cov_kwds = {}
        self._cov_approx_complex_step = (
            cov_kwds.pop('approx_complex_step', True))
        self._cov_approx_centered = cov_kwds.pop('approx_centered', False)
        try:
            self._rank = None
            self._get_robustcov_results(cov_type=cov_type, use_self=True,
                                        **cov_kwds)
        except np.linalg.LinAlgError:
            self._rank = 0
            k_params = len(self.params)
            self.cov_params_default = np.zeros((k_params, k_params)) * np.nan
            self.cov_kwds['cov_type'] = (
                'Covariance matrix could not be calculated: singular.'
                ' information matrix.')

        # Copy over arrays
        attributes = ['transition', 'initial_probabilities',
                      'conditional_likelihoods',
                      'predicted_joint_probabilities',
                      'filtered_marginal_probabilities',
                      'filtered_joint_probabilities',
                      'joint_likelihoods']
        for name in attributes:
            setattr(self, name, getattr(self.filter_results, name))

        attributes = ['smoothed_joint_probabilities',
                      'smoothed_marginal_probabilities']
        for name in attributes:
            if self.smoother_results is not None:
                setattr(self, name, getattr(self.smoother_results, name))
            else:
                setattr(self, name, None)

    def _get_robustcov_results(self, cov_type='opg', **kwargs):
        import statsmodels.stats.sandwich_covariance as sw

        use_self = kwargs.pop('use_self', False)
        if use_self:
            res = self
        else:
            raise NotImplementedError
            res = self.__class__(
                self.model, self.params,
                normalized_cov_params=self.normalized_cov_params,
                scale=self.scale)

        # Set the new covariance type
        res.cov_type = cov_type
        res.cov_kwds = {}

        # Calculate the new covariance matrix
        k_params = len(self.params)
        if k_params == 0:
            res.cov_params_default = np.zeros((0, 0))
            res._rank = 0
            res.cov_kwds['description'] = 'No parameters estimated.'
        elif cov_type == 'none':
            res.cov_params_default = np.zeros((k_params, k_params)) * np.nan
            res._rank = np.nan
            res.cov_kwds['description'] = 'Covariance matrix not calculated.'
        elif self.cov_type == 'approx':
            res.cov_params_default = res.cov_params_approx
            res.cov_kwds['description'] = (
                'Covariance matrix calculated using numerical'
                ' differentiation.')
        elif self.cov_type == 'opg':
            res.cov_params_default = res.cov_params_opg
            res.cov_kwds['description'] = (
                'Covariance matrix calculated using the outer product of'
                ' gradients.'
            )
        elif self.cov_type == 'robust':
            res.cov_params_default = res.cov_params_robust
            res.cov_kwds['description'] = (
                'Quasi-maximum likelihood covariance matrix used for'
                ' robustness to some misspecifications; calculated using'
                ' numerical differentiation.')
        else:
            raise NotImplementedError('Invalid covariance matrix type.')

        return res

    @cache_readonly
    def aic(self):
        """
        (float) Akaike Information Criterion
        """
        # return -2*self.llf + 2*self.params.shape[0]
        return aic(self.llf, self.nobs, self.params.shape[0])

    @cache_readonly
    def bic(self):
        """
        (float) Bayes Information Criterion
        """
        # return -2*self.llf + self.params.shape[0]*np.log(self.nobs)
        return bic(self.llf, self.nobs, self.params.shape[0])

    @cache_readonly
    def cov_params_approx(self):
        """
        (array) The variance / covariance matrix. Computed using the numerical
        Hessian approximated by complex step or finite differences methods.
        """
        evaluated_hessian = self.model.hessian(self.params, transformed=True)
        neg_cov, singular_values = pinv_extended(evaluated_hessian)

        if self._rank is None:
            self._rank = np.linalg.matrix_rank(np.diag(singular_values))

        return -neg_cov

    @cache_readonly
    def cov_params_opg(self):
        """
        (array) The variance / covariance matrix. Computed using the outer
        product of gradients method.
        """
        score_obs = self.model.score_obs(self.params, transformed=True)
        cov_params, singular_values = pinv_extended(
            np.inner(score_obs, score_obs))

        if self._rank is None:
            self._rank = np.linalg.matrix_rank(np.diag(singular_values))

        return cov_params

    @cache_readonly
    def cov_params_robust(self):
        """
        (array) The QMLE variance / covariance matrix. Computed using the
        numerical Hessian as the evaluated hessian.
        """
        cov_opg = self.cov_params_opg
        evaluated_hessian = self.model.hessian(self.params, transformed=True)
        cov_params, singular_values = pinv_extended(
            np.dot(np.dot(evaluated_hessian, cov_opg), evaluated_hessian)
        )

        if self._rank is None:
            self._rank = np.linalg.matrix_rank(np.diag(singular_values))

        return cov_params

    @cache_readonly
    def fittedvalues(self):
        """
        (array) The predicted values of the model. An (nobs x k_endog) array.
        """
        # This is a (k_endog x nobs array; don't want to squeeze in case of
        # the corner case where nobs = 1 (mostly a concern in the predict or
        # forecast functions, but here also to maintain consistency)
        raise NotImplementedError

    @cache_readonly
    def hqic(self):
        """
        (float) Hannan-Quinn Information Criterion
        """
        # return -2*self.llf + 2*np.log(np.log(self.nobs))*self.params.shape[0]
        return hqic(self.llf, self.nobs, self.params.shape[0])

    @cache_readonly
    def llf_obs(self):
        """
        (float) The value of the log-likelihood function evaluated at `params`.
        """
        return self.model.loglikeobs(self.params)

    @cache_readonly
    def llf(self):
        """
        (float) The value of the log-likelihood function evaluated at `params`.
        """
        return self.model.loglike(self.params)

    @cache_readonly
    def pvalues(self):
        """
        (array) The p-values associated with the z-statistics of the
        coefficients. Note that the coefficients are assumed to have a Normal
        distribution.
        """
        return norm.sf(np.abs(self.zvalues)) * 2

    @cache_readonly
    def resid(self):
        """
        (array) The model residuals. An (nobs x k_endog) array.
        """
        # This is a (k_endog x nobs array; don't want to squeeze in case of
        # the corner case where nobs = 1 (mostly a concern in the predict or
        # forecast functions, but here also to maintain consistency)
        raise NotImplementedError

    @cache_readonly
    def zvalues(self):
        """
        (array) The z-statistics for the coefficients.
        """
        return self.params / self.bse


class MarkovSwitchingResultsWrapper(wrap.ResultsWrapper):
    _attrs = {
        'zvalues': 'columns',
        'cov_params_approx': 'cov',
        'cov_params_default': 'cov',
        'cov_params_opg': 'cov',
        'cov_params_robust': 'cov',
    }
    _wrap_attrs = wrap.union_dicts(tsbase.TimeSeriesResultsWrapper._wrap_attrs,
                                   _attrs)
    _methods = {
        'forecast': 'dates',
        'simulate': 'ynames',
        'impulse_responses': 'ynames'
    }
    _wrap_methods = wrap.union_dicts(
        tsbase.TimeSeriesResultsWrapper._wrap_methods, _methods)
wrap.populate_wrapper(MarkovSwitchingResultsWrapper, MarkovSwitchingResults)
