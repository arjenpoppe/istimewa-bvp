#!/bin/bash
echo "deploy script called"

eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 .travis/deploy_rsa # Allow read access to the private key
ssh-add .travis/deploy_rsa # Add the private key to SSH

git config --global push.default matching
git remote add deploy ssh://administrator@$IP:$PORT$DEPLOY_DIR
git push deploy release

# Skip this command if you don't need to execute any additional commands after deploying.
ssh administrator@$IP -p $PORT <<EOF
  cd $DEPLOY_DIR
  python manage.py collectstatic
EOF