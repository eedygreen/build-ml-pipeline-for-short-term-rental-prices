# Build an ML Pipeline for Short-Term Rental Prices in NYC
This project assists you in building a machine learning pipeline to predict short-term rental prices in NYC. You need to estimate the typical price for a given property based on the price of similar properties. When new data is received in bulk every week. The model needs 
to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

In this project you will built such a pipeline.

## Table of contents

- [Introduction](#build-an-ML-Pipeline-for-Short-Term-Rental-Prices-in-NYC)
- [Preliminary steps](#preliminary-steps)
  * [Fork the Starter Kit](#fork-the-starter-kit)
  * [Create environment](#create-environment)
  * [Get API key for Weights and Biases](#get-api-key-for-weights-and-biases)
  * [Cookie cutter](#cookie-cutter)
  * [The configuration](#the-configuration)
  * [Running the entire pipeline or just a selection of steps](#Running-the-entire-pipeline-or-just-a-selection-of-steps)
  * [Pre-existing components](#pre-existing-components)

- [Project Completion](#project-completion)

## Preliminary steps

### Supported Operating Systems

This project is compatible with the following operating systems:

- **Ubuntu 22.04** (Jammy Jellyfish) - both Ubuntu installation and WSL (Windows Subsystem for Linux)
- **Ubuntu 24.04** - both Ubuntu installation and WSL (Windows Subsystem for Linux)
- **macOS** - compatible with recent macOS versions

Please ensure you are using one of the supported OS versions to avoid compatibility issues.

### Python Requirement

This project requires 
- **Python 3.13**
- **Conda**
- **hydra**
- **mlflow**
- **wandb**
- **cookie cutter** 
Please ensure that you have these installed - and set as the default version - in your environment to avoid any runtime issues.

### Fork the Starter kit
Go to [click me](https://github.com/eedygreen/build-ml-pipeline-for-short-term-rental-prices.git)
and click on `Fork` in the upper right corner. This will create a fork in your Github account, i.e., a copy of the
repository that is under your control. Now clone the repository locally so you can start working on it:

```
git clone https://github.com/[your github username]/build-ml-pipeline-for-short-term-rental-prices.git
```

and go into the repository:

```
cd build-ml-pipeline-for-short-term-rental-prices
```

### Create environment
Make sure to have conda installed and ready, then create a new environment using the ``environment.yml``
file provided in the root of the repository and activate it:

```bash
> conda env create -f environment.yml
> conda activate nyc_airbnb_dev
```

### Get API key for Weights and Biases
Let's make sure we are logged in to Weights & Biases. Get your API key from W&B by going to 
[https://wandb.ai/authorize](https://wandb.ai/authorize) and click on the + icon (copy to clipboard), 
then paste your key into this command:

```bash
> wandb login [your API key]
```

You should see a message similar to:
```
wandb: Appending key for api.wandb.ai to your netrc file: /home/[your username]/.netrc
```

### Cookie cutter
If you wantto add a new step to the pipeline, you can start from scratch by creating the script, the conda environment and the MLproject file, or you can use the cookie cutter template provided to create a stub for your new step.
It is not required that you use this, but it might save you from a bit of 
boilerplate code. Just run the cookiecutter and enter the required information, and a new component 
will be created including the `conda.yml` file, the `MLproject` file as well as the script. You can then modify these
as needed, instead of starting from scratch.
For example:

```bash
> cookiecutter cookie-mlflow-step -o src

step_name [step_name]: promote_pipeline
script_name [run.py]: run.py
job_type [my_step]: promote_pipeline
short_description [My step]: This steps promotes the pipeline
long_description [An example of a step using MLflow and Weights & Biases]: Promotes the pipeline and saves the results in Weights & Biases
parameters [parameter1,parameter2]: parameter1,parameter2,parameter3
```

This will create a step called ``promote_pipeline`` under the directory ``src`` with the following structure:

```bash
> ls src/promote_pipeline/
conda.yml  MLproject  run.py
```

You can now modify the script (``run.py``), the conda environment (``conda.yml``) and the project definition 
(``MLproject``) as you please.

The script ``run.py`` will receive the input parameters ``parameter1``, ``parameter2``,
``parameter3`` and it will be called like:

```bash
> mlflow run src/promote_pipeline -P parameter1=1 -P parameter2=2 -P parameter3="test"
```

To run the project without cloning the repository, you can also use the following command:

```bash
> mlflow run https://github.com/eedygreen/build-ml-pipeline-for-short-term-rental-prices.git -v 1.0.3 -P hydra_options="etl.sample='sample2.csv'"
```

### The configuration
This completed project is designed to be flexible and reusable, so that you can easily adapt it to your needs and use it for other projects. In order to do so, the parameters controlling the pipeline are defined in the ``config.yaml`` file in the root of this repository. Hydra is used to manage this configuration file. 
Open this file and get familiar with its content. Remember: this file is only read by the ``main.py`` script (i.e., the pipeline) and its content is available with the ``go`` function in ``main.py`` as the ``config`` dictionary.
For example, the name of the project is contained in the ``project_name`` key under the ``main`` section in the configuration file. It can be accessed from the ``go`` function as `config["main"]["project_name"]`.

NOTE: 
Do NOT hardcode any parameter when writing the pipeline. All the parameters should be 
accessed from the configuration file.

### Running the entire pipeline or just a selection of steps
In order to run the pipeline you need to be in the root of the directory where the ``main.py`` file is located, and then you can execute as usual:

```bash
>  mlflow run .
```
This will run the entire pipeline.

To run one step at the time. Say you want to run only
the ``download`` step. The `main.py` is written so that the steps are defined at the top of the file, in the ``_steps`` list, and can be selected by using the `steps` parameter on the command line:

```bash
> mlflow run . -P steps=download
```
If you want to run the ``download`` and the ``basic_cleaning`` steps, you can similarly do:
```bash
> mlflow run . -P steps=download,basic_cleaning
```
You can override any other parameter in the configuration file using the Hydra syntax, by
providing it as a ``hydra_options`` parameter. For example, say that we want to set the parameter
modeling -> random_forest -> n_estimators to 10 and etl->min_price to 50:

```bash
> mlflow run . \
  -P steps=download,basic_cleaning \
  -P hydra_options="modeling.random_forest.n_estimators=10 etl.min_price=50"
```


### W&B Public Link
[wandb.ai/idris-isah2-udacity/nyc_airbnb](https://wandb.ai/idris-isah2-udacity/nyc_airbnb?nw=nwuseridrisisah2)
## License

[License](LICENSE.txt)
