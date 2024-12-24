# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Any, Dict

from agentica.file.base import File
from agentica.utils.log import logger


class CsvFile(File):
    type: str = "CSV"

    def get_metadata(self) -> Dict[str, Any]:
        if self.name is None:
            self.name = Path(self.data_path).name

        if self.columns is None:
            try:
                # Get the columns from the file
                with open(self.data_path) as f:
                    dict_reader = csv.DictReader(f)
                    if dict_reader.fieldnames is not None:
                        self.columns = list(dict_reader.fieldnames)
            except Exception as e:
                logger.warning(f"Error getting columns from file: {e}")

        return self.model_dump(exclude_none=True)
