import numpy as np
import jax
from jax import lax
import jax.numpy as jnp
import flax.linen as nn
import optax
import blackjax
import arviz as az
import xarray as xr
from functools import partial
from jax_tqdm import scan_tqdm
from typing import Callable, Optional, Tuple, List
from jaxtyping import Array, Int, Float, Bool, PRNGKeyArray


class Sampler:

    def __init__(self, model_input_names: List[str], logpost_fn: Callable[[dict], [Float[Array, "1"]]],
                 post_processing_fn: Callable[[az.InferenceData], [az.InferenceData]] = lambda x: x) -> None:
        self.logpost_fn = logpost_fn
        self.model_input_names = model_input_names
        self.post_processing_fn = post_processing_fn

    def _init_positions(self, rng: PRNGKeyArray, n_chains: int = 4) -> dict:
        rngs = jax.random.split(rng, n_chains)
        init_param_positions = jax.vmap(lambda rng: jax.random.uniform(key=rng, shape=(n_chains,)))(rngs)
        init_positions = {
            name: jnp.take(init_param_positions, i, axis=0)[:, jnp.newaxis]
            for i, name in enumerate(self.model_input_names)
        }
        return init_positions

    @staticmethod
    def inference(rng: PRNGKeyArray, kernel, initial_states: dict, n_samples: int = 2_000, num_chains: int = 4)\
            -> tuple:

        def one_step(runner: tuple, i_step: int) -> Tuple[tuple, tuple]:
            states, rng = runner
            rng, rng_vmap = jax.random.split(rng)
            rngs = jax.random.split(rng_vmap, num_chains)
            states, infos = jax.vmap(kernel)(rngs, states)
            runner = (states, rng)
            return runner, (states, infos)

        runner = (initial_states, rng)
        _, (states, infos) = lax.scan(scan_tqdm(n_samples)(jax.jit(one_step)), runner, jnp.arange(n_samples))

        return states, infos

    def sample(self, rng:PRNGKeyArray, n_chains: int = 4, n_samples: int =1_000, n_warmup: int = 1_000,
               step_size: float = 1e-3, save_path: Optional[str] = None) -> None:

        n_vars = len(self.model_input_names)
        n_steps = n_samples + n_warmup

        inverse_mass_matrix = jnp.ones(n_vars, dtype=jnp.float32)
        nuts = blackjax.nuts(self.logpost_fn, step_size, inverse_mass_matrix)

        initial_positions = self._init_positions(rng, n_chains)
        initial_states = jax.vmap(nuts.init, in_axes=(0))(initial_positions)
        states, infos = self.inference(rng, nuts.step, initial_states, n_steps, n_chains)

        idata = self.arviz_idata_from_states(states, infos, n_warmup)
        self.idata = self.post_processing_fn(idata)

        self.trace = az.extract(self.idata, group='posterior')

        self.diagnose()
        self.summary(self.rhat, self.divergences)

        if save_path is not None:
            self.export_idata(save_path)

    @staticmethod
    def summary(rhat: xr.Dataset, divergences: np.ndarray["n_chains n_samples", float]) -> None:
        print(rhat)
        print('Divergences:')
        for i, div in enumerate(divergences):
            print('Chain ' + str(i + 1) + ': ' + str(int(div.sum())))

    @staticmethod
    def arviz_idata_from_states(states: dict, info: dict, n_warmup: int = 1_000, posterior: bool = True):

        position = states.position
        if isinstance(position, jax.Array):
            position = dict(samples=position)
        else:
            try:
                position = position._asdict()
            except AttributeError:
                pass

        samples = {}
        for param in position.keys():
            ndims = len(position[param].shape)
            if ndims >= 2:
                samples[param] = jnp.swapaxes(position[param], 0, 1)[:, n_warmup:]
                divergence = jnp.swapaxes(info.is_divergent[n_warmup:], 0, 1)
            if ndims == 1:
                divergence = info.is_divergent
                samples[param] = position[param]

        if posterior:
            idata = az.convert_to_inference_data(samples, group='posterior')
        else:
            idata = az.convert_to_inference_data(samples, group='prior')
        idata_sample_stats = az.convert_to_inference_data({"diverging": divergence}, group="sample_stats")

        idata = az.concat(idata, idata_sample_stats)

        return idata

    def diagnose(self) -> None:
        self.divergences = self.idata.sample_stats.diverging.values
        self.rhat = az.rhat(self.idata).max()

    def export_idata(self, save_path: str) -> None:
        self.idata.to_json(save_path)

