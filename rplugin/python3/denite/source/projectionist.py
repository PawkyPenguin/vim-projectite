# ============================================================================
# FILE: projectionist.py
# AUTHOR: Nils Leuzinger <nilsl at student.ethz.ch>
# License: MIT license
# ============================================================================

from .base import Base
import glob
import os
from denite.util import abspath, expand

BUFFER_HIGHLIGHT_SYNTAX = [
    {'name': 'Name', 'link': 'None',  're': r'[^/ \[\]]\+\s'},
    {'name': 'Type', 'link': 'Special',   're': r'\[.\{-}\] '},
    {'name': 'File', 'link': 'Statement', 're': r'(.\{-})'},
]

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.last_candidates = []

        self.name = 'projectionist'
        self.kind = 'file'
        self.matchers = ['matcher_fuzzy']
        self.vars = {
            'projectionist_type': ''
        }

    def highlight(self):
        for syn in BUFFER_HIGHLIGHT_SYNTAX:
            self.vim.command(
                'syntax match {0}_{1} /{2}/ contained containedin={0}'.format(
                    self.syntax_name, syn['name'], syn['re']))
            self.vim.command(
                'highlight default link {0}_{1} {2}'.format(
                    self.syntax_name, syn['name'], syn['link']))

    def gather_candidates(self, context):
        context['is_interactive'] = True

        projectionist_type = self.vars['projectionist_type']
        if context['args'] and context['args'][0]:
            projectionist_type = context['args'][0]

        if projectionist_type == '':
            return self._gather_project_files(context)
        else:
            return self._gather_files_of_type(context, projectionist_type)

    def _gather_project_files(self, context):
        # TODO: Fix alignment for multiple sources
        candidates = []
        file_dict = self.vim.call('projectionist#list_project_files')
        for proj_type, files in file_dict.items():
            for candidate in self._generate_candidates_from_files(context, files, proj_type):
                candidates.append(candidate)

        return candidates

    def _gather_files_of_type(self, context, projectionist_type):
        files = self.vim.call('projectionist#list_files_for_type', projectionist_type)
        candidates = [c for c in self._generate_candidates_from_files(context, files, projectionist_type)]
        return candidates

    def _generate_candidates_from_files(self, context, files, proj_type):
        candidates = []
        max_name_length = self._get_max_filename_length(files)
        for file_item in files:
            shortened_filename = self.vim.call('fnamemodify', file_item[1], ':~:.')
            candidates.append({
                'word': file_item[0],
                'action__path': file_item[1],
                'abbr': "{} [{}] ({})".format(file_item[0].ljust(max_name_length), proj_type, shortened_filename),
                'kind': 'file'
            })
        # If list is empty take old candidates because `projectionist#list_files_for_type` returns
        # `[]` when called from the denite buffer (which means candidates would vanish when the user types).
        if not candidates:
            return self.last_candidates
        else:
            self.last_candidates = candidates
            return candidates

    def _get_max_filename_length(self, files):
        if not files:
            return
        max_name_length = max([len(self.vim.call('fnamemodify', file_item[0], ':~:.')) for file_item in files])
        if max_name_length > 30:
            max_name_length = 30
        return max_name_length
