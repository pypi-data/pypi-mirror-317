from typing import Callable, Iterable, Protocol

import numpy as np
from scipy.spatial.distance import pdist

from experiment_design.variable import ParameterSpace


class Scorer(Protocol):
    def __call__(self, doe: np.ndarray) -> float:
        """
        A scoring function to evaluate an experiment design quality. Larger values are better,
        i.e. this will be maximized.

        :param doe: Design of experiments consisting of candidate samples.
        :return: score of the DoE.
        """
        ...


class ScorerFactory(Protocol):
    def __call__(
        self,
        space: ParameterSpace,
        sample_size: int,
        old_sample: np.ndarray | None = None,
    ) -> Scorer:
        """Given variables and sample size, create a scoring function"""
        ...


class MaxCorrelationScorerFactory:
    """
    A scorer factory for the maximum absolute correlation error between sampling points.

    :param local: If True, any points in the old_sample will be ignored, that fall outside the finite bounds of the
        provided variables. Has no effect if old_sample is None.
    :param eps: a small positive value to improve the stability of the log operation.

    """

    def __init__(
        self,
        local: bool = True,
        eps: float = 1e-2,
    ) -> None:
        self.local = local

        if eps < 0:
            raise ValueError("eps must be positive")
        self.eps = eps

    def __call__(
        self,
        space: ParameterSpace,
        sample_size: int,
        old_sample: np.ndarray | None = None,
    ) -> Scorer:
        """
        Creates a scorer, that computes the maximum absolute correlation error between the candidate samples
        and the target_correlation.

        :param space: Dimensions of the design space.
        :param sample_size: number of candidate points to be scored.
        :param old_sample: If passed, represents the matrix of points in an older design of experiments with shape
            (old_sample_size, len(variables)). Depending on self.local, some or all of these will be appended to the
            candidate points before computing the correlation error.
        :return: a scorer that returns the negative exp(maximum absolute correlation error + 1). If the error is
            smaller than self.eps, it returns negative exp(maximum absolute correlation error - 1) instead.
        """

        handler = create_old_doe_handler(space, old_sample, local=self.local)

        def _scorer(doe: np.ndarray) -> float:
            error = np.max(
                np.abs(np.corrcoef(handler(doe), rowvar=False) - space.correlation)
            )
            if error > self.eps:
                return -np.exp(error + 1)
            return -np.exp(error - 1)

        return _scorer


class PairwiseDistanceScorerFactory:
    """
    A scorer factory for the minimum pairwise distance between sampling points.

    Note: This currently computes all distances. Hence, it may be inefficient for very large
    sample sizes. This behaviour could be improved using algorithms like KDTrees or KNN but
    they would lead to more dependencies. Therefore, we prefer omitting the implementation for
    now and providing this note instead. If there is interest in handling large sample sizes,
    create an issue or open a pull request.

    :param local: If True, any points in the old_sample will be ignored, that fall outside the finite bounds of the
        provided variables. Has no effect if old_sample is None.
    :return: a scorer that returns the log minimum pairwise distance divided by the log max distance.
    """

    def __init__(self, local: bool = False) -> None:
        self.local = local

    def __call__(
        self,
        space: ParameterSpace,
        sample_size: int,
        old_sample: np.ndarray | None = None,
    ) -> Scorer:
        """
        Create a scorer, that computes the minimum pairwise distance between sampling points.s

        :param space: Dimensions of the design space.
        :param sample_size: number of candidate points to be scored.
        :param old_sample: If passed, represents the matrix of points in an older design of experiments with shape
            (old_sample_size, len(variables)). Depending on self.local, some or all of these will be appended to the
            candidate points before computing the correlation error.
        :return: a scorer that returns the log minimum pairwise distance divided by the log max distance,
        """

        handler = create_old_doe_handler(space, old_sample, local=self.local)
        bin_diagonal_length = calculate_equidistant_bin_diagonal_length(
            space, sample_size
        )

        def _scorer(doe: np.ndarray) -> float:
            min_pairwise_distance = np.min(pdist(handler(doe)))
            return np.exp(min_pairwise_distance / bin_diagonal_length)

        return _scorer


