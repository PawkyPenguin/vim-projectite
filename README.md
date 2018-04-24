# vim-projectite
vim-projectite is a small Vim plugin that provides sources for the denite.nvim plugin to work with vim-projectionist.

This plugin has the following dependencies:
* [denite.nvim](https://github.com/Shougo/denite.nvim)
* [vim-projectionist](https://github.com/PawkyPenguin/vim-projectionist) - note that this is my own fork. It is needed because I added some features that expose functions. This hasn't been merged into the main project yet.

## Usage
Make sure that you have both dependencies installed.

Then, when you have some project open:

* `:Denite projectionist` to list candidates for all project files. The type of the file also is displayed along with its full path to disambiguate files that have the same name.
* `:Denite projectionist:<type>` to list candidates for all project files with type *<type>*. For instance, if you have defined a *source* type in your projectionist configuration you can use `:Denite projectionist:source`.

I personally only use the second variant because I usually already know what type of file I'm interested in. This way I can avoid listing other candidates that are useless to me. Here are the mappings I use:

```vim
nnoremap <CR>s :Denite projectionist:source<CR>
nnoremap <CR>t :Denite projectionist:test<CR>
```

Note that you'll have to define them yourself: They are not included in the plugin so that they don't interfere with your own mappings.
