import json
import os
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

import pandas as pd
from datasets import (
    Dataset,
    DatasetDict,
    IterableDataset,
    IterableDatasetDict,
    load_dataset,
)

from openpo.internal.error import AuthenticationError, ProviderError


class HuggingFaceStorage:
    """Storage class for HuggingFace Datasets.

    This class provides methods to store and retrieve data from HuggingFace's dataset
    repositories. It handles the creation of repositories and manages data upload
    and download operations.

    Parameters:
        api_key (str): HuggingFace API token with write access. Environment variable can be set instead of passing in the key.

    Raises:
        AuthenticationError: If authentication fails
        ProviderError: If HuggingFace error is raised
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("HF_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                provider="Huggingface",
                message=f"HuggingFace API key must be provided.",
            )

    def _convert_to_dict(self, data: List[Dict[str, Any]]) -> Dict:
        if not data:
            return {}

        keys = data[0].keys()

        return {key: [item[key] for item in data] for key in keys}

    def push_to_repo(
        self,
        repo_id: str,
        data: Union[List[Dict[str, Any]], pd.DataFrame],
        config_name: str = "default",
        set_default: Optional[bool] = None,
        split: Optional[str] = None,
        data_dir: Optional[str] = None,
        commit_message: Optional[str] = None,
        commit_description: Optional[str] = None,
        private: Optional[bool] = False,
        token: Optional[str] = None,
        revision: Optional[str] = None,
        create_pr: Optional[bool] = False,
        max_shard_size: Optional[Union[int, str]] = None,
        num_shards: Optional[int] = None,
        embed_external_files: bool = True,
    ):
        """
        Push data to HuggingFace dataset repository.
        This is the implementation of HuggingFace Dataset's push_to_hub method.
        For parameters not listed, check HuggingFace documentation for more detail.

        Args:
            data: The data to upload.

                - List[Dict]
                - pandas DataFrame

            repo_id (str): Name of the dataset repository.

        Raises:
            Exception: If pushing to dataset repository fails.
        """

        if not isinstance(data, (list, pd.DataFrame)):
            raise TypeError("data must be a list of dictionaries or pandas DataFrame")

        if isinstance(data, pd.DataFrame):
            ds = Dataset.from_pandas(data)

        if isinstance(data, list):
            ds = self._convert_to_dict(data)
            ds = Dataset.from_dict(ds)

        try:
            ds.push_to_hub(
                repo_id=repo_id,
                config_name=config_name,
                set_default=set_default,
                split=split,
                data_dir=data_dir,
                commit_message=commit_message,
                commit_description=commit_description,
                private=private,
                token=token,
                revision=revision,
                create_pr=create_pr,
                max_shard_size=max_shard_size,
                num_shards=num_shards,
                embed_external_files=embed_external_files,
            )
        except Exception as e:
            raise ProviderError(
                provider="huggingface storage",
                message=f"Error pushing data to the repository: {str(e)}",
            )

    def load_from_repo(
        self,
        path: str,
        name: Optional[str] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[
            Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]
        ] = None,
        split: Optional[str] = None,
        cache_dir: Optional[str] = None,
        features=None,
        download_config=None,
        download_mode=None,
        verification_mode=None,
        keep_in_memory: Optional[bool] = None,
        save_infos: bool = False,
        revision: Optional[str] = None,
        token: Optional[Union[bool, str]] = None,
        streaming: bool = False,
        num_proc: Optional[int] = None,
        storage_options: Optional[Dict] = None,
        trust_remote_code: bool = None,
        **config_kwargs,
    ) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        """
        Load data from HuggingFace dataset repository.
        This is direct implementation of HuggingFace Dataset load_dataset method.
        For arguments not listed here, check HuggingFace documentation for more detail.

        Args:
            path (str): Path or name of the dataset.

        Raises:
            Exception: If loading data from repository fails.
        """

        try:
            return load_dataset(
                path=path,
                name=name,
                data_dir=data_dir,
                data_files=data_files,
                split=split,
                cache_dir=cache_dir,
                features=features,
                download_config=download_config,
                download_mode=download_mode,
                verification_mode=verification_mode,
                keep_in_memory=keep_in_memory,
                save_infos=save_infos,
                revision=revision,
                token=token,
                streaming=streaming,
                num_proc=num_proc,
                storage_options=storage_options,
                trust_remote_code=trust_remote_code,
                **config_kwargs,
            )
        except Exception as e:
            raise ProviderError(
                provider="huggingface storage",
                message=f"Error loading data from the HF repository: {str(e)}",
            )
