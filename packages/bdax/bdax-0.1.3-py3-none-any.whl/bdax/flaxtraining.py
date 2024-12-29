import os
import jax
from jax import lax
import jax.numpy as jnp
from flax.training.train_state import TrainState
import flax.linen as nn
import optax
import pickle
from jax_tqdm import scan_tqdm
from functools import partial
from typing import Callable
from jaxtyping import Array, Float, PRNGKeyArray
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class Trainer:

    def __init__(self, model: nn.Module) -> None:
        self.model = model

    @partial(jax.jit, static_argnums=(0,))
    def _loss(self, state, params, x, y):
        y_hat = state.apply_fn(params, x)
        return self.loss_fn(y_hat, y).mean()

    @partial(jax.jit, static_argnums=(0,))
    def _epoch(self, runner, epoch):
        state, x_train, y_train = runner
        loss, grads = jax.value_and_grad(self._loss, argnums=1)(state, state.params, x_train, y_train)
        state = state.apply_gradients(grads=grads)
        runner = (state, x_train, y_train)
        return runner, loss

    def train(self, x: Float[Array, "batch_size n_input"], y: Float[Array, "batch_size n_output"],
              loss_fn: Callable[
                  [Float[Array, "batch_size n_output"], Float[Array, "batch_size n_output"]],
                  [Float[Array, "batch_size 1"]]
              ], rng: PRNGKeyArray = jax.random.PRNGKey(42), n_epochs: int = 20_000, lr: float = 1e-4) -> None:

        self.loss_fn = loss_fn

        params_init = self.model.init(rng, jnp.take(x, 0, axis=0))

        state = TrainState.create(
            apply_fn=self.model.apply,
            params=params_init,
            tx=optax.adam(lr)
        )

        runner = (state, x, y)
        runner, losses = lax.scan(scan_tqdm(n_epochs)(self._epoch), runner, jnp.arange(n_epochs), n_epochs)
        state, _, _ = runner

        self.state = state
        self.params = state.params
        self.losses = losses

        self.y_hat = self.predict(x)

    @partial(jax.jit, static_argnums=(0,))
    def predict(self, x: Float[Array, "batch_size n_input"]) -> Float[Array, "batch_size n_output"]:
        return self.model.apply(self.params, x).squeeze()

    def save(self, path: os.PathLike) -> None:
        with open(path, 'wb') as f:
            pickle.dump(self.params, f)

    def load(self, path: os.PathLike) -> None:
        with open(path, 'rb') as f:
            self.params = pickle.load(f)


if __name__ == "__main__":

    pass
