import os
from unittest.mock import MagicMock, call, patch

import datasets
import pytest
from datasets import Dataset, IterableDatasetDict

from crane.core.writer import BaseDatasetWriter


class TestBaseDatasetWriter:
    @pytest.mark.parametrize("with_sharding", [True, False])
    def test_write_split(self, tmp_path, with_sharding):
        ds = Dataset.from_dict({"obj": [0]})
        ds = ds.to_iterable_dataset(1)

        class MockDatasetWriter(BaseDatasetWriter):
            write_batch = MagicMock()
            initialize = MagicMock()
            finalize = MagicMock()
            initialize_shard = MagicMock()
            finalize_shard = MagicMock()

        with (
            patch("crane.core.writer.DatasetConsumer") as consumer_mock,
            patch("crane.core.writer.ShardingController") as sharding_mock,
        ):
            sharding_mock().is_active = with_sharding
            sharding_mock.reset_mock()

            writer = MockDatasetWriter(
                save_dir=tmp_path, overwrite=True, write_batch_size=1, num_proc=1
            )
            writer._write_dataset(ds, save_dir=tmp_path)

            # check sharding strategy
            sharding_mock.assert_called_once()

            # check dataset consumer
            consumer_mock.assert_called_once()
            consumer_mock().consume.assert_called_once_with(ds)
            # get arguments to consumer initializer
            fn = consumer_mock.mock_calls[0].args[0]
            init = consumer_mock.mock_calls[0].kwargs["initialize"]
            finalize = consumer_mock.mock_calls[0].kwargs["finalize"]

            # avoid buffer clear because clearing is inplace and mock call arguments
            # would be cleared too
            with patch("crane.core.writer.BatchBuffer.clear", MagicMock()):
                mock_sample = MagicMock()
                # apply function
                fn(mock_sample)
                # make sure that the callback is called first, then the write sample
                # and finally the update function
                if with_sharding:
                    sharding_mock().callback.assert_called_once_with([mock_sample])
                    writer.write_batch.assert_called_once_with(sharding_mock().callback())
                    sharding_mock().update(writer.write_batch())
                else:
                    writer.write_batch.assert_called_once_with([mock_sample])

            # make sure the sharding initializers is called
            init()
            sharding_mock().initialize.assert_called_once()
            writer.initialize.assert_called_once()

            # make sure the sharding finalizers is called
            finalize()
            sharding_mock().finalize.assert_called_once()
            writer.finalize.assert_called_once()

            # check the output directory
            assert set(os.listdir(tmp_path)) == {
                datasets.config.DATASET_STATE_JSON_FILENAME,
                datasets.config.DATASET_INFO_FILENAME,
            }

    @pytest.mark.parametrize("path_exists", [True, False])
    def test_write_dataset(self, path_exists, tmp_path):
        tmp_path = tmp_path if path_exists else os.path.join(tmp_path, "data")

        ds = Dataset.from_dict({"obj": [0]})
        ds = ds.to_iterable_dataset(1)
        ds._format_kwargs = {"key": 0}

        class MockDatasetWriter(BaseDatasetWriter):
            initialize = MagicMock()
            write_batch = MagicMock()
            finalize = MagicMock()
            initialize_shard = MagicMock()
            finalize_shard = MagicMock()

        with patch("crane.core.writer.BaseDatasetWriter._write_dataset") as write_split_mock:
            writer = MockDatasetWriter(save_dir=tmp_path, overwrite=path_exists)
            writer.write(ds)

            write_split_mock.assert_called_once_with(ds, tmp_path)

    @pytest.mark.parametrize("path_exists", [True, False])
    def test_write_dataset_dict(self, path_exists, tmp_path):
        tmp_path = tmp_path if path_exists else os.path.join(tmp_path, "data")

        ds = Dataset.from_dict({"obj": [0]})
        ds = ds.to_iterable_dataset(1)
        ds = IterableDatasetDict({"train": ds, "test": ds})

        class MockDatasetWriter(BaseDatasetWriter):
            initialize = MagicMock()
            write_batch = MagicMock()
            finalize = MagicMock()
            initialize_shard = MagicMock()
            finalize_shard = MagicMock()

        with patch("crane.core.writer.BaseDatasetWriter._write_dataset") as write_split_mock:
            writer = MockDatasetWriter(save_dir=tmp_path, overwrite=path_exists)
            writer.write(ds)

            write_split_mock.assert_has_calls(
                [call(split, os.path.join(tmp_path, key)) for key, split in ds.items()],
                any_order=True,
            )

        # check if dataset dict json exists in output directory
        assert datasets.config.DATASETDICT_JSON_FILENAME in os.listdir(tmp_path)
