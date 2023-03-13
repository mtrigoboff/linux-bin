# display > as prompt char, current directory in PuTTY window header
PS1='\[\033]0;\w\007\033[32m\]> \[\033[33m\033[0m\]'

umask 0022		# allow group, others to read files

LS_COLORS=$LS_COLORS:'di=1;34:' ; export LS_COLORS

# set locale so that GCC won't use smart quotes in error msgs
export LC_ALL=C

PATH=".:~/bin:${PATH}"

alias bashdb='bashdb -q'
alias gdbt='gdb -q -tui'
alias ls='ls --color'
alias v='vim -S'
alias vi='vim -O'
