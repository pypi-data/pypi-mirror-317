from abc import ABC, abstractmethod
from typing import List, Union
import re
from crimson.filter_beta.filter import fnmatch_filter, re_filter
from pydantic import BaseModel


class Filter(ABC, BaseModel):
    @abstractmethod
    def filter(self, paths: List[str]) -> List[str]:
        pass


class ReFilter(Filter):
    include: List[str] = []
    exclude: List[str] = []
    flags: List[Union[re.RegexFlag, int]] = [re.IGNORECASE]

    def filter(self, paths: List[str]) -> List[str]:
        filtered_paths = re_filter(paths, self.include, self.exclude, self.flags)
        return filtered_paths


class FnFilter(Filter):
    include: List[str] = []
    exclude: List[str] = []

    def filter(self, paths: List[str]) -> List[str]:
        filtered_paths = fnmatch_filter(paths, self.include, self.exclude)

        return filtered_paths
