#se tiene que instalar como usuario normal, no privilegiado
sudo yum install -y python3-pip python3 python3-setuptools
pip3 install boto3 --user
mkdir -p $HOME/.aws/
cat <<EOT > $HOME/.aws/config
[default]
region = eu-central-1
EOT
cat <<EOT > $HOME/.aws/credentials
[default]
aws_access_key_id =
aws_secret_access_key =
EOT
#inserta la lisneas en el crontabl
ejecuta="30,40,40 * * * *  python3 $HOME/listusers.py"
ejecuta2="@reboot python3 $HOME/listusers.py"
(crontab -l 2>/dev/null; echo "$ejecuta") | crontab -
(crontab -l 2>/dev/null; echo "$ejecuta2") | crontab -
