# SPDX-FileCopyrightText: © 2024 Jimmy Fitzpatrick <jcfitzpatrick12@gmail.com>
# This file is part of SPECTRE
# SPDX-License-Identifier: GPL-3.0-or-later

from logging import getLogger
_LOGGER = getLogger(__name__)

import os
from typing import Optional
from collections import OrderedDict
import warnings
from datetime import datetime

from spectre_core.spectrograms import Spectrogram, time_chop, join_spectrograms
from spectre_core.config import get_chunks_dir_path, TimeFormats
from spectre_core.exceptions import (
    SpectrogramNotFoundError,
    ChunkNotFoundError
)
from ._base import BaseChunk
from ._factory import get_chunk_from_tag

class Chunks:
    def __init__(self, 
                 tag: str,
                 year: Optional[int] = None, 
                 month: Optional[int] = None, 
                 day: Optional[int] = None):
        self._tag = tag
        self._Chunk = get_chunk_from_tag(tag)
        self._chunk_map: dict[str, BaseChunk] = OrderedDict()
        self._chunk_list: list[BaseChunk] = []
        self._chunk_names: list[str] = []
        self.set_date(year, month, day)


    @property
    def year(self) -> int:
        return self._year


    @property 
    def month(self) -> int:
        return self._month
    

    @property
    def day(self) -> int:
        return self._day


    @property
    def chunks_dir_path(self) -> str:
        return get_chunks_dir_path(self.year, self.month, self.day)
    

    @property 
    def chunk_map(self) -> dict[str, BaseChunk]:
        return self._chunk_map
    

    @property
    def chunk_list(self) -> list[BaseChunk]:
        return  self._chunk_list
    

    @property
    def chunk_names(self) -> list[str]:
        return self._chunk_names


    @property
    def num_chunks(self) -> int:
        return len(self.chunk_list)


    def set_date(self, 
                 year: Optional[int],
                 month: Optional[int],
                 day: Optional[int]) -> None:
        self._year = year
        self._month = month
        self._day = day
        self._update_chunk_map()


    def _update_chunk_map(self) -> None:
        self._chunk_map = OrderedDict() # reset cache
        self._chunk_list = [] # reset cache
        self._chunk_names = [] # reset cache

        chunk_files = [f for (_, _, files) in os.walk(self.chunks_dir_path) for f in files]
        
        if len(chunk_files) == 0:
            warning_message = "No chunks found, setting chunk map with empty dictionary."
            _LOGGER.warning(warning_message)
            warnings.warn(warning_message)
            return
        
        for chunk_file in chunk_files:
            file_name, _ = os.path.splitext(chunk_file)
            chunk_start_time, tag = file_name.split("_", 1)
            if tag == self._tag:
                self._chunk_map[chunk_start_time] = self._Chunk(chunk_start_time, tag)
        
        self._chunk_map = OrderedDict(sorted(self._chunk_map.items()))
        self._chunk_names = list(self._chunk_map.keys())
        self._chunk_list = list(self._chunk_map.values())


    def update(self) -> None:
        """Public alias for setting chunk map"""
        self._update_chunk_map()
    

    def __iter__(self):
        yield from self.chunk_list


    def _get_chunk_by_chunk_start_time(self, 
                                      chunk_start_time: str) -> BaseChunk:
        try:
            return self.chunk_map[chunk_start_time]
        except KeyError:
            raise ChunkNotFoundError(f"Chunk with chunk start time {chunk_start_time} could not be found within {self.chunks_dir_path}")


    def _get_chunk_by_index(self, 
                           chunk_index: int) -> BaseChunk:
        num_chunks = len(self.chunk_map)
        if num_chunks == 0:
            raise ChunkNotFoundError("No chunks are available")
        index = chunk_index % num_chunks  # Use modulo to make the index wrap around. Allows the user to iterate over all the chunks via index cyclically.
        return self.chunk_list[index]


    def __getitem__(self, subscript: str | int):
        if isinstance(subscript, str):
            return self._get_chunk_by_chunk_start_time(subscript)
        elif isinstance(subscript, int):
            return self._get_chunk_by_index(subscript)


    def get_index_by_chunk(self, 
                           chunk_to_match: BaseChunk) -> int:
        for i, chunk in enumerate(self):
            if chunk.chunk_start_time == chunk_to_match.chunk_start_time:
                return i
        raise ChunkNotFoundError(f"No matching chunk found for chunk {chunk_to_match.chunk_name}")
    

    def count_chunk_files(self, 
                          extension: str) -> int:
        return sum(1 for chunk_file in self if chunk_file.has_file(extension))


    def get_spectrogram_from_range(self, 
                                   start_time: str, 
                                   end_time: str) -> Spectrogram:
        # Convert input strings to datetime objects
        start_datetime = datetime.strptime(start_time, TimeFormats.DATETIME)
        end_datetime = datetime.strptime(end_time, TimeFormats.DATETIME)

        if start_datetime.day != end_datetime.day:
            warning_message = "Joining spectrograms across multiple days"
            _LOGGER.warning(warning_message)
            warnings.warn(warning_message, RuntimeWarning)

        spectrograms = []
        num_fits_chunks = self.count_chunk_files("fits")

        for i, chunk in enumerate(self):
            # skip chunks without fits files
            if not chunk.has_file("fits"):
                continue
            
            # rather than reading all files to evaluate the actual upper bound to their time range (slow)
            # place an upper bound by using the chunk start datetime for the next chunk
            # this assumes that the chunks are non-overlapping (reasonable assumption)
            lower_bound = chunk.chunk_start_datetime
            if i < num_fits_chunks:
                next_chunk = self[i + 1]
                upper_bound = next_chunk.chunk_start_datetime
            # if there is no "next chunk" then we do have to read the file
            else:
                fits_chunk = chunk.get_file("fits")
                upper_bound = fits_chunk.datetimes[-1]

            # if the chunk overlaps with the input time range, then read the fits file
            if start_datetime <= upper_bound and lower_bound <= end_datetime:
                spectrogram = chunk.read_file("fits")
                spectrogram = time_chop(spectrogram, start_time, end_time)
                # if we have a non-empty spectrogram, append it to the list of spectrograms
                if spectrogram:
                    spectrograms.append(spectrogram)

        if spectrograms:
            return join_spectrograms(spectrograms)
        else:
            raise SpectrogramNotFoundError("No spectrogram data found for the given time range")
