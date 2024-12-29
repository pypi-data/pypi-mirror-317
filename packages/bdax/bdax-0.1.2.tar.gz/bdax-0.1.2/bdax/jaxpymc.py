import os

import jax
import jax.numpy as jnp
import flax.linen as nn
import arviz as az
import numpy as np
import pytensor
import pytensor.tensor as pt
from pytensor.graph import Apply, Op
import pymc as pm
import pymc.sampling.jax
from abc import ABC, abstractmethod
from typing import Callable, Any, Type, Optional
from jaxtyping import Array, Float
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class VJPCustomOp(Op):

    def __init__(self, custom_op_jax: Callable, output_size: int) -> None:
        self.custom_op_jax = custom_op_jax
        self.output_size = output_size
        self._jit_vjp()

    def _jit_vjp(self) -> None:

        def vjp_custom_op_jax(x, gz):
            _, vjp_fn = jax.vjp(self.custom_op_jax, x)
            return vjp_fn(gz)[0]

        self.jitted_vjp_custom_op_jax = jax.jit(vjp_custom_op_jax)

    def make_node(self, x: pt.TensorVariable, gz: pt.TensorVariable):
        inputs = [pt.as_tensor_variable(x), pt.as_tensor_variable(gz)]
        output_type = pt.TensorType(dtype=x.dtype, broadcastable=(True, False), shape=(1, self.output_size))
        outputs = [output_type(name="custom_op_output")]
        return Apply(self, inputs, outputs)

    def perform(self, node: Any, inputs: tuple, outputs: tuple):
        (x, gz) = inputs
        if x.ndim == 1: x = x[None, :]
        result = self.jitted_vjp_custom_op_jax(x, gz)
        outputs[0][0] = np.asarray(result, dtype="float64")


class CustomOp(Op):

    def __init__(self, custom_op_jax: Callable, output_size: int, vjp_custom_op: VJPCustomOp) -> None:
        self.custom_op_jax = custom_op_jax
        self.output_size = output_size
        self.jitted_custom_op_jax = jax.jit(custom_op_jax)
        self.vjp_custom_op = vjp_custom_op

    def make_node(self, x: pt.TensorVariable):
        inputs = [pt.as_tensor_variable(x)]
        output_type = pt.TensorType(dtype=x.dtype, broadcastable=(True, False), shape=(1, self.output_size))
        outputs = [output_type(name="custom_op_output")]
        return Apply(self, inputs, outputs)

    def perform(self, node: Apply, inputs: list, outputs: list):
        (x,) = inputs
        if x.ndim == 1: x = x[None, :]
        result = self.jitted_custom_op_jax(x)
        outputs[0][0] = np.asarray(result, dtype="float64")

    def grad(self, inputs: list, output_gradients: list):
        (x,) = inputs
        (gz,) = output_gradients
        return [self.vjp_custom_op(x, gz)]


