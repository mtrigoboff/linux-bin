" tabs: set to 4 spaces, autoindent
set autoindent shiftwidth=4 tabstop=4

" override vim's implementation of Python standard of 8 spaces per tab char
" https://github.com/neovim/neovim/issues/3786
autocmd FileType python setlocal tabstop=4
autocmd FileType python setlocal noexpandtab

" color scheme related
set term=xterm-256color
set t_Co=256
set background=dark
set number
syntax on				" syntax hiliting
" colorscheme gruvbox8_hard_mlt

set nowrap				" do not wrap long lines

" code folding
set foldmethod=indent	" use with za toggle folding command
set foldlevelstart=99
