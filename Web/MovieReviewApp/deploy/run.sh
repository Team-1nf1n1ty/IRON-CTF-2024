#!/bin/bash
cd /home/user

export ADMIN_USERNAME="superadmin"
export ADMIN_PASSWORD="Sup3rS3cR3TAdminP@ssw0rd\$!"

python3 -m flask run --host=0.0.0.0