class WeightedSumScorerFactory:
    """
    A factory that creates a weighted sum of multiple scorers

    :param scorer_factories: These are combined by adding the scores their scorers provide.
    :param weights: Weights to use for combining the scorers. If not passed, each scores will not be weighed.
    """

    def __init__(
        self, scorer_factories: list[ScorerFactory], weights: Iterable[float]
    ) -> None:
        self.scorer_factories = scorer_factories
        if weights is None:
            weights = np.ones(len(scorer_factories))
        self.weights = np.array(weights).ravel()
        if self.weights.size != len(self.scorer_factories):
            raise ValueError(
                f"Wrong number of scorer_factories ({len(scorer_factories)}) and weights ({self.weights.size})"
            )

    def __call__(
        self,
        space: ParameterSpace,
        sample_size: int,
        old_sample: np.ndarray | None = None,
    ) -> Scorer:

        scorers = [
            factory(space, sample_size, old_sample=old_sample)
            for factory in self.scorer_factories
        ]

        def _scorer(doe: np.ndarray) -> float:
            return sum(
                [scorer(doe) * weight for scorer, weight in zip(scorers, self.weights)]
            )

        return _scorer


def create_default_scorer_factory(
    distance_score_weight: float = 0.9,
    correlation_score_weight: float = 0.1,
    local_correlation: bool = True,
    local_pairwise_distance: bool = False,
) -> ScorerFactory:
    """
    Create a scorer factory, which is a weighted sum of maximum correlation error and
    minimum pairwise distance scorers

    :param distance_score_weight: Weight of the minimum pairwise distance score.
    :param correlation_score_weight: Weight of the maximum correlation error score.
    :param local_correlation: Controls the local attribute of the MaxCorrelationScorerFactory.
    :param local_pairwise_distance: Controls the local attribute of the PairwiseDistanceScorerFactory
    :return: WeightedSumScorerFactory instance.
    """
    corr_scorer_factory = MaxCorrelationScorerFactory(local=local_correlation)
    dist_scorer_factory = PairwiseDistanceScorerFactory(local=local_pairwise_distance)
    return WeightedSumScorerFactory(
        scorer_factories=[corr_scorer_factory, dist_scorer_factory],
        weights=[correlation_score_weight, distance_score_weight],
    )


def calculate_equidistant_bin_diagonal_length(
    space: ParameterSpace, sample_size: int
) -> float:
    """Calculate the length of the diagonal of equidistant bins the (Euclidean) design space"""
    lower, upper = space.lower_bound, space.upper_bound
    return np.linalg.norm((np.array(upper) - np.array(lower)) / sample_size)


def create_old_doe_handler(
    space: ParameterSpace,
    old_sample: np.ndarray | None = None,
    local: bool = False,
) -> Callable[[np.ndarray], np.ndarray]:
    """
    Return a function to handle any old design of experiments. Specifically,
    append some or all of the points from an old design of experiments (DoE) for
    including them in the scoring.

    :param space: Dimensions of the design space. Only relevant if local is set to True.
    :param old_sample: Matrix of points with shape=(sample_size, len(variables)) in the old DoE. If None, this returns
        a no-op function.
    :param local: If True, only include the points from the old_doe, that fall between the finite local bounds of the
        variables.
    :return: The function with a single argument, new doe, which may append points from the old doe depending on the
        arguments provided.
    """
    if old_sample is None:
        # Nothing to handle
        return lambda x: x

    if not local:
        # Append every point in the old doe
        return lambda x: np.append(old_sample, x, axis=0)

    old_sample = select_local(old_sample, space)
    return lambda x: np.append(old_sample, x, axis=0)


def select_local(samples: np.ndarray, space: ParameterSpace) -> np.ndarray:
    """Select and return samples that fall within the finite bounds of the variables"""
    lower, upper = space.lower_bound[None, :], space.upper_bound[None, :]
    local_mask = np.logical_and((samples >= lower).all(1), (samples <= upper).all(1))
    return samples[local_mask]
