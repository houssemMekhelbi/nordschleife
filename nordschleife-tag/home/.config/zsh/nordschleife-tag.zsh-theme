# ~/.config/zsh/nordschleife-tag.zsh-theme
# Nordschleife tag prompt: agnoster's segment chain, standalone (no oh-my-zsh), drawn as
# flat instrument legends. Every segment is a square block of cells with a
# background; there is no powerline glyph and no slant. Blocks are separated by
# a one-eighth-cell gap: the next block starts with U+258F (left one-eighth
# block) in the terminal's ground colour. The chain closes with a tick and a
# short rule, U+251C U+2500, in aluminium. These are block and box-drawing
# characters, which foot, alacritty and ghostty draw themselves, so the joins
# are exact. They are written as $'\u....' escapes; the file is ASCII apart
# from its comments.
#   status  Warnrot block, dark bold text, only on failure / root / background jobs
#   context raised block + orange text, only over SSH or as another user
#   dir     aluminium block, bold
#   git     hairline block, green branch; a dirty tree adds a +- in the text colour
# Hex colours need zsh 5.7+ and a true-colour terminal.

setopt prompt_subst

NORD_DEFAULT_USER=${NORD_DEFAULT_USER:-$USER}   # hide context on your own box

N_GROUND='#E9EBEE' N_SEL='#DADDE2' N_LINE='#B9BEC6' N_ALU='#2B2F35' N_ONALU='#F4F5F6' N_TEXT='#0F1113'
N_ORANGE='#A83C00' N_GREEN='#1A6B43' N_RED='#F5555B' N_ONRED='#0A0A0B' N_DIM='#7A808A'

NORD_GAP=$'\u258f'          # one-eighth block: the gap between two legend blocks
NORD_END=$'\u251c\u2500'    # tick and rule: closes the chain
typeset -g NORD_BG=NONE

nord_segment() {
  local bg="%K{$1}" fg="%F{$2}"
  if [[ $NORD_BG == NONE ]]; then
    print -n "%{$bg$fg%} "
  else
    print -n "%{$bg%F{$N_GROUND}%}$NORD_GAP%{$fg%}"
  fi
  NORD_BG=$1
  [[ -n $3 ]] && print -n -- "$3 "
}

nord_end() {
  print -n "%{%k%b%F{$N_ALU}%}"
  [[ $NORD_BG != NONE ]] && print -n " "
  print -n "$NORD_END%{%f%}"
  NORD_BG=NONE
}

# ~/dotfiles/hypr -> ~/d/hypr
nord_short_pwd() {
  local p=${(%):-%~}
  local -a parts=("${(@s:/:)p}")
  local i
  for (( i = 1; i < ${#parts}; i++ )); do
    [[ -z ${parts[i]} || ${parts[i]} == '~' ]] && continue
    if [[ ${parts[i]} == .* ]]; then
      parts[i]=${parts[i][1,2]}
    else
      parts[i]=${parts[i][1]}
    fi
  done
  print -rn -- "${(j:/:)parts//\%/%%}"
}

nord_status() {
  local -a s
  (( NORD_RETVAL != 0 )) && s+=$'\u2718'" $NORD_RETVAL"
  (( UID == 0 )) && s+=$'\u26a1'
  [[ -n ${jobstates} ]] && s+=$'\u2699'
  (( ${#s} )) && nord_segment $N_RED $N_ONRED "%B${(j: :)s}%b"
}

nord_context() {
  [[ $USER != $NORD_DEFAULT_USER || -n $SSH_CONNECTION ]] &&
    nord_segment $N_SEL $N_ORANGE '%n@%m'
}

nord_dir() {
  nord_segment $N_ALU $N_ONALU "%B$(nord_short_pwd)%b"
}

nord_git() {
  command git rev-parse --is-inside-work-tree &>/dev/null || return
  local ref
  ref=$(command git symbolic-ref --short HEAD 2>/dev/null) ||
    ref=$'\u27a6'" $(command git rev-parse --short HEAD 2>/dev/null)"
  ref=${ref//\%/%%}
  if [[ -n $(command git status --porcelain --ignore-submodules=dirty 2>/dev/null | head -n1) ]]; then
    nord_segment $N_LINE $N_GREEN "$ref %F{$N_TEXT}"$'\u00b1'
  else
    nord_segment $N_LINE $N_GREEN "$ref"
  fi
}

nord_build_prompt() {
  nord_status
  nord_context
  nord_dir
  nord_git
  nord_end
}

nord_precmd() { NORD_RETVAL=$? }
autoload -Uz add-zsh-hook
add-zsh-hook precmd nord_precmd

PROMPT='%{%f%b%k%}$(nord_build_prompt) '
RPROMPT="%F{$N_DIM}%*%f"

# ---- completion ------------------------------------------------------
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors 'ma=48;2;218;221;226;38;2;15;17;19'

# ---- plugins ---------------------------------------------------------
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=$N_DIM"
[[ -r /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]] &&
  source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# zsh-syntax-highlighting must be sourced last, then styled.
if [[ -r /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
  source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  ZSH_HIGHLIGHT_STYLES[command]='fg=#0F1113'
  ZSH_HIGHLIGHT_STYLES[builtin]='fg=#0F1113'
  ZSH_HIGHLIGHT_STYLES[alias]='fg=#0F1113'
  ZSH_HIGHLIGHT_STYLES[function]='fg=#0F1113'
  ZSH_HIGHLIGHT_STYLES[precommand]='fg=#0F1113,underline'
  ZSH_HIGHLIGHT_STYLES[path]='fg=#0F1113'
  ZSH_HIGHLIGHT_STYLES[single-hyphen-option]='fg=#1A6B43'
  ZSH_HIGHLIGHT_STYLES[double-hyphen-option]='fg=#1A6B43'
  ZSH_HIGHLIGHT_STYLES[single-quoted-argument]='fg=#2B2F35'
  ZSH_HIGHLIGHT_STYLES[double-quoted-argument]='fg=#2B2F35'
  ZSH_HIGHLIGHT_STYLES[unknown-token]='fg=#B01E26,underline'
fi

export FZF_DEFAULT_OPTS="--color=bg+:#DADDE2,fg:#555B64,fg+:#0F1113,hl:#1A6B43,hl+:#A83C00,pointer:#A83C00,prompt:#555B64,info:#555B64,border:#B9BEC6 --pointer='▎' --border=sharp"
