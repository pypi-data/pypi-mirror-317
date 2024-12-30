import os
import sys
import importlib
from tqdm import tqdm

import torch
from torch.utils.data import DataLoader
from torchvision import transforms

def is_torchvision_transform_object(transform):
    """
    Heuristic to determine if the given transform is likely a torchvision transform (e.g., Compose).
    Checks:
    - If it's an instance of torchvision.transforms.Compose
    - Or if the transform's module name starts with 'torchvision.transforms'
    """
    if isinstance(transform, transforms.Compose):
        return True
    
    transform_module = transform.__class__.__module__
    if transform_module.startswith('torchvision.transforms'):
        return True
    
    return False

def is_nn_sequential_or_scripted(transform):
    """
    Checks if the transform is an nn.Module (like nn.Sequential) or a scripted transform.
    Scripted transforms are typically torch.jit.ScriptModule objects.
    Both of these expect tensor inputs rather than PIL images.
    """
    # Check if it's a subclass of nn.Module (includes nn.Sequential)
    if isinstance(transform, torch.nn.Module):
        return True
    # Check for scripted modules (torch.jit.ScriptModule)
    # Scripted modules are not necessarily nn.Module subclasses in Python,
    # but we can try this check:
    if "ScriptModule" in str(type(transform)):
        return True
    
    return False

def get_preprocessing(preproc_config):
    if preproc_config is None:
        return None

    module_name = preproc_config['module']
    func_name = preproc_config['function']
    func_args = preproc_config.get('args', {})

    sys.path.append(os.getcwd())
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)

    if not callable(func):
        raise ValueError(f"The specified preprocessing function '{func_name}' is not callable.")

    # Always call the function to instantiate the transform
    try:
        transform = func(**func_args) if func_args else func()
    except:
        transform = func(**func_args) if func_args else func

    # The rest of your wrapper logic here...
    def preprocessing_wrapper(data):
        return transform(data)

    return preprocessing_wrapper

def get_datasets(dataset_config):
    """
    Creates train, validation, and test DataLoaders based on dataset_config.
    """
    module_name = dataset_config['module']
    class_name = dataset_config['class']
    ds_args = dataset_config.get('args', {})

    # Load preprocessing function
    preproc_config = ds_args.pop('preprocessing', None)
    transform_func = get_preprocessing(preproc_config)

    sys.path.append(os.getcwd())
    module = importlib.import_module(module_name)
    dataset_class = getattr(module, class_name)

    def create_dataset_and_loader(split_name):
        """
        Creates a dataset and corresponding DataLoader for the given split ('train', 'valid', 'test').
        """
        if split_name not in ds_args:
            return None, None

        split_config = ds_args[split_name]
        if split_config is None:
            return None, None

        split_dataset_args = split_config.get('args', {})
        preprocessing_arg_name = dataset_config.get('preprocessing_arg', 'transform')
        split_dataset_args[preprocessing_arg_name] = transform_func

        dataset = dataset_class(**split_dataset_args)

        loader_args = split_config.get('loader', None)
        loader = DataLoader(dataset=dataset, **loader_args) if loader_args else None

        return dataset, loader

    print("[Datasets] Initializing dataset loaders...")

    with tqdm(total=3, desc="[Datasets Progress]", bar_format="{l_bar}{bar:40}{r_bar}", leave=True) as pbar:
        _train_dataset, train_loader = create_dataset_and_loader('train')
        pbar.update(1)

        _valid_dataset, valid_loader = create_dataset_and_loader('valid')
        pbar.update(1)

        _test_dataset, test_loader = create_dataset_and_loader('test')
        pbar.update(1)

    print("[Datasets] Dataset loaders initialized successfully.")
    return train_loader, valid_loader, test_loader