class Sampler(ABC):

    def __init__(self, nn_model: nn.Module, params: dict, data: tuple) -> None:
        self.nn_model = nn_model
        self.params = params
        self.data = data
        self.output_size = self.nn_model.output_dim
        self._set_model_fn()
        self._set_custom_op()
        self.inference_model = self.set_inference_model()
        self._set_model_vars()

    def _set_model_fn(self) -> None:
        self.nn_model_fn = lambda x: self.nn_model.apply(self.params, x)

    def _set_custom_op(self) -> None:
        vjp_custom_op = VJPCustomOp(self.nn_model_fn, self.output_size)
        self.custom_op = CustomOp(self.nn_model_fn, self.output_size, vjp_custom_op)

    @abstractmethod
    def set_inference_model(self) -> pm.Model:
        pass

    def _set_model_vars(self) -> None:
        self.var_names = list(self.inference_model.named_vars.keys())
        self.basic_rvs = [node.name for node in self.inference_model.basic_RVs]
        self.free_rvs = [node.name for node in self.inference_model.free_RVs]
        self.observed_rvs = [node.name for node in self.inference_model.observed_RVs]

    def sample(self, n_chains: int = 4, n_samples: int = 1_000, n_warmup: int = 1_000,
               target_accept: Optional[float] = None, path: Optional[os.PathLike] = None) -> None:

        if target_accept is None:
            idata_posterior = pm.sample(
                model=self.inference_model,
                chains=n_chains,
                draws=n_samples,
                tune=n_warmup,
                idata_kwargs={"log_likelihood": True},
                progressbar=True
            )
        else:
            idata_posterior = pm.sample(
                model=self.inference_model,
                chains=n_chains,
                draws=n_samples,
                tune=n_warmup,
                target_accept=target_accept,
                idata_kwargs={"log_likelihood": True},
                progressbar=True
            )

        idata_prior = pm.sample_prior_predictive(model=self.inference_model, draws=1_000)
        idata_prior_pred = self.predict(idata_prior, type="prior")
        idata_posterior_pred = self.predict(idata_posterior, type="posterior")
        idata_pp = pm.sample_posterior_predictive(idata_posterior, self.inference_model)

        idata_posterior.add_groups({
            "prior": idata_prior.prior,
            "prior_prediction": idata_prior_pred.prediction,
            "prior_predictive": idata_prior.prior_predictive,
            "posterior_prediction": idata_posterior_pred.prediction,
            "posterior_predictive": idata_pp.posterior_predictive,
        })

        self.idata = idata_posterior
        self.summary = az.summary(self.idata, var_names=self.free_rvs)

        if path is not None:
            self.summary.to_csv("/".join(path.split("/")[:-1]+["summary.csv"]))
            self.save_idata(self.idata, path)

    def save_idata(self, idata: az.InferenceData, path: os.PathLike) -> None:
        az.to_netcdf(idata, path)

    def load_idata(self, path: os.PathLike) -> None:
        self.idata = az.from_netcdf(path)
        self.summary = az.summary(self.idata, var_names=self.free_rvs)

    @abstractmethod
    def predict(self, idata: az.InferenceData, type: str = "posterior") -> az.InferenceData:
        pass

    def plot_trace(self, path: os.PathLike, var_names: Optional[list] = None) -> None:

        if var_names is None:
            var_names = self.free_rvs

        figs = []
        for var_name in var_names:
            try:
                axes = az.plot_trace(self.idata, var_names=[var_name])
                fig = axes.ravel()[0].figure
                figs.append(fig)
                plt.close()
            except:
                pass

        pp = PdfPages(path)
        [pp.savefig(fig) for fig in figs]
        pp.close()

    def plot_posterior(self, path: os.PathLike, var_names: Optional[list] = None, ref_vals: Optional[dict] = None,
                       plot_prior: bool = True) -> None:

        if var_names is None:
            var_names = self.free_rvs

        figs = []
        for var_name in var_names:

            posterior_trace = self.idata.posterior[var_name].values
            n_dims = posterior_trace.shape[-1] if len(posterior_trace.shape) > 3 else 1
            posterior_trace = posterior_trace.reshape((-1,)+posterior_trace.shape[2:]).squeeze()
            if n_dims == 1: posterior_trace = np.expand_dims(posterior_trace, axis=-1)

            prior_trace = self.idata.prior[var_name].values
            prior_trace = prior_trace.reshape((-1,)+prior_trace.shape[2:]).squeeze()
            if n_dims == 1: prior_trace = np.expand_dims(prior_trace, axis=-1)

            plot_ref_val = False
            if ref_vals is not None and var_name in list(ref_vals.keys()):
                plot_ref_val = True

            for i in range(n_dims):

                fig = plt.figure(figsize=(6, 4))
                if plot_prior:
                    plt.hist(prior_trace[:, i], color="b", bins=100, density=True, alpha=0.6, label="Prior")
                label = "Posterior" if plot_prior else None
                plt.hist(posterior_trace[:, i], color="r", bins=100, density=True, alpha=0.6, label=label)
                if plot_ref_val:
                    plt.axvline(ref_vals[var_name][i], c="k", linewidth=2, label="Reference value")
                if n_dims == 1:
                    plt.xlabel(var_name, fontsize=12)
                else:
                    plt.xlabel(var_name+" "+str(i+1), fontsize=12)
                plt.ylabel("Density", fontsize=12)
                plt.legend(fontsize=10)
                figs.append(fig)
                plt.close()

        pp = PdfPages(path)
        [pp.savefig(fig) for fig in figs]
        pp.close()

    def plot_posteriorpredictive(self, path: os.PathLike) -> None:

        figs = []
        for observed_rv in self.observed_rvs:
            axes = az.plot_posterior(self.idata, var_names=[observed_rv], group="posterior_predictive")
            if isinstance(axes, np.ndarray):
                fig = axes.ravel()[0].figure
            else:
                fig = axes.figure
            figs.append(fig)
            plt.close()

        pp = PdfPages(path)
        [pp.savefig(fig) for fig in figs]
        pp.close()

    @abstractmethod
    def plot_model(self, path: os.PathLike) -> None:
        pass


if __name__ == "__main__":

    pass
