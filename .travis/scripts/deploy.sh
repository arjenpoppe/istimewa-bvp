#!/bin/bash
echo "deploy script called"

eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 .travis/id_rsa # Allow read access to the private key
ssh-add .travis/id_rsa # Add the private key to SSH

# Skip this command if you don't need to execute any additional commands after deploying.
ssh -tt administrator@$IP -p $PORT <<EOF
  cd $DEPLOY_DIR
  git pull origin release
  python -m pip install -r requirements.txt
  python manage.py migrate
  python manage.py collectstatic --noinput
EOF

echo "deployment successful"

# deployed successfully