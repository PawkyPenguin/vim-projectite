# vim-projectite
vim-projectite is a small Vim plugin that provides sources for the denite.nvim to work with vim-projectionist.

This plugin has the following dependencies:
* [denite.nvim](https://github.com/Shougo/denite.nvim)
* [vim-projectionist](https://github.com/PawkyPenguin/vim-projectionist) - note that this is my own fork. This is needed because I added some features for exposing projectionist's API that haven't been merged into the main project yet.

## Usage
Make sure that you have both dependencies installed.

Then, when you have some project open:

* `:Denite projectionist` to list candidates for all project files. The type of the file also is displayed along with its full path to disambiguate files that have the same name.
* `:Denite projectionist:type` to list candidates for all project files with type `type`. For instance if you have defined `source` files and `test` files, you can do `:Denite projectionist:source` or `:Denite projectionist:test`.

Personally, I would recommend only using the second command because the first form has the tendency to produce some duplicates. Here are the mappings I use:

```vimscript
nnoremap <leader>so :Denite projectionist:source<CR>
nnoremap <leader>te :Denite projectionist:test<CR>
```

Note that you'll have to map them yourself: they are not included in the plugin to avoid polluting your mappings.
