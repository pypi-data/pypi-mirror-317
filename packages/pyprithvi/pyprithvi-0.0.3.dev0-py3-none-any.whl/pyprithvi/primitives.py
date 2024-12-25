from typing import Optional, Dict, List, Literal
from pyprithvi.engine import _get_user_session, set_user_session, get_backend_url
# TODO Use post_request for all primitives
from pyprithvi.engine import post_request


def submit_program(program: str, job_config_id: str = 'cjc-10'):
    """Featurize data on Prithvi.

    Parameters
    ----------
    program: str
      prithvi program as a string
    job_config_id: str
      Job configuration id for the job

    Example
    -------
    >>> pyprithvi.program(program='')

    """
    sess = _get_user_session()
    json_params = {
        'program': program,
        'job_config_id': job_config_id,
    }
    response = sess.post(get_backend_url() + "primitive/submit-program-string",
                         params=json_params)
    set_user_session(sess)
    return response.json()


def featurize(dataset_address: str,
              featurizer: str,
              output_address_key: str,
              dataset_column: str,
              label_column: Optional[str] = None,
              feat_kwargs: Dict = dict(),
              use_ray: bool = False,
              job_config_id: str = 'cjc-10'):
    """Featurize data on Prithvi.

    Parameters
    ----------
    dataset_address: str
      datastore address of dataset which is to be featurized
    featurizer: str
      A deepchem featurizer. Featurizer currently supported are: ECFP
    output: str
      datastore address to write output (featurized dataset)
    dataset_column: str
      Input column to the featurizer
    label_column: str, *optional*
      Name of target column. Used only when dataset_column depends
      on target column.
    job_config_id: str
      Job configuration id for the job
    use_ray: bool, default False
        When set to True, uses ray for distributed featurization.


    .. list-table:: Supported Featurizers
       :widths: 25 50
       :header-rows: 1

       * - Featurizer Code
         - Featurizer Name
       * - ecfp
         - Cicular Fingerprint
       * - weave
         - WeaveFeaturizer
       * - graphconv
         - ConvMolFeaturizer


    Returns
    -------
    response: dict
      A dictionary containing job_id and operation cose of the featurization job.

    Example
    -------
    >>> pyprithvi.featurize(
    ...     dataset_address='chiron://chemberta3/zinc/zinc5k.csv',
    ...     featurizer='ECFP',
    ...     output_address_key='zinc5k_ecfp_featurized',
    ...     dataset_column='smiles',
    ...     label_column='logp',
    ...     use_ray=True)

    """
    featurizer = featurizer.lower()
    params = {
        'dataset_address': dataset_address,
        'featurizer': featurizer,
        'output_key': output_address_key,
        'dataset_column': dataset_column,
        'job_config_id': job_config_id,
        'use_ray': use_ray,
    }
    if label_column is not None:
        params['label_column'] = label_column

    json_params = {'feat_kwargs': feat_kwargs}
    api_path = "primitive/featurize"
    response = post_request(api_path, params=params, json=json_params)
    if response:
        response = response.json()
        return response
    return None


