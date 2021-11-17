#Install
cd /opt  
sudo curl -L "https://github.com/thomas10-10/repo-deploy/releases/download/$(basename $(curl -fsSLI -o /dev/null -w %{url_effective} https://github.com/thomas10-10/repo-deploy/releases/latest))/rd.tar.gz" | sudo tar -xz 
sudo ln -f -s /opt/rd/rd /usr/local/bin/rd
