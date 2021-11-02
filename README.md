**R**epo-**D**eploy is a python3 script that allows to deploy and manage several repositories from local or online yaml config

Download rd

```
cd /opt ; sudo curl -L "https://github.com/thomas10-10/repo-deploy/releases/download/$(basename $(curl -fsSLI -o /dev/null -w %{url_effective} https://github.com/thomas10-10/repo-deploy/releases/latest))/rd.tar.gz" | sudo tar -xz ; sudo ln -s /opt/rd/rd /usr/local/bin/rd
```



go in a dir and create a .repo-deploy.yml

```yaml
- repos:
  - url: "https://gitlab.com/containers-for-socle/i3-101/config-i3"
    dir: .config/i3
    branch: main
  - url: https://gitlab.com/containers-for-socle/i3-101/config-starship.git
    dir: .config/starship
  - url: https://gitlab.com/containers-for-socle/i3-101/config-polybar
    dir: .config/polybar  
  - url: https://gitlab.com/containers-for-socle/i3-101/config-wezterm
    dir: .config/wezterm

```

and 

`rd init` to clone multiple repo in .config

`rd git status`  or `rd anyCommand` to execute any command for each repo

or you can `rd init https://myRepoFile.yml`  or `rd init myOtherRepoFile.yml`



I have added some features like download files, add text in file  or add cmd loop

```

- files:
  - url: "https://raw.githubusercontent.com/thomas10-10/myDotFiles/master/Xresources"
    dest_file: ".config/Xresources/Xresources"
  - url: "https://raw.githubusercontent.com/thomas10-10/myDotFiles/master/polybar.sh"
    dest_file: "/usr/local/bin/polybar.sh"
    use_sudo: True
  - file: /usr/local/bin/chromium
    block: "/usr/bin/chromium --disable-logging"
    use_sudo: True
  - file: "./.bashrc"
    markers: ["#<[rd]-STARCHIP-CONFIG-BASH>","#</[rd]-STARCHIP-CONFIG-BASH>"]
    block: |
      export STARSHIP_CONFIG=~/.config/starship/starship.toml
      eval "$(starship init bash)"
      function set_win_title(){
      echo -ne "\033]0;$(basename "$PWD")\007"
      }
      starship_precmd_user_func="set_win_title"
  - file: "./.bash_aliases"
    markers: ["#<[rd]-ALIASES-CONFIG-BASH>","#</[rd]-ALIASES-CONFIG-BASH>"]
    block: |
      alias ls='lsd'

- cmd:
  - "sudo ln -sf ":
    - "/usr/share/zoneinfo/Europe/Paris /etc/localtime"
    - "/usr/bin/i3 /usr/bin/wm"
    - "/usr/bin/env /bin/env"
  - "sudo chmod +x ":
    - "/usr/local/bin/chromium"
    - "/usr/local/bin/polybar.sh"
```

`rd init` for execute

if you want to do something more advanced, I advise you to go to ansible
