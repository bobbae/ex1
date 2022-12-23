let mapleader = ","
set clipboard=unnamedplus

"git clone https://github.com/fatih/vim-go.git ~/.vim/pack/plugins/start/vim-go

"install vundle https://github.com/VundleVim/Vundle.vim#quick-start
"https://github.com/tabnine/YouCompleteMe#installation
"then do :PluginInstall

set number
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'


" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
Plugin 'tpope/vim-fugitive'
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub
Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Install L9 and avoid a Naming conflict if you've already installed a
" different version somewhere else.
" Plugin 'ascenator/L9', {'name': 'newL9'}

" https://github.com/codota/tabnine-vim/issues/107
"git checkout python3
"find . -name "*.pyc" -delete
"python3 install.py 

Plugin 'zxqfl/tabnine-vim'
Plugin 'ycm-core/YouCompleteMe', { 'do': './install.py' }

Plugin 'jremmen/vim-ripgrep'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
"git clone https://github.com/govim/govim.git ~/.vim/pack/plugins/start/govim
"git clone https://github.com/pangloss/vim-javascript.git ~/.vim/pack/vim-javascript/start/vim-javascript
"git clone --recurse-submodules https://github.com/python-mode/python-mode.git
"cd python-mode
"cp -R * ~/.vim
":helptags ~/.vim/doc/
set ic
set sm
set smartindent
syntax on
filetype plugin indent on
set mouse=a
set encoding=utf-8
set t_Co=256
set laststatus=0

"git clone https://github.com/govim/govim.git ~/.vim/pack/plugins/start/govim
"git clone https://github.com/pangloss/vim-javascript.git ~/.vim/pack/vim-javascript/start/vim-javascript
"git clone --recurse-submodules https://github.com/python-mode/python-mode.git
"cd python-mode
"cp -R * ~/.vim
":helptags ~/.vim/doc/
set ic
set sm
set smartindent
syntax on
filetype plugin indent on
set mouse=a
set encoding=utf-8
set t_Co=256
set laststatus=0

noremap <leader>b  :b#<CR>
noremap <leader>g  :w<CR>:GoBuild<CR>
noremap <leader>.  :GoDef<CR>