def train(model_type: str,
          dataset_address: str,
          model_key: str,
          init_kwargs: Dict = dict(),
          train_kwargs: Dict = dict(),
          pretrained_model_address: Optional[str] = None,
          use_ray: bool = False,
          task: Optional[str] = None,
          num_workers: int = 1,
          exp_name: str = 'test',
          job_config_id: str = 'cjc-10'):
    """
    Utility to train model

    Parameters
    ----------
    model_type: str
      Type of model to be trained
    dataset_address: str
      Address of dataset in chiron datastore - the dataset should be
      a DeepChem dataset.
    model_key: str
      Name of model as to be stored in datastore
    init_kwargs: Dict
      Keyword arguments to use in model initialisation, like n_layers
    train_kwargs: Dict
      Keyword arguments to use during training, like n_epoch, optimizer
    pretrained_model_address: Optional[str]
      pretrained model address. If provided, the pretrained model will be used as a base model for fine-tuning
    use_ray: bool, default False
      Uses ray for training models. Ray is a distributed computing framework.
    num_workers: int, default 1
        Number of workers to use for training the model
    exp_name: str, default 'test'
        Experiment name to use for training the model
    task: str
      task to train the model for. Required only for Foundation models
    job_config_id: str
      Job configuration id


    .. list-table:: Supported Model Types
       :widths: 25 50
       :header-rows: 1

       * - Model Types
         - Model Name/Notes
       * - weave
         - Weave model
       * - linear_regression
         - Linear Regression models
       * - graphconv
         - deepchem.models.GraphConvModel
       * - random_forest_classifier
         - A random forest classifier
       * - random_forest_regressor
         - A random forest regressor
       * - chemberta
         - ChemBERTa model
       * - support_vector_regressor
         - Support Vector Regressor
       * - infograph
         - InfoGraph model
       * - multitask_classifier
         - MultiTask Classifier


    Returns
    -------
    response: dict
      A dictionary containing job_id and operation cose of the featurization job.

    Example
    -------
    >>> pyprithvi.train(model_type="linear_regression", dataset_address="dataset.csv",
    ... model_key="lin_reg_on_dataset")
    """
    params = {
        'model_type': model_type,
        'dataset_address': dataset_address,
        'model_key': model_key,
        'job_config_id': job_config_id,
        'use_ray': use_ray,
        'task': task,
        'num_workers': num_workers,
        'exp_name': exp_name,
        'pretrained_model_address': pretrained_model_address
    }

    # Functioning of json string parser:
    # Issue:
    # 'string_text' => string_text
    # In the above case, the json parser gives 'string_text' as a unknown variable
    #
    # Solution:
    # '\"' + 'string_text' + '\"' => '"string_text"'
    # new parsing result:
    # '"string_text"' => "string_text"
    # which is a python string

    for key, value in init_kwargs.items():
        if isinstance(value, str):
            init_kwargs[key] = '\"' + value + '\"'

    for key, value in train_kwargs.items():
        if isinstance(value, str):
            init_kwargs[key] = '\"' + value + '\"'

    json_params = {'init_kwargs': init_kwargs, 'train_kwargs': train_kwargs}
    api_path = "primitive/train"
    response = post_request(api_path, params=params, json=json_params)
    if response:
        return response.json()
    return None


def infer(model_address: str,
          dataset_address: str,
          output_key: str,
          dataset_column: Optional[str] = None,
          job_config_id: str = 'cjc-10'):
    """
    Perform inference on a dataset using a trained model

    Parameters
    ----------
    model_address: str
      Address of trained model
    dataset_address: str
      Address of dataset to perform inference in prithvi datastore
    dataset_column: str
      Column in the dataset to perform inference
    output_key: str
      Datastore address to store the results inference of address.
    job_config_id: str
      Job configuration id

    Example
    -------
    >>> pyprithvi.infer(model_address = "trained_model", dataset_address = "dataset_name",
    ... output_key = "inference_dataset_key")
    """
    params = {
        'model_address': model_address,
        'dataset_address': dataset_address,
        'output_key': output_key,
        'job_config_id': job_config_id
    }
    if dataset_column is not None:
        params['dataset_column'] = dataset_column
    api_path = "primitive/infer"
    response = post_request(api_path, params=params)
    if response:
        response = response.json()
        return response
    return None


def cluster(dataset_address: str,
            num_clusters: int,
            output_key: str,
            smiles_column: str,
            job_config_id: str = 'cjc-10'):
    """
    Parameters
    ----------
    output: str
      output key used for storing output data in datastore
    num_clusters: int
      Number of clusters
    output_key: str
      Output file containing molecule name and cluster id. On datastore
    smiles_column: str
      Column containing smiles string in the csv dataset
    job_config_id: str
      Job configuration id
    """
    api_path = 'primitive/cluster'
    params = {
        'dataset_address': dataset_address,
        'num_clusters': num_clusters,
        'output_key': output_key,
        'smiles_column': smiles_column,
        'job_config_id': job_config_id,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return response


def partition(dataset_address: str,
              n_partition: int,
              shuffle: bool = False,
              job_config_id: str = 'cjc-10'):
    """
    Partition a dataset (supported only for disk dataset, csv files)

    Parameters
    ----------
    dataset_address: str
      Address of dataset to partition
    n_partition: int
      Number of partitions to make on the dataset
    shuffle: bool
      Whether to shuffle the dataset or not (supported only for CSV Files)
    job_config_id: str
      Job configuration id

    Example
    -------
    >>> pyprithvi.partition(dataset_address='smiles.csv', n_partition=5)
    """
    params = {
        'dataset_address': dataset_address,
        'n_partition': n_partition,
        'shuffle': shuffle,
        'job_config_id': job_config_id,
    }
    api_path = "primitive/data/partition"
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def merge(dataset_addresses: List[str],
          output_key: str,
          job_config_id: str = 'cjc-10'):
    """Merging datasets

    Parameters
    ----------
    dataset_addresses: List[str]
      Addresses of dataset to merge
    output_key: str
      Output key of address
    job_config_id: str
      Job configuration id

    Example
    -------
    >>> pyprithvi.merge(dataset_addresses=['part1.csv', 'part2.csv'], output_key='result.csv')
    """
    params = {'output_key': output_key, 'job_config_id': job_config_id}
    json = {'dataset_addresses': dataset_addresses}
    api_path = "primitive/data/merge"
    response = post_request(api_path, params=params, json=json)  # type: ignore
    if response:
        return response.json()
    return None


def retrosynthesis(target_smi: str, output: str, job_config_id: str = 'cjc-10'):
    """Perform retrosynthesis on a target molecule.

    Parameters
    ----------
    target_smi: str
      SMILES string of the target molecule.
    output: str
      Name of the JSON file to store the results in.
    job_config_id: str
      Job configuration id

    Example
    -------
    >>> pyprithvi.retrosynthesis(target_smi =
    ... "Cc1cccc(c1N(CC(=O)Nc2ccc(cc2)c3ncon3)C(=O)C4CCS(=O)(=O)CC4)C",
    ... output = 'retro_output.json')
    """
    sess = _get_user_session()
    json_params = {
        'target_smi': target_smi,
        'output': output,
        'job_config_id': job_config_id,
    }

    response = sess.post(get_backend_url() + "primitive/retrosynthesis",
                         params=json_params)
    set_user_session(sess)
    return response.json()


def k_fold_split(splitter_type: str,
                 dataset_address: str,
                 k: int,
                 job_config_id: Optional[str] = 'cjc-10'):
    """
    Performs k fold split on the dataset

    Parameters
    ----------
    splitter_type: str
      Splitter type to use when splitting dataset
    dataset_address: str
      Dataset to perform splitting
    k: int
      Number of folds to generate
    job_config_id: str, optional, default: cjc-10
      Job configuriton id
    """
    params = {
        'splitter_type': splitter_type,
        'dataset_address': dataset_address,
        'k': k,
        'job_config_id': job_config_id
    }
    api_path = "primitive/data/k-fold-split"
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def train_valid_test_split(splitter_type: str,
                           dataset_address: str,
                           frac_train: float = 0.8,
                           frac_test: float = 0.1,
                           frac_valid: float = 0.1,
                           job_config_id: Optional[str] = 'cjc-10') -> Dict:
    """
    Performs train test validation split on a dataset

    Parameters
    ----------
    splitter_type: str
      Splitter type to use when splitting dataset.
    dataset_address: str
      Dataset to perform splitting
    frac_train: float
      Fraction of training dataset
    frac_test: float
      Fraction of testing dataset
    frac_valid: float
      Fraction of validation dataset
    job_config_id: str, optional, default: cjc-10
      Job configuriton id

    Returns
    -------
    response: Dict
        A dictionary containing job id in the key `job_id`.


    .. list-table:: Supported splitters
       :widths: 25 50
       :header-rows: 1

       * - Splitter type
         - Description
       * - random
         - Splits data into random subsets
       * - index
         - Splits data into subsets by index
       * - scaffold
         - Splits data into subsets using scaffolds


    Example
    -------
    >>> pyprithvi.train_valid_test_split(splitter_type='random', dataset_address='zinc.csv',
    ... frac_train=0.70, frac_valid=0.15, frac_Test=0.15)
    """
    params = {
        'splitter_type': splitter_type,
        'dataset_address': dataset_address,
        'frac_train': frac_train,
        'frac_valid': frac_valid,
        'frac_test': frac_test,
        'job_config_id': job_config_id
    }
    api_path = "primitive/data/train-valid-test-split"
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None  # type: ignore


def evaluate_model(dataset_addresses: List[str],
                   model_address: str,
                   metrics: List[str],
                   output_key: str,
                   job_config_id: str = 'cjc-10'):
    """
    Model evaluator

    Parameters
    ----------
    dataset_addresses: List[str]
      List of dataset address to evaluate a model
    model_address: str
      Address of model to evaluate
    metrics: List[str]
      List of metrics to use when evaluating the model. The metric should be one of
    `pearson_r2_score`, `jaccard_index`, `prc_auc_score`, `roc_auc_score`, `rms_score`, `mae_error`, `bedroc_score`, 'accuracy_score', 'balanced_accuracy_score'.
    output_key: str
      output key to write model evaluation results
    job_config_id: str, optional, default: cjc-10
      job configuration id
    """
    params = {
        'model_address': model_address,
        'output_key': output_key,
        'job_config_id': job_config_id
    }
    json = {'dataset_addresses': dataset_addresses, 'metrics': metrics}
    api_path = "primitive/evaluate-model"
    response = post_request(api_path, params=params, json=json)
    if response:
        return response.json()
    return None


def hyperparameter_optimizer(model_type: str,
                             train_address: str,
                             valid_address: str,
                             hyperparams: Dict,
                             output_prefix: str,
                             metric: str,
                             nb_epoch: Optional[int] = 10,
                             job_config_id: str = 'cjc-10'):
    """
    Hyperparameter optimizer

    Parameters
    ----------
    model_type: str
      model to tune hyperparameters
    train_address: str
      train dataset to perform hyperparameter tuning
    valid_address: str
      valid dataset to validate tuned models
    hyperparams:
      The hyperparameter search space, represented as key-value pairs
    output_prefix:
      Datastore address's output prefix to write hyperparameter tuning results
    metric: str, optional, default: pearson_r2_score
      metric to use use for hyperparameter tuning
    nb_epoch: Optional[int]
      number of epochs
    job_config_id: str, optional, default: cjc-10
      job configuration id
    """
    # currently, we support only grid but we should add for gaussian and random
    # hyperparam search
    algorithm = 'grid'
    params = {
        'train_address': train_address,
        'valid_address': valid_address,
        'model_type': model_type,
        'metric': metric,
        'output_prefix': output_prefix,
        'nb_epoch': nb_epoch,
        'job_config_id': job_config_id,
        'algorithm': algorithm
    }
    json_params = {'hyperparams': hyperparams}
    api_path = "primitive/hyperparameter-optimizer"
    response = post_request(api_path, params=params, json=json_params)
    if response:
        return response.json()
    return None


def cleaner(pdb_address: Optional[str] = None,
            output_address: Optional[str] = None,
            ligand: Optional[str] = None,
            ligand_output: Optional[str] = None,
            optimize_ligand: Optional[bool] = None,
            remove_chains: Optional[str] = None,
            replace_nonstandard_residues: bool = True,
            remove_heterogens: bool = True,
            remove_water: bool = True,
            add_hydrogens: bool = True,
            pH: float = 7.0,
            job_config_id: str = 'cjc-10'):
    """
    Parameters
    ----------
    pdb_address: Optional[str]
        Prithvi address of the PDB file to be cleaned.
    output_address: Optional[str]
        Name to output of cleaned pdb file.
    ligand: Optional[str]
        Prithvi address of PDB file about the molecule acting as ligand in the protein.
    ligand_output: Optional[str]
        Name to output of ligand file.
    optimize_ligand: Optional[bool]
        If True, optimize ligand with RDKit.
    remove_chains: Optional[str]
        Delete chains in PDB files. Chains can be 'Protein' and 'DNA'.
    replace_nonstandard_residues: bool (default True)
        Replace nonstandard residues with standard residues.
    remove_heterogens: bool (default True)
        Removes residues that are not standard amino acids or nucleotides.
    remove_water: bool (default True)
        Remove water molecules.
    add_hydrogens: bool (default True)
        Add missing hydrogens at the protonation state given by `pH`.
    pH: float (default 7.0)
        Most common form of each residue at given `pH` value is used.
    job_config_id: str, optional, default: cjc-10
      job configuration id
    """
    api_path = 'primitive/cleaner'
    params = {
        'pdb_address': pdb_address,
        'output_address': output_address,
        'ligand': ligand,
        'ligand_output': ligand_output,
        'remove_chains': remove_chains,
        'optimize_ligand': optimize_ligand,
        'replace_nonstandard_residues': replace_nonstandard_residues,
        'remove_heterogens': remove_heterogens,
        'remove_water': remove_water,
        'add_hydrogens': add_hydrogens,
        'pH': pH,
        'job_config_id': job_config_id,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def deldenoise(dataset_address: str,
               output_key: str,
               r1_column: str,
               r2_column: str,
               r3_column: str,
               sq_count_column: str,
               cutoff: int = 100,
               job_config_id: str = 'cjc-10'):
    """
    Parameters
    ----------
    dataset_address: str
        Prithvi address of the dataset to be deldenoised.
    output_key: str
        Name to output of deldenoised dataset.
    r1_column: str
        Column name of the first reagent.
    r2_column: str
        Column name of the second reagent.
    r3_column: str
        Column name of the third reagent.
    sq_count_column: str
        Column name of the sequence count.
    job_config_id: str, optional, default: cjc-10
      job configuration id

    Returns
    -------
    response: Dict
        A dictionary containing job id in the key `job_id`.
    """
    api_path = 'primitive/deldenoise'
    params = {
        'dataset_address': dataset_address,
        'output_key': output_key,
        'r1_column': r1_column,
        'r2_column': r2_column,
        'r3_column': r3_column,
        'sq_count_column': sq_count_column,
        'job_config_id': job_config_id,
        'cutoff': cutoff,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def pose_generation(pdb_address: str,
                    ligand_address: str,
                    output: str,
                    docking_method: Literal['VINA', 'GNINA',
                                            'qVINA-W'] = 'VINA',
                    centroid: str = '',
                    box_dims: str = '',
                    exhaustiveness: Optional[int] = 10,
                    num_modes: Optional[int] = 9,
                    is_save_complex: bool = True,
                    is_save_pdbqt: bool = True,
                    job_config_id: str = 'cjc-10'):
    """
    Parameters
    ----------
    pdb_address: str
        Chiron address of the PDB protein file.
    ligand_address: str
        Chiron address of PDB file about the molecule acting as ligand in the protein.
    output: str
        Name to the PDB complex of protein-ligand pose generation molecule.
    docking_method: str
        Whether to use Vina or Gnina as docking method, both supported by Deepchem
    centroid: Optional[ArrayLike] (default None)
        The centroid to dock against. Is computed if not specified.
    box_dims: Optional[ArrayLike] (default None)
        A numpy array of shape `(3,)` holding the size of the box to dock. If not
        specified is set to size of molecular complex plus 5 angstroms.
    exhaustiveness: Optional[int] (default 10)
        Tells Autodock Vina how exhaustive it should be with pose generation. A
        higher value of exhaustiveness implies more computation effort for the
        docking experiment.
    num_modes: Optional[int] (default 9)
        Tells Autodock Vina how many binding modes it should generate at
        each invocation.
    is_save_complex: bool
        Whether to save .pdb complex file or not (Default: True)
    is_save_pdbqt: bool
        Whether to save .pdbqt file (also contains scores) or not (Default: True)
    job_config_id: str, optional, default: cjc-10
      job configuration id
    """
    api_path = 'primitive/pose_generation'
    params = {
        'pdb_address': pdb_address,
        'ligand_address': ligand_address,
        'output': output,
        'docking_method': docking_method,
        'centroid': centroid,
        'box_dims': box_dims,
        'exhaustiveness': exhaustiveness,
        'num_modes': num_modes,
        'is_save_complex': is_save_complex,
        'is_save_pdbqt': is_save_pdbqt,
        'job_config_id': job_config_id,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def pose_generation_smiles(pdb_address: str,
                           ligand_smiles: str,
                           output: str,
                           docking_method: str = 'VINA',
                           centroid: str = '',
                           box_dims: str = '',
                           exhaustiveness: Optional[int] = 10,
                           num_modes: Optional[int] = 9,
                           job_config_id: str = 'cjc-10'):
    """
    Generate pose(s) depending from given protein and ligand SMILES

    Parameters
    ----------
    pdb_address: str
        Chiron address of the PDB protein file.
    ligand_smiles: str
        ligand SMILES
    output: str
        Name to the scores files (used along with protein name)
    docking_method: str
        Wether to use Vina or Gnina as docking method, both supported by Deepchem
    centroid: Optional[ArrayLike] (default None)
        The centroid to dock against. Is computed if not specified.
    box_dims: Optional[ArrayLike] (default None)
        A numpy array of shape `(3,)` holding the size of the box to dock. If not
        specified is set to size of molecular complex plus 5 angstroms.
    exhaustiveness: Optional[int] (default 10)
        Tells Autodock Vina how exhaustive it should be with pose generation. A
        higher value of exhaustiveness implies more computation effort for the
        docking experiment.
    num_modes: Optional[int] (default 9)
        Tells Autodock Vina how many binding modes it should generate at
        each invocation.
    job_config_id: str
        job configuration id

    Returns
    -------
    response: Dict
        A dictionary containing job id in the key `job_id`.
    """
    api_path = 'primitive/pose_generation_smiles'
    params = {
        'pdb_address': pdb_address,
        'ligand_smiles': ligand_smiles,
        'output': output,
        'docking_method': docking_method,
        'centroid': centroid,
        'box_dims': box_dims,
        'exhaustiveness': exhaustiveness,
        'num_modes': num_modes,
        'job_config_id': job_config_id,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def pose_generation_csv(pdb_address: str,
                        ligands_csv_address: str,
                        smiles_column_name: str,
                        output_key: str,
                        docking_method: str = 'VINA',
                        centroid: Optional[List] = None,
                        box_dims: Optional[List] = None,
                        exhaustiveness: Optional[int] = 10,
                        num_modes: Optional[int] = 9,
                        job_config_id: str = 'cjc-10'):
    """
    Generate docking scores for protein and ligands collection from a csv file.
    The output file is in csv format.

    Parameters
    ----------
    pdb_address: str
        Chiron address of the PDB protein file.
    ligands_csv_address: str
        Ligands csv address
    smiles_column_name: str
        Name of column with ligand SMILES in the csv file
    output_key: str
        Name to the scores csv file
    docking_method: str
        Wether to use Vina or Gnina or qVina-W as docking method, both supported by Deepchem
    centroid: Optional[ArrayLike] (default None)
        The centroid to dock against. Is computed if not specified.
    box_dims: Optional[ArrayLike] (default None)
        A numpy array of shape `(3,)` holding the size of the box to dock. If not
        specified is set to size of molecular complex plus 5 angstroms.
    exhaustiveness: Optional[int] (default 10)
        Tells Autodock Vina how exhaustive it should be with pose generation. A
        higher value of exhaustiveness implies more computation effort for the
        docking experiment.
    num_modes: int (default 9)
        Tells Autodock Vina how many binding modes it should generate at
        each invocation.
    job_config_id: str
        job configuration id

    Returns
    -------
    response: Dict
        A dictionary containing job id in the key `job_id`.
    """
    api_path = 'primitive/pose_generation_csv'
    params = {
        'pdb_address': pdb_address,
        'ligands_csv_address': ligands_csv_address,
        'smiles_column_name': smiles_column_name,
        'output_key': output_key,
        'docking_method': docking_method,
        'centroid': centroid,
        'box_dims': box_dims,
        'exhaustiveness': exhaustiveness,
        'num_modes': num_modes,
        'job_config_id': job_config_id,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def batch_docking(protein_address, ligands_csv_address, smiles_column,
                  output_scores_csv_name, docking_method, exhaustiveness,
                  num_modes, child_job_config_id, chunk_size, job_limit,
                  job_config_id):
    """
    Generate pose(s) from given protein and CSV of ligand SMILES and
    save scores by running pose generation jobs parallely.

    Parameters
    ----------
    protein_address: str
        Prithvi address of the protein used for docking
    ligands_csv_address: str
        Prithvi address of the CSV files containing ligands as SMILES
    smiles_column: str
        Name of the column containing ligand SMILES
    output_scores_csv_name: str
        Name of the output csv file containing docking scores
    docking_method: str
        Docking method to be used. (VINA or GNINA or qVINA-W)
    exhaustiveness: int
        Tells docking method how exhaustive it should be with pose generation. A
        higher value of exhaustiveness implies more computation effort for the
        docking experiment.
    num_modes: int
        Tells docking method how many binding modes it should generate at
        each invocation.
    child_job_config_id: st
        Job config id of child jobs running docking of each Ligand-Protein pair.
    chunk_size: int
        Number of SMILES per docking job
    job_limit: int
        Maximum number of concurrent docking jobs
    job_config_id: str
        job configuration id

    Returns
    -------
    response: dict
      A dictionary containing job_id and operation cose of the batch docking job.
    """
    api_path = 'primitive/batch_docking'
    params = {
        'protein_address': protein_address,
        'ligands_csv_address': ligands_csv_address,
        'smiles_column': smiles_column,
        'output_scores_csv_name': output_scores_csv_name,
        'docking_method': docking_method,
        'exhaustiveness': exhaustiveness,
        'num_modes': num_modes,
        'child_job_config_id': child_job_config_id,
        'chunk_size': chunk_size,
        'job_limit': job_limit,
        'job_config_id': job_config_id,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def pose_scoring(pdb_address: str,
                 ligand_address: str,
                 output: str,
                 centroid: Optional[List] = None,
                 box_dims: Optional[List] = None,
                 job_config_id: str = 'cjc-10'):
    """
    Calculate the binding affinity of a ligand pose.

    Parameters
    ----------
    pdb_address: str
        Prithvi address of the PDB protein file.
    ligand_address: str
        Prithvi address of PDBQT file about the molecule acting as ligand in the protein.
    output: str
        Name to the CSV file that contains the minimized binding energies.
    centroid: Optional[ArrayLike] (default None)
        The centroid to dock against. Is computed if not specified.
    box_dims: Optional[ArrayLike] (default None)
        A numpy array of shape (3,) holding the size of the box to dock. If not
        specified is set to size of molecular complex plus 5 angstroms.

    Returns
    -------
    response: dict
      A dictionary containing job_id and operation cose of the pose scoring job.

    Example
    -------
    >>> pyprithvi.pose_scoring(pdb_address='5r80.pdb', ligand_address='capsaicin_conf_docked.pdbqt', output='scores.csv')
    """
    api_path = 'primitive/pose_scoring'
    params = {
        'pdb_address': pdb_address,
        'ligand_address': ligand_address,
        'output': output,
        'centroid': centroid,
        'box_dims': box_dims,
        'job_config_id': job_config_id,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def pocket_finding(pdb_address: str,
                   output: str,
                   job_config_id: str = 'cjc-10'):
    """
    Parameters
    ----------
    pdb_address: str
        Prithvi address of the PDB protein file.
    output: str
        Name to the CSV file that contains the pocket coordinates.
    job_config_id: str, optional, default: cjc-10
      job configuration id

    Returns
    -------
    response: dict
      A dictionary containing job_id and operation cose of the pocket finding job.

    Example
    -------
    >>> pyprithvi.pocket_finding(pdb_address='3cyx.pdb', output='3cyx_pocket_coordinates.csv')
    """
    api_path = 'primitive/pocket_finding'
    params = {
        'pdb_address': pdb_address,
        'output': output,
        'job_config_id': job_config_id,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def conformational_sampling(ligand_address: str,
                            output: str,
                            n_confs: int,
                            job_config_id: str = 'cjc-10'):
    """
    Generate conformers of a ligand.

    Parameters
    ----------
    ligand_address: str
        Prithvi address of the PDB/SDF ligand file.
    output: str
        Name to the PDB files of conformers.
    n_confs: str
        The number of conformers to output.

    Returns
    -------
    response: dict
      A dictionary containing job_id and operation cose of the conformational sampling job.

    Example
    -------
    >>> pyprithvi.conformational_sampling(ligand_address='ligand_3cyx.pdb', output='conformers_ligand_3cyx.pdb',
    ... n_confs=3)
    """
    api_path = 'primitive/conformational_sampling'
    params = {
        'ligand_address': ligand_address,
        'output': output,
        'n_confs': n_confs,
        'job_config_id': job_config_id,
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def predict_protein_structure(fasta_file: str,
                              output_key: str,
                              inference_type: str = 'MONOMER',
                              use_uniref90: str = False,
                              use_mgnify: bool = False,
                              use_pdb70: bool = False,
                              use_uniclust30: bool = False,
                              use_bfd: bool = False,
                              use_small_bfd: bool = False,
                              job_config_id: str = 'cjc-openfold-1'):
    """
    Predict protein struction using OpenFold library.

    Parameter
    ---------
    fasta_file: str
        Prithvi address of the fasta file
    output_key: str
        Name of the output file
    inference_type: str
        Type of protein inference (MONOMER/SOLOSEQ)

    The below options are valid only for MONOMER inference type.

    use_uniref90: bool
        Whether to use uniref90 alignment database.
    use_mgnify: bool
        Whether to use mgnify alignment database.
    use_pdb70: bool
        Whether to use pdb70 alignment database.
    use_uniclust30: bool
        Whether to use uniclust30 alignment database.
    use_bfd: bool
        Whether to use bfd alignment database.
    use_small_bfd: bool
        Whether to use small_bfd alignment database instead of bfd.

    Returns
    -------
    response: dict
        A dictionary containing job_id and operation cose of the fold job.

    Example
    -------
    >>> pyprithvi.fold(fasta_file='protein.fasta', output_key='protein_structure')
    """
    api_path = 'primitive/openfold'
    params = {
        'fasta_file': fasta_file,
        'output_key': output_key,
        'inference_type': inference_type,
        'use_uniref90': use_uniref90,
        'use_mgnify': use_mgnify,
        'use_pdb70': use_pdb70,
        'use_uniclust30': use_uniclust30,
        'use_bfd': use_bfd,
        'use_small_bfd': use_small_bfd,
        'job_config_id': job_config_id
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None


def covalent_docking(ligand_address: str,
                     protein_address: str,
                     residue: str,
                     thether_smarts: str,
                     thether_indices: str,
                     output_key: str,
                     job_config_id: str = 'cjc-10'):
    """Covalent docking

    Parameters
    ----------
    ligand_address: str
        Prithvi Address of the ligand as a SDF file. The input ligand must be the product of the
        reaction and contain the atoms of the flexible sidechain up to (and including) the C-alpha.
    protein_address: str
        Prithvi Address of the protein pdb file
    residue: str
        Protein's residue were covalent activity will take place. Please use
        following style "chain:residue:sequence number", for example "B:SER:222"
        for PDB ID: 3upo.
    tether_smarts: str
        SMARTS atoms to align ligand and protein including C-alpha and C-beta atoms.
        For a serine residue, theter_smarts="C(=O)-O-C" will work.
    thether_indices: str
        indices (1-based) of the SMARTS atoms that will be attached (default: 1 2)
    output_key: str
        The prefix of output files

    Returns
    -------
    response: dict
        A dictionary containing job_id and operation cose of the fold job.

    Example
    -------
    >>> pyprithvi.covalent_docking(ligand_address='chiron://test/user/ligand.sdf',
    ...     protein_address='3upo_protein.pdb', residue='B:SER:222',
    ...     thether_smarts='"C(=O)-O-C"', thether_indices='2 1', output_key='test_cov_dock_')
    """
    api_path = 'primitive/cov-dock'
    params = {
        'protein_address': protein_address,
        'ligand_address': ligand_address,
        'thether_smarts': thether_smarts,
        'thether_indices': thether_indices,
        'residue': residue,
        'output_key': output_key,
        'job_config_id': job_config_id
    }
    response = post_request(api_path, params=params)
    if response:
        return response.json()
    return None
